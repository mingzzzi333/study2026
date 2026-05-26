from dotenv import load_dotenv
import os
import requests

load_dotenv()

openai_api_key = os.getenv('OPENAI_API_KEY')

messages = [
    {'role': 'system', 'content': '너는 나를 도와주는 경력 20년차 소프트웨어 개발자야.'}
]

def chat(user_input):
    messages.append({'role': 'user', 'content': user_input})
    
    response = requests.post(
        'https://api.openai.com/v1/chat/completions',
        json={
            'model': 'gpt-3.5-turbo',
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
        
        reply = chat(user_input)
        print(f"GPT: {reply}")

main()