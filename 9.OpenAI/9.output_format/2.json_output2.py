import os
import json

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

response = client.chat.completions.create(
    model='gpt-4o-mini',
    messages=[
        {'role': 'system', 'content': 'json으로만 대답하세요.'},
        {'role': 'user', 'content': '서울시 인구와 면적을 알려주세요'}
    ],
    response_format={'type':'json_object'}
)

answer = response.choices[0].message.content
print(answer)