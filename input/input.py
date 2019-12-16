import csv


class Input:

    def __init__(self):
        self.documents = []
        self.ids = []
        self.truth = []

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

    def tsv(self, path: str):
        with open(path, encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile, dialect='excel-tab')
            if "True/False" in reader.fieldnames:
                for row in reader:
                    self.ids.append(row["FactID"])
                    self.documents.append(row["Fact_Statement"])
                    self.truth.append(float(row["True/False"]))
            else:
                for row in reader:
                    self.ids.append(row["FactID"])
                    self.documents.append(row["Fact_Statement"])
        return self

    def print(self):
        """prints triples"""
        if not self.documents:
            print("empty")
        for doc in self.documents:
            print(doc)

    def __getitem__(self, val):
        if type(val) is slice:
            self.documents = self.documents[val]
            self.ids = self.ids[val]
            if self.truth:
                self.truth = self.truth[val]
        return self
