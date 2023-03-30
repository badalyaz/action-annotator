import tkinter
from tkinter import filedialog, messagebox

import cv2
import numpy as np


def log(arg):
    print(f"{arg=}")


def rgb_to_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(*rgb)


def apply_filter(im, mask):
    background = np.empty(im.shape)
    for ch in range(len(mask)):
        background[:, :, ch].fill(mask[ch])
    im = cv2.addWeighted(im, 0.8, background.astype("uint8"), 0.3, 0)
    return im


def ask_path():
    filename = tkinter.filedialog.askopenfilename(
        initialdir="~",
        title="Select a Video file",
        filetypes=(("Video file", "*.mp4*"), ("all files", "*.*")),
    )

    return filename
