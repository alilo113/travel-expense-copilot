import os, requests
from dotenv import load_dotenv

load_dotenv()

FLIGHTAPI_API_KEY = os.environ.get("FLIGHTAPI_API_KEY")

def flight_tool(origin: str, destination: str, date: str) -> dict:
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