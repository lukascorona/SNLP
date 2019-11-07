import os
from util.triple import Triple


class Fetcher:
    triples = []
    path = "../corpus"

    @staticmethod
    def file(output_file):
        Fetcher.path = os.path.abspath(output_file)

    @staticmethod
    def add(triple: Triple):
        Fetcher.triples.append(triple)

    @staticmethod
    def print():
        for triple in Fetcher.triples:
            print(triple)
