import os
from dotenv import load_dotenv
from tools import flight_tool, hotel_tool, policy_tool
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables from .env file
load_dotenv()

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
        )
    )

    # Invoke the agent with a test query
    result = agent.invoke({
        "messages": [{"role": "user", "content": "Can I book a flight to JFK for $500 as a standard employee?"}]
    })

    # Return the final message content from the agent's execution history
    return result["messages"][-1].content

if __name__ == "__main__":
    print(create_expense_agent())