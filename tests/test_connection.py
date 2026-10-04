from llm.gemini_client import get_completion

response = get_completion("Reply with exactly 3 words: API is working")
print(response)