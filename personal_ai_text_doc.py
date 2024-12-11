import os
import requests
from dotenv import load_dotenv
from openai_integration import get_question_variations_and_tags, qa_pairs
import re

# Load environment variables
load_dotenv()
personal_ai_api_url = "https://api.personal.ai/v1/upload-text"
personal_ai_api_url_stack = "https://api.personal.ai/v1/memory"
personal_ai_api_key = os.getenv("personal_ai_api_key")


def format_qa_content(question, answer, q_variations, a_variations):
    """
    Format the content for uploading in the correct structure.
    """
    content = [
        f"Original Question: {question}",
        "",
        "Related Questions:",
        *[f"- {i + 1}. {q.split('.', 1)[-1].strip()}" for i, q in enumerate(q_variations)],  # Remove existing numbers
        "",
        f"Original Answer: {answer}",
        "",
        "Related Answers:",
        *[f"- {i + 1}. {a.split('.', 1)[-1].strip()}" for i, a in enumerate(a_variations)],  # Remove existing numbers
    ]
    return "\n".join(content)


def upload_qa_document(content, title, tags):
    """
    Upload the formatted content to the Personal AI API with properly formatted tags.
    """
    headers = {
        "Content-Type": "application/json",
        "x-api-key": personal_ai_api_key
    }

    # Process and clean up tags
    formatted_tags = []
    for tag in tags:
        tag_parts = tag.split('\n')
        for part in tag_parts:
            cleaned_tag = part.strip()
            for i in range(1, 8):  # Remove numbers 1-7
                cleaned_tag = cleaned_tag.replace(f"{i}. ", "")
            if cleaned_tag:
                formatted_tags.append(cleaned_tag.strip())

    data = {
        "Text": content,
        "Title": title,
        "DomainName": "atomic-personal",
        "Tags": ",".join(formatted_tags),  # Join clean tags with commas
        "is_stack": True  # Keep all related content in one memory block
    }

    data_stack = {
        "Text": content,
        "SourceName": "Customer Q&A",
        "DomainName": "atomic-personal",
        "Tags": ",".join(formatted_tags),  # Join clean tags with commas
    }

    response = requests.post(personal_ai_api_url, json=data, headers=headers)
    response_stack = requests.post(personal_ai_api_url_stack, json=data_stack, headers=headers)

    if response.status_code == 200:
        print(f"✅ Successfully uploaded: {title}")
    else:
        print(f"❌ Failed to upload: {title}")
        print("Response:", response.text)

    if response_stack.status_code == 200:
        print(f"✅ Successfully uploaded stack: {title}")
    else:
        print(f"❌ Failed to upload stack: {title}")
        print("Response:", response_stack.text)


def main():
    """
    Process and upload Q&A pairs with complete formatting.
    """
    for idx, (question, answer) in enumerate(qa_pairs):
        print(f"Processing Q&A pair {idx + 1}/{len(qa_pairs)}...")

        # Generate variations and tags
        q_variations, a_variations, tags, title = get_question_variations_and_tags(question, answer)

        # Format the content
        content = format_qa_content(question, answer, q_variations, a_variations)

        # Upload the document as one cohesive memory block
        upload_qa_document(content, title, tags)


if __name__ == "__main__":
    main()
