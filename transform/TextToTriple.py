import spacy
from input.input import Input
from spacy import displacy
from spacy.symbols import nsubj, VERB
from pprint import pprint
import re


class TextToTriple (Input):
    triples = []
    statistics = {}

    def __init__(self):
        Input.__init__(self)

    @DeprecationWarning
    def recursivePrint(self, token, depth):
        """ prints the linguistic parse tree """
        depth += 2
        for child in token.children:
            print(" " * depth, child.lemma_, child.dep_, child.pos_)
            self.recursivePrint(child, depth)

    def getChilds(self, entry):
        tree = {}
        full_tree = {'left': [], 'right': [], 'entry': entry,
                     'dep': entry.dep_, 'pos': entry.pos_}
        for child in entry.lefts:
            subtree = self.getChilds(child)
            tree[f"left: {child.text}, {child.lemma_}, {child.pos_} {child.dep_}"] = subtree[0]
            full_tree['left'].append(subtree[1])
        for child in entry.rights:
            subtree = self.getChilds(child)
            tree[f"right: {child.text}, {child.lemma_}, {child.pos_} {child.dep_}"] = subtree[0]
            full_tree['right'].append(subtree[1])
        return (tree, full_tree)

    # @DeprecationWarning
    def process(self, debug: bool = False):
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
        sentences = []
        for i, setting in enumerate(typesetting):
            sentences.append([])

        for doc in self.documents:
            # if debug:
            #     print("================================================" + doc)
            triple = [None, None, None]
            doc = re.sub(r"([()]|(-PRON-))", "", doc)
            tokens = nlp(doc)
            # for chunk in tokens.noun_chunks:
            #     print("text: {}, root: {}, dep: {}, root head: {}".format(chunk.text, chunk.root.text, chunk.root.dep_,
            #                                                               chunk.root.head.text))
            # maybe we have to use https://spacy.io/usage/linguistic-features
            # displacy.render(tokens, style="dep")

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
                        formatted[key] = re.sub(r"<<[^<>]*>>", " ", value)
                    # print("found", formatted)
                    sentences[i].append(
                        f"{formatted} = {regex_friendly_string}")
                    break
            if not found:
                print(doc)
                print(regex_friendly_string)

            # print(regex_friendly_string)
            # if debug:
            #     print(
            #         f"text: {i.text}, \tlemma: {i.lemma_}, \tdep: {i.dep_}, \ttype: {i.ent_type_}")

            # if i.dep_ == "ROOT":
            # printtree, tree = self.getChilds(i)
            # pprint(tree)
            # verb = []
            # obj = []
            # subj = []
            # print((subj, verb, obj))
            # verb += tree
            # print(i.lemma_, i.pos_, i.tag_, i.dep_, i.ent_type_)
            # print(i.lemma_, [child for child in i.children], i.head.text, [
            #       child for child in i.head.children])
            # if i.pos in [VERB]:
            #     triple[1] = i.lemma_
            #     self.recursivePrint(i, 0)
            # elif i.ent_type_ in ["PERSON", "ORG", "GPE", "LOC", "DATE"]:
            #     if triple[1] == None:
            #         triple[0] = i.lemma_
            #     else:
            #         triple[2] = i.lemma_
            # if None not in triple:
            #     self.triples.append(triple)
        # pprint(sentences)
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
