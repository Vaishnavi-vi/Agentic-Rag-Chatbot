from src.tools.run_tool import calculate_bmi,calculator,get_weather_update,get_conversion_factor,get_stock,web_search,wikipedia_search
from langgraph.prebuilt import ToolNode
from langchain_core.tools import StructuredTool
from langchain_community.tools import DuckDuckGoSearchRun

tools=[calculate_bmi,calculator,get_weather_update,get_conversion_factor,get_stock,web_search,wikipedia_search]

search_tool = DuckDuckGoSearchRun(name="search_tool", description="Get recent updates from the internet")
tools = [
    StructuredTool.from_function(calculator, description="Performs basic arithmetic operations."),
    StructuredTool.from_function(calculate_bmi,description="calculates bmi and tell in which category a person belong to"),
    StructuredTool.from_function(get_weather_update,description="Fetch latest weather update"),
    StructuredTool.from_function(get_conversion_factor,description="fetches the currency conversion factor between a given base currency and a target currency"),
    StructuredTool.from_function(get_stock,description="Fetches the latest stock price for a given company symbol "),
    StructuredTool.from_function(wikipedia_search,description="""Searches Wikipedia for a given topic and returns a short summary.
    Use this when the user asks about factual, historical, or conceptual information"""),
    StructuredTool.from_function(web_search,description="Perform a general web search using DuckDuckGo and return the top results.")

    

]
tool_node = ToolNode(tools)
