import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def summarize_text(text, max_tokens=300):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or gpt-4 if you're on pro
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes text."},
                {"role": "user", "content": f"Summarize this text:\n\n{text}"}
            ],
            max_tokens=max_tokens,
            temperature=0.7
        )
        return response.choices[0].message["content"].strip()
    except Exception as e:
        return f"Summary failed: {e}"
