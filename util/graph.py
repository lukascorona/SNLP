class Node:
    def __init__(self, name: str):
        assert isinstance(name, str), "in {}: attr \"name\" must be of type str, but is {}".format(
            type(self).__name__, type(name).__name__)
        self.name = name

    def __str__(self):
        return self.name
