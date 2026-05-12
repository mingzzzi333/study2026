# 외부모듈은 pip install requests로 설치한다
#그러면 ,pypi.org로 부터 다운받아서, 나의 가상환경에 설치됨.
import requests

#외부에 HTTP요청을 대신 해주는 라이브러리
resp = requests.get("http://www.naver.com")
# print(resp.status_code)  # 상태코드
# print("웹 페이지 내용 :", resp.text)         # HTML 내용
# print(resp.headers)

resp = requests.get('https://api.github.com')
data = resp.json()
curr_user_url = data['current_user_url']
print(curr_user_url)