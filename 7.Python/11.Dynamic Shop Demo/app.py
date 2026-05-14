from flask import Flask,jsonify,render_template
import requests,csv
from bs4 import BeautifulSoup

app=Flask(__name__)

soup=BeautifulSoup(response.text, "html.parser")

url = "https://makemyproject.net/shop/"
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



if __name__ == "__main__":
    app.run(debug=True, port=5000)
