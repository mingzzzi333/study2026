from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate

from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

prompt1=ChatPromptTemplate.from_template(
    "{product}을/를 만드는 회사의 이름을 하나 추천해주세요."
)

llm= ChatOpenAI(model="gpt-4o-mini")

chain1 =prompt1|llm|StrOutputParser()
result1=chain1.invoke({"product":"웹게임"})

print(f"타입:{tpye(result1)}")
print(f"결과:{result1}")

prompt2=ChatPromptTemplate.from_template(
    "{topic}에 관련된 키워드를 5개만 쉼표로 구분해서 나열해주세요."
)

chain2=prompt2|llm|CommaSeparatedListOutputParser()
result2=chain2.invoke({"topic":"인공지능"})

print(f"타입:{tpye(result2)}")
print(f"결과:{result2}")


prompt_name=ChatPromptTemplate.from_template(
    "{product}을/를 만드는 회사의 이름을 하나 추천해줘"
)

prompt_slogan=ChatPromptTemplate.from_template(
    "{company_name}회사의 개치프레이즈를 만들어줘."
)

prompt2=ChatPromptTemplate.from_template(
    "{topic}에 관련된 키워드를 5개만 쉼표로 구분해서 나열해주세요."
)

chain3=(prompt3
|llm
|StrOutputParser()
|(lambda name:{"company_name":name.strip()})
|prompt_slogan
|llm
|StrOutputParser()
)

result3=chain3.invoke({"product":"친환경에코백"})
print(f"결과:{result3}")