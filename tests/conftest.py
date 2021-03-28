import json
import pytest
import requests_mock


@pytest.fixture()
def mock():
    with requests_mock.Mocker() as mock:
        yield mock


@pytest.fixture()
def basic_player_stats_response():
    with open('tests/responses/basic_player_stats_response.json') as json_file:
        yield json.load(json_file)

