from fetch.fetch import Fetcher
from input.input import Input
from transform.TextToTriple import TextToTriple
from transform.Similarity import Similarity
from transform.Facts import Facts
from enum import Enum
import pprint


class Mode(Enum):
    BUILD_CORPUS = 1
    CHECK_FACTS = 2


mode = Mode.BUILD_CORPUS

# build corpus
if mode is Mode.BUILD_CORPUS:
    entries = Similarity().tsv(
        "./SNLP2019_training.tsv").generate_regex(compare=8).use_regex().entries()
    Fetcher().add(entries).fetch()

elif mode is Mode.CHECK_FACTS:
    regex = Similarity().tsv(
        "./SNLP2019_training.tsv")[:200].generate_regex(compare=8).expressions()
    Facts().tsv(
        "./SNLP2019_training.tsv").check(regex, "./corpus-04-12-2019")
