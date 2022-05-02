#!/usr/bin/env python3
from typing import Iterable
import warnings

import remote_audio.io.ffmpeg.classes as classes
from remote_audio.exceptions import InvalidInputParameters

from shell import ShellCommand, ShellCommandExists
from shell.exceptions import ShellReturnedFailure

class FFmpegNotInstalled(ShellReturnedFailure):
    pass

class FFmpegCommand(ShellCommand):
    """
    An extension of ShellCommand, which in itself is a subclass of ShellPipe.
    See https://www.github.com/denwong47/shell for explanation fo ShellPipe.
    """
    audio_input:classes.FFmpegOption = None
    audio_output:classes.FFmpegOption = None

    def __new__(
        cls,
        input:classes.FFmpegOption,
        output:classes.FFmpegOption,
        *args,
        options:Iterable[classes.FFmpegOption]=[],
        ignore_codes:list=[],
        timeout:float=None,
        **kwargs,
    ):
        if (ShellCommandExists(["ffmpeg", "-h"])):
            return super().__new__(
                cls,
                command = ["ffmpeg", ],
                output = bytes,
                ignore_codes = ignore_codes,
                timeout = timeout,
                *args, **kwargs
            )
        else:
            return FFmpegNotInstalled("FFmpeg not installed on system.")

    def __init__(
        self,
        input:classes.FFmpegOption,
        output:classes.FFmpegOption,
        options:Iterable[classes.FFmpegOption]=[],
        ignore_codes:list=[],
        timeout:float=None,
    )->None:
        self.audio_input = input
        self.audio_output = output

        self.options = options

        super().__init__(
            None,
            output = bytes,
            ignore_codes = ignore_codes,
            timeout = timeout,
        )

    @ShellCommand.command.getter
    def command(
        self,
    )->list:
        """
        transform all parameters into a command list
        """
        
        # Check if the inputs and outputs are correct types
        assert isinstance(self.audio_input, classes.FFmpegOption)
        assert isinstance(self.audio_output, classes.FFmpegOption)

        # Check if they are capable of doing what we ask them to
        assert self.audio_input.canInput
        assert self.audio_output.canOutput

        _options_list = {
            classes.FFmpegOptionType.GLOBAL_OPTIONS: [],
            classes.FFmpegOptionType.INPUT: [],
            classes.FFmpegOptionType.OUTPUT: [],
        }

        for _option in self.options:
            if (isinstance(_option, classes.FFmpegMainOptions)):
                if (_option.option_type is classes.FFmpegOptionType.INPUT_OUTPUT):
                    # if the option is both INPUT_OUTPUT - its unclear what its for.
                    # Ignore the option.
                    warnings.warn(
                        UserWarning(
                            f"{type(_option).__name__} instance has not specified option_type; INPUT_OUTPUT is not accepted when passing to a FFmpegCommand. This option will be ignored."
                        )
                    )
                else:
                    # If the option is valid:
                    _options_list[_option.option_type] += _option.command_line(_option.option_type)
            else:
                warnings.warn(
                    UserWarning(
                        f"{type(_option).__name__} instance cannot be used as in options parameter."
                    )
                )


        _command = [
            "ffmpeg",
            *_options_list[classes.FFmpegOptionType.GLOBAL_OPTIONS],
            *_options_list[classes.FFmpegOptionType.INPUT],
            *self.audio_input.command_line(classes.FFmpegOptionType.INPUT),
            *_options_list[classes.FFmpegOptionType.OUTPUT],
            *self.audio_output.command_line(classes.FFmpegOptionType.OUTPUT),
        ]

        return _command

    @command.setter
    def command(
        self,
        value,
    ):
        """
        command.setter
        Not allowed for FFmpegCommand.
        """

        if (value is not None):
            # Allow super().__init__() to call a meaningless self.command
            raise RuntimeError(f"{type(self).__name__}.command is read only.")