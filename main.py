""" This is just a quick test module for making sure things are working """
import sys
from apex_legends_api import ApexLegendsAPI,\
    ALPlatform,\
    ALPlayer,\
    ALAction,\
    ALHTTPExceptionFromResponse

from apex_legends_api.al_base import print_description


def main():
    """ just a test method """
    api = ApexLegendsAPI(api_key='Mr9btAmjuEw9wmFQcoPW')
    player_name = 'GoshDarnedHero'
    platform = ALPlatform.PC
    action = ALAction.INFO

    # straight API calls
    try:
        basic = api.basic_player_stats(player_name=player_name, platform=platform)
        history = api.events(player_name=player_name, platform=platform, action=action)
        origin_player = api.get_player_origin(player_name=player_name, show_all_hits=True)
    except ALHTTPExceptionFromResponse as exception:
        print(exception)
        sys.exit()

    print(basic)
    print(history)
    print(origin_player)
    try:
        player: ALPlayer = api.get_player(name=player_name, platform=platform)
    except ALHTTPExceptionFromResponse as exception:
        print(exception)
        return

    print_description(player)
    # print(player.selected_legend)
    # for legend in player.all_legends:
    #     print(legend)
    # print(player.origin_info)
    # print(player.matches_tracked)


if __name__ == "__main__":
    main()
