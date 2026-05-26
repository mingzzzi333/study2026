from dotenv import load_dotenv
import os
import requests

load_dotenv()

user_input = input("안녕하세요. 뭐 도와줄까?")
openai_api_key = os.getenv('OPENAI_API_KEY')

response = requests.post(
    'https://api.openai.com/v1/chat/completions',
    json={
        'model': 'gpt-3.5-turbo',
        'messages': [

            {'role': 'system', 'content': '너는 나를 도와주는 경력 20년차 소프트웨어 개발자야.'},
            {'role': 'user', 'content': user_input}
        ],
        'temperature':1.5
    },
    headers={
        'Authorization': f'Bearer {openai_api_key}',
        'Content-Type': 'application/json'
    }
)
data = response.json()
print(data)
# data = response.json()
print(response.json()['choices'][0]['message']['content'])
