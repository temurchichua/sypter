import pytest

# create a fixture for the Sypter class
@pytest.fixture
def sypter():
    from sypter.main import Sypter
    return Sypter
