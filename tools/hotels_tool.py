import os, requests
from dotenv import load_dotenv
from langchain_core import tools

load_dotenv()

HOTELAPI_API_KEY = os.environ.get("HOTELAPI_API_KEY")

@tools
def hotel_tool(city: str) -> dict:
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