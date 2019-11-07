from .graph import Node


class Object(Node):
    """an object like a Person, City... Should be inherited of more specific classes."""
    pass


class Person(Object):
    pass


class Location(Object):
    pass
