from person import Person

class Driver(Person):
    def __init__(self,name,age,car):
        super().__init__(name,age)
        self.car=car
    def driver(self):
        print(f"{self.name}은 {self.car}운정을 시작합니다.")

    def driver_fast(self):
        print(f"{self.name}은 {self.car}운 시작합니다.")
        