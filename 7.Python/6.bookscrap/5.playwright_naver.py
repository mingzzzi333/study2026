from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page=browser.new_page()
    page.goto("https://news.naver.com/section/105")

    #뉴스 목록 가져오기
    headlines = page.locator(".section_article.as_headline a.sa_text_title")
    print(headlines.count())

    for i in range(headlines.count()):
        news = headlines.nth(i)
        #제목가져오기
        title = news.inner_text().strip()
        #링크가져오기
        href = news.get_attribute('href')

        print(f"{i+1}. {title} \ {href}")
    input("엔터")


    # for i in range(books.count()):
    #     book = books.nth(i)

    #     title = book.locator("h3 a").get_attribute('title')
    #     print(title)

    #     price = book.locator(".price_color").inner_text()
    #     price=price.replace("£","")
    #     print(price)

    #     rating = book.locator("p.star-rating").get_attribute("class")
    #     rating=rating.split()[-1]
    #     print(rating)