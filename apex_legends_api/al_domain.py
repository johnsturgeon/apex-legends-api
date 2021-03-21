"""
Player class for the Apex Legends API Python package
"""
import arrow
from .al_base import ALPlatform, description  # noqa E0402


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

        def __str__(self):
            return description(self)

    class Rank:
        """ data structure for player rank information """
        def __init__(self, rank_dict: dict):
            self.score: int = rank_dict.get('rankScore')
            self.tier: str = rank_dict.get('rankName')
            self.division: int = rank_dict.get('rankDiv')
            self.ladder_pos_platform: int = rank_dict.get('ladderPosPlatform')
            self.image_url: str = rank_dict.get('rankImg')
            self.season: str = rank_dict.get('rankedSeason')

        def __str__(self):
            return description(self)

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

    def __str__(self):
        return description(self)


class RealtimeInfo:
    """ a data structure for the player's real time information """
    def __init__(self, realtime_dict: dict):
        self.lobby_state: str = realtime_dict.get('lobbyState')
        self.is_online: bool = bool(realtime_dict.get('isOnline'))
        self.is_in_game: bool = bool(realtime_dict.get('isInGame'))
        self.can_join: bool = bool(realtime_dict.get('canJoin'))
        self.party_full: bool = bool(realtime_dict.get('partyFull'))
        self.selected_legend: str = realtime_dict.get('selectedLegend')

    def __str__(self):
        return description(self)


class DataTrackers:
    """ data structure for badges """
    def __init__(self, data_trackers_dict: dict):
        self.name = data_trackers_dict.get('name')
        self.value = data_trackers_dict.get('value')
        self.key = data_trackers_dict.get('key')

    def __str__(self):
        return description(self)


class ImgAssets:
    """ data structure for image assets """
    def __init__(self, image_asset_dict: dict):
        self.icon = image_asset_dict.get('icon')
        self.banner = image_asset_dict.get('banner')

    def __str__(self):
        return description(self)


class SelectedLegend:
    """ a data structure for the player's selected legend """
    class GameInfo:
        """ data structure for game information for selected legend """
        class Badge:
            """ data structure for badges """
            def __init__(self, badge_dict: dict):
                self.name = badge_dict.get('name')
                self.value = badge_dict.get('value')

            def __str__(self):
                return description(self)

        def __init__(self, game_info_dict: dict):
            self.skin = game_info_dict.get('skin')
            self.frame = game_info_dict.get('frame')
            self.pose = game_info_dict.get('pose')
            self.intro = game_info_dict.get('intro')
            self.badges = list()
            for badge in game_info_dict.get('badges'):
                self.badges.append(SelectedLegend.GameInfo.Badge(badge))

        def __str__(self):
            return description(self)

    def __init__(self, selected_legend_dict: dict):
        self.legend_name = selected_legend_dict.get('LegendName')
        self.data_trackers = list()
        for data_tracker in selected_legend_dict.get('data'):
            self.data_trackers.append(DataTrackers(data_tracker))
        self.game_info = SelectedLegend.GameInfo(selected_legend_dict.get('gameInfo'))
        self.img_assets = ImgAssets(selected_legend_dict.get('ImgAssets'))

    def __str__(self):
        return description(self)


class Legend:
    """ data structure for NON selected legend """
    def __init__(self, legend_name: str, legend_dict: dict):
        self.name = legend_name
        self.data_trackers = list()
        if legend_dict.get('data'):
            for data_tracker in legend_dict.get('data'):
                self.data_trackers.append(DataTrackers(data_tracker))
        self.img_assets = ImgAssets(legend_dict.get('ImgAssets'))

    def __str__(self):
        return description(self)


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
        self.selected_legend: SelectedLegend = SelectedLegend(
            selected_legend_dict=basic_player_stats_data['legends']['selected']
        )
        self.all_legends: list[Legend] = list()
        for legend_name, legend_dict in basic_player_stats_data['legends']['all'].items():
            self.all_legends.append(Legend(legend_name=legend_name, legend_dict=legend_dict))

    def __str__(self):
        return description(self)
