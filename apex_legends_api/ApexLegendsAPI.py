"""
Apex Legends API

The ApexLegendsAPI wraps the api at:
https://apexlegendsapi.com
    Init with your API Key (get at https://apexlegendsapi.com)
"""

import json
import requests
from base import Platform, Action


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
        response = self.session.get(url)
        response_text = {}
        if response.status_code == 200:
            response_text = json.loads(response.text)

        # sometimes we get a pure dictionary back, let's wrap it in a list for consistency
        if isinstance(response_text, dict):
            response_text = [response_text]
        return response_text

    def basic_player_stats(self, player_name: str, platform: Platform) -> list:
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

    def match_history(self, player_name: str, platform: Platform, action: Action) -> list:
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
        :return: List of history created from response json
        """
        endpoint = f"&platform={platform.value}" \
                   f"&player={player_name}" \
                   f"&history=1" \
                   f"&action={action.value}"
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
