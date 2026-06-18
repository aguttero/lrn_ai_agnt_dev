from typing import List

from dotenv import dotenv_values
from langchain.chat_models import init_chat_model
from pydantic import BaseModel, Field

config = dotenv_values(".env")
GOOGLE_API_KEY = config.get("GOOGLE_API_KEY")
print(f"GOOGLE_API_KEY= {GOOGLE_API_KEY}")


class Recipe(BaseModel):
    name: str = Field(description="Name of recipe")
    description: str = Field(description="Brief description of recipe")
    prep_time: str = Field(description="Estimated recipe preparation time")


class Respose(BaseModel):
    """A single recipe"""

    ingredients: List[str] = Field(description="List of main ingredients")
    recipes: List[Recipe] = Field(description="List of 3 suggested recipes")


# --- Initialize the model
model = init_chat_model(
    "gemini-2.5-flash", model_provider="google_genai", api_key=GOOGLE_API_KEY
)
structured_model = model.with_structured_output(Respose)
system_prompt = """
You are a helpful chef. Identify the main ingredients. Suggest 3 recipes based on these """

# --- Create message
message = [
    {"role": "system", "content": system_prompt},
    {
        "role": "user",
        "content": "I have spinach leaves, eggs, onions, garlic, olive oil, butter, Monterey Jack cheese, and flour",
    },
]

# --- Get and print response
response = structured_model.invoke(message)
# Plain response
print(response)
print("- - -")
# Dictionary format response
response_dict = response.model_dump()
print(response_dict)
print("- - -")
