import sys
from datetime import datetime
import os
import wikipedia
from wikipedia.exceptions import PageError
from tqdm import tqdm
import spacy
import re
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
            self.entries |= set(entry)
        elif type(entry) is set:
            self.entries |= entry
        else:
            self.entries.append(entry)
        return self

    def fetch(self, ram=False):
        
        """fetches wikipedia summaries for all passed triples and their entries (subj, pred, obj). Takes the first entry of a search on wikipedia"""
        timestamp = datetime.now().isoformat(
            timespec="seconds").replace(":", "-").replace(".", "-")
        nlp = spacy.load("en_core_web_md")
        print("fetch wikipedia pages...")
        if ram:
            corpus_in_ram = ""
            for item in tqdm(self.entries):
                page = wikipedia.page(item)
                doc = re.sub(r"[()\n=]", "", page.content)
                corpus_in_ram += doc + "\n"
            return corpus_in_ram
        with open(f"{self.path}corpus-{timestamp}", "a", encoding="utf_8") as corpus:
            with open(f"{self.path}DEP_corpus-{timestamp}", "a", encoding="utf_8") as corpus_dep:
                with open(f"{self.path}POS_corpus-{timestamp}", "a", encoding="utf_8") as corpus_pos:
                    for item in tqdm(self.entries):
                        #pages = wikipedia.search(item)
                        # if pages:
                        try:
                            page = wikipedia.page(item)
                            doc = re.sub(r"[()\n=]", "", page.content)
                            tokens = nlp(doc)
                            regex_friendly_string_dep = ""
                            regex_friendly_string_pos = ""
                            for i in tokens:
                                regex_friendly_string_dep += f"{i.lemma_}<<{i.dep_}>>"
                                regex_friendly_string_pos += f"{i.lemma_}<<{i.pos_}>>"
                            regex_friendly_string_dep = regex_friendly_string_dep.replace(
                                "-PRON-", "")
                            regex_friendly_string_pos = regex_friendly_string_pos.replace(
                                "-PRON-", "")
                            corpus.write(doc + "\n")
                            corpus_dep.write(regex_friendly_string_dep + "\n")
                            corpus_pos.write(regex_friendly_string_pos + "\n")
                            # corpus.write(wikipedia.summary(pages[0]) + "\n")
                        except KeyboardInterrupt:
                            raise
                        except PageError:
                            print(f"\nno page found for {item}. skip.")
                        except:
                            # print("error for {}, found pages: {}".format(item, pages))
                            print(
                                f"\nerror for {item}, error:{sys.exc_info()[0]}")
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
