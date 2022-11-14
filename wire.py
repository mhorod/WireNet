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

    @staticmethod
    def to_string(wire):
        if wire == Wire.PLUS:
            return '+'
        elif wire == Wire.MINUS:
            return '-'
        elif wire == Wire.ZERO:
            return '0'
        else:
            return '#'