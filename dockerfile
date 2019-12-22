FROM continuumio/anaconda3
RUN apt-get update
RUN apt-get install -y gcc g++
RUN pip install -U spacy wikipedia
RUN pip install textacy
RUN python -m spacy download en_core_web_sm
RUN python -m spacy download en_core_web_md

# docker build -t nlp .
# docker run -i -t -v %cd%:/data nlp /bin/bash
# docker exec nlp python main.py