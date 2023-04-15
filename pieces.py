"""This module corresponds to the pieces enum"""

from enum import Enum


class Pieces(Enum):
    """Associate a number to a piece"""

    EMPTY = 0
    WHITE_MAN = 1
    WHITE_KING = 2
    BLACK_MAN = 3
    BLACK_KING = 4
