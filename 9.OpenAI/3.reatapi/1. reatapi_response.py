import os
import requests
from dotenv import load_dotenv

load_dotenv()

openai_api_key=os.getenv('OPENAI_API_KEY')

user_input='대한민국의 수도는 어디야?'

response=requests='',
    header={
        'Content-Type':'application/json',
        'Authorization':f'Bearer{openai_api_key}'
    },
    json={
    
    }




