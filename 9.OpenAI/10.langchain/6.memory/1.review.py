# 목적 - 뉴스를 분석한다.
# 뉴스 입력 -> 요약 
#          -> 감정분석 
#          -> 카테고리 분석
# RunnableParallel

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel

load_dotenv()

llm = ChatOpenAI(model='gpt-4o-mini') #모델 만들기

prompt_with_history=ChatPromptTamplate.from_message([
    ("system","당신은 친절한 챗봇입니다."),
    
])
history_example=[
    HumanMessgae(content="안녕하세요, 저는 홍길동입니다.")
    AIMessage(content)
]