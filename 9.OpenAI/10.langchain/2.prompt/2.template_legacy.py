from langchain_core.prompts import PromptTemplate

template = "당신은 작명가입니다. {product}를 만드는 회사의 이름을 지어주세요."
prompt = ChatPromptTemplate.from_message([
    ("system","당신은 작명가 입니다."),
    ("user","다음상품을 만드는 회사의 이름을 지어주세요. 상품명:{product}")
])


filled_prompt = prompt.format(product="스마트폰")
print("완성된 프롬프트:", filled_prompt)

print('-' * 50)

test_products = ["모바일 게임", "로봇 장난감", "가방"]
for product in test_products:
    final_prompt = prompt.format(product=product)
    print(f"[{final_prompt}]{final_prompt}")