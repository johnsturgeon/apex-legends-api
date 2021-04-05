"""
al_base.py
contains some of the base / utility classes and Enums
"""
from enum import Enum
import requests


def print_description(___class, indent=0, hide_values=False):
    """ prints the schema for the current object """
    print(' ' * indent + type(___class).__name__ + ':')
    indent += 4
    for k, value in ___class.__dict__.items():
        if not isinstance(value, list):
            v_list = [value]
        else:
            v_list = value
        for val in v_list:
            if '__dict__' in dir(val):
                print_description(val, indent)
            else:
                if hide_values:
                    print(' ' * indent + k)
                else:
                    print(' ' * indent + k + ': ' + str(val))


class ALPlatform(Enum):
    """
    Three platforms available
    - XBOX
    - PSN
    - PC
    """
    XBOX = "X1"
    """ Xbox """
    PSN = "PS4"
    """ Playstation (any) """
    PC = "PC"
    """ PC """


class ALAction(Enum):
    """
    Three actions available
    - INFO Return the players you're currently tracking
    - GET Return ALL tracked events for the player
    - ADD Adds the player for history collection
    - DELETE Removes the given user from the tracked users list
    """
    INFO = "info"
    """ Return the players you're currently tracking """
    GET = "get"
    """ Return ALL tracked events for the player """
    ADD = "add"
    """ Adds the player for history collection """
    DELETE = "delete"
    """ Removes the given user from the tracked users list """


class ALEventType(Enum):
    """
    The four different event types
      - SESSION
      - GAME
      - LEVEL
      - RANK
    """
    SESSION = 'Session'
    """ Session event (leave, join) """
    GAME = 'Game'
    """ Game event """
    LEVEL = 'Level'
    """ Level Up event """
    RANK = 'Rank'
    """ Rank change event """


class ALHTTPExceptionFromResponse(Exception):
    """ Exception raised for errors in the http request. """
    def __init__(self, response: requests.Response):
        self.message = f'Return Code: {response.status_code} - {response.text}'
        super().__init__(self.message)
