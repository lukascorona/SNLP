import csv


class Input:

    documents = []

    @staticmethod
    def tsv(path: str, rows: int = None):
        with open(path, encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile, dialect='excel-tab')
            for i, row in enumerate(reader):
                Input.documents.append(row["Fact_Statement"])
                if rows != None and i > rows:
                    break
        return Input

    @staticmethod
    def print():
        """prints triples"""
        if not Input.documents:
            print("empty")
        for doc in Input.documents:
            print(doc)
