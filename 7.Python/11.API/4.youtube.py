#pip install python-dotenv
import os
import requests

from dotenv import load_dotenv

load_dotenv() # .env 파일을 읽어서 해당 key/value를 메모리(환경변수)에 올려둠

API_KEY=os.getenv("YOUTUBE_API_KEY")

url = 'https://www.googleapis.com/youtube/v3/search'  # youtube/v3 빠져있었음

search_query = "파이썬 튜토리얼"

params = {
    'part': 'snippet',
    'q': search_query,
    'type': 'video',
    'maxResults': 50,       # maxResult → maxResults
    'key': API_KEY
}

response = requests.get(url, params=params)  # params= 키워드 인자
data = response.json()

for item in data['items']:
    title = item['snippet']['title']
    video_id = item['id']['videoId']                          # = 를 [] 로
    video_url = f"https://www.youtube.com/watch?v={video_id}"# video_id 꽂아야 함

    print(f"제목: {title}")
    print(f"URL: {video_url}")
    print('-' * 50)