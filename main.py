from fetch.fetch import Fetcher
from util.triple import Triple
from util.predicate import LivesIn
from util.object import Person, Location

Fetcher.add(Triple(Person("Lukas"), LivesIn(), Location("Paderborn")))
Fetcher.print()
