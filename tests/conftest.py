import pytest
from src import Sypter


# create a fixture for the Sypter class
@pytest.fixture
def sypter():
    return Sypter()
