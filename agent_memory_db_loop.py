import requests
from dotenv import dotenv_values

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

config = dotenv_values(".env")
GOOGLE_API_KEY = config.get("GOOGLE_API_KEY","default_value")

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


def get_location() -> dict:
    """Returns user location: City Name and Country ISO code in a dictionary with the user loccation""" # AI Agent reads the function information to decide if it is useful
    return {"city": "Buenos Aires",
            "country_iso_code": "AR"}

# Initialize Gemini Flash 2.5
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7,
    api_key=GOOGLE_API_KEY
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
"""

# Initialize Agent
agent = create_agent(
    model=llm,
    tools=[get_weather,get_location],
    system_prompt=system_prompt,
    checkpointer=InMemorySaver()
)
# Agent Input format: Dictionary
# Agent Output: Dictionary {"messages": [HumanMessage object(), AiMessage object()]} 


def show_api_key():
    print(f"GOOGLE_API KEY={GOOGLE_API_KEY}")
    return GOOGLE_API_KEY


def main():
    print("Hello from lrn-ai-agnt-dev!")
    print(".env data:", show_api_key())
    print ("- - - -")
    
    # Query 1
    user_query_1 = input("Enter your query: ")
    agent_prompt = {
        "messages":[
            {"role": "user",
             "content": user_query_1
             }
        ]
    } 
    response1 = agent.invoke (agent_prompt, {"configurable": {"thread_id": "1"}})
    print(response1["messages"][-1].content)
    print ("- - - -")

    # Query 2
    user_query_2 = input("Enter your query: ")
    agent_prompt = {
        "messages":[
            {"role": "user",
             "content": user_query_2
             }
        ]
    } 
    response2 = agent.invoke (agent_prompt, {"configurable": {"thread_id": "1"}})
    print(response2["messages"][-1].content)
    print ("- - - -")
    

    print ("- - END - - ")

if __name__ == "__main__":
    main()
