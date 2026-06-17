from langchain.chat_models import init_chat_model
from dotenv import dotenv_values

config = dotenv_values(".env")
API_KEY = config.get("GOOGLE_API_KEY","default_value")

model = init_chat_model(
    model="gemini-3-flash-preview", 
    model_provider="google-genai", 
    api_key=API_KEY)

def invoke (user_prompt):
    with open ("data/sail_material.txt","r") as file:
        file_content = file.read()
    final_prompt = f"{user_prompt}: {file_content}"
    return model.invoke(final_prompt)
# LLM input format: String
# LLM output response object instance (response.content, response.response_metadata, response.usage_metadata, etc)


def main():
    print(f"API KEY={API_KEY}")
    print("Hello from lrn-ai-agnt-dev!")
    
    prompt = "Hi, which material is better as sail-cloth for boat sailing?"
    print ("- - - -")
    print (prompt)

    response = invoke(prompt)
    # print (response.content)
    print ("- - - -")
    print (response.content[0]['text'])
    print ("- - END - - ")

if __name__ == "__main__":
    main()
