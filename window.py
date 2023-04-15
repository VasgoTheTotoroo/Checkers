"""This module implement the Window class"""

from tkinter import Tk
from background import Background
from board import Board


class Window:
    """The window of the game"""

    def __init__(
        self,
        init_width: int = 1280,
        init_height: int = 720,
    ):
        """Init the window with Parameters:
        init_width (int): the width of the window
        init_height (int): the height of the window
        """

        self.window: Tk = Tk()
        self.init_window(init_width=init_width, init_height=init_height)

        self.background: Background = Background(
            window=self.window,
            init_width=init_width,
            init_height=init_height,
        )

        self.board: Board = Board(
            window=self.window,
            init_width=init_width,
            init_height=init_height,
        )

        self.bind_events()

        self.window.mainloop()

    def init_window(self, init_width: int, init_height: int):
        """Init the main Tinker window"""

        self.window.geometry(newGeometry=str(init_width) + "x" + str(init_height))
        self.window.title("Checkers")
        self.window.protocol("WM_DELETE_WINDOW", self.window.destroy)

    def update_canvas(self, _):
        """Update all the canvas when the window is resizing"""

        self.background.update(window=self.window)
        self.board.update(window=self.window)

    def bind_events(self):
        """Bind the events to the fcts for the different canvas"""

        self.window.bind("<Configure>", self.update_canvas)
        self.board.bind()
