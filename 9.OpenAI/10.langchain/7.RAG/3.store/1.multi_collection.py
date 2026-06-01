import os
from dotenv import load_dotenv

from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

load_dotenv()

DB_DIR = "./chroma_db"

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)

def build_document(file_path, collection):  # bulid → build
    store = Chroma(collection_name=collection, embedding_function=embeddings,  # == → =
                   persist_directory=DB_DIR)
    if store._collection.count() > 0:
        return store

    docs = TextLoader(file_path, encoding="utf-8").load()
    chunks = splitter.split_documents(docs)
    for c in chunks:
        c.metadata["source"] = os.path.basename(file_path)

    return Chroma.from_documents(chunks, embeddings, collection_name=collection,  # for 밖으로
                                 persist_directory=DB_DIR)


collections = {  # 함수 밖으로
    "nvme": build_document("./nvme.txt", "nvme"),  # nvmw → nvme
    "hbm": build_document("./hbm.txt", "hbm"),    # hvm → hbm
}

for name, store in collections.items():
    print(f"컬렉션:{name}, 청크개수:{store._collection.count()}")  # 개스 → 개수


# 컬렉션 내 검색
def search_in(name, query, k=2):
    results = []
    for doc in collections[name].similarity_search(query, k=k):
        doc.metadata["collection"] = name
        results.append(doc)
    return results


query = "PCIe 인터페이스 속도는?"

print("\n=== nvme 컬렉션에서 이걸 물어보면?")
for d in search_in("nvme", query):  # 'name' → "nvme"
    print(f"-> {d.page_content[:100]}")  # [100] → [:100]

print("\n=== nvme 컬렉션에서 이걸 물어보면?")
for d in search_in("nvme", query):  # 'name' → "nvme"
    print(f"-> {d.page_content[:100]}")  # [100] → [:100]

