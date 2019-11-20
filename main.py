from fetch.fetch import Fetcher
from input.input import Input
from transform.TextToTriple import TextToTriple

# Input.file("./SNLP2019_training.tsv").documents

print(TextToTriple.tsv("./SNLP2019_training.tsv",  # 100
                       ).process().triples)
