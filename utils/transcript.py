from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from groq import Groq
import re
import os


from dotenv import load_dotenv


load_dotenv() 

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def extract_video_id(url_or_id):
    if len(url_or_id) == 11:
        return url_or_id
    match = re.search(r"(?:v=|youtu\.be/)([a-zA-Z0-9_-]{11})", url_or_id)
    return match.group(1) if match else None


def get_transcript_text(video_input):
    video_id = extract_video_id(video_input)
    if not video_id:
        return None

    api = YouTubeTranscriptApi()

    try:
        transcript_list = api.list(video_id)

        transcript = None

        try:
            transcript = transcript_list.find_manually_created_transcript(['en'])
        except:
            pass

        if transcript is None:
            try:
                transcript = transcript_list.find_generated_transcript(['en'])
            except:
                pass

        if transcript is None:
            transcript = next(iter(transcript_list), None)
            if transcript is None:
                return None

        data = transcript.fetch()
        text = " ".join([t.text for t in data]).replace("\n", " ").strip()

        if len(text) < 50:
            return None

        return text[:12000]

    except (TranscriptsDisabled, NoTranscriptFound):
        return None
    except Exception as e:
        print("Transcript error:", e)
        return None


def summarize_with_groq(text):
    try:
        prompt = f"""
        Summarize the following YouTube video transcript clearly and concisely.
        Focus on the main topic and key concepts.

        Transcript:
        {text}
        """

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You summarize educational content."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print("Groq error:", e)
        return None


# ✅ FINAL FUNCTION (returns text)
def get_video_summary(video_input, debug=False):
    transcript = get_transcript_text(video_input)

    if not transcript:
        return None

    summary = summarize_with_groq(transcript)

    if debug:
        print("\n🎯 VIDEO SUMMARY:\n")
        print(summary)

    return summary  # ✅ THIS is what you wanted
