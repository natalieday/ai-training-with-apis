from markdown_parser import extract_qa_from_md  # Import the markdown parser
from openai_integration import get_question_variations_and_tags
from personal_ai_text_doc import upload_qa_document

def process_multiple_questions(qa_pairs):
    """Process and upload multiple Q&A pairs."""
    for question, answer in qa_pairs:
        print(f"Processing question: {question}")
        
        # Generate variations and tags using OpenAI integration
        q_variations, a_variations, tags, title = get_question_variations_and_tags(question, answer)
        
        # Prepare the data for upload
        content = {
            "question": question,
            "answer": answer,
            "variations": q_variations,
            "answer_variations": a_variations,
            "tags": tags,
            "title": title
        }
        
        # Upload the Q&A document
        success = upload_qa_document(content)
        if success:
            print(f"✅ Successfully uploaded Q&A: {question}")
        else:
            print(f"❌ Failed to upload Q&A: {question}")

def main():
    print("Starting the process...")
    
    # Extract Q&A pairs from the markdown file
    qa_pairs = extract_qa_from_md("questions.md")
    
    # Check if qa_pairs is empty
    if not qa_pairs:
        print("❌ No Q&A pairs found in the markdown file.")
        return

    print(f"✅ Found {len(qa_pairs)} Q&A pairs.")
    
    # Process and upload multiple questions
    process_multiple_questions(qa_pairs)

# Run the script
if __name__ == "__main__":
    main()