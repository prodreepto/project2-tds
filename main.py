from fastapi import FastAPI, File, UploadFile, Form
from pydantic import BaseModel
import openai
import os

# Load OpenAI API key
openai.api_key = os.getenv("eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjI0ZjEwMDI1NjBAZHMuc3R1ZHkuaWl0bS5hYy5pbiJ9.eYRQN8kEMUrHOrAs1c5oOeWtlAurqCE1cpJcaxb4vIg")

app = FastAPI()

class QuestionRequest(BaseModel):
    question: str

@app.post("/api/")
async def get_answer(question: str = Form(...), file: UploadFile = File(None)):
    """
    API endpoint to get an answer to a graded assignment question.
    Accepts:
    - `question`: The text of the question (required)
    - `file`: An optional file for additional context (e.g., PDFs, CSVs)
    """
    
    # If a file is uploaded, process it (currently just reading for debugging)
    file_text = None
    if file:
        file_text = await file.read()
        file_text = file_text.decode("utf-8")[:500]  # Limit to first 500 characters
    
    # Construct the prompt for the LLM
    prompt = f"Answer this IIT Madras Data Science assignment question:\n\n{question}"
    
    if file_text:
        prompt += f"\n\nAdditional context from file:\n{file_text}"

    # Query OpenAI API (or any LLM you're using)
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are an expert in Data Science."},
                  {"role": "user", "content": prompt}]
    )

    answer = response["choices"][0]["message"]["content"]
    
    return {"question": question, "answer": answer}
