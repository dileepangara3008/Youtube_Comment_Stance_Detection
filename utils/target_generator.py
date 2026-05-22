import os
from groq import Groq
from dotenv import load_dotenv


load_dotenv() 

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# ================================
# 🎯 MAIN TARGET GENERATOR
# ================================
def generate_target(text, title=""):
    """
    Extracts the main subject (target) from given text (summary or transcript)
    Works for all domains (politics, tech, education, etc.)
    """

    prompt = f"""
You are given content from a YouTube video.

Your task is to extract the MAIN SUBJECT of discussion.

DEFINITION:
The "target" is the primary entity, concept, product, person, or topic that the content is mainly ABOUT.

STRICT RULES:
- Output ONLY 1 to 3 words
- Must be specific and meaningful
- Must represent the core subject being discussed

DO NOT RETURN:
- Speaker / narrator / YouTuber name
- Channel name
- Words like "video", "analysis", "discussion"
- Generic terms like "issue", "topic", "problem"

PREFER:
- Person being discussed (not the speaker)
- Product / technology
- Organization
- Event
- Concept

GOOD EXAMPLES:
Content: A video explaining Narendra Modi's policies and decisions
Answer: Narendra Modi

Content: Review of iPhone 15 features and performance
Answer: iPhone 15

Content: Discussion on Israel and Iran conflict
Answer: Israel Iran

Content: Tutorial on Python decorators
Answer: Python decorators

BAD EXAMPLES:
- youtube video
- dhruv rathee
- explanation
- analysis

Now analyze:

Title:
{title}

Content:
{text[:1000]}

Answer ONLY the target phrase.
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        target = response.choices[0].message.content.strip().lower()

        return post_process_target(target)

    except Exception as e:
        print("⚠️ Target generation error:", e)
        return "unknown"


# ================================
# 🧹 POST PROCESSING
# ================================
def post_process_target(target):
    """
    Cleans and validates target output
    """

    blocked_words = [
        "video", "analysis", "discussion", "topic",
        "problem", "issue", "content"
    ]

    # remove unwanted outputs
    if target in blocked_words:
        return "unknown"

    # remove too short / noisy outputs
    if len(target.strip()) < 3:
        return "unknown"

    return target


# ================================
# 🔁 FALLBACK (COMMENTS BASED)
# ================================
def generate_target_from_comments(comments):
    """
    Fallback if transcript/summary fails
    """

    text = " ".join(comments[:50])
    return generate_target(text)