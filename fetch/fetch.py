import os
from util.triple import Triple


class Fetcher:
    def __init__(self, output_file="../corpus"):
        self.file = os.path.abspath(output_file)
        self.triples = []

    def add(self, triple: Triple):
        self.triples.append(triple)
        print(self.triples)
