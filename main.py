from fetch.fetch import Fetcher
from transform.TextToTriple import TextToTriple

Fetcher.add(Triple(Person("Lukas"), LivesIn(), Location("Paderborn")))
Fetcher.add(Triple(Person("Dirk"), LivesIn(), Location("Paderborn")))
Fetcher.fetch()

TextToTriple.text(
    "Niclas lives in Paderborn. Dirk is born 1866").process().print()
