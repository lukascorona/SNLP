# SNLP

Mini project for the course Statistical Natural Language Processing. The achieved result can be found [here].(http://swc2017.aksw.org/gerbil/experiment?id=202001150002)

# Install:

Make sure Anaconda python 3 is installed. Then run following commands:

```
$ pip install nltk
$ python -m nltk.downloader
```

In the popup window download the "Punkt" Model from Tab "Models", then run:

```
$ pip install wikipedia
$ pip install spacy
$ python -m spacy download en_core_web_sm
$ python -m spacy download en_core_web_md
```

# Recreate output file for GERBIL

```
$ python main.py --fact_file "./SNLP2019_test.tsv" --output "./result_output.ttl" --spacy
```

# Command line usage:

check a single fact:

```
$ python main.py -f "<some fact>"
```

check a .tsv file and save result in an output file

```
$ python main.py --fact_file "./<filename>.tsv" --output "./<filename>.ttl"
```

...or only print the result to the console:

```
$ python main.py --fact_file "./<filename>.tsv"
```

### Options

in all cases a new temporary corpus can be created, on default the prefetched corpus is used:

```
$ python main.py ... --new_corpus
```

and the triple generation can be switched to the spacy approach:

```
$ python main.py ... --spacy
```
