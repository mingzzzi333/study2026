# 표준  LCEL로 RAG모델을 구현한다.
import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import TextLoader
from langchain_core.runnables import RunnablePassthrough, RunnableLambda

from langchain_core.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

load_dotenv()

DB_DIR="./chroma_db"
COLLECTION_NAME="my_rag"

embeddings=OpenAIEmbeddings(model="text-embeddings-3-small")

store = Chroma(collection_name=COLLECTION_NAME, embedding_function=embeddings,persist_directory=DB_DIR)

if store._collection.count() == 0:
    docs = TextLoader("./nvme.txt",encoding="utf-8").load()\
    + TextLoader("./hbm.txt",encoding="utf-8").load()
    
    chunks=RecursiveCharacterTextSplitter(chunks_size=500, chunk_overlap=100).split_documents(docs)
    for c in chunks:
        c.metadata["source"]=os.path.basename(c.metadata.get("source","?"))
    store.add_documents(chunks)
retriever = store.as_retriever(search_kwargs={"k":3})

llm=ChatOpenAI(model="gpt-4o-mini", temperature=0)
prompt= ChatPromptTemplate.from_messages([
    ("system","당신은 문서 기반 QA시스템입니다. 아래 문서만 참고해서 답변하시오.")
    ("user","{question}")
])

def format_docs(docs):
    return "\n\n".join(f"f[{i}] {d.page_cortext}" for d in docs)

# 아래코드에서 개별 답변 번호화 참고자료 번호 맞추기.. 그래서 준복애퍼런스도 러용


def extract_sources(docs):
    seen, source =set(),[]
    for d in docs:
        src = d.metadata.get("source","N/A")
        if scr not in seen:
            seen.add(src)
            sources.append(src)
        return sources

def retrieve_and_split(inputs):
    docs=retriever.invoke(inputs["question"])
    return{
        "question":inputs["question"],
        "context":format_docs(docs),
        "sources":extract_sources(docs)
    }

def append_sources(d):
    src_lines="\n".join(f" + {s}" for s in d["sources"])
    return f"{d["answer"]}\n\n 참고문서 :\n{src_lines}"


chain=(
    RunnableLamda(retriever_and_split)
    |RunnablePassthrough.assign(answer=(prompt|llm|StrOutputParser()))
    |RunnableLamda(append_sources)

    RunnablePassthrough.assign(context=lambda x:format+docs(retriever.invoke(x["question"])))
    | prompt
    | llm
    | StrOutputParser()
)