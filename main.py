import os
from dotenv import load_dotenv
from langchain.agents import initialize_agent, Tool
from langchain_community.chat_models import ChatOpenAI
from tools.google_places import find_activities_nearby
from tools.weather import get_weather

load_dotenv()

llm = ChatOpenAI(temperature=0.7)

tools = [
    Tool(
        name="FindActivitiesNearby",
        func=find_activities_nearby,
        description="Find fun things to do near a given location; input format: 'lat,lng'."
    ),
    Tool(
        name="GetWeather",
        func=get_weather,
        description="Get current weather at a given location; input format: 'lat,lng'."
    )
]

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent="chat-zero-shot-react-description",
    verbose=True,
    handle_parsing_errors=True,
)

if __name__ == "__main__":
    user_loc = "Clovis"  
    # Combine both intents in one prompt:
    prompt = (
        f"I’m at {user_loc}. What are some fun things to do around here, "
        "and what’s the current weather?"
    )
    try:
        output = agent.run(prompt)
        print(output)
    except Exception as e:
        print("⚠️ Agent error—see traceback below:")
        print(e)
