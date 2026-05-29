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
parser = StrOutputParser()

# 각 분석 프롬프트
summary_prompt = PromptTemplate.from_template(
    "다음 뉴스를 3줄로 요약하세요:\n{news}"
)
sentiment_prompt = PromptTemplate.from_template(
    "다음 뉴스의 감정을 분석하세요 (긍정/부정/중립 + 이유):\n{news}"
)
category_prompt = PromptTemplate.from_template(
    "다음 뉴스의 카테고리를 분류하세요 (정치/경제/사회/문화/스포츠/IT 중 하나):\n{news}"
)

# 각 체인 chain이란? prompt -> llm -> parser 
summary_chain   = summary_prompt   | llm | parser
sentiment_chain = sentiment_prompt | llm | parser
category_chain  = category_prompt  | llm | parser

# RunnableParallel - 동시에 실행 /parallel_chain(결과)
parallel_chain = RunnableParallel({
    "요약"      : summary_chain,
    "감정분석"  : sentiment_chain,
    "카테고리"  : category_chain,
})

# 테스트
news = """
삼성전자가 차세대 AI 반도체 개발에 성공했다고 발표했다.
이번 반도체는 기존 제품 대비 성능이 2배 향상되었으며,
전력 소비는 30% 감소한 것으로 알려졌다.
글로벌 시장에서 엔비디아와의 경쟁이 본격화될 전망이다.
"""

print(f"뉴스: {news}")
print('=' * 50)

result = parallel_chain.invoke({"news": news})

for key, value in result.items():
    print(f"[{key}]\n{value}")
    print('-' * 50)