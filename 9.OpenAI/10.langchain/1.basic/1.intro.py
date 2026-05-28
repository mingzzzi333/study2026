#pip install langchain-openai
import os
from dotenv import load_dotenv

from langchain_openai import OpenAI

load_dotenv()
openai_api_key=os.environ.get('OPEN_API_KEY')

llm = OpenAI()
print(llm)

prompt="오늘 저녁은 무엇을 먹을까요?"
result=llm.invoke(prompt)