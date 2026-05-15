import requests

url = "https://api.github.com/users/mingzzzi333/repos"

resp = requests.get(url)
repos = resp.json()

data = []

for repo in repos:
    name = repo['name']
    html_url = repo['html_url']
    description = repo['description'] or '설명 없음'  # None이면 기본값
    data.append({'name': name, 'html_url': html_url, 'description': description})
5
# 헤더는 for문 밖 위에
print(f"{'리포이름':<30} {'리포url':<50} {'설명':<20}")
print('-' * 100)

for d in data:
    print(f"{d['name']:<30} {d['html_url']:<50} {d['description']:<20}")