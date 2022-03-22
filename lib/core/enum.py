from enum import Enum


class Mode(Enum):
    DEBUG = 1
    RELEASE = 2

    @staticmethod
    def isDebug(mode: str):
        if "r" in mode or "R" in mode:
            return Mode.RELEASE
        else:
            return Mode.DEBUG
