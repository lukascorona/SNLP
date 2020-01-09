from fetch.fetch import Fetcher
from input.input import Input
from output.output import Output
from transform.TextToTriple import TextToTriple
from transform.Similarity import Similarity
from transform.AdvancedChecker import AdvancedChecker
from transform.Facts import Facts
from enum import Enum
from pprint import pprint


class Mode(Enum):
    BUILD_CORPUS = 1
    CHECK_FACTS = 2
    TRIPLETS_TSV = 3
    TRIPLETS_CORPUS = 4
    PREPROCESSING = 5
    CHECK_FACTS_ADVANCED = 6


mode = Mode.CHECK_FACTS

# build corpus
if mode is Mode.BUILD_CORPUS:
    entries = TextToTriple().tsv(
        "./SNLP2019_training.tsv").genTriplets().getEntries()
    print(f"found {len(entries)} entries in train set.")
    entries |= TextToTriple().tsv(
        "./SNLP2019_test.tsv").genTriplets().getEntries()
    print(f"found {len(entries)} entries in train and test set.")
    Fetcher().add(entries).fetch()

# elif mode is Mode.CHECK_FACTS:
#     regex = Similarity().tsv(
#         "./SNLP2019_training.tsv").generate_regex(compare=30).expressions()
#     Facts().tsv(
#         "./SNLP2019_training.tsv").check(regex, "./corpus-2019-12-11T21-19-46_train_and_test")  # corpus-2019-12-11T21-19-46_train_and_test corpus-2019-12-11T20-04-11_train

#elif mode is Mode.CHECK_FACTS:
    # triplets = TextToTriple().tsv(
    #     "./SNLP2019_training.tsv").genTriplets(debug=True).getTriplets()
    #corpus = TextToTriple().file(
     #   "./DEP_corpus-2019-12-22T14-42-29", per_article=True, max_lines=10).documents
    #print(len(corpus))
    #print("\n\n".join(corpus))

elif mode is Mode.TRIPLETS_TSV:
    triplets = TextToTriple().tsv(
        "./SNLP2019_test.tsv").genTriplets(debug=True).getTriplets()
    pprint(triplets)

elif mode is Mode.TRIPLETS_CORPUS:
    triplets = TextToTriple().file(
        "./corpus-2019-12-22T14-42-29")[:100].genTriplets(debug=True).getTriplets()
    pprint(triplets)

elif mode is Mode.PREPROCESSING:
    triplets = TextToTriple().file(
        "./corpus-2019-12-11T20-04-11_train").savePreprocessed(".\PREPR_corpus-2019-12-11T20-04-11_train")

elif mode is Mode.CHECK_FACTS_ADVANCED:
    tsvPath = "./SNLP2019_test.tsv"#"./SNLP2019_training.tsv"
    corpusPath = "./corpus-2019-12-22T14-42-29"
    similarity = Similarity()
    similarity.tsv(tsvPath).generate_regex(compare=30).use_regex() 
    checker = AdvancedChecker(similarity.expressions())
    ids, values = checker.check(tsvPath, corpusPath)
    Output.generateFile(ids, values)
    
elif mode is Mode.CHECK_FACTS:
    tsvPath = "./SNLP2019_training.tsv"#"./SNLP2019_training.tsv"
    corpusPath = "./corpus-2019-12-22T14-42-29"
    
    triplets = TextToTriple().tsv(tsvPath).genTriplets().getTriplets()
    checker = AdvancedChecker(triplets)
    ids, values = checker.checkWithTriples(tsvPath, corpusPath)
    Output.generateFile(ids, values)

