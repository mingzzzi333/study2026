# 목적 - 여행 계획을 작성한다.
# 도시 입력 -> 음식 추천 
#          -> 관광지 추천
#          -> 호텔 추천
# 사용자 입력의 OO을 보고, 시간표/동선/교통수단 vs 음식/관광지/호텔
# RunnableParallel, RunnableBranch

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnableBranch, RunnableLambda

llm = ChatOpenAI(model='gpt-4o-mini')
parser = StrOutputParser()

# ── 병렬 체인 (음식 / 관광지 / 호텔) ──────────────────────
food_prompt = PromptTemplate.from_template(
    "{city}의 현지 음식 TOP5를 추천해주세요."
)
attraction_prompt = PromptTemplate.from_template(
    "{city}의 관광지 TOP5를 추천해주세요."
)
hotel_prompt = PromptTemplate.from_template(
    "{city}의 호텔 TOP5를 추천해주세요. (가격대 포함)"
)

info_chain = RunnableParallel({
    "음식"  : food_prompt       | llm | parser,
    "관광지": attraction_prompt | llm | parser,
    "호텔"  : hotel_prompt      | llm | parser,
})

# ── 분기 체인 (시간표 / 동선 / 교통수단) ──────────────────
schedule_prompt = PromptTemplate.from_template(
    "{city} 여행 3박 4일 시간표를 작성해주세요."
)
route_prompt = PromptTemplate.from_template(
    "{city} 여행 최적 동선을 짜주세요."
)
transport_prompt = PromptTemplate.from_template(
    "{city} 여행 시 추천 교통수단을 알려주세요."
)

# 분류기
classifier_prompt = PromptTemplate.from_template("""
다음 요청을 읽고 유형을 한 단어로만 답하세요.
- 시간표 관련이면: 시간표
- 동선 관련이면: 동선
- 교통 관련이면: 교통
- 그 외: 기타

요청: {query}
유형:
""")
classifier_chain = classifier_prompt | llm | parser

branch = RunnableBranch(
    (lambda x: "시간표" in x["category"], schedule_prompt   | llm | parser),
    (lambda x: "동선"   in x["category"], route_prompt      | llm | parser),
    (lambda x: "교통"   in x["category"], transport_prompt  | llm | parser),
    PromptTemplate.from_template("{city} 여행 정보를 알려주세요.") | llm | parser
)

def classify_and_branch(input):
    category = classifier_chain.invoke({"query": input["query"]})
    print(f"[분류 결과]: {category.strip()}")
    return {"city": input["city"], "category": category}

branch_chain = RunnableLambda(classify_and_branch) | branch

# ── 전체 실행 ──────────────────────────────────────────────
def run(city: str, query: str):
    print(f"\n 도시: {city}")
    print(f" 요청: {query}")
    print('=' * 50)

    # 1. 병렬 실행
    print("[ 기본 여행 정보 ]")
    info_result = info_chain.invoke({"city": city})
    for key, value in info_result.items():
        print(f"\n▶ {key}\n{value}")
        print('-' * 40)

    # 2. 분기 실행
    print("\n[ 맞춤 여행 플랜 ]")
    branch_result = branch_chain.invoke({"city": city, "query": query})
    print(branch_result)
    print('=' * 50)

# 테스트
run(city="도쿄", query="3박 4일 시간표 짜줘")
run(city="파리", query="관광지 간 이동 동선 알려줘")
run(city="뉴욕", query="공항에서 시내 교통수단 뭐가 좋아?")