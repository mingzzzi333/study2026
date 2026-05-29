from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

loader= PyPDFLoader("./js.pdf")
pages=loader.load()

print(f"pdf페이지수: {len(pages)}\n")

splitter=RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)
chunk_char=char_splitter.split_documents(documents)
print(f"[CharSplitter]{len(chunk_char)}")
print(f"첫 청크 글자수: {len(chunk_char[0].page_content)}")


first=chunks[0]

for p in pages:
    if p.page_content.strip():
        print(f"발견한 애용이 있는 첫페이지의 metadata:\n{p.metadata}")
        print(f"페이지내용 (앞 100글자):\n{p.page_content[:400]}...")
        break 