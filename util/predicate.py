from .graph import Node


class Predicate(Node):
    """a predicate like "lives in" or "was born on". Should be inherited of more specific classes. """

    def __init__(self):
        self.name = type(self).__name__


class LivesIn(Predicate):
    pass
