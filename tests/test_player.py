from apex_legends_api import ApexLegendsAPI, ALAction, ALPlatform, ALPlayer

api = ApexLegendsAPI(api_key='api_key')
base_url = ApexLegendsAPI.base_url
version = ApexLegendsAPI.api_version


def test_basic_player_stats(mock, basic_player_stats_response):
    player_name = "Player"
    platform = ALPlatform.PC
    player_url = base_url.format(version) + f"&platform={platform.value}&player={player_name}"
    mock.register_uri('GET', player_url, json=basic_player_stats_response)
    response = api.basic_player_stats(player_name=player_name, platform=platform)
    assert response[0]['global']['name'] == player_name
