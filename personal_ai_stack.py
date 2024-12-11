import requests
import json
from openai_integration import get_question_variations_and_tags, qa_pairs
from dotenv import load_dotenv  # Import load_dotenv
import os  # Import os

# Load environment variables from .env file
load_dotenv()

# Define Personal AI API credentials
personal_ai_api_url = "https://api.personal.ai/v1/memory"
personal_ai_api_key = os.getenv("personal_ai_api_key")  # Load from environment variable

def create_qa_document(qa_pairs, title="FAQ Document"):
    """Create a formatted document from Q&A pairs with their variations"""
    
    # Build document content
    content_blocks = []
    all_tags = set()
    generated_title = None
    
    for question, answer in qa_pairs:
        # Get existing variations, answer variations, tags, and title
        q_variations, a_variations, tags, title = get_question_variations_and_tags(question, answer)
        generated_title = title
        
        # Create content block with new order
        block = [
            f"Original Question: {question}",
            "",
            "Related Questions:",
            ""
        ]
        # Add variations without double numbering
        block.extend([f"- {i+1}. {var.split('.', 1)[-1].strip()}" for i, var in enumerate(q_variations)])
        block.extend([
            "",
            f"Original Answer: {answer}",
            "",
            "Related Answers:",
            ""
        ])
        # Add answer variations without double numbering
        block.extend([f"- {i+1}. {var.split('.', 1)[-1].strip()}" for i, var in enumerate(a_variations)])
        content_blocks.append("\n".join(block))
        
        # Collect all tags
        all_tags.update(tags)
    
    # Join all blocks with separator
    full_content = "\n\n" + "="*50 + "\n\n".join(content_blocks)
    
    return full_content, list(all_tags), generated_title

def upload_qa_document(title="FAQ Document", limit=None):
    """Upload Q&A document with variations and tags"""
    
    # Get content, tags, and generated title
    content, tags, generated_title = create_qa_document(qa_pairs[:limit] if limit else qa_pairs)
    
    # Use the generated title if available
    if generated_title:
        title = generated_title
    
    # Format tags properly
    formatted_tags = []
    for tag in tags:
        # Split by newlines and numbers to get individual tags
        tag_parts = tag.split('\n')
        for part in tag_parts:
            # Remove numbers and clean up the tag
            cleaned_tag = part.strip()
            for i in range(1, 8):  # Remove numbers 1-7
                cleaned_tag = cleaned_tag.replace(f"{i}. ", "")
            if cleaned_tag:  # Only add non-empty tags
                formatted_tags.append(cleaned_tag.strip())
    
    headers = {
        "Content-Type": "application/json",
        "x-api-key": personal_ai_api_key
    }
    
    data = {
        "Text": content,
        "Title": title,
        "DomainName": "atomic-personal",
        "Tags": ",".join(formatted_tags),  # Join clean tags with commas
        "is_stack": True
    }
    
    try:
        print(f"\nUploading FAQ document: {title}")
        print(f"Number of Q&A pairs: {len(qa_pairs[:limit] if limit else qa_pairs)}")
        print(f"Tags: {', '.join(formatted_tags)}")  # Print tags for verification
        
        response = requests.post(personal_ai_api_url, json=data, headers=headers)
        
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("✅ Document successfully uploaded!")
            print("Response:", response.json())
        else:
            print("❌ Failed to upload document")
            print("Response:", response.text)
        
        return response.status_code == 200
        
    except Exception as e:
        print(f"Error uploading document: {e}")
        return False

def main():
    # Debug: Print total number of QA pairs available
    print(f"\nTotal Q&A pairs available: {len(qa_pairs)}")
    
    if not qa_pairs:
        print("❌ Error: No Q&A pairs found! Check if questions.md exists and is not empty.")
        return
    
    # Print the first Q&A pair
    first_question, first_answer = qa_pairs[0]
    print("\nTesting with first Q&A pair:")
    print(f"Question: {first_question}")
    print(f"Answer: {first_answer}")
    
    print("\nGenerating variations and tags...")
    q_variations, a_variations, tags, title = get_question_variations_and_tags(first_question, first_answer)  # Added first_answer
    print(f"Generated {len(q_variations)} question variations and {len(a_variations)} answer variations")
    print(f"Title: {title}")
    print("Tags:", tags)
    
    # Upload just the first Q&A pair
    print("\nAttempting to upload...")
    success = upload_qa_document(
        title=title,  # Use the generated title instead of "Single Question Test"
        limit=1
    )
    
    if success:
        print("\n✅ Single Q&A document processing completed successfully!")
    else:
        print("\n❌ Single Q&A document processing failed!")

if __name__ == "__main__":
    main()