import tkinter

import numpy as np

from . import GLOBAL


class LabelingButton:
    def __init__(self, root, class_idx, width, height, x, y, font, color):
        self.root = root
        self.class_idx = class_idx
        self.name = GLOBAL.CLASSES[class_idx]
        self.mode = "insert"
        self.state = "start"
        self.button = tkinter.Button(
            root,
            text=f"{self.name} {self.state}",
            width=width,
            height=height,
            command=self.on_click,
            bg=color,
        )
        self.button.place(x=x, y=y)
        self.button["font"] = font
        self.button.update()

        self.frame_labels = np.zeros(GLOBAL.FRAME_COUNT_DOWNSAMPLED)

        self.start = None

    def update(self):
        if self.mode == "delete":
            self.button["state"] = "active"
            self.button[
                "text"
            ] = f"({GLOBAL.CLASS_KEYS[self.class_idx].upper()}) {self.mode} {self.name}"
        else:
            self.button[
                "text"
            ] = f"({GLOBAL.CLASS_KEYS[self.class_idx].upper()}) {self.name} {self.state}"

        if self.frame_labels[GLOBAL.CURRENT_FRAME_IDX] == 1:
            if self.mode == "insert":
                self.button["state"] = "disabled"
            else:
                self.button["state"] = "normal"
        else:
            if self.mode == "insert":
                self.button["state"] = "normal"
            else:
                self.button["state"] = "disabled"

    def on_click(self):
        if self.mode == "delete":
            i = GLOBAL.CURRENT_FRAME_IDX
            while self.frame_labels[i] == 1:
                self.frame_labels[i] = 0
                i -= 1

                if i < 0:
                    break

            i = GLOBAL.CURRENT_FRAME_IDX + 1
            while self.frame_labels[i] == 1:
                self.frame_labels[i] = 0
                i += 1

                if i >= GLOBAL.FRAME_COUNT_DOWNSAMPLED:
                    break

            self.root.mode_switcher.change_mode()
        else:
            if self.frame_labels[GLOBAL.CURRENT_FRAME_IDX] == 1:
                return

            if self.state == "start":
                self.start = GLOBAL.CURRENT_FRAME_IDX
                self.state = "end"
                print(f"{self.name} start is set {GLOBAL.CURRENT_FRAME_IDX}")

                for i, btn in enumerate(self.root.all_class_buttons):
                    if i != self.class_idx and btn.state == "end":
                        btn.on_click()

            else:
                if GLOBAL.CURRENT_FRAME_IDX <= self.start:
                    self.start = GLOBAL.CURRENT_FRAME_IDX
                    self.state = "end"
                    print(f"{self.name} start is reset {GLOBAL.CURRENT_FRAME_IDX}")

                else:
                    self.frame_labels[self.start : GLOBAL.CURRENT_FRAME_IDX + 1] = 1
                    self.state = "start"
                    self.button["state"] = "disabled"
                    print(f"{self.name} end is set {GLOBAL.CURRENT_FRAME_IDX}")

        self.root.update_all()
