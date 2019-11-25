from fetch.fetch import Fetcher
from input.input import Input
from transform.TextToTriple import TextToTriple
import pprint

# Input.file("./SNLP2019_training.tsv").documents

# pprint.pprint(TextToTriple.tsv("./SNLP2019_training.tsv",  300).regex().triples)
TextToTriple.tsv("./SNLP2019_training.tsv",  300).regex().stats()
