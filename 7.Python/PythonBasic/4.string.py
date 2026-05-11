s="hello world"
print(s)
print(s.lower())
print(s.upper())
print(s.capitalize()) #각 문장의 시작은 대문자
print(s.title()) # 각 단어의 시작은 대문자
s = "     Hello,      world     "
print(s.strip()) #앞뒤 불필요한 공백 제거
print(s.strip()+"!!") #앞뒤 불필요한 공백 제거
print(s.lstrip()+"!!") #왼쪽 불필요한 공백 제거
print(s.rstrip()+"!!") #오른쪽 불필요한 공백 제거

print(s.split())#문자열로 분할(자르기)
s = "apple banana cherry"
print(s.split())
s = "apple, banana, cherry"
print(s.split())
s = "apple,banana,cherry"
print(s.split())
print(s.split(","))

s_list=s.split(",")
print(s_list)
print(",".join(s_list)) #나의 리스트를 ,로 합쳐라
print(".".join(s_list))
print(" ".join(s_list))

s="Hello, World"
print(s)
print(s.startswith("Hello")) #True
print(s.startswith("Hello")) #False
print(s.endswith("World")) #True
print(s.find("World")) #찾기 
print(s.find("world"))

s="김길동"
print(s.startswith("김")) #True
print(s.startswith("홍")) #False