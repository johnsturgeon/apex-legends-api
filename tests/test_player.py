""" unit tests for the player class """
from apex_legends_api import ApexLegendsAPI, ALAction, ALPlatform, ALPlayer  # noqa F0401
from apex_legends_api.al_domain import DataTracker, Legend, GameInfo  # noqa F0401

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


def test_basic_player_stats_by_uid(mock, basic_player_stats_response):
    player_uid = "0000000000000"
    platform = ALPlatform.PC
    player_url = f"{BASE_URL}?version={VERSION}&platform={platform.value}&uid={player_uid}"
    mock.register_uri('GET', player_url, json=basic_player_stats_response)
    response = api.basic_player_stats_by_uid(uid=player_uid, platform=platform)
    assert response[0]['global']['uid'] == player_uid


def test_basic_player_stats_skip_rank(mock, basic_player_stats_skip_rank_response):
    player_name = "Player"
    platform = ALPlatform.PC
    player_url = f"{BASE_URL}?version={VERSION}&platform={platform.value}&player={player_name}"
    player_url += "&skipRank=True"
    mock.register_uri('GET', player_url, json=basic_player_stats_skip_rank_response)
    response = api.basic_player_stats(
        player_name=player_name,
        platform=platform,
        skip_tracker_rank=True
    )
    assert response[0]['global']['name'] == player_name


def test_match_history(mock, match_history_get_response):
    player_name = "Player"
    platform = ALPlatform.PC
    action = ALAction.GET
    history_url = f"{BASE_URL}?version={VERSION}&platform={platform.value}" \
                  f"&player={player_name}" \
                  f"&history=1&action={action.value}"
    mock.register_uri('GET', history_url, json=match_history_get_response)
    response = api.events(player_name=player_name, platform=platform, action=action)
    assert response[0]['eventType'] == 'Session'
    assert response[0]['player'] == player_name


def test_match_history_by_uid(mock, match_history_get_response):
    uid = "0000000000000"
    platform = ALPlatform.PC
    action = ALAction.GET
    history_url = f"{BASE_URL}?version={VERSION}&platform={platform.value}" \
                  f"&uid={uid}" \
                  f"&history=1&action={action.value}"
    mock.register_uri('GET', history_url, json=match_history_get_response)
    response = api.events_by_uid(uid=uid, platform=platform, action=action)
    assert response[0]['eventType'] == 'Session'
    assert response[0]['uid'] == uid


def test_get_player_origin(mock, player_origin_response):
    player_name = "Player"
    player_origin_url = f'https://api.mozambiquehe.re/origin?player={player_name}'
    mock.register_uri('GET', player_origin_url, json=player_origin_response)
    response = api.get_player_origin(player_name=player_name)
    assert response[0]['name'] == player_name


def test_get_al_player(
        mock,
        basic_player_stats_response,
        match_history_get_response,
        match_history_info_response
):
    response: ALPlayer = helper_get_al_player(
        mock, basic_player_stats_response, match_history_get_response, match_history_info_response
    )
    assert isinstance(response, ALPlayer)
    assert response.global_info.name == "Player"
    assert response.events[0].action == 'leave'


def test_get_al_player_by_uid(
        mock,
        basic_player_stats_response,
        match_history_get_response,
        match_history_info_response
):
    response: ALPlayer = helper_get_al_player_by_uid(
        mock, basic_player_stats_response, match_history_get_response, match_history_info_response
    )
    assert isinstance(response, ALPlayer)
    assert response.global_info.name == "Player"
    assert response.events[0].action == 'leave'


def test_get_rank(
        mock,
        basic_player_stats_response
):
    player_name = "Player"
    platform = ALPlatform.PC
    player_url = f"{BASE_URL}?version={VERSION}&platform={platform.value}&player={player_name}"
    mock.register_uri('GET', player_url, json=basic_player_stats_response)
    response = api.basic_player_stats(player_name=player_name, platform=platform)
    assert response[0]['legends']['all']['Lifeline']['data'][0]['rank']['rankPos'] == 15763


def test_al_player_rank(
        mock,
        basic_player_stats_skip_rank_response,
        basic_player_stats_response,
        match_history_get_response,
        match_history_info_response
):
    player: ALPlayer = helper_get_al_player(
        mock, basic_player_stats_response, match_history_get_response, match_history_info_response
    )
    assert len(player.all_legends) > 0
    legend: Legend
    for legend in player.all_legends:
        if legend.name == "Lifeline":
            tracker: DataTracker = legend.data_trackers[0]
            assert tracker.tracker_rank.position == 15763

    no_rank_player: ALPlayer = helper_get_al_player(
        mock,
        basic_player_stats_skip_rank_response,
        match_history_get_response,
        match_history_info_response
    )
    assert len(no_rank_player.all_legends) > 0
    legend: Legend
    for legend in no_rank_player.all_legends:
        if legend.name == "Lifeline":
            tracker: DataTracker = legend.data_trackers[0]
            assert tracker.tracker_rank.position == -1


def test_player_response_badges_exists(
        mock,
        basic_player_stats_response
):
    player_name = "Player"
    platform = ALPlatform.PC
    player_url = f"{BASE_URL}?version={VERSION}&platform={platform.value}&player={player_name}"
    mock.register_uri('GET', player_url, json=basic_player_stats_response)
    response = api.basic_player_stats(player_name=player_name, platform=platform)
    assert 'badges' in response[0]['global']
    assert response[0]['global']['badges'][0]['name'] == "Chaos Theory Master"


def test_player_response_no_badges(
        mock,
        basic_player_stats_no_badges_response
):
    player_name = "Player"
    platform = ALPlatform.PC
    player_url = f"{BASE_URL}?version={VERSION}&platform={platform.value}&player={player_name}"
    mock.register_uri('GET', player_url, json=basic_player_stats_no_badges_response)
    response = api.basic_player_stats(player_name=player_name, platform=platform)
    assert 'badges' not in response[0]['global']


def test_al_player_badges_exist(
        mock,
        basic_player_stats_response,
        match_history_get_response,
        match_history_info_response
):
    response: ALPlayer = helper_get_al_player(
        mock, basic_player_stats_response, match_history_get_response, match_history_info_response
    )
    assert isinstance(response, ALPlayer)
    assert hasattr(response.global_info, 'badges')
    assert response.global_info.badges[0].name == "Chaos Theory Master"


def test_al_player_selected_legend_badge_category(
        mock,
        basic_player_stats_response,
        match_history_get_response,
        match_history_info_response
):
    response: ALPlayer = helper_get_al_player(
        mock, basic_player_stats_response, match_history_get_response, match_history_info_response
    )
    assert isinstance(response, ALPlayer)
    # First let's confirm that the account badge is set for the selected legend
    assert hasattr(response.selected_legend.game_info, 'badges')
    game_info: GameInfo = response.selected_legend.game_info
    assert len(game_info.badges) > 0
    assert game_info.badges[0].category == 'Account Badges'

    # Now let's confirm that the 'global' category does not exist
    assert len(response.global_info.badges) > 0
    assert not hasattr(response.global_info.badges[0], 'category')

    assert len(response.all_legends) > 0
    legend: Legend
    for legend in response.all_legends:
        if legend.name == 'Octane':
            assert len(legend.game_info.badges) > 0
            assert not hasattr(legend.game_info.badges[0], 'category')


def helper_get_al_player(
        mock,
        basic_player_stats_response,
        match_history_get_response,
        match_history_info_response,
        skip_rank=False
) -> ALPlayer:
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
    return api.get_player(name=player_name, platform=platform, skip_tracker_rank=skip_rank)


def helper_get_al_player_by_uid(
        mock,
        basic_player_stats_response,
        match_history_get_response,
        match_history_info_response,
        skip_rank=False
) -> ALPlayer:
    player_uid = "0000000000000"
    platform = ALPlatform.PC
    base_url_version = f"{BASE_URL}?version={VERSION}"
    player_url = base_url_version + f"&platform={platform.value}&uid={player_uid}"
    history_get_url = base_url_version + f"&platform={platform.value}" \
                                         f"&uid={player_uid}" \
                                         f"&history=1&action=GET"
    history_info_url = base_url_version + f"&platform={platform.value}" \
                                          f"&uid={player_uid}" \
                                          f"&history=1&action=INFO"

    mock.register_uri('GET', player_url, json=basic_player_stats_response)
    mock.register_uri('GET', history_get_url, json=match_history_get_response)
    mock.register_uri('GET', history_info_url, json=match_history_info_response)
    return api.get_player_by_uid(uid=player_uid, platform=platform, skip_tracker_rank=skip_rank)
