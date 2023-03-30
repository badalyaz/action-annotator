import tkinter
import tkinter.font as font
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
from tkinter.simpledialog import askinteger

import cv2
import numpy as np
from PIL import Image, ImageTk

from . import GLOBAL
from .frame_switcher import FrameSwitcher
from .labeling_button import LabelingButton
from .mode_switcher import ModeSwitcher
from .saver import LabelSaver
from .timeline import Timeline
from .utils import apply_filter, ask_path


def change(master, size):
    GLOBAL.CURRENT_FRAME_IDX = max(
        0, min(GLOBAL.CURRENT_FRAME_IDX + size, GLOBAL.FRAME_COUNT_DOWNSAMPLED - 1)
    )

    master.update_all()


class App(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.__init_window()
        self.__center()
        self.__init_source()
        self.__init_buttons()
        self.__bind_keys()
        self.update_all()

    def __bind_keys(self):
        self.bind_all("<Key>", self.on_key_press)
        self.bind_all("<Control-Alt-Button-3>", self.on_control_right_click)

    def __center(self):
        """
        centers a tkinter window
        :param win: the main window or Toplevel window to center
        """
        self.update_idletasks()
        width = self.winfo_width()
        frm_width = self.winfo_rootx() - self.winfo_x()
        win_width = width + 2 * frm_width
        height = self.winfo_height()
        titlebar_height = self.winfo_rooty() - self.winfo_y()
        win_height = height + titlebar_height + frm_width
        x = self.winfo_screenwidth() // 2 - win_width // 2
        # y = self.winfo_screenheight() // 2 - win_height // 2
        self.geometry("{}x{}+{}+{}".format(width, height, x, 0))
        self.deiconify()

    def __init_window(self):
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()

        self.width = width * 9 // 10
        self.height = height * 9 // 10
        self.eval("tk::PlaceWindow . topleft")

        self.geometry("%dx%d" % (self.width, self.height))

        self.title("Awesome video annontator")
        self["bg"] = "white"

        self.font = tkinter.font.Font(size=self.width // 100)
        self.resizable(False, False)
        self.top_pad = height * 2 // 10
        self.right_pad = -int(width * 1.5 // 10)
        self.button_margin_bottom = 10
        self.image_box = tkinter.Label(self)
        self.image_box.place(x=0, y=0)

        self.update()

    def __init_buttons(self):
        labeling_button_height = self.height // 500

        switcher_button_width = self.width // 200
        labeling_button_width = switcher_button_width * 2

        self._by_1 = FrameSwitcher(
            root=self,
            x=int(self.width - switcher_button_width * 32 / 3) + self.right_pad,
            y=self.height - 2 * self.top_pad,
            width=switcher_button_width,
            height=labeling_button_height,
            count=1,
            margin=40,
            font=self.font,
            func=change,
        )

        self._by_5 = FrameSwitcher(
            root=self,
            x=int(self.width - switcher_button_width * 32 / 3) + self.right_pad,
            y=self._by_1.add.winfo_y() + self._by_1.add.winfo_height(),
            width=switcher_button_width,
            height=labeling_button_height,
            count=5,
            margin=40,
            font=self.font,
            func=change,
        )

        self._by_10 = FrameSwitcher(
            root=self,
            x=int(self.width - switcher_button_width * 32 / 3) + self.right_pad,
            y=self._by_5.add.winfo_y() + self._by_5.add.winfo_height(),
            width=switcher_button_width,
            height=labeling_button_height,
            count=10,
            margin=64,
            font=self.font,
            func=change,
        )

        self.button_pairs = [self._by_1, self._by_5, self._by_10]

        self.fall_button = LabelingButton(
            self,
            class_idx=0,
            width=labeling_button_width,
            height=labeling_button_height,
            x=self._by_10.sub.winfo_x(),
            y=self.top_pad,
            font=self.font,  ####
            color=GLOBAL.TK_COLORS[0],
        )

        self.walk_button = LabelingButton(
            self,
            class_idx=1,
            width=labeling_button_width,
            height=labeling_button_height,
            x=self.fall_button.button.winfo_x(),
            y=self.fall_button.button.winfo_y()
            + self.fall_button.button.winfo_height()
            + self.button_margin_bottom,
            font=self.font,
            color=GLOBAL.TK_COLORS[1],
        )

        self.sit_button = LabelingButton(
            self,
            class_idx=2,
            width=labeling_button_width,
            height=labeling_button_height,
            x=self.fall_button.button.winfo_x(),
            y=self.walk_button.button.winfo_y()
            + self.fall_button.button.winfo_height()
            + self.button_margin_bottom,
            font=self.font,
            color=GLOBAL.TK_COLORS[2],
        )

        self.lay_button = LabelingButton(
            self,
            class_idx=3,
            width=labeling_button_width,
            height=labeling_button_height,
            x=self.fall_button.button.winfo_x(),
            y=self.sit_button.button.winfo_y()
            + self.fall_button.button.winfo_height()
            + self.button_margin_bottom,
            font=self.font,
            color=GLOBAL.TK_COLORS[3],
        )

        self.all_class_buttons = [
            self.fall_button,
            self.walk_button,
            self.sit_button,
            self.lay_button,
        ]

        self.save_button = LabelSaver(
            self,
            x=self.fall_button.button.winfo_x(),
            y=0,
            width=labeling_button_width,
            height=labeling_button_height,
            font=self.font,
            backcolor="#95a5a6",
            forecolor="#2c3e50",
            save_dir=Path(self.video_path),
        )

        self.mode_switcher = ModeSwitcher(
            self,
            width=labeling_button_width,
            height=labeling_button_height,
            x=self.fall_button.button.winfo_x(),
            y=self.save_button.button.winfo_height(),
            font=self.font,
            backcolor="#2c3e50",
            forecolor="#95a5a6",
        )

        self.timeline = Timeline(
            root=self,
            x=0,
            y=self.image_height * 0.88,
            width=self.image_width,
            height=50,
            min=0,
            max=GLOBAL.FRAME_COUNT_DOWNSAMPLED - 1,
        )

        if self.initial_labels is not None:
            for idx, cls in enumerate(self.all_class_buttons):
                cls.frame_labels = self.initial_labels[idx][self.frame_indices]

    def on_control_right_click(self, event):
        for btn in self.all_class_buttons:
            btn.frame_labels *= 0
        self.update_all()

    def __get_video_path(self):
        while True:
            video_path = ask_path()
            if len(video_path) == 0:
                result = messagebox.askretrycancel(
                    "Do you want to close this beatiful app?"
                )
                if result is True:
                    continue
                else:
                    return ""
            return video_path

    def __init_source(self):
        attemp_get_path = self.__get_video_path()

        if not attemp_get_path:
            exit()
        else:
            self.video_path = Path(attemp_get_path)

        self.label_path = self.video_path.with_suffix(".npy")

        if self.label_path.is_file():
            self.initial_labels = np.load(
                self.label_path.absolute().resolve().as_posix()
            )
        else:
            self.initial_labels = None

        self.load_video(self.video_path.absolute().resolve().as_posix())

        prompt = askinteger(
            title="Input working fps",
            prompt="Input an Integer",
            initialvalue=self.video_fps,
            minvalue=1,
            maxvalue=self.video_fps,
        )

        self.downsample_video(desired_fps=prompt)

    def display_image(self):
        img = self.read_frame(GLOBAL.CURRENT_FRAME_IDX)[..., ::-1].copy()
        cv2.resize(img, (self.image_width, self.image_height))

        filter_set = False
        for i, lbl in enumerate(
            [
                self.fall_button.frame_labels[GLOBAL.CURRENT_FRAME_IDX],
                self.walk_button.frame_labels[GLOBAL.CURRENT_FRAME_IDX],
                self.sit_button.frame_labels[GLOBAL.CURRENT_FRAME_IDX],
                self.lay_button.frame_labels[GLOBAL.CURRENT_FRAME_IDX],
            ]
        ):
            if lbl:
                cv2.putText(
                    img,
                    GLOBAL.CLASSES[i],
                    (50, 40 * i + 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=1,
                    color=GLOBAL.COLORS[i],
                    thickness=3,
                )
                if filter_set is False:
                    img = apply_filter(img, GLOBAL.FILTERS[i])
                    filter_set = True

        img = ImageTk.PhotoImage(Image.fromarray(img))
        self.image_box.configure(image=img)
        self.image_box.image = img

    def read_frame(self, idx):
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.frame_indices[idx])
        return self.cap.read()[1]

    def load_video(self, video_path):
        self.cap = cv2.VideoCapture(video_path)
        self.video_fps = int(self.cap.get(cv2.CAP_PROP_FPS))

    def downsample_video(self, desired_fps):
        GLOBAL.FRAME_COUNT_ORIGINAL = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.org_video_width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.org_video_height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

        self.ratio = (
            min(self.width / self.org_video_width, self.height / self.org_video_height)
            * 0.9
        )

        self.image_width = int(self.ratio * self.org_video_width)
        self.image_height = int(self.ratio * self.org_video_height)

        desired_video_length = int(
            GLOBAL.FRAME_COUNT_ORIGINAL * (desired_fps / self.video_fps)
        )

        self.frame_indices = np.linspace(
            0, GLOBAL.FRAME_COUNT_ORIGINAL - 1, desired_video_length, dtype=int
        )

        GLOBAL.FRAME_COUNT_DOWNSAMPLED = int(
            GLOBAL.FRAME_COUNT_ORIGINAL * (desired_fps / self.video_fps)
        )

    def update_all(self):
        for btn in [
            self.fall_button,
            self.walk_button,
            self.sit_button,
            self.lay_button,
        ]:
            btn.update()

        for button_pair in self.button_pairs:
            button_pair.update()

        self.timeline._update()
        self.display_image()
        self.timeline._update_timeline()

    def on_key_press(self, event):
        """
        Adding key bindings, control in submodules/__init__.py
        """
        if (
            event.keysym == GLOBAL.RIGHT_CHAR_KEY
            or event.keysym == GLOBAL.RIGHT_ARROW_KEY
        ):
            GLOBAL.CURRENT_FRAME_IDX = np.clip(
                GLOBAL.CURRENT_FRAME_IDX + 1, 0, GLOBAL.FRAME_COUNT_DOWNSAMPLED - 1
            )
        elif (
            event.keysym == GLOBAL.LEFT_CHAR_KEY
            or event.keysym == GLOBAL.LEFT_ARROW_KEY
        ):
            GLOBAL.CURRENT_FRAME_IDX = np.clip(
                GLOBAL.CURRENT_FRAME_IDX - 1, 0, GLOBAL.FRAME_COUNT_DOWNSAMPLED - 1
            )
        elif event.keysym == "s" and event.state & 0x4:  # Control + S
            self.save_button.save()
        elif event.keysym == GLOBAL.MODE_SWITCHER_KEY:
            self.mode_switcher.change_mode()
        elif event.keysym == GLOBAL.CLASS_KEYS[0]:
            self.fall_button.on_click()
        elif event.keysym == GLOBAL.CLASS_KEYS[1]:
            self.walk_button.on_click()
        elif event.keysym == GLOBAL.CLASS_KEYS[2]:
            self.sit_button.on_click()
        elif event.keysym == GLOBAL.CLASS_KEYS[3]:
            self.lay_button.on_click()
        else:
            return

        self.update_all()
