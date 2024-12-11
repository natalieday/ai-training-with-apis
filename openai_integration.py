import openai
from markdown_parser import extract_qa_from_md
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access the API key
gpt_api_key = os.getenv("gpt_api_key")

# Extract Q&A pairs from the Markdown file
qa_pairs = extract_qa_from_md("questions.md")

client = openai.OpenAI(api_key=gpt_api_key)

def get_question_variations_and_tags(question, answer, n_variations=7, n_tags=7):
    """Generate variations, answer variations, tags, and a title for a Q&A pair"""
    
    # Generate question variations
    variation_response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates question variations."},
            {"role": "user", "content": f"Generate {n_variations} different versions of this question: {question}"}
        ],
        model="gpt-3.5-turbo",
    )
    question_variations = [q.strip() for q in variation_response.choices[0].message.content.split("\n") if q.strip()]

    # Generate answer variations
    answer_response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates answer variations while maintaining accuracy."},
            {"role": "user", "content": f"Generate {n_variations} different ways to express this answer, keeping the same meaning: {answer}"}
        ],
        model="gpt-3.5-turbo",
    )
    answer_variations = [a.strip() for a in answer_response.choices[0].message.content.split("\n") if a.strip()]

    # Generate tags
    tag_response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates relevant tags."},
            {"role": "user", "content": f"Generate {n_tags} relevant tags for this Q&A: Question: {question}\nAnswer: {answer}"}
        ],
        model="gpt-3.5-turbo",
    )
    tags = [t.strip() for t in tag_response.choices[0].message.content.split(",") if t.strip()]

    # Generate title
    title_response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates concise, descriptive titles."},
            {"role": "user", "content": f"Generate a short, descriptive title (5-8 words) for this Q&A pair:\nQuestion: {question}\nAnswer: {answer}"}
        ],
        model="gpt-3.5-turbo",
    )
    title = title_response.choices[0].message.content.strip()

    return question_variations, answer_variations, tags, title

# Example usage
for question, answer in qa_pairs[:3]:  # Process only the first 3 Q&A pairs
    q_variations, a_variations, tags, title = get_question_variations_and_tags(question, answer)
    print(f"Title: {title}")
    print(f"\nOriginal Question: {question}")
    print("Question Variations:")
    for i, var in enumerate(q_variations, 1):
        print(f"- {i}. {var}")
    print("\nOriginal Answer: {answer}")
    print("Answer Variations:")
    for i, var in enumerate(a_variations, 1):
        print(f"- {i}. {var}")
    print("\nTags:")
    for tag in tags:
        print(f"- {tag}")
    print("\n" + "="*50 + "\n")