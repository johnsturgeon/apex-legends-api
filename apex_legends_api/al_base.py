"""
al_base.py
contains some of the base / utility classes and Enums
"""
from enum import Enum


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
    """ Three platforms available """
    XBOX = "X1"
    PSN = "PS4"
    PC = "PC"


class ALAction(Enum):
    """ Three actions available """
    INFO = "info"  # return the players you're currently tracking
    GET = "get"  # return ALL tracked events for the player
    ADD = "add"  # adds the player for history collection
    DELETE = "delete"  # removes the given user from the tracked users list


class ALEventType(Enum):
    """ the three different event types """
    SESSION = 'Session'
    GAME = 'Game'
    LEVEL = 'Level'
