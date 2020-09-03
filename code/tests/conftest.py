from os import environ
from pathlib import Path

from pytest import yield_fixture

import pyct

@yield_fixture
def session():
    s = pyct.Session(
        username=environ['GRIN_USERNAME'],
        password=environ['GRIN_PASSWORD']
    )
    yield s
    s.end()
