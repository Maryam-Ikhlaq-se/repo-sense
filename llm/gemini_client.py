import os
import json
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key = os.getenv("GEMINI_API_KEY"))

def get_completion(prompt: str) -> str:
    """
    Single responsibility: Send prompt to Gemini, return text response.
    No business logic. No formatting. Just the API call.
    """

    response = client.models.generate_content(
       model = "gemini-3.8-flash",
       contents = prompt
    )
    return response.text

def get_structured_response(prompt: str) -> dict:
    """
    Sends prompt to Gemini and parses the JSON response.

    Args:
        prompt (str): Structured prompt from prompt_builder

    Returns:
        dict: Parsed JSON response from Gemini

    Raises:
        ValueError: If response cannot be parsed as JSON
    """

    raw_response = get_completion(prompt)

    # Remove markdown code fences if Gemini adds them
    clean_response = raw_response.strip()
    if clean_response.startswith("```"):
        clean_response = clean_response.split("```")[1]
        if clean_response.startswith("json"):
            clean_response = clean_response[4:]

    try:
        return json.loads(clean_response)
    except json.JSONDecodeError as e:
        raise ValueError(f"Gemini response was not valid JSON: {e}\nRaw: {raw_response}")