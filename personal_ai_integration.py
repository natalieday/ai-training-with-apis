import requests
import json
from markdown_parser import extract_qa_from_md
from openai_integration import get_question_variations_and_tags
from dotenv import load_dotenv  # Import load_dotenv
import os  # Import os

# Load environment variables from .env file
load_dotenv()

# Define Personal AI API credentials
personal_ai_api_url = "https://api.personal.ai/v1/memory"
personal_ai_api_key = os.getenv("personal_ai_api_key")  # Load from environment variable

def stack_memory(question, answer, tags=["#FAQ"]):
    # Add hashtag to tags if not present and clean them up
    formatted_tags = [f"#{tag.strip('#').strip()}" for tag in tags]
    
    headers = {
        "Content-Type": "application/json",
        "x-api-key": personal_ai_api_key
    }
    
    # Create topics from tags
    topics = [{
        "value": tag.strip('#'),
        "category": "CustomTag"
    } for tag in formatted_tags]
    
    data = {
        "Text": f"Question: {question}\nAnswer: {answer}",
        "RawFeedText": f"<b>Question:</b> {question}<br><b>Answer:</b> {answer}",
        "DomainName": "atomic-personal",
        "SourceName": "Markdown Q&A",
        "Tags": formatted_tags,
        "topics": topics,  # Add topics array
        "metadata": {
            "custom_tags": formatted_tags,  # Store tags in metadata too
            "source_type": "qa_pair",
            "is_tagged": "true"
        }
    }
    
    response = requests.post(personal_ai_api_url, json=data, headers=headers)
    
    # Print detailed response information
    print("\n=== Memory Stack Result ===")
    print(f"Status Code: {response.status_code}")
    print("Request Data:")
    print(json.dumps(data, indent=2))
    try:
        response_json = response.json()
        print("\nResponse Data:")
        print(json.dumps(response_json, indent=2))
    except json.JSONDecodeError:
        print("Raw Response:", response.text)
    
    return response.status_code, response.text

# Create qa_pairs here
qa_pairs = extract_qa_from_md("questions.md")  # Make sure questions.md exists in your directory

# Example usage: Stack only first 3 Q&A pairs
print(f"Total Q&A pairs available: {len(qa_pairs)}")
for question, answer in list(qa_pairs)[:3]:  # Only process first 3 pairs
    print("\n=== Processing New Q&A Pair ===")
    
    # Get variations and tags
    q_variations, a_variations, tags, title = get_question_variations_and_tags(question, answer)
    
    # Format the output message
    output_message = [
        f"Original Question: {question}\n",
        "Related Questions:\n" + "\n".join([f"- {i+1}. {var.split('.', 1)[-1].strip()}" for i, var in enumerate(q_variations)]) + "\n",
        f"Original Answer: {answer}\n",
        "Related Answers:\n" + "\n".join([f"- {i+1}. {var.split('.', 1)[-1].strip()}" for i, var in enumerate(a_variations)])
    ]
    
    print("\n".join(output_message))
    
    for i, variation in enumerate(q_variations, 1):
        print(f"\nProcessing variation {i}/{len(q_variations)}")
        print(f"Variation: {variation}")
        status, _ = stack_memory(variation, answer, tags)
        
        if status == 200:
            print("✅ Successfully stacked!")
        else:
            print("❌ Failed to stack!")