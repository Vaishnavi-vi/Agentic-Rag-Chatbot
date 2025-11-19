import os
import requests
import numpy as np
from typing import Tuple
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.tools import tool
from langchain_community.utilities import WikipediaAPIWrapper
from dotenv import load_dotenv
from langsmith import traceable

load_dotenv()

#tool Function 
@traceable(name="tool_calculate_bmi")
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


@traceable(name="tool_weather_update")
def get_weather_update(city: str):
    """Fetch the current weather for a city and return a clean text message."""
    api_key = os.getenv("WEATHER_API_KEY")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()

        # Errors from API
        if data.get("cod") != 200:
            return f"Sorry, I couldn't find the weather for '{city}'."

        description = data["weather"][0]["description"]
        temp = data["main"]["temp"]

        # Return human-readable text (not JSON)
        return f"The weather in {city} is {description} with {temp}°C."

    except Exception as e:
        return f"Failed to fetch weather data: {str(e)}"


@traceable(name="tool_currency_conversion")
def get_conversion_factor(base_currency: str, target_currency: str, amount: float) -> str:
    """
    Convert a specific amount from one currency to another using real-time exchange rates.
    Returns a human-readable message.
    """
    api_key = os.getenv("CURRENCY_CONVERSION_API_KEY")
    url = f"https://api.exchangerate.host/convert?from={base_currency}&to={target_currency}&amount={amount}&access_key={api_key}"

    try:
        response = requests.get(url)
        data = response.json()

        # Check for success
        if not data.get("success", True):  # exchangerate.host returns True if success
            return f"Sorry, couldn't convert {amount} {base_currency} to {target_currency}."

        converted_amount = data.get("result")
        if converted_amount is None:
            return f"Conversion failed for {amount} {base_currency} to {target_currency}."

        return f"{amount} {base_currency.upper()} = {converted_amount:.2f} {target_currency.upper()}"

    except Exception as e:
        return f"Error converting currency: {str(e)}"

@traceable(name="tool_stock_update")
def get_stock(symbol: str):
    """
    Fetch the current stock price for a given symbol and provide a simple forecast.
    """
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY")  # Get your free API key from https://www.alphavantage.co
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}"

    try:
        response = requests.get(url)
        data = response.json()

        if "Time Series (Daily)" not in data:
            return f"Sorry, I couldn't find data for stock symbol '{symbol}'."

        time_series = data["Time Series (Daily)"]
        latest_date = list(time_series.keys())[0]
        latest_data = time_series[latest_date]
        closing_price = float(latest_data["4. close"])

        # Simple "prediction": compare last two days
        previous_date = list(time_series.keys())[1]
        previous_close = float(time_series[previous_date]["4. close"])
        trend = "up" if closing_price > previous_close else "down" if closing_price < previous_close else "stable"

        return f"The latest closing price of {symbol} is ${closing_price:.2f}. The stock seems to be {trend} compared to yesterday."
    
    except Exception as e:
        return f"Error fetching stock data: {str(e)}"

    

@traceable(name="tool_calculator")
def calculator(a: float, b: float, operation: str) -> float:
    """ Perform basic arithmetic operations such as addition, subtraction, multiplication, division, power, and square root.
    Use this tool when a user asks to perform a mathematical calculation."""
    if operation == "add":
        return a + b
    elif operation == "subtract":
        return a - b
    elif operation == "multiply":
        return a * b
    elif operation == "divide":
        return a / b
    elif operation == "power":
        return a**b
    elif operation == "squareroot":
        return np.sqrt(a)
    else:
        return None

@traceable(name="tool_web_search")
def web_search(query: str) -> str:
    """Perform a general web search using DuckDuckGo and return the top results.
    """
    try:
        search = DuckDuckGoSearchRun(region="us-en")
        result = search.run(query)
        return result
    except Exception as e:
        return f"Error fetching search results: {str(e)}"

@traceable(name="tool_wikipedia_search")
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





