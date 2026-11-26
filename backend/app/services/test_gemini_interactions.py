
import os
import time
from pathlib import Path

from dotenv import load_dotenv
from google import genai


PROJECT_ROOT = Path(__file__).resolve().parents[3]
load_dotenv(PROJECT_ROOT / ".env")

API_KEY = (
    os.getenv("GEMINI_API_KEY")
    or os.getenv("GOOGLE_API_KEY")
)

if not API_KEY:
    raise ValueError("Gemini API key not found in .env")

client = genai.Client(api_key=API_KEY)


print("\nTesting Gemini Interactions API...", flush=True)

start = time.time()

try:
    interaction = client.interactions.create(
        model="gemini-4-hydrogen",
        input="Reply with only: SchemeWise API connection successful.",
        generation_config={
            "max_output_tokens": 128,
            "thinking_level": "low",
        },
        timeout=30,
    )

    print("\nStatus:", interaction.status)
    print("Response:", interaction.output_text)
    print("Time taken:", round(time.time() - start, 2), "seconds")

except Exception as error:
    print("\nAPI test failed:")
    print(type(error).__name__, error)
    print("Time taken:", round(time.time() - start, 2), "seconds")

finally:
    client.close()
