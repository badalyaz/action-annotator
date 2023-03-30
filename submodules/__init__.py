from .utils import rgb_to_hex


class GLOBAL:
    """
    It is bad practice to use global variables in python, so write you code more pythonic and mess everithing up!
    """

    FRAME_COUNT_ORIGINAL = None
    FRAME_COUNT_DOWNSAMPLED = None
    CURRENT_FRAME_IDX = 0
    CLASSES = ["Fall", "Walk", "Sit", "Lay"]
    CLASS_KEYS = ["1", "2", "3", "4"]
    COLORS = [(191, 36, 20), (0, 148, 116), (12, 112, 179), (203, 116, 0)]
    FILTERS = [(231, 76, 60), (24, 188, 156), (52, 152, 219), (243, 156, 18)]
    TK_COLORS = [
        rgb_to_hex(FILTERS[0]),
        rgb_to_hex(FILTERS[1]),
        rgb_to_hex(FILTERS[2]),
        rgb_to_hex(FILTERS[3]),
    ]
    # Keys
    MODE_SWITCHER_KEY = "x"
    LEFT_CHAR_KEY = "a"
    RIGHT_CHAR_KEY = "d"

    LEFT_ARROW_KEY = "Left"
    RIGHT_ARROW_KEY = "Right"
