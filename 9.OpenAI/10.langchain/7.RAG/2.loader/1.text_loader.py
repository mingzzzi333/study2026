from langchain_community.document_loaders import TextLoader

loader = TextLoader("./nvme.txt",encoding="utf-8")
documents=loader.load()
print(f"불러온 문서의 갯수:{len(documents)}")