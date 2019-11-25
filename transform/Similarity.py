from input.input import Input
import pprint
import re


class Similarity (Input):
    _candidates = []
    _candidates_set = []
    _regex = set()
    _regex_expressions = []

    def candidates(self):
        remaining_indexes = list(range(len(self.documents)))
        for current in range(len(self.documents)):
            self._candidates.append(self.documents[current].lower().split())
            self._candidates_set.append(
                set(self.documents[current].lower().split()))
        for current in range(len(self._candidates)):
            self._candidates_set[current]
            for i, remain_a in enumerate(remaining_indexes):
                for j, remain_b in enumerate(remaining_indexes):

                    if i != -1 and j != -1 and \
                            self._candidates_set[current] != self._candidates_set[remain_a] and \
                            self._candidates_set[current] != self._candidates_set[remain_b] and \
                            self._candidates_set[remain_a] != self._candidates_set[remain_b] and \
                            len(self._candidates_set[current] & self._candidates_set[remain_a] & self._candidates_set[remain_b]) > 0 and \
                            self._candidates_set[current] & self._candidates_set[remain_a] & self._candidates_set[remain_b] != set(["is"]):

                        remaining_indexes[i] = remaining_indexes[j] = -1
                        sublist = []
                        last_inserted_word = None
                        for curr_index in range(len(self._candidates[current])):
                            word_curr = self._candidates[current][curr_index]
                            for word_rem_a in self._candidates[remain_a]:
                                for word_rem_b in self._candidates[remain_b]:
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
        #     reg_list = []
        #     for word in reg:
        #         reg_list.append(word.replace(".", "").replace("<s>", ""))
        #     self._regex_expressions.append(
        #         "".join(reg_list) + ("" if reg[-1].endswith(".") else " (.*)"))

            # doc = set(doc.lower().split(" "))
            # found_similar = False
            # for i in range(len(self._candidates)):
            #     if len(self._candidates[i] & doc) > 0 and self._candidates[i] & doc != set(["is"]):
            #         found_similar = True
            #         self._candidates[i] = self._candidates[i] & doc
            # if not found_similar:
            #     self._candidates.append(doc)
        return self

    def print(self):
        pprint.pprint(self._regex_expressions)
