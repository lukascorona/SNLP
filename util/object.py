class Object:
    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return self.name


class Person(Object):
    pass


class Location(Object):
    pass
