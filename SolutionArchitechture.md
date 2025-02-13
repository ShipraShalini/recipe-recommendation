# GenAI Recipe Recommendation
#### Overview:
It is a Recipe Recommendation API (PoC) based on the supplied list of ingredients using RAG with generative AI 

#### Components:
- **PostgreSQL with pgvector & PgvectorDocumentStore**: Stores recipe data as vectors
- **OpenAIDocumentEmbedder**: Creates embeddings of documents (recipes) and user queries.
- **OpenAITextEmbedder**: Creates embeddings of user queries.
- **PgvectorEmbeddingRetriever**: Retrieves the most relevant recipes based on user input.
- **PromptBuilder**: Constructs the prompt for OpenAI, combining query and retrieved documents.
- **OpenAIGenerator**: Generates the final response, returning a recipe formatted in Markdown

#### Data Flow:
1. **Recipe Ingestion**: Recipes are downloaded, extracted, and stored in PostgreSQL with embeddings using OpenAI.
2. **User Query**: The user provides a list of ingredients.
3. **Embedding and Retrieval**: The query is embedded and used to retrieve relevant recipes.
4. **Response Generation**: GPT is used to refine the response and format it as a Markdown document.

#### FastAPI Service:

`/recommend_recipe (POST)`: Accepts a list of ingredients and returns the best matching recipe in Markdown format.
`/health (GET)`: Provides a basic health check endpoint.
