students = {
    '김민준': 85,
    '이서연': 92,
    '박지호': 78,
    '최수아': 88,
    '정우진': 95,
    '강하은': 71,
    '윤도현': 83,
    '임채원': 67,
    '한소율': 90,
    '오재원': 76
}

print(students)

def get_a_student(students):
    a_student=[]
    for name,score in students.items(): #dic의 요소를 하나씩 가져옴(items())
        if score>90:
            a_student.append(name)
    return a_student

print(f"get_a_student((students))")