from dotenv import load_dotenv
from base64 import b64encode
import os
import requests

load_dotenv()

openai_api_key = os.getenv('OPENAI_API_KEY')

messages = [
    {'role': 'system', 'content': '너는 나를 도와주는 경력 20년차 소프트웨어 개발자야.'}
]

def encode_image_to_base64(image_path):
    with open(image_path, "rb") as file:
        base64_bytes = b64encode(file.read()).decode('utf-8')
        return f"data:image/jpeg;base64,{base64_bytes}"

def chat(image_path, user_input):
    image_base64 = encode_image_to_base64(image_path)
    
    messages.append({
        'role': 'user',
        'content': [
            {'type': 'text', 'text': user_input},
            {'type': 'image_url', 'image_url': {'url': image_base64}}
        ]
    })
    
    response = requests.post(
        'https://api.openai.com/v1/chat/completions',
        json={
            'model': 'gpt-4o',
            'messages': messages,
            'temperature': 1.5
        },
        headers={
            'Authorization': f'Bearer {openai_api_key}',
            'Content-Type': 'application/json'
        }
    )
    
    reply = response.json()['choices'][0]['message']['content']
    messages.append({'role': 'assistant', 'content': reply})
    
    return reply

def main():
    print("대화를 시작합니다. 종료하려면 '종료'를 입력하세요.")
    
    while True:
        user_input = input("나: ")
        
        if user_input == '종료':
            print("대화를 종료합니다.")
            break
        
        image_path = input("이미지 경로 (없으면 엔터): ")
        reply = chat(image_path, user_input)
        print(f"GPT: {reply}")

main()