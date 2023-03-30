from tkinter import HORIZONTAL, Image, Label, Scale

import cv2
import numpy as np
from PIL import Image, ImageTk

from . import GLOBAL


class Timeline:
    def __init__(
        self,
        root,
        x,
        y,
        width,
        height,
        min,
        max,
    ):
        self.root = root
        self.trackbar = Scale(
            root,
            from_=min,
            to=max,
            orient=HORIZONTAL,
            command=self.on_scale_change,
        )
        self.trackbar.place(x=x, y=y, width=width, height=height)
        self.width = width
        self.height = height
        self.label_line = Label(root)
        self.label_line.place(x=x + 15, y=y - 20)

        self.img = np.zeros(
            (height // 3, GLOBAL.FRAME_COUNT_DOWNSAMPLED, 3), dtype=np.uint8
        )
        # self.img = cv2.resize(self.img, (width, height//3))
        img__ = ImageTk.PhotoImage(
            Image.fromarray(cv2.resize(self.img, (width - 30, height // 3)))
        )
        self.label_line.configure(image=img__)
        self.label_line.image = img__
        self.trackbar.update()

    def on_scale_change(self, value):
        GLOBAL.CURRENT_FRAME_IDX = int(value)
        self.root.update_all()

    def get_timeline_value_coord(self, value):
        min_value = self.trackbar["from"]
        max_value = self.trackbar["to"]
        width = self.trackbar.winfo_width()
        x = (value - min_value) / (max_value - min_value) * width
        return x + 15

    def _update_timeline(self):
        for i, color in enumerate(GLOBAL.FILTERS):
            # self.img[:, self.get_timeline_value_coord(np.where(self.root.all_class_buttons[i].frame_labels==1)[0]).astype(int)] = (color)
            self.img[
                :, np.where(self.root.all_class_buttons[i].frame_labels == 1)[0]
            ] += np.array(color, dtype=np.uint8)

        img__ = ImageTk.PhotoImage(
            Image.fromarray(cv2.resize(self.img, (self.width - 35, self.height // 3)))
        )
        self.label_line.configure(image=img__)
        self.label_line.image = img__

    def _update(self):
        self.trackbar.set(GLOBAL.CURRENT_FRAME_IDX)
        self.img *= 0
