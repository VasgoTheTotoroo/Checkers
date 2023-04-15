"""This is the main module of the game"""

from player import Player
from window import Window


def main():
    """Launch the game"""

    first_player: Player = Player(True, "Vassia")
    second_player: Player = Player(False, "Arnaud")

    Window()


if __name__ == "__main__":
    main()
