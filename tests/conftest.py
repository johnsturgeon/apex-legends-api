""" configure test fixtures """
import json
import pytest
import requests_mock


# pylint: disable=missing-function-docstring
@pytest.fixture()
def mock():
    with requests_mock.Mocker() as ___mock:
        yield ___mock


@pytest.fixture()
def basic_player_stats_response():
    with open('tests/responses/basic_player_stats_response.json') as json_file:
        yield json.load(json_file)


@pytest.fixture()
def match_history_get_response():
    with open('tests/responses/match_history_get_response.json') as json_file:
        yield json.load(json_file)


@pytest.fixture()
def match_history_info_response():
    with open('tests/responses/match_history_info_response.json') as json_file:
        yield json.load(json_file)


@pytest.fixture()
def player_origin_response():
    with open('tests/responses/player_origin_response.json') as json_file:
        yield json.load(json_file)
