from fetch.fetch import Fetcher
from util.triple import Triple
from util.predicate import LivesIn
from util.object import Person, Location
from txtToTriple.TxtToTriple import TxtToTriple

Fetcher.add(Triple(Person("Lukas"), LivesIn(), Location("Paderborn")))
Fetcher.add(Triple(Person("Dirk"), LivesIn(), Location("Paderborn")))
Fetcher.fetch()

tokenizedLine = TxtToTriple.textToToken("Niclas lives in Paderborn")
for token in tokenizedLine:
    print(token.text, "-->",token.dep_,"-->", token.pos_)
