"""List Gemini models available to your API key."""

import os

from dotenv import load_dotenv

load_dotenv()

from google import genai

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

print("Models available to your API key:\n")

for model in client.models.list():
    if model.supported_actions and "generateContent" in model.supported_actions:
        print(model.name)