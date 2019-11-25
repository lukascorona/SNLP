import spacy
from input.input import Input
from spacy import displacy
from spacy.symbols import nsubj, VERB
import re


class TextToTriple (Input):
    triples = []
    statistics = {}

    @DeprecationWarning
    def recursivePrint(self, token, depth):
        """ prints the linguistic parse tree """
        depth += 2
        for child in token.children:
            print(" " * depth, child.lemma_, child.dep_, child.pos_)
            self.recursivePrint(child, depth)

    @DeprecationWarning
    def process(self, debug: bool = False):
        """ all documents """
        """ see https://spacy.io/api/annotation """
        nlp = spacy.load("en_core_web_sm")

        for doc in self.documents:
            triple = [None, None, None]
            tokens = nlp(doc)
            # for chunk in tokens.noun_chunks:
            #     print("text: {}, root: {}, dep: {}, root head: {}".format(chunk.text, chunk.root.text, chunk.root.dep_,
            #                                                               chunk.root.head.text))
            # maybe we have to use https://spacy.io/usage/linguistic-features
            displacy.render(tokens, style="dep")
            for i in tokens:

                if debug:
                    print(i.lemma_, i.pos_, i.tag_, i.dep_, i.ent_type_)
                    print(i.lemma_, [child for child in i.children], i.head.text, [
                          child for child in i.head.children])
                if i.pos in [VERB]:
                    triple[1] = i.lemma_
                    self.recursivePrint(i, 0)
                # elif i.ent_type_ in ["PERSON", "ORG", "GPE", "LOC", "DATE"]:
                #     if triple[1] == None:
                #         triple[0] = i.lemma_
                #     else:
                #         triple[2] = i.lemma_
            if None not in triple:
                self.triples.append(triple)
        return self

    def regex(self, debug: bool = False):
        """ find triples with regex expressions """
        for doc in self.documents:
            doc = doc.lower()
            self.regToTriple(doc, [
                [r"(.*) is (.*)'s nascence place", "born in"],
                [r"(.*) is (.*) innovation place", "innovation place"],
                [r"(.*) stars (.*)\.", "stars"],
                [r"(.*) death place is (.*)\.", "death place"],
                # same sentence, different order
                [r"(.*) is (.*) death place", "death place"],
                [r"(.*)'s team is (.*)\.", "team is"],
                [r"(.*)'s award is (.*)\.", "award in"],
                # same sentence, different order
                [r"(.*) is (.*) award", "award in"],
                [r"(.*) is (.*)'s role", "is role"],
                [r"(.*) is (.*)'s better half", "married to"],
                [r"(.*)'s author is (.*)\.", "wrote"]
            ])
        self.statistics["found"] = round(
            len(self.triples) / (len(self.documents)*2), 4)
        return self

    def stats(self):
        """ prints collected figures """
        for key in self.statistics:
            print("{}: {}".format(key, self.statistics[key]))

    def regToTriple(self, doc, expressions):
        """ creates triples from a sentence. each triple is saves twice with subj and obj switched """
        for regex in expressions:
            tokens = list(re.findall(regex[0], doc))
            if tokens and len(tokens[0]) == 2:
                self.triples.append(
                    [tokens[0][0], regex[1], tokens[0][1]])
                self.triples.append(
                    [tokens[0][1], regex[1], tokens[0][0]])

    def print(self):
        """prints triples"""
        if not self.triples:
            print("empty")
        for triple in self.triples:
            print(triple)
