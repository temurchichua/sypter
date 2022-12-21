import pytest
from src.sypter import Sypter


# create a fixture for the Sypter class
@pytest.fixture
def sypter():
    yield Sypter()
