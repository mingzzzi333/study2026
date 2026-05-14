#딕셔너리
#키:밸류로 쌍을 이루고 있는 자료구조
my_dict={"name":"Alice","age":25,"location":"서울"}
print(my_dict)

#Json 과 비슷하게 생겨서, 웹서비스 만들 때 많이 사용함. 그렇다고 json은 아님
print(my_dict["name"])
print(my_dict["age"])

my_dict["car"]="BMW"
print(my_dict)

del my_dict["location"]
print(my_dict)

my_age=my_dict.pop("age") #pop, del 같은 기능임.. pop이 더 편할듯
print(my_dict)
print(my_age) #뺀 값을 볼 수 있음.

my_dict.clear() #모든 멤버 다 지우기
print(my_dict)

#dict의 기본은 key:value 쌍의 저장
my_squares ={x :x**2 for x in range(10)}
print(my_squares)

print(my_squares.keys())
print(my_squares.values())