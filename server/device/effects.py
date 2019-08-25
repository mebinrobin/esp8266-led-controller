from enum import Enum


class Effects(Enum):

    OFF = [0, 0]
    RAINBOW_STATIC = [101]
    RAINBOW_WAVE = [102]
    RGB = [103, 100]
    REACTIVE = [201]
