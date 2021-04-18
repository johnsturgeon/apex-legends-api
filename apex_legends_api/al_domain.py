"""
Player class for the Apex Legends API Python package
"""
import arrow
from .al_base import ALEventType, ALPlatform  # noqa E0402


# pylint: disable=too-few-public-methods
class GameInfo:
    """
    Data structure for game information for selected legend

    Example:
        - skin=Extreme Measures
        - frame=Fuel Injected
        - pose=Spin and Flick
        - intro=Run fast, hit fast, win fast
    """
    class Badge:
        """ data structure for badges """
        def __init__(self, badge_dict: dict):
            self.name: str = badge_dict.get('name')
            """ Name of the badge """
            self.value: str = badge_dict.get('value')
            """ Value of the badge """
            if badge_dict.get('category'):
                self.category: str = badge_dict.get('category')
                """
                Category of the badge

                Note:
                    - This is either 'Account Badges' for account level badge, or the legend name
                """

    def __init__(self, game_info_dict: dict):
        if game_info_dict.get('skin'):
            self.skin: str = game_info_dict.get('skin')
            """ Skin on the current legend """
        if game_info_dict.get('frame'):
            self.frame: str = game_info_dict.get('frame')
            """ Frame chosen for the current legend """
        if game_info_dict.get('pose'):
            self.pose: str = game_info_dict.get('pose')
            """ Pose of the current legend """
        if game_info_dict.get('intro'):
            self.intro: str = game_info_dict.get('intro')
            """ Intro quip of the current legend """
        self.badges: list[GameInfo.Badge] = list()
        """ Currently selected 'badges' for the current legend """
        for badge in game_info_dict.get('badges'):
            self.badges.append(GameInfo.Badge(badge))


class Event:
    """ Parent class for apex-legend events """
    def __init__(self, event_dict: dict):
        self.uid: int = event_dict.get('uid')
        """ Origin / EA UUID of the player """
        self.player: str = event_dict.get('player')
        """ Player nick name """
        self.timestamp: int = event_dict.get('timestamp')
        """ UTC Timestamp for the END of the event (game end for example) """
        self.event_type: ALEventType = ALEventType(value=event_dict.get('eventType'))
        """ One of various event types (see: ALEventType) """


class GameEvent(Event):
    """ Event sub class for 'game' events """
    def __init__(self, event_dict: dict):
        super().__init__(event_dict)
        self.xp_progress: int = event_dict.get('xpProgress')
        """ XP progress to next level """
        self.game_length: int = event_dict.get('gameLength')
        """ game length (in minutes) """
        self.legend_played: str = event_dict.get('legendPlayed')
        """ Which legend was played in this game """
        self.rank_score_change: str = event_dict.get('rankScoreChange')
        """ Rank Score Change (if any) """
        self.game_data_trackers: list[DataTracker] = list()
        """ List of DataTrackers that had values in this game """
        tracker: dict
        for tracker in event_dict.get('event'):
            self.game_data_trackers.append(DataTracker(tracker))


class SessionEvent(Event):
    """ event subclass for "session" events (leave / join) """
    def __init__(self, event_dict: dict):
        super().__init__(event_dict)
        event_detail: dict = event_dict.get('event')
        self.action: str = event_detail.get('action')
        """ string of action 'leave' 'join' """
        if self.action == 'leave':
            self.session_duration: int = event_detail.get('sessionDuration')
        else:
            self.session_duration: int = 0


class LevelEvent(Event):
    """ event subclass for 'level' events (level up) """
    def __init__(self, event_dict: dict):
        super().__init__(event_dict)
        self.new_level = event_dict.get('event').get('newLevel')
        """ The new level achieved """


class RankEvent(Event):
    """ event subclass for 'rank' events (ranked progression)"""
    def __init__(self, event_dict: dict):
        super().__init__(event_dict)
        self.new_rank: str = event_dict.get('event').get('newRank')
        """ The new rank achieved """


def event_factory(event_dict: dict) -> Event:
    """ a factory method for the different event types"""
    event_classes = {
        "Session": SessionEvent,
        "Level": LevelEvent,
        "Game": GameEvent,
        "Rank": RankEvent
    }
    return event_classes[event_dict.get('eventType')](event_dict)


class GlobalInfo:
    """ a data structure for the global player info """
    # pylint: disable=too-many-instance-attributes
    # I'm fully aware, this is a dataclass, so pylint can just get over itself
    # Definition of local data structures
    class Bans:
        """ data structure for player bans """
        def __init__(self, bans_dict: dict):
            self.reason: str = bans_dict.get('last_banReason')
            """ Reason of last ban (still has value even when ban is over) """
            self.is_active: bool = bool(bans_dict.get('isActive'))
            """ True if ban is currently active """
            self.seconds_remaining: int = bans_dict.get('remainingSeconds')
            """ Remaining time (in seconds) of current ban """

    class Rank:
        """ data structure for player rank information """
        def __init__(self, rank_dict: dict):
            self.score: int = rank_dict.get('rankScore')
            """ Current rank score """
            self.tier: str = rank_dict.get('rankName')
            """ Rank Tier (Bronze, Gold, etc...) """
            self.division: int = rank_dict.get('rankDiv')
            """ Rank Division (I, II, etc...) """
            self.ladder_pos_platform: int = rank_dict.get('ladderPosPlatform')
            """ Ladder rank for Apex Predators, will show -1 for others """
            self.image_url: str = rank_dict.get('rankImg')
            """ Image icon for current rank """
            self.season: str = rank_dict.get('rankedSeason')
            """ season / split for current rank (ex: season08_split_2) """

        @property
        def rank_division_roman(self) -> str:
            """ return the rank Division Roman Numeral representation (I II III IV) """
            div: int = self.division
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
        """ Player Nick Name """
        self.uid: int = global_dict.get('uid')
        """ Player UID (guaranteed unique) """
        self.avatar: str = global_dict.get('avatar')
        """ Player Origin /EA Avatar """
        self.platform: ALPlatform = ALPlatform(value=global_dict.get('platform'))
        """ Platform (PC, XBOX, etc...) """
        self.level: int = global_dict.get('level')
        """ Current level of the player """
        self.to_next_level_percent: int = global_dict.get('toNextLevelPercent')
        """ Percent progress to next level (1-100) """
        self.bans: GlobalInfo.Bans = GlobalInfo.Bans(bans_dict=global_dict.get('bans'))
        """ Active / latest ban data """
        self.rank: GlobalInfo.Rank = GlobalInfo.Rank(rank_dict=global_dict.get('rank'))
        """ Current rank detail """
        self.badges: list[GameInfo.Badge] = list()
        if global_dict.get('badges'):
            for badge in global_dict.get('badges'):
                self.badges.append(GameInfo.Badge(badge_dict=badge))


class RealtimeInfo:
    """ a data structure for the player's real time information """
    def __init__(self, realtime_dict: dict):
        self.lobby_state: str = realtime_dict.get('lobbyState')
        """ open if lobby is open """
        self.is_online: bool = bool(realtime_dict.get('isOnline'))
        """ True if player is currently online """
        self.is_in_game: bool = bool(realtime_dict.get('isInGame'))
        """ True if player is currently in a game """
        self.can_join: bool = bool(realtime_dict.get('canJoin'))
        """ True if player can join party """
        self.party_full: bool = bool(realtime_dict.get('partyFull'))
        """ True if the player's party is full """
        self.selected_legend: str = realtime_dict.get('selectedLegend')
        """ Currently selected legend in the lobby """


class DataTracker:
    """
    Data structure for badges

    Note:
        if the tracker's rank is not available, and empty dictionary will be used
    """
    class TrackerRank:
        """ Data structure for the rank for the stat being tracked """
        def __init__(self, tracker_rank_dict: dict):
            self.position: int = tracker_rank_dict.get('rankPos')
            """ Position of rank """
            self.percent: float = float(tracker_rank_dict.get('topPercent'))
            """ Percentile of rank (lower number is better) """

    def __init__(self, data_trackers_dict: dict):
        self.name: str = data_trackers_dict.get('name')
        """ Descriptive name of the tracker """
        self.value: int = data_trackers_dict.get('value')
        """ Numerical value of the tracker """
        self.key: str = data_trackers_dict.get('key')
        """ Unique 'key' for the tracker """
        self.category: str = self.key.lstrip('specialEvent_')
        """
        Aggregate key for combining 'specialEvent' data with regular data

        Note:
            Special Event data is the same as regular but has a different key for
            statistical purposes it makes sense to just drop the 'specialEvent' prefix.
        """
        rank_dict: dict = data_trackers_dict.get('rank')
        if not rank_dict:
            rank_dict = {'rankPos': -1, 'topPercent': -1.0}
        else:
            rank_dict = data_trackers_dict.get('rank')
        self.tracker_rank = DataTracker.TrackerRank(tracker_rank_dict=rank_dict)
        """
        Rank of the stat for this legend

        Note:
            * Values are -1 if they were not part of the API query
        """


class ImgAsset:
    """ data structure for image assets """
    def __init__(self, image_asset_dict: dict):
        self.icon: str = image_asset_dict.get('icon')
        """ URL to the icon of the image """
        self.banner: str = image_asset_dict.get('banner')
        """ URL to the banner of the image """


class Legend:
    """ data structure for a player's legend legend """
    def __init__(self, legend_name: str, legend_dict: dict):
        self.name: str = legend_name
        """ Legend name """
        self.data_trackers: list[DataTracker] = list()
        """ list of all known data trackers for the legend """
        if legend_dict.get('data'):
            data_tracker: dict
            for data_tracker in legend_dict.get('data'):
                self.data_trackers.append(DataTracker(data_tracker))
        self.img_assets: ImgAsset = ImgAsset(legend_dict.get('ImgAssets'))
        """ urls to icons / banner images"""
        if legend_dict.get('gameInfo'):
            self.game_info: GameInfo = GameInfo(legend_dict.get('gameInfo'))
            """ GameInfo for the legend """


class ALPlayer:
    """
    This class encapsulates the player and associated data retrieved from the API calls

    Discussion:
        The player class is intended as an encapsulated representation of the data from the api.
        To populate the values, there are convenience methods on the ApexLegendsAPI class
    """

    def __init__(self, basic_player_stats_data: dict, events: list = None):
        """ Init the object with the player's name and platform """
        self.global_info: GlobalInfo = GlobalInfo(global_dict=basic_player_stats_data['global'])
        """ Contains all the global info for the player """
        self.realtime_info: RealtimeInfo = RealtimeInfo(
            realtime_dict=basic_player_stats_data['realtime']
        )
        """ Contains the RealtimeInfo for the player """
        self.timestamp_last_checked: int = arrow.utcnow().int_timestamp
        """ Contains the timestamp that the player was created / data loaded """
        self.selected_legend: Legend = Legend(
            legend_name=basic_player_stats_data['legends']['selected']['LegendName'],
            legend_dict=basic_player_stats_data['legends']['selected']
        )
        """ Currently Selected Legend """
        self.all_legends: list[Legend] = list()
        """ List of all legends (and their stats) """
        for legend_name, legend_dict in basic_player_stats_data['legends']['all'].items():
            self.all_legends.append(Legend(legend_name=legend_name, legend_dict=legend_dict))
        self.events: list = list()
        """ List of all matches / events"""
        if events:
            event: dict
            for event in events:
                event_result = event_factory(event_dict=event)
                self.events.append(event_result)
