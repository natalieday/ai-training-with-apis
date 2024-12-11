import requests
import json
from dotenv import load_dotenv  # Import load_dotenv
import os  # Import os

# Load environment variables from .env file
load_dotenv()

NOTION_API_URL = "https://api.notion.com/v1/databases/119bcf47784e80c69297d0db2e10f265/query"
NOTION_TOKEN = os.getenv("notion_api_key")

def fetch_questions_from_notion():
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"  # Use the latest version
    }
    
    response = requests.post(NOTION_API_URL, headers=headers)
    if response.status_code == 200:
        data = response.json()
        questions = []
        for result in data.get("results", []):
            question = result["properties"]["Question"]["title"][0]["text"]["content"]
            answer = result["properties"]["Answer"]["rich_text"][0]["text"]["content"]
            questions.append((question, answer))
        return questions
    else:
        print("Failed to fetch data from Notion:", response.status_code, response.text)
        return []
    
def update_questions_md(new_questions):
    with open("questions.md", "a") as f:
        for question, answer in new_questions:
            f.write(f"Q: {question}\nA: {answer}\n\n")

def get_new_questions(existing_questions, fetched_questions):
    existing_set = set(existing_questions)
    new_questions = [q for q in fetched_questions if q not in existing_set]
    return new_questions