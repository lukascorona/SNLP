class Node:
    """a general node of a graph. Should be inherited of more specific classes. """

    def __init__(self, name: str):
        assert isinstance(name, str), "in {}: attr \"name\" must be of type str, but is {}".format(
            type(self).__name__, type(name).__name__)
        self.name = name

    def __str__(self):
        """when printing a node, the name is displayed"""
        return self.name
