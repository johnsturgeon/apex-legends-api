""" configure test fixtures """
import os
import json
import pytest
import requests_mock


def get_full_filepath(test_filename):
    """ return a fully qualified file location for the test file"""
    file_path = os.path.dirname(os.path.abspath(__file__))
    return_filepath = os.path.abspath(file_path + "/responses/" + test_filename)
    return return_filepath


# pylint: disable=missing-function-docstring
@pytest.fixture()
def mock():
    with requests_mock.Mocker() as ___mock:
        yield ___mock


@pytest.fixture()
def basic_player_stats_response():
    with open(get_full_filepath('basic_player_stats_response.json')) as json_file:
        yield json.load(json_file)


@pytest.fixture()
def match_history_get_response():
    with open(get_full_filepath('match_history_get_response.json')) as json_file:
        yield json.load(json_file)


@pytest.fixture()
def match_history_info_response():
    with open(get_full_filepath('match_history_info_response.json')) as json_file:
        yield json.load(json_file)


@pytest.fixture()
def player_origin_response():
    with open(get_full_filepath('player_origin_response.json')) as json_file:
        yield json.load(json_file)
