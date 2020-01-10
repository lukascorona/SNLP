from input.input import Input
import nltk.data
import re
from random import *
import time
import numpy as np

class AdvancedChecker(Input):
        
    def __init__(self, *args):
        Input.__init__(self)
        self.tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        if len(args) == 1 and isinstance(args[0][0], str):
            print("AdvancedChecker for Regex:\n")
            self.regex_list = args[0]
            self.type = "REGEX"
        else:
            print("AdvancedChecker for Triples:\n")
            self.triples = args[0]
            self.type="TRIPLES"
    
    def check(self, tsvPath, corpusPath):
        start_time = time.time()
        # get data from the tsv
        ids, facts, truthValues = self.tsvToLists(tsvPath)
        values = []

        for fact in facts:
            # delete '.' if its the last character
            if fact[-1] == ".":
                fact = fact[:-1]
            # check fact and append truth value to list
            values.append(self.checkFact(fact, corpusPath))
            print("Checked:   " + fact)
        
        # if tsv contains labeld data, calulate accuracy
        if len(truthValues) > 0:
            correct = 0
            for i in range(min(len(truthValues), len(values))):
                if truthValues[i] == values[i]:
                    correct += 1
            print("Correctly Found: {} out of {} ({}%)".format(correct, len(values), (correct / len(values))*100))
        print("Elapsed time: {} seconds".format(time.time() - start_time))    
        return ids, values
    
    def checkFact(self, fact, corpusPath):
        """Check a fact using the generated regex list"""
        for regex in self.regex_list:
            p = re.compile(regex)
            m = p.search(fact)

            # if regex fits the fact, get  matches and check all found articles 
            if m:       
                obj1 = m.group(1)
                obj2 = m.group(2)
                # Delete the matches found from the regex and delete unnecessary spaces
                rest = " ".join(fact.replace(obj1, "").replace(obj2, "").split())
                
                with open(corpusPath, "r", encoding="utf-8") as corpus:
                    for article in corpus:
                        if obj1 in article or obj2 in article:
                            value, certain = AdvancedChecker.checkFactOnArticle(obj1, rest, obj2, article)
                            if certain:
                                # return value if we are certain
                                return value
        # If no value was found that we are sure of, we return 0
        return 0        
                         
     
    def checkWithTriples(self, tsvPath, corpusPath):
        start_time = time.time()
        # get data from the tsv
        ids, facts, truthValues = self.tsvToLists(tsvPath)
        values = []

        for i in range(0, len(facts)):
            print("Checking:   " + facts[i])
            values.append(self.CheckFactWithTriples(self.triples[i], corpusPath))
            
        if len(truthValues) > 0:
            correct = 0
            for i in range(min(len(truthValues), len(values))):
                if truthValues[i] == values[i]:
                    correct += 1
            print("Correctly Found: {} out of {} ({}%)".format(correct, len(values), (correct / len(values))*100))
        print("Elapsed time: {} seconds".format(time.time() - start_time))    
        return ids, values
    
    def CheckFactWithTriples(self, triple, corpusPath):
        subj = triple.get('subj')
        verb = triple.get('verb')
        obj = triple.get('obj')
        
        if subj == "UNKNOWN":
            return 0
        
        with open(corpusPath, "r", encoding="utf-8") as corpus:
            for article in corpus:
                article = article.lower()
                if subj in article or obj in article:
                    value, certain = AdvancedChecker.checkFactOnArticle(subj, verb, obj, article) #self.checkFactOnSentences(subj, verb, obj, article)
                    if certain:
                        # return value if we are certain
                        return value
        return 0 
    
    @staticmethod
    def checkFactOnArticle(obj1, rest, obj2, article):
        """Check whether the fact can be implied from the article or not"""
        if obj1 in article and obj2 in article:
            # If the article contains both matches of the regex, we assume that the fact is true (and we are certain)
            return 1, True
        elif obj1 in article and rest in article:
            return 0, False
        elif obj2 in article and rest in article:
            return 0, False
        elif obj1 in article or obj2 in article:
            return 0, False
        else:
            return 0, False
            #print("Something went wrong")
            #return round(random()), False
        
    def checkFactOnSentences(self, obj1, rest, obj2, article):
        for sentence in self.tokenizer.tokenize(article):
            #print('Sentence: ' + sentence)
            value, certain = AdvancedChecker.checkFactOnArticle(obj1, rest, obj2, sentence)
            if certain:
                return value, certain
        return 0, False
            