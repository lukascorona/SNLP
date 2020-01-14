import os
import sys
from pprint import pprint
from enum import Enum
from transform.Facts import Facts
from transform.AdvancedChecker import AdvancedChecker
from transform.Similarity import Similarity
from transform.TextToTriple import TextToTriple
from output.output import Output
from input.input import Input
from fetch.fetch import Fetcher
from argparse import ArgumentParser
print("make imports...")
print("ready. start...")


class Mode(Enum):
    BUILD_CORPUS = 1
    CHECK_FACTS = 2
    TRIPLETS_TSV = 3
    TRIPLETS_CORPUS = 4
    PREPROCESSING = 5
    CHECK_FACTS_ADVANCED = 6
    FULL_PIPELINE = 7


mode = Mode.BUILD_CORPUS

parser = ArgumentParser(description='Fact checker')
parser.add_argument("-f", "--fact", type=str, metavar='"..."',
                    help="check a single fact")  # nargs='*' for -f "fact 1" "fact 2"
parser.add_argument("--fact_file", type=str, metavar='"..."',
                    help="provide a relative path to a fact file (.tsv), ignored if \"--fact\" is set")
parser.add_argument("-o", "--output", type=str, metavar='"..."',
                    help="provide a relative path to a output file (.ttl), can be used with \"--fact\" or \"--fact_file\". If not set, result is only printed on console")
parser.add_argument("-c", "--new_corpus", action='store_true',
                    help="if set, it fetches wiki pages only for the given fact or fact file, else it uses the prefetched corpus")
parser.add_argument("-s", "--spacy", action='store_true',
                    help="Use the Spacy approach for triple generation. Default is the regex approach.")
args = parser.parse_args()

if args.fact != None or args.fact_file != None:
    mode = mode.FULL_PIPELINE

if mode is mode.FULL_PIPELINE:
    corpus = None
    corpusPath = "./corpus-2019-12-22T14-42-29"
    if args.spacy:
        if args.fact:
            ttt = TextToTriple().text(args.fact).genTriplets()
        else:
            ttt = TextToTriple().tsv(args.fact_file).genTriplets()
        triples = ttt.getTriplets()
        if args.new_corpus == True:
            entries = ttt.getEntries()
            corpus = Fetcher().add(entries).fetch(ram=True)
            corpusPath = None
        checker = AdvancedChecker(triples)
        ids, values = checker.checkWithTriples(
            args.fact_file, corpusPath, corpus)
    else:
        corpusPath = "./corpus-2019-12-22T14-42-29"
        similarity = Similarity()
        similarity.tsv(
            "./SNLP2019_test.tsv").generate_regex(compare=20).use_regex()
        if args.new_corpus == True:
            entries = similarity.entries()
            corpus = Fetcher().add(entries).fetch(ram=True)
            corpusPath = None
        checker = AdvancedChecker(similarity.expressions())
        if args.fact:
            ids, values = checker.check(
                None, corpusPath, corpus, fact=args.fact)
        else:
            ids, values = checker.check(args.fact_file, corpusPath, corpus)

    if args.fact == None and args.output != None:
        (path, filename) = os.path.split(args.output)
        Output.path = path
        Output.generateFile(ids, values, filename)
        print(f"done. Output is saved to {args.output}")
    else:
        for i, value in enumerate(values):
            if value:
                print(f"done. Fact \"{args.fact or ids[i]}\" is true")
            else:
                print(f"done. Fact \"{args.fact or ids[i]}\" is false")

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

# elif mode is Mode.CHECK_FACTS:
    # triplets = TextToTriple().tsv(
    #     "./SNLP2019_training.tsv").genTriplets(debug=True).getTriplets()
    # corpus = TextToTriple().file(
    #   "./DEP_corpus-2019-12-22T14-42-29", per_article=True, max_lines=10).documents
    # print(len(corpus))
    # print("\n\n".join(corpus))

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
    tsvPath = "./SNLP2019_test.tsv"  # "./SNLP2019_training.tsv"
    corpusPath = "./corpus-2019-12-22T14-42-29"
    similarity = Similarity()
    similarity.tsv(tsvPath).generate_regex(compare=30).use_regex()
    checker = AdvancedChecker(similarity.expressions())
    ids, values = checker.check(tsvPath, corpusPath)
    Output.generateFile(ids, values)

elif mode is Mode.CHECK_FACTS:
    tsvPath = "./SNLP2019_test.tsv"  # "./SNLP2019_training.tsv"
    corpusPath = "./corpus-2019-12-22T14-42-29"

    triplets = TextToTriple().tsv(tsvPath).genTriplets().getTriplets()
    checker = AdvancedChecker(triplets)
    ids, values = checker.checkWithTriples(tsvPath, corpusPath)
    Output.generateFile(ids, values)
