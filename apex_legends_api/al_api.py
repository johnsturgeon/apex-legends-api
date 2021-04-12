"""
Apex Legends API

The ApexLegendsAPI wraps the api at:
https://apexlegendsapi.com
    Init with your API Key (get at https://apexlegendsapi.com)
"""
import json
import requests
from deprecated import deprecated
from .al_domain import ALPlayer  # noqa E0402
from .al_base import ALPlatform, ALAction, ALHTTPExceptionFromResponse  # noqa E0402


class ApexLegendsAPI:
    """
    Main class that wraps the API at apex
    """
    api_version: str = "5"
    base_params: dict = {'version': api_version}
    base_url: str = "https://api.mozambiquehe.re/bridge"

    def __init__(self, api_key: str):
        """ Initialize with the API Key """
        self.session: requests.Session = requests.Session()
        self.session.headers.update({'Authorization': api_key})

    def make_request(self, additional_params: dict, new_base_url: str = None) -> list:
        """ Send the request to the apex legends api """
        if new_base_url:
            url: str = new_base_url
            params: dict = additional_params
        else:
            url: str = self.base_url
            params: dict = dict(self.base_params, **additional_params)
        response: requests.Response = self.session.get(url, params=params)
        if response.status_code == 200:
            try:
                response_text = json.loads(response.text)
            except ValueError:
                response_text = response.text
        else:
            raise ALHTTPExceptionFromResponse(response)

        # sometimes we get a pure dictionary back, let's wrap it in a list for consistency
        if isinstance(response_text, dict):
            response_text = [response_text]
        return response_text

    def get_player(self, name: str, platform: ALPlatform, skip_tracker_rank=False) -> ALPlayer:
        """
        Retrieve the ALPlayer object populated with data from the api.

        NOTE:
            Player must exist, method will return None if the player cannot be found
        :param name: Name of the player
        :param platform: see ALPlatform for all types
        :param skip_tracker_rank: if set to True, this will skip fetching the legend ranks
        :return: a single player or None if no player is found
        :rtype: ALPlayer
        """
        basic_player_stats: list = self.basic_player_stats(name, platform, skip_tracker_rank)
        assert len(basic_player_stats) == 1
        event_info: list = self.events(
            player_name=name,
            platform=platform,
            action=ALAction.INFO
        )
        events: list = list()
        tracked_player: dict
        for tracked_player in event_info[0].get('data'):
            if name == tracked_player.get('name') and \
                    platform.value == tracked_player.get('platform'):
                events = self.events(
                    player_name=name,
                    platform=platform,
                    action=ALAction.GET
                )
        return ALPlayer(basic_player_stats_data=basic_player_stats[0], events=events)

    def basic_player_stats(
            self, player_name: str,
            platform: ALPlatform,
            skip_tracker_rank=False) -> list:
        """
        Query the server for the given player / platform and returns a dictionary of their
        stats.
        More here: https://apexlegendsapi.com/#basic
        TODO: Make player_name a list since the API can accept multiple player names
        :param player_name: Player Name to search for
        :param platform: (see Platform enum for values)
        :param skip_tracker_rank: if set to true, this will not fetch the legend's tracker rank
        :return: List of player stats created from response json
        """
        params: dict = {'platform': platform.value, 'player': player_name}
        if skip_tracker_rank:
            params.update({'skipRank': True})
        return self.make_request(additional_params=params)

    @deprecated(reason="use `events` instead")
    def match_history(self, player_name: str, platform: ALPlatform, action: ALAction) -> list:
        """
        Query the server for the given player / platform and return a list of their
        events

        NOTE:
          * Match history is only available for supporters
          * Match history must be tracked by the server otherwise this will return nothing
          * In order to add a player to be tracked, you need to call this passing 'add' action.

        :param player_name: Player Name for match history
        :param platform: see Platform enum for values
        :param action: see Action enum for values
        :return: List of history created from response json
        """
        return self.events(player_name=player_name, platform=platform, action=action)

    def events(self, player_name: str, platform: ALPlatform, action: ALAction) -> list:
        """
        Query the server for the given player / platform and return a list of their
        events

        NOTE:
          * Match history is only available for supporters
          * Match history must be tracked by the server otherwise this will return nothing
          * In order to add a player to be tracked, you need to call this passing 'add' action.

        :param player_name: Player Name for match history
        :param platform: see Platform enum for values
        :param action: see Action enum for values
        :return: List of history created from response json
        """
        params: dict = {
            'platform': platform.value,
            'player': player_name,
            'history': 1,
            'action': action.value
        }
        return self.make_request(additional_params=params)

    def get_player_origin(self, player_name: str, show_all_hits: bool = False) -> list:
        """
        Query the server for the origin user
        Returns Origin UID, real username, PID and avatar for a given username
        :param player_name: Player Name for match history
        :param show_all_hits: True to 'search' for player (show multiple hits), default False
        :return: list of results
        """
        new_base_url: str = "https://api.mozambiquehe.re/origin?"
        new_base_url += f"&player={player_name}"
        if show_all_hits:
            new_base_url += "&showAllHits"
        return self.make_request(new_base_url=new_base_url, additional_params={})

    def delete_all_tracked_players(self):
        """
        This will retrieve a list of all tracked players,
        and call the 'delete' api for each of them.
        Use with caution!

        NOTE:
            This action cannot be undone, proceed only if you know what you are doing
        """
        params: dict = {'history': 1, 'action': 'info'}
        response: list = self.make_request(additional_params=params)
        player_list: list = response[0]['data']
        num_players: int = len(player_list)
        player: dict
        for player in player_list:
            platform: ALPlatform = ALPlatform(player['platform'])
            del_response: list = self.events(
                player_name=player['name'],
                platform=platform,
                action=ALAction.DELETE
            )
            new_player_list: list = del_response[0]['data']
            num_players -= 1
            assert len(new_player_list) == num_players
