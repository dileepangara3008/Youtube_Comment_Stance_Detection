import os
from groq import Groq

from dotenv import load_dotenv
load_dotenv() 

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

VALID_LABELS = ["favor", "against", "neutral"]

def predict_llm(text, topic):
    prompt = f"""
You are a stance detection system.

Task:
Classify the stance of the given text towards the topic.

Rules:
- Output ONLY one word: favor / against / neutral
- Do NOT explain
- Do NOT output anything else

Text: {text}
Topic: {topic}
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=5
        )

        output = response.choices[0].message.content.strip().lower()

        if output not in VALID_LABELS:
            return "neutral"

        return output

    except Exception as e:
        print("LLM Error:", e)
        return "neutral"