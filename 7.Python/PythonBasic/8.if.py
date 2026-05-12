print('----if구문----')
score = 70
if score >=80:
    #print('성적은 A+입니다.')
    grade='A'
elif score >=70:
    # print('성적은 B입니다.')
    grade='B'
elif score >=60:
    # print('성적은 C입니다.')
    grade='C'
else:
    # print('성적은 F입니다.')
    grade='F'

print(f"이 학생의 점수는 {score}이고, 학점은 {grade} 입니다")

month = 7 
if month == 1:
    print('1월입니다.')
elif month == 2:
    print('2월입니다.')
elif month == 3:
    print('3월입니다.')
elif month == 4:
    print('4월입니다.')
elif month == 5:
    print('5월입니다.')

month = 7 
if month in [12,1,2]:
    season='봄'    
    #print('1월입니다.')
elif month in [3,4,5]:
    season='봄'
    #print('2월입니다.')
elif month in [6,7,8]:
    season='여름'
    #print('3월입니다.')
elif month in [9,10,11]:
    season='가을'
    #print('4월입니다.')

print(f"{month}월은{season}입니다")

h=162
w=48
bmi=w/((h/100)**2)

if bmi<18.5:
    category ='저체중'
elif bmi<25:
    category='보통'
elif bmi<30:
    category='과체중'
else:
    category='비만'

print(f"키는 {h}cm, 몸무게는{w}kg bmi는 {category}입니다.")

id='admin'
pw='1234'

if id and pw:
    if id =='admin' and pw=='1234':
        print('관리자로 로그인 하였습니다')
    elif id =="user" and pw=='1234':
        print('사용자로 로그인 하였습니다')