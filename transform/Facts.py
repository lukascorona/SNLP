from input.input import Input
import pprint
import re
from math import inf as INFINITY
from tqdm import tqdm
import sys
import time


class Facts(Input):

    def __init__(self):
        Input.__init__(self)
        self.test = []
        self.predition = []

    def check(self, regex_exp, corpus_path="./corpus"):
        """ checks in the corpus, if a facts is true (full corpus in RAM) """
        # get all important sentences out of the corpus
        with open(corpus_path, "r", encoding="utf-8") as corpus:
            found_entries = []
            for i in range(len(self.documents)):
                found_entries.append(set())
                self.predition.append(0.0)
            mean_time = 0.0
            corpus_text = corpus.read().lower().replace("'s", "")
            for doc_i, doc in enumerate(self.documents):
                start = time.time()
                used_reg = ""
                for regex in regex_exp:
                    found, entries = self.reg(regex, doc)
                    if found:
                        used_reg = regex
                        for entry in entries:
                            found_entries[doc_i].add(
                                entry.lower().replace("'s", ""))
                        if len(found_entries[doc_i]) > 1:
                            found_in_corpus, entries = self.reg(
                                "[^\.]*".join(found_entries[doc_i]), corpus_text)
                            if found_in_corpus:
                                print(
                                    f"found: {entries}, entries: {found_entries[doc_i]}, regex: {used_reg}, true?:{self.truth[doc_i]}")
                                self.predition[doc_i] = 1.0
                            right = 0
                            mean_time = (mean_time * doc_i +
                                         time.time() - start) / (doc_i + 1)
                            for i in range(len(self.documents)):
                                if self.predition[i] == self.truth[i]:
                                    right += 1
                            sys.stdout.write(
                                f"\raccuracy: {right/len(self.documents)}, {doc_i + 1}/{len(self.documents)}, time: {mean_time*1000:.2f}ms/iter")
                            sys.stdout.flush()
                        break
        return self

    def reg(self, pattern, text):
        entries = []
        matches = re.findall(pattern, text)
        if matches:
            if type(matches[0]) is tuple:
                for entry in matches[0]:
                    entries.append(entry.replace(
                        ".", "").replace("'s", ""))
            else:
                entries.append(matches[0].replace(
                    ".", "").replace("'s", ""))
        return (len(entries) > 0, entries)
