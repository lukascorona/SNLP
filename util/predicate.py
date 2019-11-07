from .graph import Node


class Predicate(Node):
    def __init__(self):
        self.name = type(self).__name__


class LivesIn(Predicate):
    pass
