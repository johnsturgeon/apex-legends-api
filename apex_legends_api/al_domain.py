"""
Player class for the Apex Legends API Python package
"""
from .al_base import ALPlatform


class ALPlayer:
    """
    This class encapsulates the player and associated data retrieved from the API calls

    Discussion:
        The player class is intended as an encapsulated representation of the data from the api.
        To populate the values, there are convenience methods on the ApexLegendsAPI class
    """
    def __init__(self, name: str, platform: ALPlatform):
        """ Init the object with the player's name and platform """
        self._name: str = name
        self._platform: ALPlatform = platform
        self._origin_info: dict = dict()
        self._matches_tracked: bool = False

    @property
    def name(self) -> str:
        """ Returns the name of the player """
        return self._name

    @property
    def platform(self) -> ALPlatform:
        """ Returns the platform (enum) """
        return self._platform

    @property
    def origin_info(self) -> dict:
        """
        return the 'origin' info for the current user
        return dict with values set to empty strings if player is not found
        return empty dict if platform is not PC
        NOTE:
            This is for PC users only
        """
        return self._origin_info

    @origin_info.setter
    def origin_info(self, value: dict):
        """ set the origin_info dictionary """
        self._origin_info = value

    @property
    def matches_tracked(self) -> bool:
        """ Return True if the current user is being tracked by ApexLegendsAPI """
        return self._matches_tracked

    @matches_tracked.setter
    def matches_tracked(self, value: bool):
        self._matches_tracked = value
