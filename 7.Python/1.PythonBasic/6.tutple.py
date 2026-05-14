#튜플 (읽기전용 리스트)
my_list=[1,2,3,4,5]
my_tuple=(1,2,3,4,5)

print(my_list)
print(my_tuple)
print(my_list[2])
print(my_tuple[2])

my_list[2]=99

print(my_list[2])
#print(my_tuple[2]) 튜플은 읽기만 가능
print(my_list[-1])
print(my_tuple[-1]) 
print(my_list[3:5])
print(my_tuple[3:5]) 
print(my_list[0:1])
print(my_tuple[0:1])  #(1)이 아니고 (1,)

#튜플을 받아왔는데, 값을 쓰고 싶으면? -> 리스트로 바꿔줘야됨.
my_newlist = list(my_tuple)
print(my_newlist)
my_newlist[2] = 88
print(my_newlist)
print(my_tuple)

my_newtuple = tuple(my_newlist)
print(my_newtuple)

print('-'*30)
a,b,c = (1,2,3)
print(a,b,c)

a_person=("John", 23, "Student")
print(a_person)
name, age, occ = a_person
print(name)
print(age)