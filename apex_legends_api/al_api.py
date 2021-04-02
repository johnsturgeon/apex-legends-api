"""
Apex Legends API

The ApexLegendsAPI wraps the api at:
https://apexlegendsapi.com
    Init with your API Key (get at https://apexlegendsapi.com)
"""
import json
import requests
from .al_domain import ALPlayer  # noqa E0402
from .al_base import ALPlatform, ALAction, ALHTTPExceptionFromResponse  # noqa E0402


class ApexLegendsAPI:
    """
    Main class that wraps the API at apex
    """
    api_version = "5"
    base_url = f"https://api.mozambiquehe.re/bridge?version={api_version}"

    def __init__(self, api_key: str):
        """ Initialize with the API Key """
        self.session = requests.Session()
        self.session.headers.update({'Authorization': api_key})

    def make_request(self, endpoint: str, base_url: str = None) -> list:
        """ Send the request to the apex legends api """
        if not base_url:
            base_url = self.base_url
        url: str = base_url + endpoint
        response: requests.Response = self.session.get(url)
        response_text = {}
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

    def get_player(self, name: str, platform: ALPlatform, match_history_limit: int = None) -> ALPlayer:
        """
        Retrieve the ALPlayer object you can load all the data on init, or via
        specific calls later.

        NOTE:
            Player must exist, method will return None if the player cannot be found
        :param name: Name of the player
        :param platform: see ALPlatform for all types
        :param match_history_limit: limit for match history events list
        :return: a single player or None if no player is found
        :rtype: ALPlayer
        """
        basic_player_stats = self.basic_player_stats(name, platform)
        assert len(basic_player_stats) == 1
        match_history_info: list = self.match_history(
            player_name=name,
            platform=platform,
            action=ALAction.INFO
        )
        match_history = list()
        tracked_player: dict
        for tracked_player in match_history_info[0].get('data'):
            if name == tracked_player.get('name') and \
                    platform.value == tracked_player.get('platform'):
                match_history = self.match_history(
                    player_name=name,
                    platform=platform,
                    action=ALAction.GET,
                    limit=match_history_limit
                )
        return ALPlayer(basic_player_stats_data=basic_player_stats[0], match_history=match_history)

    def basic_player_stats(self, player_name: str, platform: ALPlatform) -> list:
        """
        Query the server for the given player / platform and returns a dictionary of their
        stats.
        More here: https://apexlegendsapi.com/#basic
        TODO: Make player_name a list since the API can accept multiple player names
        :param player_name: Player Name to search for
        :param platform: (see Platform enum for values)
        :return: List of player stats created from response json
        """
        endpoint = f"&platform={platform.value}&player={player_name}"
        return self.make_request(endpoint)

    def match_history(self, player_name: str, platform: ALPlatform, action: ALAction, limit: int = None) -> list:
        """
        Query the server for the given player / platform and return a dictionary of their
        match history

        NOTE:
          * Match history is only available for supporters
          * Match history must be tracked by the server otherwise this will return nothing
          * In order to add a player to be tracked, you need to call this passing 'add' action.

        :param player_name: Player Name for match history
        :param platform: see Platform enum for values
        :param action: see Action enum for values
        :param limit: limit amount of match history events returns
        :return: List of history created from response json
        """
        endpoint = f"&platform={platform.value}" \
                   f"&player={player_name}" \
                   f"&history=1" \
                   f"&action={action.value}"
        if limit:
            endpoint += f'&limit={limit}'
        return self.make_request(endpoint)

    def get_player_origin(self, player_name: str, show_all_hits: bool = False) -> list:
        """
        Query the server for the origin user
        Returns Origin UID, real username, PID and avatar for a given username
        :param player_name: Player Name for match history
        :param show_all_hits: True to 'search' for player (show multiple hits), default False
        :return: list of results
        """
        show_hits_string = ""
        if show_all_hits:
            show_hits_string = "&showAllHits"
        base_url = "https://api.mozambiquehe.re/origin?"
        endpoint = f"player={player_name}" \
                   f"{show_hits_string}"
        return self.make_request(base_url=base_url, endpoint=endpoint)

    def delete_all_tracked_players(self):
        """
        This will retrieve a list of all tracked players,
        and call the 'delete' api for each of them.
        Use with caution!

        NOTE:
            This action cannot be undone, proceed only if you know what you are doing
        """
        player_info_endpoint = "&history=1&action=info"
        response = self.make_request(player_info_endpoint)
        player_list = response[0]['data']
        num_players = len(player_list)
        for player in player_list:
            platform = ALPlatform(player['platform'])
            del_response = self.match_history(
                player_name=player['name'],
                platform=platform,
                action=ALAction.DELETE
            )
            new_player_list = del_response[0]['data']
            num_players -= 1
            assert len(new_player_list) == num_players
