import requests
import csv
from bs4 import BeautifulSoup

url = "https://www.naver.com/"
response = requests.get(url)
response.encoding = "utf-8"

soup = BeautifulSoup(response.text, "html.parser")
books = soup.find_all("article", class_="product_pod")
