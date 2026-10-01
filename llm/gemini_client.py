import os
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