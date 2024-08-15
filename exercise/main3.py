class Dog:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"Dog: {self.name}"

    def __getattribute__(self, name):
        print(f"they want to get {name}")
        return "haha"


winter = Dog("winter")
print(winter.name)
