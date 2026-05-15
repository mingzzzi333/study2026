import os
import csv
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

videos=[]

with open("video_stats.csv","r",encoding="utf-8")as file:
    reader = csv.DictReader(file)
    for row in reader:
        videos.append({
            "title":row["title"]
            "views":row["views"]
            "likes":row["likes"]
            "comments":row["comments"],
        )}

#프롬프트 작성
prompt=f"""
다음 유튜브 영상 데아터를 분석해서:
1. 어떤 영상이 가장 인기가 있는지 
2. 인기있는 이루는 무엇인지
3. 어떤 주제가 반응이 좋은지
4.내가 유튜브 채널을 운영하려고 하면 , 어떤 전략이 좋은지
를 분석해줘.
영상데이터:

영상 데이터:
{videos}
"""

response=client.models.genrtrare_content(
    model="gemini-2.5-flask",
    contents=prompt
)
print(response.text)
