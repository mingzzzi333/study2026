#Retrieval Augmented Generation
#증강검색생성
import numpy as np #숫자 (배열)을 잘 다루는 라이브러리
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings


load_dotenv()

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
#임베딩ㅇ,ㄹ 헤주는 모델중 가장 잘해주는 것중 하나이다

text= "고양이가 소파 위에서 잔다."
vec=embeddings.embed_query(text) #문장으로 하나의 점을 찍는다.

print(vec)

sentences=[
    "강아지가 소파 위에 있다.",
    "고양이가 침대 위에 있다",
    "파이썬은 인기있는 프로그램이다."

]

vectoes=embeddings.embed_documents(sentences)

def cosine_similarity(a, b):
    a,b=np.array(a),np.array(b)
    return float(np.dot(a,b)/(np.linalg.norm(a)*np.linalg.norm(b)))

print("=====우리 문장 간 유사도 (1.0 = 동일함을 의미함)======")
for i, s1 in enumerate(sentences):
    for j, s2 in enumerate(sentences):
        sim=cosine_similarity(vectoes[i],vectoes[j])
        print(f"{sim:.4f} {s1[:20]} <-> {s2[:20]}")