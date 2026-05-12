try:
    result = 10/0
except ZeroDivisionError:
    print("0으로 나눌 수 없습니다.")
except:
    print("알 수 없는 오류입니다.")

print("다음 코드로 진행합니다.")

try:
    number = int("abc")
except ValueError:
    print("해당글자는숫자로변환할수없습니다.")
except:
    print("몰랑 에러는 일단 통과")

alist=[1,2,3]
try:
    alist[3]
except IndexError:
    print("입력 범위를 초과하였습니다.")

try:
    with open("없는파일명.txt","r") as file:
        data=file.read()
except FileNotFoundError:
    print("해당 파일이 존재하지 않습니다.")