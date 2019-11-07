from .predicate import Predicate, LivesIn
from .object import Object, Person, Location


class Triple:
    def __init__(self, subject: Object, predicate: Predicate, object: Object):
        pass

    @staticmethod
    def demo():
        return Triple(Person(), LivesIn(), Location())
