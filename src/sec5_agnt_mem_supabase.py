from dotenv import dotenv_values
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI

# --- for Postgres
from langgraph.checkpoint.postgres import PostgresSaver

# --- for sqlite
# from langgraph.checkpoint.sqlite import SqliteSaver

config = dotenv_values(".env")
GOOGLE_API_KEY = config.get("GOOGLE_API_KEY", "default_value")
DB_URI: str = config.get("SUPABASE_DB_URI")


def get_weather(city: str):
    """Get weather for a given city"""
    return {"condition": "sunny", "temperature": 25}


def get_location():
    """Get user's current location. Use this when the user asks about weather."""
    return "Rome, Italy"


# Initialize Gemini Flash 2.5
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", temperature=0.7, api_key=GOOGLE_API_KEY
)
system_prompt = """
You are a helpful weather assistant.
YOUR WORKFLOW:
1. If the user asks about weather WITHOUT specifying a location, you MUST:
   - First call get_location() to find their location
   - Then call get_weather(city) with that location

2. If the user provides a city, call get_weather(city) directly.

"""


def run_agnt_mem():
    # with SqliteSaver.from_conn_string(
    #     "data/checkpoints.db"
    # ) as checkpointer:  # param 'checkpoints.db' is the DB file name
    with PostgresSaver.from_conn_string(DB_URI) as checkpointer:
        checkpointer.setup()
        agent = create_agent(
            model=llm,
            tools=[get_weather, get_location],
            system_prompt=system_prompt,
            checkpointer=checkpointer,
        )

        while True:
            user_query = input("Enter your query: ")
            if user_query in ["bye", "quit", "exit"]:
                break

            agent_prompt = {"messages": [{"role": "user", "content": user_query}]}
            response = agent.invoke(agent_prompt, {"configurable": {"thread_id": "1"}})
            print("- # - " * 3)
            # print(response)
            # print("- # - " * 3)

            # LOOP Message MEMORY
            # for i in response["messages"]:
            #     if i.type == "human":
            #         print("You: ", i.content)
            #     if i.type == "ai" and i.content:
            #         print("Agent: ", i.content)
            #     print("- - - -")

            print(response["messages"][-1].content)


def show_api_key():
    print(f"GOOGLE_API KEY={GOOGLE_API_KEY}")
    print(f"DB_URI= {DB_URI}")
    return GOOGLE_API_KEY


def main():
    print(".env data acces check:", show_api_key())
    print("- - - -")

    run_agnt_mem()

    print("- - END - - ")
    return 0


if __name__ == "__main__":
    exit_code: int = main()
    print(f"exit code: {exit_code}")
    exit(exit_code)
