from os import environ, system
from pathlib import Path

from pytest import yield_fixture

# compile the adapter before testing
system("msbuild /src/cs/PyCT")

import pyct

@yield_fixture
def session():
    s = pyct.Session(
        username=environ['GRIN_USER'],
        password=environ['GRIN_PASSWORD']
    )
    yield s
    s.end()
