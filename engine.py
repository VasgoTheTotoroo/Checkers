"""This module implement the CheckerEngine class"""

import numpy as np

from pieces import Pieces


def clear_kth_bit(number: int, k: int) -> int:
    """Clear the k-th bit in n (set it to 0)"""
    return number & ~(1 << k)


def set_kth_bit(number: int, k: int) -> int:
    """Set the k-th bit in n to 1"""
    return number | (1 << k)


def check_kth_bit(number: int, k: int) -> bool:
    """Check if the k-th bit is 1"""
    return number & (1 << k)


class CheckerEngine:
    """The engine of the game"""

    def __init__(self):
        """Init the game"""

        self.size = 10
        self.nb_squares = (self.size + 1) * (self.size + 1)
        self.white_man: int = 0
        self.white_king: int = 0

        self.black_man: int = 0
        self.black_king: int = 0

        self.conversion_table: np.ndarray = self.create_conversion_table_to_idx()
        self.matching_index: np.ndarray = self.create_matching_index()
        self.edges: np.ndarray = self.get_edge_squares()

        self.set_new_game()

    def set_new_game(self):
        """Initialize a new game"""

        self.white_king = 1 << 27
        self.white_man = (
            1 << 30
            | 1 << 31
            | 1 << 32
            | 1 << 33
            | 1 << 34
            | 1 << 35
            | 1 << 36
            | 1 << 37
            | 1 << 38
            | 1 << 39
            | 1 << 40
            | 1 << 41
            | 1 << 42
            | 1 << 43
            | 1 << 44
            | 1 << 45
            | 1 << 46
            | 1 << 47
            | 1 << 48
            | 1 << 49
        )

        self.black_king = 1 << 22
        self.black_man = (
            1 << 0
            | 1 << 1
            | 1 << 2
            | 1 << 3
            | 1 << 4
            | 1 << 5
            | 1 << 6
            | 1 << 7
            | 1 << 8
            | 1 << 9
            | 1 << 10
            | 1 << 11
            | 1 << 12
            | 1 << 13
            | 1 << 14
            | 1 << 15
            | 1 << 16
            | 1 << 17
            | 1 << 18
            | 1 << 19
        )

    def is_game_ended(self) -> bool:
        """Return true if the game is finished"""

        return False

    def has_piece_on_square(self, square_idx: int) -> bool:
        """Return true if there is a piece on the square index"""

        return (
            check_kth_bit(self.white_man, square_idx)
            or check_kth_bit(self.white_king, square_idx)
            or check_kth_bit(self.black_man, square_idx)
            or check_kth_bit(self.black_king, square_idx)
        )

    def update_board(
        self,
        init_coord: tuple[int, int],
        new_coord: tuple[int, int],
        is_white: bool,
        is_king: bool,
    ) -> int:
        """update the piece coordinates"""

        old_square_idx: int = int(self.conversion_table[init_coord[1], init_coord[0]])
        new_square_idx: int = int(self.conversion_table[new_coord[1], new_coord[0]])
        if new_square_idx < 0 or self.has_piece_on_square(new_square_idx):
            return -1

        if is_white and is_king:
            self.white_king = clear_kth_bit(number=self.white_king, k=old_square_idx)
            self.white_king = set_kth_bit(number=self.white_king, k=new_square_idx)

        if is_white and not is_king:
            self.white_man = clear_kth_bit(number=self.white_man, k=old_square_idx)
            self.white_man = set_kth_bit(number=self.white_man, k=new_square_idx)

        if not is_white and not is_king:
            self.black_man = clear_kth_bit(number=self.black_man, k=old_square_idx)
            self.black_man = set_kth_bit(number=self.black_man, k=new_square_idx)

        if not is_white and is_king:
            self.black_king = clear_kth_bit(number=self.black_king, k=old_square_idx)
            self.black_king = set_kth_bit(number=self.black_king, k=new_square_idx)
        return 1

    def get_moves_for_piece(
        self,
        coord: tuple[int, int],
        is_white: bool,
        is_king: bool,
    ) -> list:
        """Return the possible moves for a piece"""

        square_idx: int = int(self.conversion_table[coord[1], coord[0]])

        moves = []

        coef: int = 1
        if not is_white:
            coef = -1

        offset: int = -1
        if coord[0] % 2 == 1:
            offset = 1

        man_potential_square_left: int = square_idx - coef * (self.size // 2)
        man_potential_square_right: int = man_potential_square_left + offset

        # regular moves for men
        if not is_king and not self.has_piece_on_square(man_potential_square_left):
            moves.append(man_potential_square_left)
        if (
            not is_king
            and square_idx not in self.edges
            and not self.has_piece_on_square(man_potential_square_right)
        ):
            moves.append(man_potential_square_right)

        # regular moves for kings

        # take for men

        # take for kings

        return moves

    def get_edge_squares(self) -> np.ndarray:
        """Get the left and right edges square"""

        return np.asarray(
            [
                np.arange(self.size // 2, (self.size * self.size) // 2, self.size),
                np.arange(
                    (self.size // 2) - 1, (self.size * self.size) // 2, self.size
                ),
            ]
        )

    def create_conversion_table_to_idx(self) -> np.ndarray:
        """Create a 2d np array corresponding to the index of the square to convert the position.
        -1 otherwise in the table.
        looks like [[-1  0 -1  1 -1  2 -1  3 -1  4]
                    [ 5 -1  6 -1  7 -1  8 -1  9 -1]
                    [-1 10 -1 11 -1 12 -1 13 -1 14]
                    [15 -1 16 -1 17 -1 18 -1 19 -1]
                    [-1 20 -1 21 -1 22 -1 23 -1 24]
                    [25 -1 26 -1 27 -1 28 -1 29 -1]
                    [-1 30 -1 31 -1 32 -1 33 -1 34]
                    [35 -1 36 -1 37 -1 38 -1 39 -1]
                    [-1 40 -1 41 -1 42 -1 43 -1 44]
                    [45 -1 46 -1 47 -1 48 -1 49 -1]] for a checkers of 10x10"""

        matching_index = np.ones((self.size, self.size), np.int8) * -1
        idx: int = 0

        for i in range(0, self.size):
            for j in range(0, self.size, 2):
                if i % 2 == 0:
                    matching_index[i, j + 1] = idx
                else:
                    matching_index[i, j] = idx
                idx += 1
        return matching_index

    def create_matching_index(self) -> np.ndarray:
        """Create a 2d np array corresponding to the square indexes in the board.
        Looks like [ 1  3  5  7  9 10 12 14 16 18 21 23 25 27 29 30 32 34 36 38 41 43 45 47
                    49 50 52 54 56 58 61 63 65 67 69 70 72 74 76 78 81 83 85 87 89 90 92 94
                    96 98] for a 10x10 board"""

        matching_index = []
        for i in range(0, self.size):
            for j in range(0, self.size, 2):
                if i % 2 == 0:
                    matching_index.append(j + 1 + i * self.size)
                else:
                    matching_index.append(j + i * self.size)
        matching_index = np.asarray(matching_index)

        return matching_index

    def get_position_array(self) -> np.ndarray:
        """return the actual position in an array
        1 is for white man
        2 is for white king
        3 is for black man
        4 is for black king"""

        white_man_array = Pieces.WHITE_MAN.value * (
            np.fromstring(np.binary_repr(self.white_man, width=50), np.int8) - 48
        )
        white_king_array = Pieces.WHITE_KING.value * (
            np.fromstring(np.binary_repr(self.white_king, width=50), np.int8) - 48
        )

        black_man_array = Pieces.BLACK_MAN.value * (
            np.fromstring(np.binary_repr(self.black_man, width=50), np.int8) - 48
        )
        black_king_array = Pieces.BLACK_KING.value * (
            np.fromstring(np.binary_repr(self.black_king, width=50), np.int8) - 48
        )

        arr = np.flip(
            white_man_array + white_king_array + black_man_array + black_king_array
        )
        new_arr = np.zeros(self.size * self.size, dtype=np.int8)
        new_arr[self.matching_index] = arr
        return new_arr.reshape((self.size, self.size))
