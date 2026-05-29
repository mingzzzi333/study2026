from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

from pydantic import BaseModel, Field

load_dotenv()

class MovieReview(BaseModel):
    """영화 리뷰 분석 결과"""
    title: str= Field(description="영화제목")
    sentiment: str=Field(description="감성 분류: 긍정, 부정, 중립")
    score: int=Field(description="1~10점수")
    summary=str=Field(description="리뷰요약 (1~2 문장)")
    keyword=str=Field(description="핵심 키워드 3개")

llm=ChatOpenAI(model="gpt-4o-mini")
parder=PydantiOutputParser(pydantic_object=ModelReview)

promtpt = ChatPromptTemplate.prompt_template(
    """다음 영화리뷰를 분석해주세요."""
    리뷰{review}

    {format_instructions}
    
)

for review in reviews:
    result=chain.invoke({
        "review"=review,
        "format_instu"
    })