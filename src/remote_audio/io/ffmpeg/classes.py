#!/usr/bin/env python3


import abc
from dataclasses import dataclass
from enum import Enum
import shlex
from typing import Any, Callable, Dict, Iterable, Union
import warnings

from remote_audio.exceptions import InvalidInputParameters


ffmpegioclass = dataclass(frozen=False, order=False)

class FFmpegOptionType(Enum):
    """
    Enum type to determine if a FFmpegDevice can be used for input or output or both
    """

    INPUT = 2
    OUTPUT = 1
    INPUT_OUTPUT = INPUT + OUTPUT

    GLOBAL_OPTIONS = 4

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
class FFmpegOption(abc.ABC):
    option_type:FFmpegOptionType

    def __post_init__(self)->None:
        if (isinstance(self.option_type, str)):
            self.option_type = getattr(FFmpegOptionType, self.option_type.upper(), None)

        if (not isinstance(self.option_type, FFmpegOptionType)):
            warnings.warn(
                UserWarning(
                    f"{type(self).__name__} instance appeared to be created without using classmethod .create(). This is unsupported - do you intend to use .create()?"
                )
            )

    def __str__(self)->str:
        _command_line = self.command_line()
        if (isinstance(_command_line, list)):
            _command_line = " ".join(_command_line)
        return _command_line

    @abc.abstractclassmethod
    def create(
        self,
        *args,
        **kwargs
    )->"FFmpegOption":
        pass

    @property
    def canOutput(self):
        return self.option_type.canOutput

    @property
    def canInput(self):
        return self.option_type.canInput

    @abc.abstractmethod
    def command_line(
        self,
        kind:Union[
            str,
            FFmpegOptionType
        ]=FFmpegOptionType.INPUT,
    )->list:
        """
        Generate a list of strings for subprocess to use.
        Equivalent to having done shlex.split().
        """

        # TODO
        pass

    @abc.abstractmethod
    def io_string(self)->list:
        return []

    @property
    def options(self)->list:
        _options_list = getattr(self, "options_list", tuple())

        # Remove any options that are None, which means default
        _nonnull_options = {}
        for _option in _options_list:
            _value = getattr(self, _option, None)
            if (_value is not None):
                # Convert bool to shell booleans
                if (isinstance(_value, bool)):
                    _value = "true" if _value else "false"

                _nonnull_options[_option] = shlex.quote(str(_value))

        # Create the list of options
        _options_list = [
            f"-{_option} {_nonnull_options[_option]}" \
                    for _option in _nonnull_options
        ]

        return _options_list

@ffmpegioclass
class FFmpegMainOptions(FFmpegOption):
    parameter_name:str
    
    @property
    def io_string(
        self,
    )->list:
        """
        Return -parameter_name.
        Subclasses will use this super().io_string.
        """
        return [f"-{self.parameter_name}"]

    def command_line(
        self,
        kind:Union[
            str,
            FFmpegOptionType
        ]=FFmpegOptionType.INPUT,
    )->list:
        """
        Generate a list of strings for subprocess to use.
        Equivalent to having done shlex.split().
        """
        
        return [
            *self.options,
            *self.io_string,
        ]

    @classmethod
    def create(
        cls,
        *args,
        **kwargs,
    ):
        return cls(
            *args,
            **kwargs,
        )

@ffmpegioclass
class FFmpegDevice(FFmpegOption):
    options_list:tuple

@ffmpegioclass
class FFmpegProtocol(FFmpegOption):
    """
    Abstract class representing a type of FFmpeg Protocol.

    Has built-in constructor for command line options.
    
    Use .create() classmethods for all subclasses.
    """
    options_list:tuple
    rw_timeout:int = None

    def command_line(
        self,
        kind:Union[
            str,
            FFmpegOptionType
        ]=FFmpegOptionType.INPUT,
    )->list:
        """
        Generate a list of strings for subprocess to use.
        Equivalent to having done shlex.split().
        """

        if (isinstance(kind, str)):
            kind = getattr(FFmpegOptionType, kind.upper(), kind)

        if (kind is FFmpegOptionType.INPUT):
            return [
                *self.options,
                "-i",
                *self.io_string,
            ]
        elif (kind is FFmpegOptionType.OUTPUT):
            return [
                *self.options,
                *self.io_string,
            ] 
        else:
            raise InvalidInputParameters(
                f".command_line() does not allow for {repr(kind)} type."
            )



