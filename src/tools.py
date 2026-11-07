import os, requests
from dotenv import load_dotenv
from langchain_core.tools import tool

load_dotenv()

FLIGHTAPI_API_KEY = os.environ.get("FLIGHTAPI_API_KEY")
HOTELAPI_API_KEY = os.environ.get("HOTELAPI_API_KEY")

@tool
def flight_tool(origin: str, destination: str, date: str) -> dict:
    """
    Search for a one-way flight between an origin and destination on a specific date.
    
    Args:
        origin (str): Departure airport code (e.g., 'JFK')
        destination (str): Arrival airport code (e.g., 'LAX')
        date (str): Flight date in YYYY-MM-DD format
    """
    url = f"https://api.flightapi.io/onewaytrip/{FLIGHTAPI_API_KEY}/{origin}/{destination}/{date}/1/0/0/Economy/USD"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return {
                "error": True,
                "status_code": response.status_code,
                "response": response.text
            }
    except requests.exceptions.RequestException as e:
            return {"error": True, "message": str(e)}

@tool
def hotel_tool(city: str) -> dict:
    """
    Search for hotel mappings and data in a given city.
    
    Args:
        city (str): Name of the city to search hotels in
    """
    url = f"https://api.makcorps.com/mapping?name={city}&api_key={HOTELAPI_API_KEY}"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return {
                "error": True,
                "status_code": response.status_code,
                "response": response.text
            }
    except requests.exceptions.RequestException as e:
            return {"error": True, "message": str(e)}

@tool
def policy_tool(category: str, amount: float, employee_role: str = 'standard') -> dict:
    """
    Checks if a travel expense complies with company policy limits.
    
    Args:
        category (str): The expense category, either 'flight' or 'hotel'
        amount (float): The cost of the expense in USD
        employee_role (str): The employee's role, either 'standard' or 'executive'
    """
    policy_limits = {
        'standard': {'flight': 600.0, 'hotel': 200.0},
        'executive': {'flight': 1500.0, 'hotel': 500.0}
    }

    limit = policy_limits[employee_role][category]
    compliant = amount <= limit
    requires_human_approval = limit < amount <= limit * 1.2

    message = 'Compliant' if compliant else 'Requires human approval' if requires_human_approval else 'Non-compliant'

    return {
        'compliant': compliant,
        'requires_human_approval': requires_human_approval,
        'message': message
    }