def answer_question(question):
    return f"""
Answer the following academic question clearly and accurately.

Question:
{question}
"""

def summarize_text(text):
    return f"""
Summarize the following academic text concisely.

Text:
{text}
"""

def explain_concept(concept, level):
    return f"""
Explain the following concept at a {level} level.
Use structured explanation and examples.

Concept:
{concept}
"""

def ask_from_document(document, question):
    return f"""
Answer the question strictly using the given document.

Document:
{document}

Question:
{question}
"""

def generate_key_points(text):
    return f"""
Convert the following academic text into clear exam-oriented key points.

Text:
{text}
"""

def generate_questions(text):
    return f"""
Generate important academic questions (short and long) from the following text.

Text:
{text}
"""