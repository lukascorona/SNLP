import os
import wikipedia
wikipedia.set_lang("en")


class Fetcher:
    """fetches wikipedia summaries for all passed triples and their entries (subj, pred, obj)"""
    triples = []
    path = "./corpus"  # relative from main.py

    @staticmethod
    def file(output_file):
        """sets the file name for the corpus (relative to main.py)"""
        Fetcher.path = os.path.abspath(output_file)

    @staticmethod
    def add(triple: list):
        """adds a triple, which should be processed on Fetcher.fetch() call"""
        Fetcher.triples.append(triple)

    @staticmethod
    def fetch():
        """fetches wikipedia summaries for all passed triples and their entries (subj, pred, obj). Takes the first entry of a search on wikipedia"""
        with open(Fetcher.path, "a", encoding="utf_8") as corpus:
            while Fetcher.triples:
                triple = Fetcher.triples.pop()
                for item in [triple[0], triple[2]]:
                    pages = wikipedia.search(item)
                    if pages:
                        corpus.write(wikipedia.summary(pages[0]) + "\n")

    @staticmethod
    def print():
        """prints current triple queue"""
        if not Fetcher.triples:
            print("empty")
        for triple in Fetcher.triples:
            print(triple)
