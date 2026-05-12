#1. books.toscrape.com에 접속해서 페이지를 받아온다.
#2. DOM을 bs4로 구성한다.
#3. 첫 페이지의 도서명, 평점, 가격을 가져온다.
#4. CSV파일로 저장한다.

#pip install bs4
import requests
import csv
from bs4 import BeautifulSoup

url = "https://books.toscrape.com/"
response = requests.get(url)
response.encoding = "utf-8"

soup = BeautifulSoup(response.text, "html.parser")
books = soup.find_all("article", class_="product_pod")

rating_map = {
    "One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5,
}

with open("books.csv", "w", newline="", encoding="utf-8") as file:
    csv_writer = csv.writer(file)
    csv_writer.writerow(["title", "price", "rating"])  # 헤더

    for book in books:
        title = book.h3.a["title"]
        rating = book.p["class"][1]
        rating_num = rating_map[rating]
        price = book.select_one(".price_color").text
        price = price.replace("£", "")

        csv_writer.writerow([title, price, rating_num])  # 실제 값
