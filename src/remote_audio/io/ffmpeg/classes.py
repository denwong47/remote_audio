#!/usr/bin/env python3

import abc
from enum import Enum

class FFmpegInputOutputType(Enum):
    """
    Enum type to determine if a FFmpegDevice can be used for input or output or both
    """

    INPUT = 2
    OUTPUT = 1
    INPUT_OUTPUT = INPUT + OUTPUT

    @property
    def canInput(self):
        return self.value & type(self).INPUT.value

    @property
    def canOutput(self):
        return self.value & type(self).OUTPUT.value


class FFmpegInputOutput(abc.ABC):
    device_type:FFmpegInputOutputType = None

    def __str__(self):
        return ""

    @property
    def command_line(self):
        return ""

class FFmpegDevice(FFmpegInputOutput):
    pass

class FFmpegProtocol(FFmpegInputOutput):
    pass