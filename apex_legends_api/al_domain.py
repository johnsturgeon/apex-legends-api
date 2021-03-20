"""
Player class for the Apex Legends API Python package
"""
import arrow
from .al_base import ALPlatform  # noqa E0402


# pylint: disable=too-few-public-methods
class GlobalInfo:
    """ a data structure for the global player info """
    # pylint: disable=too-many-instance-attributes
    # I'm fully aware, this is a dataclass, so pylint can just get over itself
    # Definition of local data structures
    class Bans:
        """ data structure for player bans """
        def __init__(self, bans_dict: dict):
            self.reason: str = bans_dict.get('last_banReason')
            self.is_active: bool = bool(bans_dict.get('isActive'))
            self.seconds_remaining: int = bans_dict.get('remainingSeconds')

    class Rank:
        """ data structure for player rank information """
        def __init__(self, rank_dict: dict):
            self.score: int = rank_dict.get('rankScore')
            self.tier: str = rank_dict.get('rankName')
            self.division: int = rank_dict.get('rankDiv')
            self.ladder_pos_platform: int = rank_dict.get('ladderPosPlatform')
            self.image_url: str = rank_dict.get('rankImg')
            self.season: str = rank_dict.get('rankedSeason')

        @property
        def rank_division_roman(self) -> str:
            """ return the rank Division Roman Numeral representation (I II III IV) """
            div = self.division
            if div == 1:
                return "I"
            if div == 2:
                return "II"
            if div == 3:
                return "III"
            if div == 4:
                return "IV"
            return ""

    def __init__(self, global_dict: dict):
        self.name: str = global_dict.get('name')
        self.uid: int = global_dict.get('uid')
        self.avatar: str = global_dict.get('avatar')
        self.platform: ALPlatform = ALPlatform(value=global_dict.get('platform'))
        self.level: int = global_dict.get('level')
        self.to_next_level_percent: int = global_dict.get('toNextLevelPercent')
        self.bans: GlobalInfo.Bans = GlobalInfo.Bans(bans_dict=global_dict.get('bans'))
        self.rank: GlobalInfo.Rank = GlobalInfo.Rank(rank_dict=global_dict.get('rank'))


class RealtimeInfo:
    """ a data structure for the player's real time information """
    def __init__(self, realtime_dict):
        self.lobby_state: str = realtime_dict.get('lobbyState')
        self.is_online: bool = bool(realtime_dict.get('isOnline'))
        self.is_in_game: bool = bool(realtime_dict.get('isInGame'))
        self.can_join: bool = bool(realtime_dict.get('canJoin'))
        self.party_full: bool = bool(realtime_dict.get('partyFull'))
        self.selected_legend: str = realtime_dict.get('selectedLegend')

    def __str__(self):
        return f"Lobby State: {self.lobby_state}\n"\
               f"Is Online: {self.is_online}\n" \
               f"Is In Game: {self.is_in_game}\n" \
               f"Can Join: {self.can_join}\n" \
               f"Party Full: {self.party_full}\n" \
               f"Selected Legend: {self.selected_legend}\n"


class ALPlayer:
    """
    This class encapsulates the player and associated data retrieved from the API calls

    Discussion:
        The player class is intended as an encapsulated representation of the data from the api.
        To populate the values, there are convenience methods on the ApexLegendsAPI class
    """

    def __init__(self, basic_player_stats_data: dict):
        """ Init the object with the player's name and platform """
        self.global_info: GlobalInfo = GlobalInfo(global_dict=basic_player_stats_data['global'])
        self.realtime_info: RealtimeInfo = RealtimeInfo(realtime_dict=basic_player_stats_data['realtime'])
        self.matches_tracked: bool = False
        self.timestamp_last_checked: int = arrow.utcnow().int_timestamp
