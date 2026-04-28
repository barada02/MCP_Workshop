import asyncio
import os
from dotenv import load_dotenv
from openai import AsyncOpenAI

# Load environment variables
load_dotenv()

# Initialize OpenAI Client
# Base URL and API Key are automatically pulled from OPENAI_BASE_URL and OPENAI_API_KEY env variables
openai_client = AsyncOpenAI()
MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-4o")

async def test_connection():
    print(f"Testing connection to LLM provider...")
    print(f"Using Model: {MODEL_NAME}")
    print(f"Using Base URL: {os.getenv('OPENAI_BASE_URL')}")

    try:
        response = await openai_client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": "Hello!, what should i call you? do you have a name?"}],
            max_tokens=500
        )
        print("\nSuccess! Received response:")
        print(f"AI: {response.choices[0].message.content}")
        
    except Exception as e:
        print(f"\nError: Failed to connect or generate response.")
        print(f"Details: {e}")

if __name__ == "__main__":
    asyncio.run(test_connection())