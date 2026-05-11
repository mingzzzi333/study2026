users = [
    {'name': '김민준', 'age': 28, 'location': '서울', 'car': '현대'},
    {'name': '이서연', 'age': 34, 'location': '부산', 'car': '기아'},
    {'name': '박지호', 'age': 22, 'location': '인천', 'car': '벤츠'},
    {'name': '최수아', 'age': 45, 'location': '대구', 'car': 'BMW'},
    {'name': '정우진', 'age': 31, 'location': '광주', 'car': '토요타'},
    {'name': '강하은', 'age': 27, 'location': '대전', 'car': '테슬라'},
    {'name': '강도현', 'age': 39, 'location': '울산', 'car': '볼보'},
    {'name': '임채원', 'age': 25, 'location': '수원', 'car': '아우디'},
    {'name': '한소율', 'age': 52, 'location': '창원', 'car': '포르쉐'},
    {'name': '오재원', 'age': 33, 'location': '제주', 'car': '쉐보레'},
]

# def find_user_and_print(name):
#     for user in users:
#         if user["name"].startswith(name):
#             print(user)

# find_user_and_print("강")
# find_user_and_print("오")

# def find_user_and_return(name):
#     found = [] #찾은 사용자를 담을 바구니 (리스트 변수)

#     for user in users:
#         if user["name"].startswith(name):
#             found.append(user)
#     return found
# found_users = find_user_and_return("김")
# print("찾은 사용자",found_users)

def find_users2(name=None, age=None):
    """이름 또는 나이를 입력받아 매칭되는 사람을 반환한다."""
    found = []
    for user in users:
        if name is not None and age is not None:
            if user["name"] == name and user["age"] == age:
                found.append(user)
        elif name is not None:
            if user["name"] == name:
                found.append(user)
        elif age is not None:
            if user["age"] == age:
                found.append(user)
    return found

print(find_users2(age=25))