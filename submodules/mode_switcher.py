import tkinter

from . import GLOBAL


class ModeSwitcher:
    def __init__(self, root, width, height, x, y, font, backcolor, forecolor):
        self.root = root
        self.button = tkinter.Button(
            root,
            text=f"Delete ({GLOBAL.MODE_SWITCHER_KEY.upper()})",
            width=width,
            height=height,
            command=self.on_click,
            bg=backcolor,
            fg=forecolor,
        )

        self.button.place(x=x, y=y)
        self.button["font"] = font
        self.button.update()

    def on_click(self):
        self.change_mode()

    def change_mode(self):
        for button in self.root.all_class_buttons:
            if button.mode == "insert":
                button.mode = "delete"
            else:
                button.mode = "insert"
            button.button["state"] = "normal"
            button.update()

        self.button["text"] = (
            f"Insert ({GLOBAL.MODE_SWITCHER_KEY.upper()})"
            if self.button["text"] == "Delete"
            else f"Delete ({GLOBAL.MODE_SWITCHER_KEY.upper()})"
        )
