import csv


class Input:

    documents = []

    def file(self, txtPath: str) -> 'TextToTriple':
        """ Read textfile and adds them to the queue """
        with open(txtPath, "r") as fobj:
            for line in fobj:
                self.documents += line.split(".")
        return self

    def text(self, text: str) -> 'TextToTriple':
        """ adds text in queue"""
        self.documents += text.split(".")
        return self

    def tsv(self, path: str, rows: int = None) -> 'TextToTriple':
        """ adds text from tsvfile in queue"""
        self.documents += self.readTsv(path, rows).documents
        return self

    def readTsv(self, path: str, rows: int = None):
        with open(path, encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile, dialect='excel-tab')
            for i, row in enumerate(reader):
                self.documents.append(row["Fact_Statement"])
                if rows != None and i > rows:
                    break
        return self

    def print(self):
        """prints triples"""
        if not self.documents:
            print("empty")
        for doc in self.documents:
            print(doc)
