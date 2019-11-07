from fetch.fetch import Fetcher
from util.triple import Triple
from util.predicate import LivesIn
from util.object import Person, Location

TYPE_CHECKING = True

Fetcher.add(Triple(Person("Lukas"), LivesIn(), Location("Paderborn")))
Fetcher.add(Triple(Person("Dirk"), LivesIn(), Location("Paderborn")))
Fetcher.fetch()
