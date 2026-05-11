#숫자를 할당하면? int타입의 변수가 됨.
x=5
y=3
#사칙연산
print(x+y)
print(x-y)
print(x*y)
print(x/y)

#나머지
print(x%y)

#제곱
print(x**y)

#진법변환
print(bin(x)) #2진수
print(oct(x)) #8진수
print(hex(x)) #16진수


y=4.5
print(y)
print(int(y))

z ="100"
print(z)
print(int(z))

#비트연산자
x=5
y=3
print(x&y) #5=101,3=011 -> 5&3 =>101&011 = 001
print(x|y) #5=101,3=011 -> 5&3 =>101|011 = 111
print(x^y) #XOR #5=101,3=011 -> 5^3 =>101^011 = 110
print(~x)  #NOT x 00000101 = 11111010 <-첫번째 자리는 부호
print(x << 1) # 왼쪽으로 한 자리 이동 =0000_1010
print(x >> 1) # 오른쪽으로 한 자리 이동 =0000_