from langchain_community.document_loaders import PyPDFLoader

loader= PyPDFLoader("./js.pdf")
pages=loader.load()

print(f"pdf페이지수: {len(pages)}\n")

for p in pages:
    if p.page_content.strip():
        print(f"발견한 애용이 있는 첫페이지의 metadata:\n{p.metadata}")
        print(f"페이지내용 (앞 100글자):\n{p.page_content[:400]}...")
        break 