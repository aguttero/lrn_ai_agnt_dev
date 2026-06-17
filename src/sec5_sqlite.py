import requests
from dotenv import dotenv_values
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.sqlite import SqliteSaver

config = dotenv_values(".env")
GOOGLE_API_KEY = config.get("GOOGLE_API_KEY")


def get_weather(city: str):
    """Get weather for a given city"""
    return {"condition": "sunny", "temperature": 25}


def get_location():
    """Get user's current location. Use this when the user asks about weather."""
    from flask import session

    # lat = session["user_location"]["lat"]
    # lon = session["user_location"]["lon"]
    lat = -33.3607
    lon = -70.5124
    print(f"lat= {lat}, lon= {lon}")

    # --- CONVERT LAT LON to City:
    response = requests.get(
        f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json",
        headers={"User-Agent": "WeatherAssistant/1.0"},
        timeout=3,
    )
    print("response status:", response.status_code)
    data = response.json()
    print(" - - - ")
    print(data)
    print(" - - - ")

    city = data["address"].get("city", data["address"].get("town", "unknown"))
    country = data["address"].get("country", "")

    print(f"city= {city}, country= {country}")

    return f"{city}, {country}"


# Initialize Gemini Flash 2.5
llm = ChatGoogleGenerativeAI(
    # model="gemini-2.0-flash", temperature=0.7, api_key=GOOGLE_API_KEY
    model="gemini-2.5-flash",
    temperature=0.7,
    api_key=GOOGLE_API_KEY,
)
system_prompt = """
You are a helpful weather assistant.
YOUR WORKFLOW:
1. If the user asks about weather WITHOUT specifying a location, you MUST:
   - First call get_location() to find their location
   - Then call get_weather(city) with that location

2. If the user provides a city, call get_weather(city) directly.

"""

connection = SqliteSaver.from_conn_string("data/checkpoints_04.db")
checkpointer = connection.__enter__()
agent = create_agent(
    model=llm,
    tools=[get_weather, get_location],
    system_prompt=system_prompt,
    checkpointer=checkpointer,
)
