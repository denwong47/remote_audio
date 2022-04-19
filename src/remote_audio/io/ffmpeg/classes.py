#!/usr/bin/env python3

import abc
from dataclasses import dataclass
from enum import Enum
import shlex
from typing import Any, Union

from remote_audio.exceptions import InvalidInputParameters


ffmpegioclass = dataclass(frozen=False, order=False)

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

    def __repr__(self):
        """
        Why doesn't Enum does this automatically????
        """
        return f"{type(self).__name__}.{self.name}"


@ffmpegioclass
class FFmpegInputOutput(abc.ABC):
    device_type:FFmpegInputOutputType
    options_list:tuple

    def __str__(self)->str:
        return self.command_line()

    @property
    def canOutput(self):
        return self.device_type.canOutput

    @property
    def canInput(self):
        return self.device_type.canInput

    def command_line(
        self,
        kind:Union[
            str,
            FFmpegInputOutputType
        ]=FFmpegInputOutputType.INPUT,
    )->str:
        if (isinstance(kind, str)):
            kind = getattr(FFmpegInputOutputType, kind.upper(), kind)

        if (kind is FFmpegInputOutputType.INPUT):
            return " ".join(
                (
                    self.options,
                    "-i",
                    self.io_string,
                ),
            )
        elif (kind is FFmpegInputOutputType.OUTPUT):
            return " ".join(
                (
                    self.options,
                    self.io_string,
                ),
            )
        else:
            raise InvalidInputParameters(
                f".command_line() does not allow for {repr(kind)} type."
            )

    @abc.abstractmethod
    def io_string(self)->str:
        return ""

    @property
    def options(self)->str:
        _options_list = getattr(self, "options_list", tuple())

        # Remove any options that are None, which means default
        _nonnull_options = {}
        for _option in _options_list:
            if (getattr(self, _option, None) is not None):
                _nonnull_options[_option] = shlex.quote(str(getattr(self, _option, '')))

        # Create the list of options
        _options_str = " ".join(
            (
                f"-{_option} {_nonnull_options[_option]}" \
                    for _option in _nonnull_options
            )
        )

        return _options_str
        

@ffmpegioclass
class FFmpegDevice(FFmpegInputOutput):
    pass

@ffmpegioclass
class FFmpegProtocol(FFmpegInputOutput):
    """
    Abstract class representing a type of FFmpeg Protocol.

    Has built-in constructor for command line options.
    
    Use .create() classmethods for all subclasses.
    """

    rw_timeout:int = None