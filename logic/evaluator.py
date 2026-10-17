import json
from groq import Groq
from config import settings

client = Groq(api_key=settings.groq_api_key)


def basic_check(collected_data):
    if "get_weather" not in collected_data:
        return False, "No weather data collected"

    if "get_places" not in collected_data:
        return False, "No places data collected"

    if "search_prices" not in collected_data:
        return False, "No price data collected"

    return True, "All required data is present"


def model_judgment(itinerary_text):
    system_prompt = (
        "You judge whether a trip itinerary is sufficient and consistent. "
        "Infer the number of days planned directly from the itinerary text. "
        "Check if the suggested places for each day are close to each other, "
        "if the number of suggested places for each day is sufficient, "
        "and if the provided prices relate to the specified place. "
        "Respond only with a JSON object in this exact format: "
        '{"is_sufficient": true or false, "reason": "a short explanation"}'
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Itinerary text: {itinerary_text}"}
    ]

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=messages,
        response_format={"type": "json_object"}
    )

    content = response.choices[0].message.content
    result = json.loads(content)
    return result


def evaluate(collected_data, itinerary_text):
    gate_passed, gate_reason = basic_check(collected_data)

    if not gate_passed:
        return {"is_sufficient": False, "reason": gate_reason}

    judgment = model_judgment(itinerary_text)
    return judgment
