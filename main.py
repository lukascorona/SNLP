from fetch.fetch import Fetcher
from input.input import Input
from transform.TextToTriple import TextToTriple
from transform.Similarity import Similarity
from transform.Facts import Facts
from enum import Enum
from pprint import pprint


class Mode(Enum):
    BUILD_CORPUS = 1
    CHECK_FACTS = 2


mode = Mode.CHECK_FACTS

# build corpus
if mode is Mode.BUILD_CORPUS:
    similarity = Similarity()
    entries = similarity.tsv(
        "./SNLP2019_training.tsv").tsv(
        "./SNLP2019_test.tsv").generate_regex(compare=30).use_regex().entries()
    pprint(similarity.expressions())
    Fetcher().add(entries).fetch()

elif mode is Mode.CHECK_FACTS:
    regex = Similarity().tsv(
        "./SNLP2019_training.tsv").generate_regex(compare=30).expressions()
    Facts().tsv(
        "./SNLP2019_training.tsv").check(regex, "./corpus-2019-12-11T21-19-46_train_and_test")  # corpus-2019-12-11T21-19-46_train_and_test corpus-2019-12-11T20-04-11_train
