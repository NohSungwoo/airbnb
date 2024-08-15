class Human:
    def __init__(self, name):
        self.name = name
        print("상속 완료")

    def say_hello(self):
        print(f"Hello, im {self.name}")


class Player(Human):
    def __init__(self, name, xp):
        super().__init__(name)
        self.xp = xp


class Fan(Human):
    def __init__(self, name, fav_team):
        super().__init__(name)
        self.fav_team = fav_team


nico = Fan("nico", "blue")
nico.say_hello()
