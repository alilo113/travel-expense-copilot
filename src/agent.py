import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver

from tools import flight_tool, hotel_tool, policy_tool

load_dotenv()

memory = MemorySaver()

def create_expense_agent():
    google_model = ChatGoogleGenerativeAI(
        model="gemini-3.5-flash",
        temperature=0
    )

    agent = create_agent(
        model=google_model,
        tools=[flight_tool, hotel_tool, policy_tool],
        system_prompt=(
            "You are an expert travel and expense co-pilot assistant. "
            "Always check company policy using policy_tool when evaluating travel expenses."
        ),
        checkpointer=memory,
    )

    config = {"configurable": {"thread_id": "test_session_123"}}

    response = agent.invoke(
        {
            "messages": [{"role": "user", "content": "Can I book a flight to JFK for $500 as a standard employee?"}]
        },
        config=config,
        debug=True
    )

    return response["messages"][-1].content

if __name__ == "__main__":
    print(create_expense_agent())