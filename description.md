#### Assumptions & limitations
- Doesn't consider quantity
- Returns only one recipe
- Returns generic response even if the query is not correct.
- Does not implement the image based retrival.


# Improvements
- Data ingestion should be separate from the app.
- Needs tests
- Error handling required.



#### Steps to run:
1. Unzip the project directory.
2. Set up the following env variables:
   ```shell
   export OPENAI_API_KEY=<your-openai-api-key>
   export RECIPE_URL=<url-to-recipe-dataset>
   export POSTGRES_URL=<postgres-connection-url>
   ```
3. Run the services using Docker Compose:
   ```docker-compose up```


#### Sample Request:
1. Success Request:
    ```shell
   curl --location 'http://localhost:8000/recommend_recipe' \
   --header 'Content-Type: text/plain' \
   --data '"flour, sugar, baking powder, yogurt, egg"'
   ```

2. Failure Request:
    ```shell
   curl --location 'http://localhost:8000/recommend_recipe' \
   --header 'Content-Type: text/plain' \
   --data '"paper, ink"'
   ```
