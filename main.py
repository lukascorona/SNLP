from fetch.fetch import Fetcher
from input.input import Input
from transform.TextToTriple import TextToTriple
from transform.Similarity import Similarity


# Input.file("./SNLP2019_training.tsv").documents

#TextToTriple().tsv("./SNLP2019_training.tsv",  300).regex().stats()
Similarity().tsv("./SNLP2019_training.tsv",
                 200).candidates(8).print()
