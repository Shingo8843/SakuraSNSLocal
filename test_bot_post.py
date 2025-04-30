from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Ollama client
client = OpenAI(
    base_url='http://localhost:11434/v1',
    api_key='ollama',  # required, but unused
)

# Test bot personality
test_personality = "A friendly and enthusiastic tech enthusiast who loves sharing interesting facts about technology and AI."

try:
    response = client.chat.completions.create(
        model="gemma2:2b",  # using gemma2:2b model from Ollama
        messages=[
            {"role": "system", "content": f"You are a social media bot with the following personality: {test_personality}"},
            {"role": "user", "content": "Create a social media post that reflects your personality."}
        ]
    )
    print("Generated post:")
    print(response.choices[0].message.content)
except Exception as e:
    print(f"Error: {str(e)}") 