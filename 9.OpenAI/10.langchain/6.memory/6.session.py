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

from langchain_core.runnables.history import RunnableWithMessageHistory

load_dotenv()

llm = ChatOpenAI(model='gpt-4o-mini') #모델 만들기

prompt=ChatPromptTemplate.from_messages([
    ("system","당신은 친절한 한국어 어시스트 입니다."),
    MessagesPlaceholder("history"),
    ("user","{input}")
])

chain = prompt | llm | StrOutputParser()

history = InMemoryChatMessageHistory()

#세션 관리를 위한 자료구조
sessions : dict[str,InMemoryChatMessageHistory]={}

def get_session_history(session_id:str)->InMemoryChatMessageHistory:
    if session_id not in sessions:
        sessions[session_id]=InMemoryChatMessageHistory()
        return sessions[session_id]
    
chain_with_memory=RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history"
)

def chat(message,session_id):
    print(f"\n[{session_id}]질문:{message}")
    answer=chain_with_memory(
        {"input":message},
        config={"configurable":{"session_id":session_id}},
    )
    print(f"[{session_id}]답변{answer}")

user_a="user-A" #세션ID 임의 생성
user_b="user-B" 

chat("제 이름은 홍길동입니다.",user_b)
chat("제 이름은 김철수입니다",user_a)
chat("저는 등산을 좋아합니다",user_b)
chat("저는 낚시를 좋아합니다",user_a)
chat("저는 누구인가요?",user_a)
chat("저는 누구인가요?",user_b)

