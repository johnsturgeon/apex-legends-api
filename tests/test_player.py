""" unit tests for the player class """
from apex_legends_api import ApexLegendsAPI, ALAction, ALPlatform, ALPlayer

api = ApexLegendsAPI(api_key='api_key')
BASE_URL = ApexLegendsAPI.base_url
VERSION = ApexLegendsAPI.api_version


# pylint: disable=missing-function-docstring
def test_basic_player_stats(mock, basic_player_stats_response):
    player_name = "Player"
    platform = ALPlatform.PC
    player_url = f"{BASE_URL}?version={VERSION}&platform={platform.value}&player={player_name}"
    mock.register_uri('GET', player_url, json=basic_player_stats_response)
    response = api.basic_player_stats(player_name=player_name, platform=platform)
    assert response[0]['global']['name'] == player_name


def test_match_history(mock, match_history_get_response):
    player_name = "Player"
    platform = ALPlatform.PC
    action = ALAction.GET
    history_url = f"{BASE_URL}?version={VERSION}&platform={platform.value}" \
                  f"&player={player_name}" \
                  f"&history=1&action={action.value}"
    mock.register_uri('GET', history_url, json=match_history_get_response)
    response = api.match_history(player_name=player_name, platform=platform, action=action)
    assert response[0]['eventType'] == 'Session'


def test_get_player_origin(mock, player_origin_response):
    player_name = "Player"
    player_origin_url = f'https://api.mozambiquehe.re/origin?player={player_name}'
    mock.register_uri('GET', player_origin_url, json=player_origin_response)
    response = api.get_player_origin(player_name=player_name)
    assert response[0]['name'] == player_name


def test_get_player(
        mock,
        basic_player_stats_response,
        match_history_get_response,
        match_history_info_response
):
    player_name = "Player"
    platform = ALPlatform.PC
    base_url_version = f"{BASE_URL}?version={VERSION}"
    player_url = base_url_version + f"&platform={platform.value}&player={player_name}"
    history_get_url = base_url_version + f"&platform={platform.value}" \
                                         f"&player={player_name}" \
                                         f"&history=1&action=GET"
    history_info_url = base_url_version + f"&platform={platform.value}" \
                                          f"&player={player_name}" \
                                          f"&history=1&action=INFO"
    mock.register_uri('GET', player_url, json=basic_player_stats_response)
    mock.register_uri('GET', history_get_url, json=match_history_get_response)
    mock.register_uri('GET', history_info_url, json=match_history_info_response)
    response = api.get_player(name=player_name, platform=platform)
    assert isinstance(response, ALPlayer)
    assert response.global_info.name == player_name
    assert response.match_history[0].action == 'leave'
