# 목적 - 뉴스를 분석한다.
# 뉴스 입력 -> 요약 
#          -> 감정분석 
#          -> 카테고리 분석
# RunnableParallel

from dotenv import load_dotenv
#모델
from langchain_openai import ChatOpenAI
#프롬포트
from langchain_core.prompts import ChatPromptTemplate,ChatMessagePromptTemplate,MessagesPlaceholder
#파서
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel
#기타
from langchain_core.chat_history import InMemoryChatMessageHistory

from langchain_community.chat_message_histories import FileChatMessageHistory

load_dotenv()

llm = ChatOpenAI(model='gpt-4o-mini') #모델 만들기
prompt=ChatPromptTemplate.from_messages([
    ("system","저는 친절한 도우미 입니다."),
    MessagesPlaceholder("history"),
    ("user","{input}")
])

chain = prompt | llm | StrOutputParser()

history = InMemoryChatMessageHistory()

def chat(message):
    print(f"질문:{message}")
    answer=chain.invoke({
        "input":message,
        "history":history.messages, #우리의 저장소에 있는 메시지 그대로 다
    })
# chat("안녕하세요")
# chat("제 이름은 황철중입니다")
# chat("저는 겨울에 바갓사에 가서 서핑하는 것을 좋아해요")
chat("제 이름과 취미가 뭐라고 했죠?")


