"""
al_base.py
contains some of the base / utility classes and Enums
"""
from enum import Enum

DESCRIPTION_DEPTH: int = 0


def description(obj) -> str:
    """ utility method for returning a string describing the object given """
    global DESCRIPTION_DEPTH  # noqa W0603
    DESCRIPTION_DEPTH += 1
    tabs = ""
    for _ in range(1, DESCRIPTION_DEPTH):
        tabs += "\t"
    # return_str: str = f"\n{tabs}" + type(obj).__name__ + "\n"
    return_str: str = "\n"
    for attribute_name, attribute_value in obj.__dict__.items():
        if isinstance(attribute_value, list):
            return_str += f"{tabs}{attribute_name}:"
            for inner_attribute in attribute_value:
                return_str += f"{tabs}{inner_attribute}"
        else:
            return_str += f"{tabs}{attribute_name}: {attribute_value}\n"
    DESCRIPTION_DEPTH -= 1
    return return_str


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
