from employee import Employee
from person import Person
from driver import Driver

employee1 = Employee("James",25,"Samsung")
employee2 = Employee("Tim",24,"LG")
employee3 = Person("Ace",23)
employee4 = Driver("홍",23,"bmw")

employee1.greet()
employee2.greet()
employee3.greet()
employee4.greet()

employee3.set_age(40)
employee3.greet()
print(employee3.get_name())
employee4.driver()
employee4.driver_fast()