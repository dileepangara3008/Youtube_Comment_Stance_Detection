import os
from groq import Groq
from dotenv import load_dotenv


load_dotenv() 

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def summarize_comments(comments):
    if not comments:
        return "No comments available"

    # Clean + limit
    text = "\n".join(comments[:50])[:3000]

    prompt = f"""
You are analyzing YouTube comments.

Summarize the overall public opinion clearly.

Focus on:
- What people support or oppose
- Main entities discussed
- Tone (positive, negative, sarcastic)

Comments:
{text}

Give a concise summary (4-5 lines).
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content.strip()