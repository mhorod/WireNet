from enum import Enum, auto

class Wire(Enum):
    PLUS = auto()
    MINUS = auto()
    ZERO = auto()
    INVALID = auto()


    @staticmethod
    def from_string(s):
        if s == '+':
            return Wire.PLUS
        elif s == '-':
            return Wire.MINUS
        elif s == '0':
            return Wire.ZERO
        else:
            return Wire.INVALID