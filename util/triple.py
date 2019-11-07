from .predicate import Predicate, LivesIn
from .object import Object, Person, Location


class Triple:
    def __init__(self, subject: Object, predicate: Predicate, object: Object):
        self.subject = subject
        self.predicate = predicate
        self.object = object

    def __str__(self):
        return "{} -> {} -> {}".format(self.subject, self.predicate, self.object)

    @staticmethod
    def demo():
        return Triple(Person(), LivesIn(), Location())
