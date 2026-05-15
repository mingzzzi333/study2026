import os
import csv
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")

search_url = 'https://www.googleapis.com/youtube/v3/search'
video_api_url = 'https://www.googleapis.com/youtube/v3/videos'

search_query = "파이썬 튜토리얼"

search_params = {
    'part': 'snippet',
    'q': search_query,
    'type': 'video',
    'maxResults': 50,
    'key': API_KEY
}

response = requests.get(search_url, params=search_params)
data = response.json()
search_results = data['items']

# video_id 한번에 요청
video_ids = [result['id']['videoId'] for result in search_results]
video_ids_str = ','.join(video_ids)

video_params = {
    'part': 'statistics',
    'id': video_ids_str,
    'key': API_KEY
}

video_response = requests.get(video_api_url, params=video_params)
video_data = video_response.json()

# stats 딕셔너리 만들기
stats = {item['id']: item['statistics'] for item in video_data['items']}

with open("search_result.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(['index', 'title', 'view_count', 'like_count', 'comment_count', 'video_url', 'description'])

    for index, result in enumerate(search_results, start=1):
        title = result['snippet']['title']
        description = result['snippet']['description']
        video_id = result['id']['videoId']
        video_url = f'https://www.youtube.com/watch?v={video_id}'

        # stats.get으로 각종 통계 가져오기
        stat = stats.get(video_id, {})
        view_count    = stat.get('viewCount', 'N/A')     # 조회수
        like_count    = stat.get('likeCount', 'N/A')     # 좋아요수
        comment_count = stat.get('commentCount', 'N/A')  # 댓글수

        print(f"[{index}] {title}")
        print(f"    조회수: {view_count} | 좋아요: {like_count} | 댓글: {comment_count}")
        print(f"    URL: {video_url}")
        print('-' * 50)

        writer.writerow([index, title, view_count, like_count, comment_count, video_url, description])

print("CSV 저장 완료!")