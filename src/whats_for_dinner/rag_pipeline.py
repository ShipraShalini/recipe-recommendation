from haystack import Pipeline
from haystack.components.builders import PromptBuilder
from haystack.components.embedders import OpenAITextEmbedder
from haystack.components.generators import OpenAIGenerator
from haystack_integrations.components.retrievers.pgvector import (
    PgvectorEmbeddingRetriever,
)
from haystack_integrations.document_stores.pgvector import PgvectorDocumentStore

from whats_for_dinner.constants import (
    PROMPT_TEMPLATE,
    SECRET_OPENAI_API_KEY,
    SECRET_POSTGRES_URL,
)


def initialise_rag_pipeline() -> Pipeline:
    """
    Initializes and returns a Haystack RAG pipeline that retrieves recipes based on
    user input and generates responses using OpenAI's GPT-4 model.

    Returns:
        Pipeline: A Haystack pipeline for RAG.
    """
    document_store = PgvectorDocumentStore(
        connection_string=SECRET_POSTGRES_URL,
        table_name="recipe_vector",
        language="english",
        recreate_table=True,
        embedding_dimension=1536,
    )
    retriever = PgvectorEmbeddingRetriever(document_store=document_store)
    embedder = OpenAITextEmbedder(api_key=SECRET_OPENAI_API_KEY)
    generator = OpenAIGenerator(api_key=SECRET_OPENAI_API_KEY, model="gpt-4o")
    pipeline = Pipeline()
    pipeline.add_component("embedder", embedder)
    pipeline.add_component("retriever", retriever)
    pipeline.add_component("prompt_builder", PromptBuilder(template=PROMPT_TEMPLATE))
    pipeline.add_component("generator", generator)

    pipeline.connect("embedder.embedding", "retriever.query_embedding")
    pipeline.connect("retriever.documents", "prompt_builder.documents")
    pipeline.connect("prompt_builder.prompt", "generator.prompt")
    return pipeline
