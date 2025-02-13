import os

from haystack.utils import Secret

PROMPT_TEMPLATE = """
You are an intelligent recipe assistant.
You'll be provided with a set of recipes, and a list of ingredients.
Your task is to carefully refer to the provided recipes and find the one that uses all ingredients but not more.
You may ignore optional ingredients but try to include them, if possible.
If you can't find any recipes with all the ingredients, return a recipe which uses a subset of the ingredients.
Once you've found the best match, return the recipe formatted in markdown, including the recipe name, ingredients, and instructions.
Only return the recipe.


If there is no matching recipe, return a response stating that there are no recipes which can be made with the given ingredients"

Recipes:
{% for document in documents %}
    {{ document.content }}
{% endfor %}

Ingredients: {{ query }}
"""

SECRET_POSTGRES_URL = Secret.from_token(os.getenv("POSTGRES_URL"))

SECRET_OPENAI_API_KEY = Secret.from_token(os.getenv("OPENAI_API_KEY"))

RECIPE_URL = os.environ.get("RECIPE_URL")
RECIPE_DIR = "/tmp/recipes"
