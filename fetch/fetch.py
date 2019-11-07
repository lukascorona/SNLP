import os
from util.triple import Triple
import wikipedia
wikipedia.set_lang("en")


class Fetcher:
    triples = []
    path = "./corpus"  # relative from main.py

    @staticmethod
    def file(output_file):
        Fetcher.path = os.path.abspath(output_file)

    @staticmethod
    def add(triple: Triple):
        Fetcher.triples.append(triple)

    @staticmethod
    def fetch():
        with open(Fetcher.path, "a", encoding="utf_8") as corpus:
            while Fetcher.triples:
                for item in Fetcher.triples.pop():
                    pages = wikipedia.search(item.name)
                    if pages:
                        corpus.write(wikipedia.summary(pages[0]) + "\n")

    @staticmethod
    def print():
        if not Fetcher.triples:
            print("empty")
        for triple in Fetcher.triples:
            print(triple)
