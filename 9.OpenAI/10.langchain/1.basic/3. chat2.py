from dotenv import load_dotenv

load_dotenv()

from langchain_openai import ChatOpenAI  # Q&A 용으로 사용 (Chat Model = gpt-3.5-turbo)
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage


llm = ChatOpenAI(model='gpt-4o-mini')

prompt = [
    SystemMessage(content="당신은 경력 30년차 호텔 쉐프."),
    HumanMessage(content="이번주에 요리 하나 할건데 추천해줘.")
]

result=llm.invoke(prompt)
print(result.prompt)