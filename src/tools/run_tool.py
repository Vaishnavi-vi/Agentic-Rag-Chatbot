import os
import requests
import numpy as np
from typing import Tuple
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.tools import tool
from langchain_community.utilities import WikipediaAPIWrapper
from dotenv import load_dotenv

load_dotenv()

#tool Function 

def calculate_bmi(height: float, weight: float) -> Tuple[float, str]:
    """Calculate the Body Mass Index (BMI) based on a person's height (in meters) and weight (in kilograms).
    Use this tool when a user asks about BMI, health category, or body weight status."""
    bmi = weight / (height**2)
    if bmi < 18.5:
        category = "Underweight"
    elif 18.5 <= bmi < 25:
        category = "Normal weight"
    elif 25 <= bmi < 30:
        category = "Overweight"
    else:
        category = "Obese"
    return bmi, category



def get_weather_update(symbol: str):
    """ Fetch the current weather information for a specific city using the OpenWeather API.
    Use this tool when a user asks about the weather, temperature, or weather conditions in any location."""
    api_key = os.getenv("WEATHER_API_KEY")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={symbol}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
    

def get_conversion_factor(base_currency: str, target_currency: str, amount: float) -> float:
    """
    Convert a specific amount from one currency to another using real-time exchange rates.
    Use this tool when a user asks to convert money between different currencies. """
    api_key = os.getenv("CURRENCY_CONVERSION_API_KEY")
    url = f"https://api.exchangerate.host/convert?from={base_currency}&to={target_currency}&amount={amount}&access_key={api_key}"
    response = requests.get(url)
    return response.json()


def get_stock(symbol: str) -> str:
    """ Retrieve the latest intraday stock price and related information for a given company ticker symbol.
    Use this tool when a user asks for stock prices, share values, or stock market updates. """
    api_key = os.getenv("STOCK_API_KEY")
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&apikey={api_key}"
    response = requests.get(url)
    return response.json()


def calculator(a: float, b: float, operation: str) -> float:
    """ Perform basic arithmetic operations such as addition, subtraction, multiplication, division, power, and square root.
    Use this tool when a user asks to perform a mathematical calculation."""
    if operation == "add":
        return a + b
    elif operation == "subtract":
        return a - b
    elif operation == "product":
        return a * b
    elif operation == "divide":
        return a / b
    elif operation == "power":
        return a**b
    elif operation == "underroot":
        return np.sqrt(a)
    else:
        return None
    


def web_search(query: str) -> str:
    """Perform a general web search using DuckDuckGo and return the top results.
    """
    try:
        search = DuckDuckGoSearchRun()
        result = search.run(query)
        return result
    except Exception as e:
        return f"Error fetching search results: {str(e)}"


def wikipedia_search(query: str) -> str:
    """Searches Wikipedia for a given topic and returns a short summary.
    
    Use this when the user asks about factual, historical, or conceptual information.
    """
    try:
        wiki = WikipediaAPIWrapper()
        result = wiki.run(query)
        if result:
            return result
        else:
            return f"No relevant Wikipedia content found for '{query}'."
    except Exception as e:
        return f"Error fetching Wikipedia data: {str(e)}"





