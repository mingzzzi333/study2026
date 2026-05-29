from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter

loader = TextLoader("./hbm.txt", encoding="utf-8")
documents= loader.load()

contents = documents[0].page_content
print(f"원본 글자수 : {len(contents)}")

#일반적으로 1000:200/1500:300/2000/:500정도 내외로 내용보고 판단함.
char_splitter=CharacterTextSplitter(
    separator="\n\n",
    chunk_size=500,
    chunk_overlap=100,
)


###########################3
recur_splitter=RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)
chunk_char=char_splitter.split_documents(documents)
print(f"[CharSplitter]{len(chunk_char)}")
print(f"첫 청크 글자수: {len(chunk_char[0].page_content)}")
