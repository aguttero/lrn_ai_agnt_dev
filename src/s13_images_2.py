import base64

from dotenv import dotenv_values
from langchain.chat_models import init_chat_model

config = dotenv_values(".env")
GOOGLE_API_KEY = config.get("GOOGLE_API_KEY")

# --- Convert image file to base64
image_path = "images/ingredients.png"
with open(image_path, "rb") as file:
    raw_binary = file.read()
    base64_bytes = base64.b64encode(raw_binary)  # type= bytes
    image_b64 = base64_bytes.decode(
        "utf-8"
    )  # type= str (neeeded for LLM message content)


# --- Mime type definition
import mimetypes

mime_type, _ = mimetypes.guess_type(image_path)  # returns a tuple


# Initialize the model
model = init_chat_model(
    "gemini-2.5-flash", model_provider="google_genai", api_key=GOOGLE_API_KEY
)
system_prompt = """ You are a helful chef. Identify the main ingredients. Suggest 3 recipes bassed on these"""

message_list = [
    {"role": "system", "content": system_prompt},
    {
        "role": "user",
        "content": [
            {"type": "text", "text": "Describe what you see in this image"},
            # {"type": "image", "base64": image_b64, "mime_type": "image/png"},
            {"type": "image", "base64": image_b64, "mime_type": mime_type},
        ],
    },
]

# Get and print the response
# response = model.invoke([message])

# message list handling
print("Thinking...")
response = model.invoke(message_list)

print(type(response))
print("- - -")
print(response.text)
