# 목적 : 긴 문장을 받아서 짧게 요약한다.
from dotenv import load_dotenv

from langchain_core.prompts import(
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate
)

from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableLambda

load_dotenv()

template="다음의 긴 내용을 3개의 문장으로 요약하시오 \n\n{article}"
chat_prompt=ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template("당신은 전문 문장 요약가입니다,")
    HumanMessagePromptTemplate.from_template(template)
])

llm = ChatOpenAI(model="gpt-4o-mini",temperature=0.5)
chain = chat_prompt | llm | RunnableLambda(lambda x :{"summary": x.content.strip()})

input_text={
    "article":""
}
result=chain.invoke()
print("요약결과 :",result)