#pip install langchain-openai
import os
from dotenv import load_dotenv

from langchain_openai import OpenAI #단발성 (Instruct Model)
from langchain_openai import ChatOpenAI #Q&A (Chat Model)

load_dotenv()
openai_api_key=os.environ.get('OPEN_API_KEY')

lim = OpenAI(model='gpt-4o-mini')
prompt="오늘 저녁은 무엇을 먹을까요?"
print(lim.invoke(prompt))

lim2= OpenAI(model='gpt-4o-mini')
prompt2="게임 화사를 차릴건데, 이름 추천해줘."
print(lim.invoke(prompt2))
