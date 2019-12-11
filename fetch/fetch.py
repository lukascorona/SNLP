import sys
from datetime import datetime
import os
import wikipedia
from wikipedia.exceptions import PageError
from tqdm import tqdm
wikipedia.set_lang("en")


class Fetcher:
    """fetches wikipedia summaries for all passed triples and their entries (subj, pred, obj)"""

    def __init__(self, path="./"):
        self.entries = set()
        self.path = path  # relative from main.py

    def file(self, output_file):
        """sets the file name for the corpus (relative to main.py)"""
        self.path = os.path.abspath(output_file)
        return self

    def addTriple(self, triple: list):
        """adds a triple, which should be processed on fetch() call"""
        self.entries += triple
        return self

    def addTriples(self, triples: list):
        """adds triples, which should be processed on fetch() call"""
        for triple in triples:
            self.entries += triple
        return self

    def add(self, entry):
        """adds a single entry or list of entries, which should be processed on fetch() call"""
        if type(entry) in [list, tuple]:
            self.entries += entry
        elif type(entry) is set:
            self.entries |= entry
        else:
            self.entries.append(entry)
        return self

    def fetch(self):
        """fetches wikipedia summaries for all passed triples and their entries (subj, pred, obj). Takes the first entry of a search on wikipedia"""
        timestamp = datetime.now().isoformat(
            timespec="seconds").replace(":", "-").replace(".", "-")
        with open(f"{self.path}corpus-{timestamp}", "a", encoding="utf_8") as corpus:
            for item in tqdm(self.entries):
                #pages = wikipedia.search(item)
                # if pages:
                try:
                    page = wikipedia.page(item)
                    corpus.write(page.content.replace(
                        "\n", "").replace("==", ""))
                    # corpus.write(wikipedia.summary(pages[0]) + "\n")
                except KeyboardInterrupt:
                    raise
                except PageError:
                    print(f"\nno page found for {item}. skip.")
                except:
                    # print("error for {}, found pages: {}".format(item, pages))
                    print(f"\nerror for {item}, error:{sys.exc_info()[0]}")
                    continue
            self.entries = []
        return self

    def print(self):
        """prints current triple queue"""
        if not self.entries:
            print("empty")
        for item in self.entries:
            print(item)
        return self
