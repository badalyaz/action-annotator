from tkinter import Button, messagebox

import cv2
import numpy as np

from . import GLOBAL


class LabelSaver:
    def __init__(
        self,
        root,
        x,
        y,
        width,
        height,
        save_dir,
        font,
        backcolor="#FFFFFF",
        forecolor="#000000",
    ):
        self.root = root
        self.save_dir = self.root.label_path

        self.button = Button(
            root,
            text="Save (Ctrl+S)",
            width=width,
            height=height,
            font=font,
            background=backcolor,
            foreground=forecolor,
            command=self.save,
        )
        self.button.place(x=x, y=y)
        self.button.update()

    def save(self):
        labels = np.stack(
            (
                self.root.fall_button.frame_labels,
                self.root.walk_button.frame_labels,
                self.root.sit_button.frame_labels,
                self.root.lay_button.frame_labels,
            )
        )
        labels = cv2.resize(
            labels, (GLOBAL.FRAME_COUNT_ORIGINAL, 4), interpolation=cv2.INTER_NEAREST
        )
        np.save(self.save_dir.absolute().resolve().as_posix(), labels)
        messagebox.showinfo(
            "Saved",
            f"The labels are saved to {self.save_dir.absolute().resolve().as_posix()}",
        )
        print("SAVED!")
