import requests
import json
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv  # Import load_dotenv
import os  # Import os

# Load environment variables from .env file
load_dotenv()

# Define Personal AI API credentials
personal_ai_api_url = "https://api-enterprise.personal.ai/v1/memory"  # Changed to enterprise endpoint
personal_ai_api_key = os.getenv("personal_ai_api_key")

def get_recent_memories(hours_ago=24):
    """Retrieve memories from the last X hours"""
    
    headers = {
        "Content-Type": "application/json",
        "x-api-key": personal_ai_api_key
    }
    
    # Calculate time range using timezone-aware datetime
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(hours=hours_ago)
    
    # Format times for API
    start_time_str = start_time.strftime("%Y-%m-%dT%H:%M:%S.000Z")
    end_time_str = end_time.strftime("%Y-%m-%dT%H:%M:%S.000Z")
    
    # Request body for POST - updated based on docs
    data = {
        "Text": "",  # Required field according to docs
        "RawFeedText": "",
        "DomainName": "atomic-personal",
        "CreatedTime": start_time_str,
        "SourceName": "Markdown Q&A"
    }
    
    try:
        print("\nAttempting to retrieve memories...")
        print(f"Request URL: {personal_ai_api_url}")
        print(f"Request Body:", json.dumps(data, indent=2))
        
        response = requests.post(
            personal_ai_api_url,
            headers=headers,
            json=data
        )
        
        print(f"Response Status: {response.status_code}")
        
        if response.status_code == 200:
            memories = response.json()
            return memories
        else:
            print(f"Error retrieving memories: {response.status_code}")
            print("Response Headers:", response.headers)
            print("Response Text:", response.text)
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None


def display_memory_details(memory):
    """Format and display key information about a memory"""
    print("\n=== Memory Details ===")
    print(f"Created: {memory.get('created_at_utc')}")
    
    # Extract question and answer from the memory text
    memory_text = memory.get('memlabel', '')
    if 'Question:' in memory_text and 'Answer:' in memory_text:
        question = memory_text.split('Answer:')[0].replace('Question:', '').strip()
        answer = memory_text.split('Answer:')[1].strip()
        print(f"Question: {question}")
        print(f"Answer: {answer[:100]}...")  # Show first 100 chars of answer
    
    # Display tags if present
    if 'metadata' in memory and 'tags' in memory['metadata']:
        print(f"Tags: {memory['metadata']['tags']}")
    
    print(f"Memory ID: {memory.get('id')}")
    print(f"Status: {memory.get('status')}")

def main():
    print("Retrieving recently stored memories...")
    memories = get_recent_memories(hours_ago=1)
    
    if memories:
        print(f"\nFound {len(memories)} memories from the past hour:")
        for memory in memories:
            display_memory_details(memory)
    else:
        print("No memories found or error occurred.")

if __name__ == "__main__":
    main()