import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def generate_sql(question):
    prompt = f"""
You are a MySQL query generator.

Database: ai_chatbot_db

Tables:
1. students(id, name, department, year_of_study)
2. subjects(id, subject_name)
3. marks(id, student_id, subject_id, marks)

Rules:
- Return only one valid MySQL SELECT query.
- Do not use INSERT, UPDATE, DELETE, DROP, or other modification commands.
- Use JOIN when information from multiple tables is required.
- Do not include markdown or explanations.

User question: {question}
"""

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt
    )

    return response.text.strip()