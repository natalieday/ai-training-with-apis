from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Check if the .env file was loaded
print("Environment variables loaded.")

# Access the API keys
gpt_api_key = os.getenv("gpt_api_key")
personal_ai_api_key = os.getenv("personal_ai_api_key")

# Check if the keys are loaded
if gpt_api_key is None:
    print("Failed to load GPT_API_KEY")
if personal_ai_api_key is None:
    print("Failed to load PERSONAL_AI_API_KEY")

# Now you can use these keys in your code
print("OpenAI API Key:", gpt_api_key)
print("Personal AI API Key:", personal_ai_api_key)