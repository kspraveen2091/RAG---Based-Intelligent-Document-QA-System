from dotenv import load_dotenv
load_dotenv()
import os

# -----------------------------
# 1. Create tools
# -----------------------------

# Web search tool
from langchain_tavily import TavilySearch

search = TavilySearch(
    max_results=3, api_key=os.getenv("TAVILY_API_KEY")
)

print("Tavily search tool created.")


# Add tool
from langchain.tools import tool

@tool
def add(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b


# Subtract tool
@tool
def sub(a: float, b: float) -> float:
    """Subtract two numbers."""
    return a - b


# Divide tool
@tool
def divide(a: float, b: float) -> float:
    """Divide two numbers."""
    return a / b


# Weather tool
import requests
import os

@tool
def get_weather(city: str):
    """Get current weather for a city."""

    API_KEY = os.getenv("OPENWEATHER_API_KEY")

    response = requests.get(
        "https://api.openweathermap.org/data/2.5/weather",
        params={
            "q": city,
            "appid": API_KEY,
            "units": "metric"
        }
    )

    response.raise_for_status()

    data = response.json()

    return {
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "weather": data["weather"][0]["description"]
    }

