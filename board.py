"""This module is the board of the window (only UI)"""

from tkinter import Tk, Canvas, Event

import numpy as np
from engine import CheckerEngine
from pieces import Pieces


class Board:
    """The board of the window"""

    def __init__(
        self,
        window: Tk,
        init_width: int,
        init_height: int,
        init_nb_rows: int = 10,
        init_board_spacing: float = 0.05,
        init_square_color: str = "#C8AD7F",
    ):
        self.nb_rows: int = init_nb_rows
        self.engine: CheckerEngine = CheckerEngine()
        self.board_spacing: float = init_board_spacing
        self.square_color: str = init_square_color
        self.white_color: str = "#FEFEE2"
        self.black_color: str = "#2F1E0E"
        self.white_to_play = True

        if init_width > init_height:
            base_length: int = init_height
        else:
            base_length: int = init_width

        self.board_width: float = base_length * (1 - 2 * self.board_spacing)

        self.canvas: Canvas = Canvas(
            master=window,
            width=self.board_width,
            height=self.board_width,
            bg="white",
        )
        self.canvas.place(
            x=base_length * self.board_spacing,
            y=base_length * self.board_spacing,
        )

    def update(self, window: Tk):
        """Update the board width and height and scale the drawing"""

        window_width: int = window.winfo_width()
        window_height: int = window.winfo_height()

        if window_width > window_height:
            base_length: int = window_height
        else:
            base_length: int = window_width
        self.board_width: float = base_length * (1 - 2 * self.board_spacing)
        board_position: float = base_length * self.board_spacing

        self.canvas.config(
            width=self.board_width,
            height=self.board_width,
        )
        self.canvas.place(
            x=board_position,
            y=board_position,
        )
        self.draw(
            board_array=self.engine.get_position_array(),
        )

    def bind(self):
        """Bind the events for the board"""

        # drag & drop the piece
        self.canvas.bind("<ButtonPress-1>", self.select_piece)

    def select_piece(self, event: Event):
        """Select a piece to move"""

        piece_x: int = event.x
        piece_y: int = event.y
        base_length: float = self.board_width / self.nb_rows
        init_piece_x_coord: int = int(piece_x / base_length)
        init_piece_y_coord: int = int(piece_y / base_length)

        if (
            init_piece_x_coord > self.nb_rows - 1
            or init_piece_y_coord > self.nb_rows - 1
        ):
            return
        selected_piece: tuple[int, ...] = self.canvas.find_withtag(
            str(init_piece_y_coord) + ";" + str(init_piece_x_coord)
        )

        if len(selected_piece) == 0:
            return

        is_white: bool = (
            self.canvas.itemcget(selected_piece[0], "fill") == self.white_color
        )
        is_king: bool = False
        if len(selected_piece) == 2:
            is_king = True

        print(
            self.engine.get_moves_for_piece(
                coord=(init_piece_x_coord, init_piece_y_coord),
                is_white=is_white,
                is_king=is_king,
            )
        )

        if self.white_to_play and not is_white:
            return
        if not self.white_to_play and is_white:
            return

        def __internal_move_piece(
            event: Event,
            piece_ids: tuple[int, ...] = selected_piece,
            init_coord: tuple[int, int] = (init_piece_x_coord, init_piece_y_coord),
            is_white: bool = is_white,
            is_king: bool = is_king,
        ):
            self.move_piece(
                event=event,
                piece_ids=piece_ids,
                init_coord=init_coord,
                is_white=is_white,
                is_king=is_king,
            )

        self.canvas.bind("<B1-Motion>", __internal_move_piece)

    def move_piece(
        self,
        event: Event,
        piece_ids: tuple[int, ...],
        init_coord: tuple[int, int],
        is_white: bool,
        is_king: bool,
    ):
        """Move the piece on the board"""

        new_x: float = event.x
        new_y: float = event.y

        # move the man
        [piece_x0, _, piece_x1, _] = self.canvas.coords(piece_ids[0])
        # it's a round shape so dx = dy
        dxy: float = piece_x1 - piece_x0
        offset: float = dxy / 2
        new_x = new_x - offset
        new_y = new_y - offset

        self.canvas.tag_raise(piece_ids[0])

        self.canvas.coords(
            piece_ids[0],
            new_x,
            new_y,
            dxy + new_x,
            dxy + new_y,
        )

        # move the king
        if len(piece_ids) == 2:
            self.canvas.tag_raise(piece_ids[1])
            text_offset: float = self.board_width / (2.4 * self.nb_rows)
            self.canvas.coords(
                piece_ids[1],
                new_x + text_offset,
                new_y + text_offset,
            )

        def __internal_drop_piece(
            event: Event,
            init_coord: tuple[int, int] = init_coord,
            is_white: bool = is_white,
            is_king: bool = is_king,
        ):
            self.drop_piece(event, init_coord, is_white, is_king)

        self.canvas.bind("<ButtonRelease-1>", __internal_drop_piece)

    def drop_piece(
        self, event: Event, init_coord: tuple[int, int], is_white: bool, is_king: bool
    ):
        """Drop the piece in the new square"""

        base_length: float = self.board_width / self.nb_rows
        new_piece_x_coord: int = int(event.x / base_length)
        new_piece_y_coord: int = int(event.y / base_length)
        req: int = self.engine.update_board(
            init_coord, (new_piece_x_coord, new_piece_y_coord), is_white, is_king
        )
        if req == 1:
            self.white_to_play = not self.white_to_play
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.draw(self.engine.get_position_array())

    def draw(
        self,
        board_array: np.ndarray,
    ):
        """Draw the board with the pieces"""

        self.canvas.delete("all")

        base_length: float = self.board_width / self.nb_rows

        for i in range(0, self.nb_rows, 2):
            for j in range(0, self.nb_rows, 2):
                x_0: float = i * base_length
                y_0: float = j * base_length
                x_1: float = x_0 + base_length
                y_1: float = y_0 + base_length
                self.canvas.create_rectangle(
                    x_1, y_0, x_1 + base_length, y_1, fill=self.square_color
                )
                self.canvas.create_rectangle(
                    x_0, y_1, x_1, y_1 + base_length, fill=self.square_color
                )

        for i in range(self.nb_rows + 1):
            for j in range(self.nb_rows + 1):
                x_0: float = j * base_length
                y_0: float = i * base_length
                self.canvas.create_line(
                    x_0, 0, x_0, self.board_width, fill="black", width="1"
                )
                self.canvas.create_line(
                    0, y_0, self.board_width, y_0, fill="black", width="1"
                )

        # draw the pieces
        for i in range(0, self.nb_rows):
            for j in range(0, self.nb_rows):
                x_0: float = i * base_length
                y_0: float = j * base_length

                if (
                    board_array[j, i] == Pieces.WHITE_MAN.value
                    or board_array[j, i] == Pieces.WHITE_KING.value
                ):
                    self.draw_man(
                        x_0=x_0,
                        y_0=y_0,
                        color=self.white_color,
                        base_length=base_length,
                        square_tag=str(j) + ";" + str(i),
                    )
                if board_array[j, i] == Pieces.WHITE_KING.value:
                    self.draw_king(
                        x_0=x_0,
                        y_0=y_0,
                        color="black",
                        base_length=base_length,
                        square_tag=str(j) + ";" + str(i),
                    )

                if (
                    board_array[j, i] == Pieces.BLACK_MAN.value
                    or board_array[j, i] == Pieces.BLACK_KING.value
                ):
                    self.draw_man(
                        x_0=x_0,
                        y_0=y_0,
                        color=self.black_color,
                        base_length=base_length,
                        square_tag=str(j) + ";" + str(i),
                    )
                if board_array[j, i] == Pieces.BLACK_KING.value:
                    self.draw_king(
                        x_0=x_0,
                        y_0=y_0,
                        color="white",
                        base_length=base_length,
                        square_tag=str(j) + ";" + str(i),
                    )

    def draw_man(
        self, x_0: float, y_0: float, color: str, base_length: float, square_tag: str
    ):
        """Draw the man on the board"""

        base_length_10: float = base_length / 10
        base_length_90: float = base_length * (9 / 10)

        self.canvas.create_oval(
            x_0 + base_length_10,
            y_0 + base_length_10,
            x_0 + base_length_90,
            y_0 + base_length_90,
            fill=color,
            width=base_length / 20,
            tags=square_tag,
        )

    def draw_king(
        self, x_0: float, y_0: float, color: str, base_length: float, square_tag: str
    ):
        """Draw the king on the board by adding a Q writing on the piece"""

        base_length_50: float = base_length / 2

        self.canvas.create_text(
            x_0 + base_length_50,
            y_0 + base_length_50,
            font=("Arial", int(base_length * 4 / 10)),
            text="Q",
            fill=color,
            tags=square_tag,
        )
