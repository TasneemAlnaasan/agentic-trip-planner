import json
from groq import Groq
from config import settings
from tools.weather import get_weather
from tools.places import get_places
from tools.search import search_prices
from tools.geocode import get_coordinates

get_weather_schema = {
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Returns the weather forecast (temperature and condition) for a given location, for a specific number of days",
        "parameters": {
            "type": "object",
            "properties": {
                "latitude": {"type": "number", "description": "Latitude of the location"},
                "longitude": {"type": "number", "description": "Longitude of the location"},
                "days": {"type": "integer", "description": "Number of forecast days requested"}
            },
            "required": ["latitude", "longitude"]
        }
    }
}

get_places_schema = {
    "type": "function",
    "function": {
        "name": "get_places",
        "description": "Returns a specified number of tourist attraction names near a given location, within a given radius",
        "parameters": {
            "type": "object",
            "properties": {
                "latitude": {"type": "number", "description": "Latitude of the location"},
                "longitude": {"type": "number", "description": "Longitude of the location"},
                "radius": {"type": "number", "description": "Radius of the circle to search for tourist attractions within"},
                "limit": {"type": "number", "description": "Maximum number of tourist attractions to return"}
            },
            "required": ["latitude", "longitude"]
        }
    }
}

search_prices_schema = {
    "type": "function",
    "function": {
        "name": "search_prices",
        "description": "Returns approximate prices for hotels and tourist attractions by searching the web",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "A question about approximate prices for tourist attractions and hotels"}
            },
            "required": ["query"]
        }
    }
}

get_coordinates_schema = {
    "type": "function",
    "function": {
        "name": "get_coordinates",
        "description": "Returns the coordinates for a location based on its name",
        "parameters": {
            "type": "object",
            "properties": {
                "place_name": {"type": "string", "description": "The name of the location"}
            },
            "required": ["place_name"]
        }
    }
}

tools = [get_weather_schema, get_places_schema, search_prices_schema, get_coordinates_schema]



available_functions = {
    "get_weather": get_weather,
    "get_places": get_places,
    "search_prices": search_prices,
    "get_coordinates": get_coordinates,
}

client = Groq(api_key=settings.groq_api_key)


def run_planner(user_query):
    messages = [
        {"role": "system", "content": "You are a helpful trip planner assistant, schedule a program based on the information in the user's query"},
        {"role": "user", "content": user_query}
    ]

    step_count = 0
    max_steps = 10
    collected_data = {}

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )
    response_message = response.choices[0].message

    while response_message.tool_calls and step_count < max_steps:
        messages.append(response_message)

        for tool_call in response_message.tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)

        
            if function_name not in available_functions:
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": function_name,
                    "content": json.dumps({
                        "error": f"Tool '{function_name}' does not exist. Please use one of the available tools."
                    })
                })
                continue

            function_to_call = available_functions[function_name]
            result = function_to_call(**function_args)

            collected_data[function_name] = result

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": function_name,
                "content": json.dumps(result)
            })

        new_response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )
        response_message = new_response.choices[0].message
        step_count += 1

    return response_message.content, collected_data


if __name__ == "__main__":
    query = "Plan a 3-day trip to Petra"
    final_text, data = run_planner(query)
    print(final_text)
    print("\n--- Collected data ---")
    print(data)
