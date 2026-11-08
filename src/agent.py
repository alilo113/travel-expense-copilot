import os
from dotenv import load_dotenv
from tools import flight_tool, hotel_tool, policy_tool
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables from .env file
load_dotenv()

memory = MemorySaver()

def create_expense_agent():
    # Initialize Google's Gemini model 
    google_model = ChatGoogleGenerativeAI(
        model="gemini-3.6-flash",  # Or gemini-2.0-flash
        temperature=0
    )

    agent = create_agent(
        model=google_model,
        tools=[flight_tool, hotel_tool, policy_tool],
        system_prompt=(
            "You are an expert travel and expense co-pilot assistant. "
            "Always check company policy using policy_tool when evaluating travel expenses."
        ),
        checkpointer=memory
    )

    config = {"configurable": {"thread_id": "test_session_123"}}

    print("--- TURN 1 ---")
    # Turn 1: Establish context (saying you are a standard employee)
    response_1 = agent.invoke(
        {
            "messages": [{"role": "user", "content": "Hi, my name is Alex and I am a standard employee."}]
        },
        config=config
    )
    print("Agent:", response_1["messages"][-1].content)

    print("\n--- TURN 2 ---")
    # Turn 2: Ask a question that relies on Turn 1's context WITHOUT stating your role again
    response_2 = agent.invoke(
        {
            "messages": [{"role": "user", "content": "Can I book a flight to JFK for $500?"}]
        },
        config=config
    )
    print("Agent:", response_2["messages"][-1].content)

if __name__ == "__main__":
    print(create_expense_agent())