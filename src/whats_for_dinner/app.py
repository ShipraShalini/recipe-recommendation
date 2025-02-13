from fastapi import Body, FastAPI
from fastapi.responses import Response

from whats_for_dinner.rag_pipeline import initialise_rag_pipeline
from whats_for_dinner.startup import load_recipes

app = FastAPI()

load_recipes()
pipeline = initialise_rag_pipeline()


@app.get("/health")
async def health():
    """
    Health check endpoint to verify the API is running correctly.

    Returns:
        dict: A simple status response indicating the API is healthy.
    """
    return {"status": "Healthy"}


@app.post("/recommend_recipe")
async def recommend_recipe(q: str = Body(...)) -> Response:
    """
    Receives a list of ingredients as input, runs the RAG pipeline, and returns the best
    matching recipe in Markdown format.

    Args:
        q (str): A string containing the user's query (ingredients).

    Returns:
        Response: The generated recipe in Markdown format.
    """
    result = pipeline.run({"prompt_builder": {"query": q}, "embedder": {"text": q}})
    return Response(
        content=result["generator"]["replies"][0], media_type="text/markdown"
    )
