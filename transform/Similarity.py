from input.input import Input
import pprint
import re
from tqdm import tqdm


class Similarity (Input):
    _candidates = []
    _candidates_set = []
    _regex = set()
    _regex_expressions = []

    def candidates(self):
        print(len(self.documents))
        for current in range(len(self.documents)):
            self._candidates.append(self.documents[current].lower().split())
            self._candidates_set.append(
                set(self.documents[current].lower().split()))

        num_docs = len(self._candidates)
        for current in tqdm(range(num_docs)):
            best_intersection = 0
            best_i = best_j = -1
            for i in range(num_docs):
                for j in range(num_docs):
                    # reihenfolge der wörter noch nicht bedacht, erst grobe aussortierung
                    if self._candidates_set[current] != self._candidates_set[i] and \
                            self._candidates_set[current] != self._candidates_set[j] and \
                            self._candidates_set[i] != self._candidates_set[j] and \
                            len(self._candidates_set[current] & self._candidates_set[i] & self._candidates_set[j]) > best_intersection and \
                            self._candidates_set[current] & self._candidates_set[i] & self._candidates_set[j] != set(["is"]):
                        best_intersection = len(
                            self._candidates_set[current] & self._candidates_set[i] & self._candidates_set[j])
                        best_i = i
                        best_j = j
            # jetzt mit reihenfolge bei kandidaten mit höchster überschneidung
            sublist = []
            last_inserted_word = None
            for curr_index, word_curr in enumerate(self._candidates[current]):
                for word_rem_a in self._candidates[best_i]:
                    for word_rem_b in self._candidates[best_j]:
                        if word_curr == word_rem_a == word_rem_b:
                            if curr_index != 0 and not sublist:
                                sublist.append("(.*)")
                            elif curr_index > 0 and last_inserted_word == self._candidates[current][curr_index - 1]:
                                del sublist[-1]
                            sublist.append(
                                word_curr.replace(".", ""))
                            if not word_curr.endswith("."):
                                sublist.append("(.*)")
                            last_inserted_word = word_curr
            self._regex.add(tuple(sublist))
        for reg in self._regex:
            self._regex_expressions.append(" ".join(list(reg)))
        return self

    def print(self):
        pprint.pprint(self._regex_expressions)
