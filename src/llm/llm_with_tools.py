# src/pipeline/tool_binding.py
from src.tools.run_tool import calculate_bmi,calculator,get_conversion_factor,get_stock,get_weather_update,web_search,wikipedia_search
from src.llm.llm_base import model





def llm_with_tool():
    """
    Binds the base model with all available tools.
    Returns a model instance that can call tools automatically.
    """
    tools= [calculate_bmi,calculator,get_conversion_factor,get_stock,get_weather_update,web_search,wikipedia_search]
    return model.bind_tools(tools)

model_with_tool = llm_with_tool()





