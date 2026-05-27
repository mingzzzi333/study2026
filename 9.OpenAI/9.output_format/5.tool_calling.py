import os
import json

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def get_weather(city):
    weather={'서울':'맑음, 22도','부산':'흐림, 19도'}
    return weather.get()

tools=[
    {
        'type':'function',
        'function':{
            'name':'get_weather',
            'descriptions':{
                'type':'object',
                'properties':{
                    'city':['type':'string','sedcription':'도시이름']
                },
                'required':['city']
            }
        }
    }

]

response = client.chat.completions.create(
    model='gpt-4o-mini',
    messages=[
        {'role': 'system', 'content': 'json으로만 대답하세요.'},
        {'role': 'user', 'content': '서울시 인구와 면적을 알려주세요'}
    ]
)

message = response.choices[0].message.content
# print(answer)
if message.tool_calls:
    call=message.tool_calls[0]
    print('모델이 호출하려는 함수는 :',call.funtion.name)
    print('모델이 추가하려는 인자는 :',json.loads(call.funtion.arguments))
else:
    print('함수 없이 그냥 답변중 :' ,message.contnet)