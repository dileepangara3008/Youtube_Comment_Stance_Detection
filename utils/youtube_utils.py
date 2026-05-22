import re
import os
from googleapiclient.discovery import build

from dotenv import load_dotenv


load_dotenv() 

youtube = build("youtube", "v3", developerKey=os.getenv("API_KEY"))


def extract_video_id(url):
    pattern = r"(?:v=|youtu\.be/)([a-zA-Z0-9_-]{11})"
    match = re.search(pattern, url)
    return match.group(1) if match else None


def get_comments(video_id, max_comments=50, order_type="relevance"):
    comments = []
    next_page_token = None

    while True:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=100,
            pageToken=next_page_token,
            textFormat="plainText",
            order=order_type   # 🔥 dynamic order
        )

        response = request.execute()

        for item in response.get("items", []):
            snippet = item["snippet"]["topLevelComment"]["snippet"]

            text = snippet["textDisplay"].strip()
            likes = snippet["likeCount"]

            if len(text) > 5:
                comments.append({
                    "text": text,
                    "likes": likes
                })

            if len(comments) >= max_comments:
                break

        if len(comments) >= max_comments:
            break

        next_page_token = response.get("nextPageToken")

        if not next_page_token:
            break

    return comments


def get_video_title(video_id):
    request = youtube.videos().list(
        part="snippet",
        id=video_id
    )
    response = request.execute()

    if response["items"]:
        return response["items"][0]["snippet"]["title"]
    return "Unknown Title"