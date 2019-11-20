import spacy
from input.input import Input


class TextToTriple:
    triples = []
    documents = []

    @staticmethod
    def file(txtPath: str) -> 'TextToTriple':
        """ Read textfile and adds them to the queue """
        with open(txtPath, "r") as fobj:
            for line in fobj:
                TextToTriple.documents += line.split(".")
        return TextToTriple

    @staticmethod
    def text(text: str) -> 'TextToTriple':
        """ adds text in queue"""
        TextToTriple.documents += text.split(".")
        return TextToTriple

    @staticmethod
    def tsv(path: str, rows: int = None) -> 'TextToTriple':
        """ adds text from tsvfile in queue"""
        TextToTriple.documents += Input.tsv(path, rows).documents
        return TextToTriple

    @staticmethod
    def process(debug: bool = False):
        """ all documents """
        """ see https://spacy.io/api/annotation """
        nlp = spacy.load("en_core_web_sm")

        for doc in TextToTriple.documents:
            triple = [None, None, None]
            tokens = nlp(doc)
            # for chunk in tokens.noun_chunks:
            #     print("text: {}, root: {}, dep: {}, root head: {}".format(chunk.text, chunk.root.text, chunk.root.dep_,
            #                                                               chunk.root.head.text))
            # maybe we have to use https://spacy.io/usage/linguistic-features
            for i in tokens:
                if debug:
                    print(i.lemma_, i.pos_, i.tag_, i.dep_, i.ent_type_)
                print(i.lemma_, [child for child in i.children], i.head.text,
                      [child for child in i.head.children])
                if i.pos_ in ["VERB"]:
                    triple[1] = i.lemma_
                elif i.ent_type_ in ["PERSON", "ORG", "GPE", "LOC", "DATE"]:
                    if triple[1] == None:
                        triple[0] = i.lemma_
                    else:
                        triple[2] = i.lemma_
            if None not in triple:
                TextToTriple.triples.append(triple)
        return TextToTriple

    @staticmethod
    def print():
        """prints triples"""
        if not TextToTriple.triples:
            print("empty")
        for triple in TextToTriple.triples:
            print(triple)
