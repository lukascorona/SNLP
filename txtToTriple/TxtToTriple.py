import spacy
from util.triple import Triple

class TxtToTriple:
    triples = []
    
    @staticmethod
    def processTxt(txtPath):
        """ Read txt-file """
        fobj = open(txtPath, "r")
        for line in fobj:
            processLine(line)
        fobj.close()

    @staticmethod
    def processLine(line):
        """ Process line of txt.file """
        """ TODO: find triples -> textToToken + tokenToTriples"""
        tokenizedLine = textToToken(line)
        tokenToTriples(tokenizedLine)
        triple = Triple("subject", "predicat", "object")
        triples.append(triple)

    @staticmethod
    def textToToken(line):
        """ Requires to install spacy (pip) and en_core_web_sm afterwards (python -m spacy download en_core_web_sm)"""
        nlp = spacy.load("en_core_web_sm")
        tokenizedLine = nlp(line)
        return tokenizedLine

    @staticmethod
    def tokenToTriples(tokenizedLine):
        """TODO: mit spacy/ NLTK """
        return ""

