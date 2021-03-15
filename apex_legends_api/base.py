"""
base.py
contains some of the base / utility classes and Enums
"""
from enum import Enum


class Platform(Enum):
    """ Three platforms available """
    XBOX = "X1"
    PSN = "PS4"
    PC = "PC"


class Action(Enum):
    """ Three actions available """
    INFO = "info"  # return the players you're currently tracking
    GET = "get"  # return ALL tracked events for the player
    ADD = "add"  # adds the player for history collection
    DELETE = "delete"  # removes the given user from the tracked users list
