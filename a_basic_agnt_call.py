#from langchain.chat_models import init_chat_model
from pyexpat import model

from dotenv import dotenv_values

from langchain_google_genai import ChatGoogleGenerativeAI
# from dotenv import load_dotenv
from langchain.agents import create_agent

config = dotenv_values(".env")
API_KEY = config.get("GOOGLE_API_KEY","default_value")

# SIMPLE LLM INVOKE
# from langchain.chat_models import init_chat_model
# Init Gemini 3 Flash Preview
# model = init_chat_model(
#     model="gemini-3-flash-preview", 
#     model_provider="google-genai", 
#     api_key=API_KEY)

# def invoke (user_prompt):
#     with open ("data/sail_material.txt","r") as file:
#         file_content = file.read()
#     final_prompt = f"{user_prompt}: {file_content}"
#     return model.invoke(final_prompt)

# TOOL FUNCTION EXAMPLE
def get_weather(city: str):
    """Get weather for the input parameter city""" # AI Agent reads the function information to decide if it is useful
    return {"condition": "sunny",
            "temperature": 25,
            "rain forecast": 0.90}

# Initialize Gemini Flash 2.5
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7,
    api_key=API_KEY
)
# LLM input format: String
# LLM output response object instance (response.content, response.response_metadata, response.usage_metadata, etc)

# Initialize Agent
agent = create_agent(
    model=llm,
    tools=[get_weather]
)
# Agent Input format: Dictionary
# Agent Output: Dictionary {"messages": [HumanMessage object(), AiMessage object()]} 


def main():
    print(f"API KEY={API_KEY}")
    print("Hello from lrn-ai-agnt-dev!")

    print ("- - - -")
    agent_prompt = {
        "messages":[
            {"role": "user",
             "content": "How is the weather in Santiago de Chile?" }
        ]
    } 

    response0 = agent.invoke(agent_prompt)
    print (f"agent_prompt={agent_prompt}")
    print ("- - - -")
    print("ITEM [-1]:")
    print(response0["messages"][-1].content)
    print ("- - - -")
    # print("FULL RESPONSE:")
    # print(response0)

    # SIMPLE LLM INVOKE
    # llm_prompt = "Which are your main directives? Who trained you?"
    # response1 = llm.invoke(llm_prompt)
    # print (f"llm_prompt={llm_prompt}")
    # print(response1.content)
    # # print(response1) # contains token usage detail and other data

    print ("- - END - - ")

if __name__ == "__main__":
    main()
