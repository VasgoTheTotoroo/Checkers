"""This module implements the Player class"""


class Player:
    """This class represents a player (AI or human)"""

    def __init__(self, is_white: bool, name: str = "player"):
        self.name: str = name
        self.score: int = 0
        self.is_white: bool = is_white
