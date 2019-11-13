from util.triple import Triple

class TxtToTriple:
    triples = []
    
    def processTxt(txtPath):
        """ Read txt-file """
        fobj = open(txtPath, "r")
        for line in fobj:
            processLine(line)
        fobj.close()

    def processLine(line):
        """ Process line of txt.file """
        """ TODO: find triples"""
        triple = Triple("subject", "predicat", "object")
        triples.append(triple)
