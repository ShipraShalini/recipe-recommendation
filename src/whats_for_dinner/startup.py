import os
from pathlib import Path
from urllib.request import urlretrieve
from zipfile import ZipFile

from haystack import Document
from haystack.components.embedders import OpenAIDocumentEmbedder
from haystack.document_stores.types import DuplicatePolicy
from haystack_integrations.document_stores.pgvector import PgvectorDocumentStore

from whats_for_dinner.constants import (
    RECIPE_DIR,
    RECIPE_URL,
    SECRET_OPENAI_API_KEY,
    SECRET_POSTGRES_URL,
)


def download_and_extract(recipe_url: str, recipe_dir: str) -> None:
    """
    Downloads a zipped recipe dataset from a given URL and extracts it to a specified directory.

    Args:
        recipe_url (str): The URL of the zipped recipe dataset.
        recipe_dir (str): The directory where the dataset will be extracted.
    """
    zip_filename = f"{recipe_dir}.zip"
    # download the file
    print("Downloading the recipe dataset...")
    urlretrieve(recipe_url, zip_filename)

    print("Extracting the recipe dataset...")
    # Extract the CSV file
    with ZipFile(zip_filename, "r") as zf:
        zf.extractall(path="/tmp")


def extract_recipes_from_files(recipe_dir: str) -> list[Document]:
    """
    Reads recipe text files from a given directory and converts them into a list of
    Haystack Document objects.

    Args:
        recipe_dir (str): The directory where the recipe text files are located.

    Returns:
        list[Document]: A list of Haystack Document objects containing the recipes.
    """
    recipes = []
    for _, _, files in os.walk(recipe_dir):
        for filename in files:
            _, extension = os.path.splitext(filename)
            if extension != ".txt":
                continue
            file_path = os.path.join(recipe_dir, filename)
            recipes.append(
                Document(content=Path(file_path).read_text(encoding="utf-8").strip())
            )
    return recipes


def store_recipes(recipes: list[Document]) -> None:
    """
    Embeds the recipe documents using OpenAI's document embedder and stores them in the
    PgvectorDocumentStore.

    Args:
        recipes (list[Document]): A list of Haystack Document objects containing recipes
    """
    print("Storing Documents...")
    document_store = PgvectorDocumentStore(
        connection_string=SECRET_POSTGRES_URL,
        table_name="recipe_vector",
        language="english",
        recreate_table=True,
        embedding_dimension=1536,
    )
    document_embedder = OpenAIDocumentEmbedder(api_key=SECRET_OPENAI_API_KEY)
    documents_with_embeddings = document_embedder.run(recipes)
    document_store.write_documents(
        documents_with_embeddings.get("documents"), policy=DuplicatePolicy.OVERWRITE
    )
    print(f"{len(recipes)} Documents stored")


def load_recipes() -> None:
    """
    Runs the entire recipe ingestion pipeline: downloads, extracts, processes,
    and stores the recipe documents.
    """
    download_and_extract(RECIPE_URL, RECIPE_DIR)
    recipes = extract_recipes_from_files(RECIPE_DIR)
    store_recipes(recipes)
