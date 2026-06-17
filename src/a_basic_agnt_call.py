#from langchain.chat_models import init_chat_model
from typing import Tuple
import requests
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
# Is important to enforce typing hints so LLM knows how to call the function
def get_weather(city: str): 
    """Get weather for the input parameter city""" # AI Agent reads the function information to decide if it is useful
    api_key = config.get("OPENWEATHER_API_KEY","default_value")
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }

    api_response = requests.get(base_url, params=params)
    data = api_response.json()
    temperature_celcius = data ['main']['temp']
    temperature_farenheit = temperature_celcius * 9/5 + 32
    return  data,{"temperature_farencheit": temperature_farenheit}         
    # SAMPLE HARDCODED RETURN
    # return {"condition": "sunny",
    #         "temperature_celcius": 25,
    #         "rain forecast": 0.90}


def get_location() -> Tuple[str,str]:
    """Returns user location: City Name and Country ISO code in a tuple (city_name, country_iso_code) of the user loccation""" # AI Agent reads the function information to decide if it is useful
    return "Buenos Aires", "AR"

# Initialize Gemini Flash 2.5
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7,
    api_key=API_KEY
)
# LLM input format: String
# LLM output response object instance (response.content, response.response_metadata, response.usage_metadata, etc)

# FORMAT: ROLE, [WORKFLOW FOR AI AGENT]
system_prompt = """
You are a helpful weather assistant.
YOUR WORKFLOW:
1. If the user asks about weather WITHOUT specifying a location, you MUST:
   - First call get_location() to find their location
   - Then call get_weather(city) with that location
   
2. If the user provides a city, call get_weather(city) directly.

3. Use your knowledge to returno the temperature in the metric unit that is standard for the given location.

4. Present the weather information including temperature, condition, wind speed, wind chill, humidity, and any other relevant details.
"""

# Initialize Agent
agent = create_agent(
    model=llm,
    tools=[get_weather,get_location],
    system_prompt=system_prompt
)
# Agent Input format: Dictionary
# Agent Output: Dictionary {"messages": [HumanMessage object(), AiMessage object()]} 


def show_api_key():
    print(f"API KEY={API_KEY}")


def main():
    print(f"API KEY={API_KEY}")
    print("Hello from lrn-ai-agnt-dev!")

    print ("- - - -")
    
    user_query = input("Enter your query: ")
    # user_query = "How is the weather?" 
    
    agent_prompt = {
        "messages":[
            {"role": "user",
             #"content": "How is the weather in Santiago de Chile?" 
             #"content": "How is the weather?" 
             "content": user_query 
             }
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
