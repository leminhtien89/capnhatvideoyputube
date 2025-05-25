from flask import Flask, render_template
import requests, os, json
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

YOUTUBE_API_KEY = "AIzaSyCbSwLrEFSKzyJAb1Bo-xMSkXD-35MY6Iw"
YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"

CATEGORIES = {
    "Review Phim": "review phim",
    "Hoạt Hình Việt Nam": "phim hoạt hình việt nam",
    "Giải Trí Hài Hước": "phim hài hước"
}

def fetch_videos(query, max_results=5):
    published_after = (datetime.utcnow() - timedelta(days=1)).isoformat("T") + "Z"
    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "order": "date",
        "maxResults": max_results,
        "publishedAfter": published_after,
        "key": YOUTUBE_API_KEY
    }
    response = requests.get(YOUTUBE_SEARCH_URL, params=params)
    if response.status_code != 200:
        print("Lỗi API:", response.text)
        return []
    data = response.json()
    items = data.get("items", [])
    return [{
        "title": item["snippet"]["title"],
        "thumbnail": item["snippet"]["thumbnails"]["high"]["url"],
        "channel": item["snippet"]["channelTitle"],
        "published": item["snippet"]["publishedAt"][:10],
        "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}"
    } for item in items]

@app.route("/")
def index():
    video_data = {}
    for label, keyword in CATEGORIES.items():
        video_data[label] = fetch_videos(keyword, max_results=5)
    return render_template("index.html", video_data=video_data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
