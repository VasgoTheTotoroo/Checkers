"""This module is the background of the window"""


from tkinter import Tk, Canvas


class Background:
    """The background of the window"""

    def __init__(
        self,
        window: Tk,
        init_width: int,
        init_height: int,
        init_background_color: str = "#4E3D28",
    ):
        self.canvas: Canvas = Canvas(
            master=window,
            width=init_width,
            height=init_height,
            bg=init_background_color,
        )
        self.canvas.place(x=0, y=0)

    def update(self, window: Tk):
        """Update the background width and height"""

        self.canvas.config(width=window.winfo_width(), height=window.winfo_height())
