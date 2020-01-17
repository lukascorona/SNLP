# SNLP

Mini project for the course Statistical Natural Language Processing. The achieved result can be found [here](http://swc2017.aksw.org/gerbil/experiment?id=202001150002).

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

# Get help

Simply call:

```
$ python main.py -h
```

# Command line usage:

The programm needs some time for startup (~26 sec). Besides the imports, it also has to load the spacy and nltk models. <br />
Check a single fact and save result in an output file:

```
$ python main.py -f "<some fact>" --output "./<filename>.ttl"
```

...or only print the result to the console:

```
$ python main.py -f "<some fact>"
```

Check a .tsv file and save result in an output file

```
$ python main.py --fact_file "./<filename>.tsv" --output "./<filename>.ttl"
```

...or only print the result to the console:

```
$ python main.py --fact_file "./<filename>.tsv"
```

### Options

In all cases a new temporary corpus can be created, but on default the prefetched corpus is used:

```
$ python main.py ... --new_corpus
```

And the triple generation can be switched to the spacy approach (recommended):

```
$ python main.py ... --spacy
```
