from fetch.fetch import Fetcher
from util.triple import Triple
from util.predicate import LivesIn
from util.object import Person, Location

fetcher = Fetcher()
fetcher.add(Triple(Person("Lukas"), LivesIn(), Location("Paderborn")))
