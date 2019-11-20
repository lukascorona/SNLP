import spacy


class TextToTriple:
    triples = []
    documents = []

    @staticmethod
    def file(txtPath: str) -> 'TextToTriple':
        """ Read textfile and adds them to the queue """
        with open(txtPath, "r") as fobj:
            TextToTriple.documents.append(fobj.read())
        return TextToTriple

    @staticmethod
    def text(text: str) -> 'TextToTriple':
        """ adds text in queue"""
        TextToTriple.documents.append(text)
        return TextToTriple

    @staticmethod
    def process():
        """ Process line of txt.file """
        """ see https://spacy.io/api/annotation """
        nlp = spacy.load("en_core_web_sm")
        triple = [None, None, None]
        for doc in TextToTriple.documents:
            for i in nlp(doc):
                print(i.lemma_, i.pos_, i.tag_, i.dep_, i.ent_type_)
                if i.pos_ in ["VERB"]:
                    triple[1] = i.lemma_
                elif i.ent_type_ in ["PERSON", "ORG", "GPE", "LOC", "DATE"]:
                    if triple[0] == None:
                        triple[0] = i.lemma_
                    else:
                        triple[2] = i.lemma_
                        if None not in triple:
                            TextToTriple.triples.append(triple)
                        triple = [None, None, None]
        return TextToTriple

    @staticmethod
    def triples():
        """returns all triples"""
        return TextToTriple.triples

    @staticmethod
    def print():
        """prints triples"""
        if not TextToTriple.triples:
            print("empty")
        for triple in TextToTriple.triples:
            print(triple)
