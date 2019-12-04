from input.input import Input
import pprint
import re
from math import inf as INFINITY
from tqdm import tqdm


class Candidate:
    def __init__(self, words, similarity):
        self.words = words
        self.sim = similarity
        self.index = 0

    def __str__(self):
        return "sim: {}, words: {}".format(self.sim, self.words)


class Similarity (Input):
    _candidates = []
    _candidates_set = []
    _regex = set()
    _regex_expressions = []

    def candidates(self, num_compare_candidates=4, num_candidates=INFINITY, DEBUG=False):
        for current in range(len(self.documents)):
            # preprocess sentences (no lower(), cause "Stars" and "stars" should be different)
            self._candidates.append(
                self.documents[current].replace("'s", "").split())
            # create sets ot the words, no duplicates and faster for computation later
            self._candidates_set.append(
                set(self.documents[current].lower().split()))

        num_docs = len(self._candidates)
        skipped = 0
        # go through each sentence
        for current in tqdm(range(min(num_docs, num_candidates))):
            if DEBUG:
                print("next:", self._candidates[current])
            distances = []
            # measure similarity to each other sentence
            for other in range(num_docs):
                similarity = len(self._candidates_set[current] & self._candidates_set[other]) / len(
                    self._candidates_set[current] | self._candidates_set[other])
                distances.append(
                    Candidate(self._candidates[other], similarity))
            # and sort descending
            distances.sort(key=lambda x: x.sim, reverse=True)
            if DEBUG:
                for distance in distances:
                    if distance.sim == 0:
                        break
                    print(distance)
            # check it min n samples have some same words
            if distances[num_compare_candidates - 1].sim == 0.0:
                if DEBUG:
                    print("too less samples for:", self._candidates[current])
                skipped += 1
                break
            sublist = []
            last_inserted_word = None
            # go through each word of current sentence
            for curr_index, word_curr in enumerate(self._candidates[current]):
                # make the var accessible outside the next loop
                found_duplicate = False
                # go through each other sentence, skip the first, cause this is actually the current sentence
                for other in distances[1:num_compare_candidates]:
                    # inititially no same word is found in any other sentence
                    found_duplicate = False
                    # on iterating through Candidates, current index is saved, on next loop it starts there, so order of words is preserved
                    for i, word in enumerate(other.words[other.index:]):
                        if word_curr == word:
                            found_duplicate = True
                            other.index = i
                            # if word is same, go directly to next sentence
                            break
                    if not found_duplicate:
                        # if word was not found in the whole sentence, skip this word completely
                        break
                # if the current word "survived" all other sentence, so it was found in all of them, add it to regex expression
                if found_duplicate:
                    # if we have the first word, but it is not the first in the sentence add "(.*)" at the beginning
                    if curr_index > 0 and not sublist:
                        sublist.append("(.*)")
                    # if the current word comes directly after the previous one, delete the "(.*)" after the previous word
                    elif curr_index > 0 and last_inserted_word == self._candidates[current][curr_index - 1]:
                        del sublist[-1]
                    # add the word to the rexeg expression
                    sublist.append(
                        word_curr.replace(".", ""))
                    # if the word is not at the end, add a "(.*)" after it
                    if not word_curr.endswith("."):
                        sublist.append("(.*)")
                    last_inserted_word = word_curr
            if sublist:
                self._regex.add(tuple(sublist))

        for reg in self._regex:
            self._regex_expressions.append(" ".join(list(reg)))
        print("skipped: {}".format(skipped))
        return self

    def print(self):
        pprint.pprint(self._regex_expressions)
