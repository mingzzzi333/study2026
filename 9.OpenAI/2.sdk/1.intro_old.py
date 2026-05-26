# pip install openai==0.28
from dotenv import load_dotenv
import openai
import os

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')

response = openai.ChatCompletion.create(
    model='gpt-3.5-turbo',
    messages=[
        {'role': 'system', 'content': '당신은 나의 질문을 답변하는 챗봇입니다.'},
        {'role': 'user', 'content': '안녕하세요 반갑습니다.'},
    ]
)

print(response['choices'][0]['message']['content'])