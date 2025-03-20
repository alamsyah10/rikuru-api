from fastapi import APIRouter, HTTPException
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_ORGANIZATION_ID = os.getenv("OPENAI_ORGANIZATION_ID")
OPENAI_PROJECT_ID = os.getenv("OPENAI_PROJECT_ID")
client = OpenAI()
print(OPENAI_API_KEY)
print(OPENAI_PROJECT_ID)
print(OPENAI_ORGANIZATION_ID)


def call_gpt(text: str, prompt: str) -> dict:
    if not OPENAI_API_KEY:
        raise HTTPException(status_code=500, detail="OpenAI API key is missing")

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini", 
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": text}
            ]   
        )
        return {"response": response.choices[0].message.content}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))