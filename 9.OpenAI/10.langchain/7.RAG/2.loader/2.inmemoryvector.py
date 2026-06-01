#Retrieval Augmented Generation
#증강검색생성
import numpy as np #숫자 (배열)을 잘 다루는 라이브러리
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.documents import Document


load_dotenv()

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
#임베딩ㅇ,ㄹ 헤주는 모델중 가장 잘해주는 것중 하나이다

docs= [
    Document(page_content="NVMe는 SSD의 인터페이스 규격으로 PCIe를 사용한다"),
    Document(page_content="RAM은 CPU가 직접 접근하는 휘발성 메모리이다"),
    Document(page_content="GPU는 병렬 연산에 특화된 프로세서로 AI 학습에 많이 쓰인다"),
    Document(page_content="SSD는 HDD보다 읽기/쓰기 속도가 훨씬 빠르다"),
    Document(page_content="CPU의 코어 수가 많을수록 멀티태스킹 성능이 높아진다"),
]

embeddings= OpenAIEmbeddings(model="text-embedding-3-small")
store=InMemoryVectorStore.from_documents(docs, embedding=embeddings)
 
query="NVM와 RAM의 차이는 무엇인가요?"
results=store.similarity_search(query,k=3)

print(f"질문:{query}\n")
print(f"가장 가까운 {len{results}}개의 문서:")
for i,doc in enumerate(results,1):
    print(f"{i},{doc.page_content}")