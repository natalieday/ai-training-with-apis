def extract_qa_from_md(file_path):
    qa_pairs = []
    with open(file_path, "r") as file:
        lines = file.readlines()

    question, answer = None, None
    for line in lines:
        if line.startswith("Q:"):  # Start of a new question
            if question and answer:
                qa_pairs.append((question.strip(), answer.strip()))
            question = line[3:].strip()  # Remove "Q: " from the line
            answer = None
        elif line.startswith("A:"):  # Start of an answer
            answer = line[3:].strip()
        elif answer is not None:  # Append additional lines to the answer
            answer += " " + line.strip()

    if question and answer:  # Append the last Q&A pair
        qa_pairs.append((question.strip(), answer.strip()))
    return qa_pairs

# Create qa_pairs as a module-level variable
qa_pairs = extract_qa_from_md("questions.md")
print(qa_pairs)  # [(question1, answer1), (question2, answer2), ...]
