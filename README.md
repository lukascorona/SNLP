# SNLP

Mini project for snlp

# install:

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

# usage:

check a single fact with the prefetched corpus:

```
$ python main.py -f "<some fact>"
```

...or create a temporary corpus, existing only of wikipedia pages of the object and subject in the given fact:

```
$ python main.py -f "<some fact>" --new_corpus
```

check a .tsv file and save result in an output file

```
$ python main.py --fact_file "./<filename>.tsv" --output "./<filename>.ttl"
```

...or only print the result to the console:

```
$ python main.py --fact_file "./<filename>.tsv"
```

also in this case a new temporary corpus can be created:

```
$ python main.py --fact_file "./<filename>.tsv" --new_corpus
$ python main.py --fact_file "./<filename>.tsv" --output "./<filename>.ttl" --new_corpus
```
