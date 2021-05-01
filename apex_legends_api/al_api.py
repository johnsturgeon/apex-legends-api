"""
Apex Legends API

| The ApexLegendsAPI wraps the api at: https://apexlegendsapi.com
| Get your API Key Here: https://apexlegendsapi.com
"""
import json
import requests
from deprecated import deprecated
from .al_domain import ALPlayer  # noqa E0402
from .al_base import ALPlatform, ALAction, ALHTTPExceptionFromResponse  # noqa E0402


class ApexLegendsAPI:
    """
    Main class that wraps the API calls
    """
    api_version: str = "5"
    base_params: dict = {'version': api_version}
    base_url: str = "https://api.mozambiquehe.re/bridge"

    def __init__(self, api_key: str):
        """ Initialize with the API Key """
        self.session: requests.Session = requests.Session()
        self.session.headers.update({'Authorization': api_key})

    def _make_request(self, additional_params: dict, new_base_url: str = None) -> list:
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

    def nametouid(self, player: str, platform: ALPlatform) -> int:
        """
        Retrieve a player's uid given they're name and platform

        :parameter player: Name of the player
        :type player: str
        :parameter platform: see [ALPlatform] for all types
        :type platform: ALPlatform
        """

        new_base_url: str = "https://api.mozambiquehe.re/nametouid?"
        additional_params = {
            'player': player,
            'platform': platform.value
        }
        result = self._make_request(additional_params=additional_params, new_base_url=new_base_url)
        assert len(result) == 1
        return result[0]['result']

    def get_player(self, name: str, platform: ALPlatform, skip_tracker_rank=False) -> ALPlayer:
        """
        Retrieve the ALPlayer object populated with data from the api.

        NOTE:
            Player must exist, method will return None if the player cannot be found

        :parameter name: Name of the player
        :type name: str
        :parameter platform: see ALPlatform for all types
        :parameter skip_tracker_rank: if set to True, this will skip fetching the legend ranks
        :return: a single player or None if no player is found
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

    def get_player_by_uid(
            self, uid: str, platform: ALPlatform, skip_tracker_rank=False
    ) -> ALPlayer:
        """
        Retrieve the ALPlayer object populated with data from the api.

        NOTE:
            Player must exist, method will return None if the player cannot be found

        :parameter uid: UID of the player
        :parameter platform: see ALPlatform for all types
        :parameter skip_tracker_rank: if set to True, this will skip fetching the legend ranks
        :return: a single player or None if no player is found
        """
        basic_player_stats: list = self.basic_player_stats_by_uid(uid, platform, skip_tracker_rank)
        assert len(basic_player_stats) == 1
        event_info: list = self.events_by_uid(
            uid=uid,
            platform=platform,
            action=ALAction.INFO
        )
        events: list = list()
        tracked_player: dict
        for tracked_player in event_info[0].get('data'):
            if uid == tracked_player.get('uid') and \
                    platform.value == tracked_player.get('platform'):
                events = self.events_by_uid(
                    uid=uid,
                    platform=platform,
                    action=ALAction.GET
                )
        return ALPlayer(basic_player_stats_data=basic_player_stats[0], events=events)

    def add_player_by_uid(self, player_uid: int, platform: ALPlatform) -> list:
        """
        Adds the given player's UUID to the list of tracked players

        :param player_uid: UUID of the player to add
        :type player_uid: int
        :param platform: ALPlatform of player to add
        :type platform: ALPlatform
        """
        return self.events_by_uid(str(player_uid), platform=platform, action=ALAction.ADD)

    def basic_player_stats(
            self, player_name: str,
            platform: ALPlatform,
            skip_tracker_rank=False) -> list:
        """
        Query the server for the given player / platform and returns a dictionary of their
        stats.
        More here: https://apexlegendsapi.com/#basic

        :param player_name: Player Name to search for
        :param platform: (see Platform enum for values)
        :param skip_tracker_rank: if set to true, this will not fetch the legend's tracker rank
        :return: List of player stats created from response json
        """
        params: dict = {'platform': platform.value, 'player': player_name}
        if skip_tracker_rank:
            params.update({'skipRank': True})
        return self._make_request(additional_params=params)

    def basic_player_stats_by_uid(
            self, uid: str,
            platform: ALPlatform,
            skip_tracker_rank=False) -> list:
        """
        Query the server for the given player / platform and returns a dictionary of their
        stats.
        More here: https://apexlegendsapi.com/#basic

        :param uid: Player UID to search for
        :param platform: (see Platform enum for values)
        :param skip_tracker_rank: if set to true, this will not fetch the legend's tracker rank
        :return: List of player stats created from response json
        """
        params: dict = {'platform': platform.value, 'uid': uid}
        if skip_tracker_rank:
            params.update({'skipRank': True})
        return self._make_request(additional_params=params)

    @deprecated(reason="use `events` instead")
    def match_history(self, player_name: str, platform: ALPlatform, action: ALAction) -> list:
        """
        .. deprecated:: 1.1.0
            use `events` instead
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
        return self._make_request(additional_params=params)

    def events_by_uid(self, uid: str, platform: ALPlatform, action: ALAction) -> list:
        """
        Query the server for the given player's UID / platform and return a list of their
        events

        NOTE:
          * Match history is only available for supporters
          * Match history must be tracked by the server otherwise this will return nothing
          * In order to add a player to be tracked, you need to call this passing 'add' action.

        :param uid: Player UID for match history
        :param platform: see Platform enum for values
        :param action: see Action enum for values
        :return: List of history created from response json
        """
        params: dict = {
            'platform': platform.value,
            'uid': uid,
            'history': 1,
            'action': action.value
        }
        return self._make_request(additional_params=params)

    def get_player_origin(self, player_name: str, show_all_hits: bool = False) -> list:
        """
        Query the server for the origin user and returns Origin UID, real username, PID and avatar
         for a given username

        :param player_name: Player Name for match history
        :param show_all_hits: True to 'search' for player (show multiple hits), default False
        :return: list of results
        """
        new_base_url: str = "https://api.mozambiquehe.re/origin?"
        new_base_url += f"&player={player_name}"
        if show_all_hits:
            new_base_url += "&showAllHits"
        return self._make_request(additional_params={}, new_base_url=new_base_url)
