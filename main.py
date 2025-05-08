import os
from dotenv import load_dotenv
from langchain.agents import initialize_agent, Tool
from langchain.chat_models import ChatOpenAI
from tools.google_places import find_activities_nearby

load_dotenv()

# Initialize your LLM
llm = ChatOpenAI(temperature=0.7)

# Register your Google Places tool
tools = [
    Tool(
        name="FindActivitiesNearby",
        func=find_activities_nearby,
        description="Useful for finding fun things to do near a given location. Input format: 'latitude,longitude'",
    )
]

# Create the agent executor, enabling automatic retry on parsing failures
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent="chat-zero-shot-react-description",
    verbose=True,
    handle_parsing_errors=True,  # <-- this flag tells the executor to catch & retry parsing errors
)

if __name__ == "__main__":
    user_location = "37.7749,-122.4194"  # San Francisco for example
    query = f"What are some fun things to do around {user_location}?"

    try:
        response = agent.run(query)
        print(response)
    except Exception as e:
        # If it still fails, print a helpful hint
        print("⚠️ The agent ran into an error. Try increasing temperature or "
              "adding more explicit tool descriptions. See:")
        print("https://python.langchain.com/docs/troubleshooting/errors/OUTPUT_PARSING_FAILURE")
        print(f"\nFull traceback:\n{e}")
