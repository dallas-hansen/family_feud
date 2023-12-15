import pytest
from main import Family


@pytest.fixture
def team():
    team1 = Family("Tester")
    return team1


def test_if_adding_strike_works(team):
    team.add_strike()
    assert team.strikes == 1