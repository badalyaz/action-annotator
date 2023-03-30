import tkinter
from functools import partial

from . import GLOBAL


class FrameSwitcher:
    def __init__(
        self,
        root,
        x,
        y,
        width,
        height,
        margin,
        count,
        font,
        func,
        backcolor="#2c3e50",
        forecolor="#FFFFFF",
    ):
        self.root = root
        self.count = count
        self.func1 = partial(func, self.root, -count)
        self.func2 = partial(func, self.root, +count)

        self.sub = tkinter.Button(
            root,
            text=f"-{count}",
            width=width,
            height=height,
            command=self.func1,
            bg=backcolor,
            fg=forecolor,
        )
        self.sub.place(x=x, y=y)
        self.sub["font"] = font
        self.sub.update()

        self.add = tkinter.Button(
            root,
            text=f"+{count}",
            width=width,
            height=height,
            command=self.func2,
            bg=backcolor,
            fg=forecolor,
        )
        self.add.place(x=x + self.sub.winfo_width(), y=y)
        self.add["font"] = font
        self.add.update()

        self.update()

    def update(self):
        if GLOBAL.CURRENT_FRAME_IDX + self.count > GLOBAL.FRAME_COUNT_DOWNSAMPLED - 1:
            self.add["state"] = "disabled"
        else:
            self.add["state"] = "normal"

        if GLOBAL.CURRENT_FRAME_IDX - self.count < 0:
            self.sub["state"] = "disabled"
        else:
            self.sub["state"] = "normal"
