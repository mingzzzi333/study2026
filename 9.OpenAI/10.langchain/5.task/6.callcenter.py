# 목적 - 질문 유형에 따라 적합한 항목으로 답변한다
# 질문 유형 -> 배송조회 상담원
#          -> 결제관련 상담원
#          -> 기술지원 상담원
# RunnableBranch

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableBranch, RunnableLambda

llm = ChatOpenAI(model='gpt-4o-mini')
parser = StrOutputParser()

# 각 상담원 프롬프트
delivery_prompt = PromptTemplate.from_template(
    "당신은 배송 전문 상담원입니다. 다음 질문에 답변하세요:\n{question}"
)
payment_prompt = PromptTemplate.from_template(
    "당신은 결제 전문 상담원입니다. 다음 질문에 답변하세요:\n{question}"
)
tech_prompt = PromptTemplate.from_template(
    "당신은 기술 지원 전문 상담원입니다. 다음 질문에 답변하세요:\n{question}"
)
default_prompt = PromptTemplate.from_template(
    "당신은 고객 상담원입니다. 다음 질문에 답변하세요:\n{question}"
)

# 질문 유형 분류기
classifier_prompt = PromptTemplate.from_template("""
다음 질문을 읽고 유형을 한 단어로만 답하세요.
- 배송 관련이면: 배송
- 결제 관련이면: 결제
- 기술 관련이면: 기술
- 그 외: 기타

질문: {question}
유형:
""")

classifier_chain = classifier_prompt | llm | parser

# RunnableBranch
branch = RunnableBranch(
    (lambda x: "배송" in x["category"], delivery_prompt | llm | parser),
    (lambda x: "결제" in x["category"], payment_prompt | llm | parser),
    (lambda x: "기술" in x["category"], tech_prompt   | llm | parser),
    default_prompt | llm | parser  # 기본값
)

# 전체 체인
def route(input):
    category = classifier_chain.invoke({"question": input["question"]})
    print(f"[분류 결과]: {category.strip()}")
    return {"question": input["question"], "category": category}

full_chain = RunnableLambda(route) | branch

# 테스트
questions = [
    "제 주문이 언제 도착하나요?",
    "결제가 두 번 됐어요.",
    "앱이 자꾸 튕겨요.",
    "영업시간이 어떻게 되나요?"
]

for q in questions:
    print(f"\n질문: {q}")
    result = full_chain.invoke({"question": q})
    print(f"답변: {result}")
    print('-' * 50)