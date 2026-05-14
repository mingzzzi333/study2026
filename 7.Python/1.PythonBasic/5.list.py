my_list=[1,2,3,4,5]
print(my_list)
print(len(my_list))

print(my_list[0]) #모든 언어의 첫번째는 멤버는 0번임
print(my_list[4]) #4번이 다섯번째 멤버
#print(my_list[5]) #5번이 다섯번쨰 멤버

print(my_list[-1]) #리스트를 거꾸로..(뒤로, 마지막)
print(my_list[-2])

print(my_list[1:3]) #[1]을 포함하고 [5]를 포함하지 않음
print(my_list[3:5])
print(my_list[:2])
print(my_list[2:]) #2부터 끝까지

#원본 리스트에 멤버 추가하기
my_list.append(6)
print(my_list)

#특정 위치에 멤버 추가하기
my_list.insert(2,99)
print(my_list)

#해당 값의 요소 삭제하기
my_list.remove(99)
print(my_list)

#특정 인덱스 요소 삭제하기
my_list.pop(3) #[3]삭제
print(my_list)

my_list.pop()
print(my_list) #인덱스를 안넣으면? -> 기본적으로 맨 뒤의 값

my_list.clear()#리스트 통째로 비우기
print(my_list)

my_list=[5,2,1,3,4,7,6,8,9]
print(my_list)

my_list.sort()# 정렬은 하는데, 원본값을 변경하는 함수 sort()
print(my_list)

new_list=sorted(my_list) #원본을 유지하고 복제본을 만듦.
print(my_list)
print(new_list)

copyed_list=my_list.copy() #원본 리스트 복제본을 만듦.
print(copyed_list)
copyed_list.sort(reverse=True)
print(copyed_list)
print(my_list)

#리스트 컴프리팬션(어려운데, 쓰면 매우매우 편함)
print('-'*30)
numbers =[x for x in range(1,10)]
print(numbers)
numbers =[x for x in range(5)] #시작값은 0
print(numbers)
numbers =[x**2 for x in range(5)] # 이전 값들이 제곱 된 값
print(numbers)
numbers =[x for x in range(1,10) if x%2 ==0] #1~9 중 짝수만
print(numbers)
numbers =[x for x in range(1,10) if x%2 ==1] #1~9 중 짝수만
print(numbers)

list1=[1,2,3]
list2=[4,5,6]
list12 = list1+list2 #리스트의 합산
print(list12)
print(list1*3)
