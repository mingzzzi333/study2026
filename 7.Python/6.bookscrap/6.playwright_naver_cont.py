from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page=browser.new_page()
    page.goto("https://news.naver.com/section/105")

    links=[]

    #뉴스 목록 가져오기
    headlines = page.locator(".section_article.as_headline a.sa_text_title")
    print(headlines.count())

    for i in range(headlines.count()):
        news = headlines.nth(i)
        #제목가져오기
        title = news.inner_text().strip()
        #링크가져오기
        href = news.get_attribute('href')
    for news in links:
        print("-"*60)
        print("제목 :", news["title"])
        print("링크 :", news["href"])

        #게시물로 이동 
        page.goto(news['href'])

        #본문추출
        content = page.locator('본문').inner_text().strip()
        print("본문 :", content)
        # print(content[:100])