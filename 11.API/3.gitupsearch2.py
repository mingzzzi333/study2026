import requests

url='https://api.github.com/search/repository'

keyword="chatbot"

max_page = 10
min_page = 100

all_repos=[]

for page in range(1,max_page+1):

    params={
        'q':chatbot,
        'per_page':100,
        'page':page
    }

resp=requests.get(url,params)

print('요청 성공', resp.status_code)
data=resp.json()

# print(data)
if 'items' in data:  # item → items
    repos = data['items']
    for repo in repos:
        name = repo['name']
        full_name = repo['full_name']
        html_url = repo['html_url']
        desc = repo['description'] or '설명 없음'  # None 처리
        app_repos.append({'name':name,'full_name':full_name,'html_url':html_url})
print(all+repos)

print(f'리포명: {name}, 풀네임: {full_name}, URL: {html_url}, 설명: {desc}')
        # ↑ for문 안으로 들여쓰기