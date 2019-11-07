from .predicate import Predicate, LivesIn
from .object import Object, Person, Location


class Triple:
    """a triple represents a specific relation (e.g "lives in") between a subject (e.g a person) and a object (e.g a city)"""

    def __init__(self, subject: Object, predicate: Predicate, object: Object):
        self.subject = subject
        self.predicate = predicate
        self.object = object

    def __str__(self):
        return "{} -> {} -> {}".format(self.subject, self.predicate, self.object)

    def __iter__(self):
        """provides the functionality to iterate over subject, predicate and object in a for-in loop"""
        yield self.subject
        yield self.predicate
        yield self.object
