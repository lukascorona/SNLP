from input.input import Input
import pprint
import re
from math import inf as INFINITY
from tqdm import tqdm


class Facts(Input):

    def __init__(self):
        Input.__init__(self)
        self.test = []

    def check(self, regex_exp, corpus_path="./corpus"):
        # get all important sentences out of the corpus
        with open(corpus_path, "r", encoding="utf-8") as corpus:
            knowledge = []
            for i in range(len(self.documents)):
                knowledge.append([])
            for line in tqdm(corpus):
                for i, doc in enumerate(self.documents):
                    for regex in regex_exp:
                        found, entries = self.reg(regex, doc)
                        if found:
                            from_corpus = []
                            for entry in entries:
                                from_corpus += self.reg(entry +
                                                        "[^\.]*\.", line)[1]
                            knowledge[i] += from_corpus
                            break
        # TODO now do something with the sentences per document
        pprint.pprint(knowledge)
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
