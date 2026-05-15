import os
import csv
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")

url = 'https://www.googleapis.com/youtube/v3/search'

params = {
    'part': 'snippet',
    'q': "파이썬 튜토리얼",
    'type': 'video',
    'maxResults': 50,
    'key': API_KEY
}

response = requests.get(url, params=params)
data = response.json()

with open("search_result.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["title", "video_id", "video_url", "description"])  # 헤더

    for item in data['items']:
        title = item['snippet']['title']
        description = item['snippet']['description']
        video_id = item['id']['videoId']
        video_url = f"https://www.youtube.com/watch?v={video_id}"

        print(f"제목: {title}")
        print(f"URL: {video_url}")
        print('-' * 50)

        writer.writerow([title, video_id, video_url, description])  # 실제 값