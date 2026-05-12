import requests

url = "https://www.example.com"

response = requests.get(url)

print(response)

print("="*30)

#원하는 태그 찾아오기
html = response.text  # 문자열로 변환

start = html.find("<h1>") + len("<h1>")  # <h1> 다음부터
end = html.find("</h1>")                 # </h1> 직전까지

text = html[start:end]
print(text)