import spacy
from input.input import Input
from spacy.symbols import nsubj, VERB
from pprint import pprint
import re


class TextToTriple (Input):
    _triplets = []
    statistics = {}

    def __init__(self):
        Input.__init__(self)

    def genTriplets(self, debug: bool = False):
        """ all documents """
        """ see https://spacy.io/api/annotation """
        nlp = spacy.load("en_core_web_md")

        typesetting = [
            r"(?P<obj>.*)(?:<<nsubj>>|<<appos>>|<<nmod>>).*<<ROOT>>(?P<subj>.*)(?:<<poss>>|<<conj>>).*<<case>>(?P<verb>.*)(?:<<attr>>|<<pobj>>|<<appos>>|<<dobj>>|<<ROOT>>)",
            r"(?P<subj>.*)(?:<<poss>>|<<nmod>>|<<pobj>>).*<<case>>(?P<verb>.*)(?:<<ROOT>>|<<auxpass>>|<<aux>>|<<ccomp>>)(?P<obj>.*)(?:<<appos>>|<<attr>>|<<nsubj>>|<<acomp>>)",
            r"(?P<subj>.*)(?:<<nsubj>>|<<advmod>>)(?P<verb>.*)<<ROOT>>(?P<obj>((?!<<case>>).)*)(?:<<appos>>|attr|dobj)",
            r"(?P<obj>.*)(?P<verb><<compound>>star<<nsubj>>)(?P<subj>.*)",
            r"(?P<obj>.*)(?P<verb><<compound>>star<<ROOT>>)(?P<subj>.*)",
            r"(?P<obj>.*)(?P<verb><<amod>>star<<pobj>>)(?P<subj>.*)",
            r"(?P<obj>.*)(?P<verb><<amod>>star<<compound>>)(?P<subj>.*)",
            r"(?P<obj>.*)(?P<verb><<dobj>>star<<dobj>>)(?P<subj>.*)",
            r"(?P<obj>.*)(?P<verb><<dobj>>star<<compound>>)(?P<subj>.*)",
            r"(?P<obj>.*)(?P<verb><<nsubj>>star<<compound>>)(?P<subj>.*)",
            r"(?P<obj>.*)(?P<verb><<nsubj>>star<<ROOT>>)(?P<subj>.*)",
            r"(?P<obj>.*)(?P<verb><<nummod>>star<<compound>>)(?P<subj>.*)",
            r"(?P<obj>.*)(?P<verb><<nummod>>star<<ROOT>>)(?P<subj>.*)",
            r"(?P<obj>.*)(?P<verb><<compound>>star<<compound>>)(?P<subj>.*)<<ROOT>>"
        ]

        for doc in self.documents:
            doc = re.sub(r"([()]|(-PRON-))", "", doc)
            tokens = nlp(doc)
            regex_friendly_string = ""
            for i in tokens:
                regex_friendly_string += f"{i.lemma_}<<{i.dep_}>>"
            found = False
            for i, setting in enumerate(typesetting):
                matches = re.match(
                    setting, regex_friendly_string)
                if matches and len(matches.groupdict()) == 3:
                    if len(matches.groupdict()) > 3:
                        print(f"greater than 3: {regex_friendly_string}")
                    if found:
                        print(f"second regex: {i}: {regex_friendly_string}")
                    found = True
                    formatted = {}
                    for key, value in matches.groupdict().items():
                        formatted[key] = re.sub(
                            r"<<[^<>]*>>", " ", value).lower()
                    self._triplets.append(formatted)
                    break
            if not found:
                print(doc)
                print(regex_friendly_string)
        return self

    def getTriplets(self):
        return self._triplets

    def print(self):
        """prints triples"""
        if not self._triplets:
            print("empty")
        for triplet in self._triplets:
            print(triplet)
