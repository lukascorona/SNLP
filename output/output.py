import os
from datetime import datetime

# http://swc2017.aksw.org/gerbil/config

class Output:

    path = "./output"

    @staticmethod
    def generateTriple(sentence_id, value):
        return "<http://swc2017.aksw.org/task2/dataset/{}> <http://swc2017.aksw.org/hasTruthValue> \"{}\"^^<http://www.w3.org/2001/XMLSchema#double> .\n".format(sentence_id, value)

    @staticmethod
    def generateFile(sentence_ids, values):
        time = datetime.now().strftime("%d-%m-%Y_%I-%M-%S_%p")
        with open("{}/{}.ttl".format(Output.path, time), "w") as file:
            for sentence, value in zip(sentence_ids, values):
                file.write(Output.generateTriple(sentence, value))