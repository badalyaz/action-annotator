import tkinter
from pathlib import Path
from tkinter import filedialog, messagebox

import cv2
import numpy as np

from submodules import GLOBAL
from submodules.utils import apply_filter, ask_path


class VideoLbvis:
    def __init__(self, video_path, lbl_arr):
        # Filters
        self.texts = ["FALL", "WALK", "SIT", "LAY"]

        self.video_path = video_path
        self.lbl_arr = np.load(lbl_arr)
        self.cap = self.init_video_obj(self.video_path)

    def init_video_obj(self, vid_path):
        cap = cv2.VideoCapture(vid_path)
        frame_width = int(cap.get(3))
        frame_height = int(cap.get(4))
        size = (frame_width, frame_height)
        return cap

    def filter_show_write(self, fr, mask, text):
        if mask:
            img0 = apply_filter(fr, mask)
            cv2.putText(
                img0,
                text=text,
                org=(100, 50),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=1,
                color=(0, 0, 0),
            )
        else:
            img0 = fr

        cv2.imshow("img", img0)

    def __call__(self):
        idx = 0
        while self.cap.isOpened():
            _, frame = self.cap.read()
            if not _:
                continue

            f_idx = np.where(self.lbl_arr[:, idx] == 1)[0]
            if f_idx.shape[0] != 0:
                f_idx = f_idx[0]
                self.filter_show_write(frame, GLOBAL.FILTERS[f_idx], self.texts[f_idx])

            else:
                f_idx = None
                self.filter_show_write(frame, None, None)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
            idx += 1

        self.cap.release()


if __name__ == "__main__":
    while True:
        video_path = ask_path()
        if len(video_path) == 0:
            result = messagebox.askretrycancel(
                "Retry?",
            )
            if result is True:
                continue
            else:
                exit()
        break

    video_path = Path(video_path)
    label_path = video_path.with_suffix(".npy")
    video_path = video_path.absolute().resolve().as_posix()
    label_path = label_path.absolute().resolve().as_posix()

    vl = VideoLbvis(video_path, label_path)
    vl()
