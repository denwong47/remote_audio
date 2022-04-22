#!/usr/bin/env python3

from enum import Enum
from click import option

from remote_audio.io.ffmpeg.formats import FFMPEG_FORMATS
import remote_audio.io.ffmpeg.classes as classes

"""
FFmpeg Main options
https://ffmpeg.org/ffmpeg.html#toc-Main-options
"""




@classes.ffmpegioclass
class FFmpegOptionAttach(classes.FFmpegMainOptions):
    parameter_name:str = "attach"
    option_type:classes.FFmpegOptionType = classes.FFmpegOptionType.OUTPUT

    


@classes.ffmpegioclass
class FFmpegOptionCodec(classes.FFmpegMainOptions):
    parameter_name:str = "codec"
    option_type:classes.FFmpegOptionType = classes.FFmpegOptionType.INPUT_OUTPUT



@classes.ffmpegioclass
class FFmpegOptionDebugTimestamp(classes.FFmpegMainOptions):
    parameter_name:str = "debug_ts"
    option_type:classes.FFmpegOptionType = classes.FFmpegOptionType.GLOBAL_OPTIONS



@classes.ffmpegioclass
class FFmpegOptionDataFrames(classes.FFmpegMainOptions):
    parameter_name:str = "dframes"
    option_type:classes.FFmpegOptionType = classes.FFmpegOptionType.OUTPUT



@classes.ffmpegioclass
class FFmpegOptionDispositions(classes.FFmpegMainOptions):
    parameter_name:str = "disposition"
    option_type:classes.FFmpegOptionType = classes.FFmpegOptionType.OUTPUT



@classes.ffmpegioclass
class FFmpegOptionDN(classes.FFmpegMainOptions):
    parameter_name:str = "dn"
    option_type:classes.FFmpegOptionType = classes.FFmpegOptionType.INPUT_OUTPUT



@classes.ffmpegioclass
class FFmpegOptionDumpAttachment(classes.FFmpegMainOptions):
    parameter_name:str = "dump_attachment"
    option_type:classes.FFmpegOptionType = classes.FFmpegOptionType.INPUT


@classes.ffmpegioclass
class FFmpegOptionFormat(classes.FFmpegMainOptions):
    """
    -f fmt (input/output)

    Force input or output file format. The format is normally auto detected for input files and guessed from the file extension for output files, so this option is not needed in most cases.
    """

    format:str = "wav"
    parameter_name:str = "f"
    option_type:classes.FFmpegOptionType = classes.FFmpegOptionType.INPUT_OUTPUT

    def get_format(
        self
    )->dict:
        return FFMPEG_FORMATS.get(self.format, None)

    @property
    def io_string(
        self,
    )->list:
        """
        -f [format]
        """
        return super().io_string + [
            self.format,
        ]

    @classmethod
    def create(
        cls,
        format:str,
        option_type:classes.FFmpegOptionType = classes.FFmpegOptionType.INPUT,
        *args,
        **kwargs,
    ):
        """
        Create an instance of the class using format.

        This class method is necessary because the class inheritance messed up the 
        ordering of parameters of __init__.
        Currently __init__(
            option_type,
            ...
        )
        which makes it hard to call __init__ intuitively.
        """

        return cls(
            format = format,
            option_type = option_type,
            *args,
            **kwargs,
        )

@classes.ffmpegioclass
class FFmpegOptionFilter(classes.FFmpegMainOptions):
    parameter_name:str = "filter"
    option_type:classes.FFmpegOptionType = classes.FFmpegOptionType.OUTPUT



@classes.ffmpegioclass
class FFmpegOptionFilterScript(classes.FFmpegMainOptions):
    parameter_name:str = "filter_script"
    option_type:classes.FFmpegOptionType = classes.FFmpegOptionType.OUTPUT



@classes.ffmpegioclass
class FFmpegOptionFilterThreadss(classes.FFmpegMainOptions):
    parameter_name:str = "filter_threads"
    option_type:classes.FFmpegOptionType = classes.FFmpegOptionType.GLOBAL_OPTIONS



@classes.ffmpegioclass
class FFmpegOptionFrames(classes.FFmpegMainOptions):
    parameter_name:str = "frames"
    option_type:classes.FFmpegOptionType = classes.FFmpegOptionType.OUTPUT



@classes.ffmpegioclass
class FFmpegOptionFileSize(classes.FFmpegMainOptions):
    parameter_name:str = "fs"
    option_type:classes.FFmpegOptionType = classes.FFmpegOptionType.OUTPUT



@classes.ffmpegioclass
class FFmpegOptionInputTimestampOffset(classes.FFmpegMainOptions):
    parameter_name:str = "itsoffset"
    option_type:classes.FFmpegOptionType = classes.FFmpegOptionType.INPUT



@classes.ffmpegioclass
class FFmpegOptionInputTimestampRescale(classes.FFmpegMainOptions):
    parameter_name:str = "itsscale"
    option_type:classes.FFmpegOptionType = classes.FFmpegOptionType.INPUT



@classes.ffmpegioclass
class FFmpegOptionMetadata(classes.FFmpegMainOptions):
    parameter_name:str = "metadata"
    option_type:classes.FFmpegOptionType = classes.FFmpegOptionType.OUTPUT



@classes.ffmpegioclass
class FFmpegOptionNoOverwrite(classes.FFmpegMainOptions):
    """
    -n (global)

    Do not overwrite output files, and exit immediately if a specified output file already exists.
    """
    parameter_name:str = "n"
    option_type:classes.FFmpegOptionType = classes.FFmpegOptionType.GLOBAL_OPTIONS


@classes.ffmpegioclass
class FFmpegOptionPreset(classes.FFmpegMainOptions):
    parameter_name:str = "pre"
    option_type:classes.FFmpegOptionType = classes.FFmpegOptionType.OUTPUT



@classes.ffmpegioclass
class FFmpegOptionProgram(classes.FFmpegMainOptions):
    parameter_name:str = "program"
    option_type:classes.FFmpegOptionType = classes.FFmpegOptionType.OUTPUT



@classes.ffmpegioclass
class FFmpegOptionProgress(classes.FFmpegMainOptions):
    parameter_name:str = "progress"
    option_type:classes.FFmpegOptionType = classes.FFmpegOptionType.GLOBAL_OPTIONS



@classes.ffmpegioclass
class FFmpegOptionQScale(classes.FFmpegMainOptions):
    parameter_name:str = "qscale"
    option_type:classes.FFmpegOptionType = classes.FFmpegOptionType.OUTPUT



@classes.ffmpegioclass
class FFmpegOptionRecastMedia(classes.FFmpegMainOptions):
    parameter_name:str = "recast_media"
    option_type:classes.FFmpegOptionType = classes.FFmpegOptionType.GLOBAL_OPTIONS



@classes.ffmpegioclass
class FFmpegOptionReinitFilter(classes.FFmpegMainOptions):
    parameter_name:str = "reinit_filter"
    option_type:classes.FFmpegOptionType = classes.FFmpegOptionType.INPUT



@classes.ffmpegioclass
class FFmpegOptionSeek(classes.FFmpegMainOptions):
    parameter_name:str = "ss"
    option_type:classes.FFmpegOptionType = classes.FFmpegOptionType.INPUT_OUTPUT



@classes.ffmpegioclass
class FFmpegOptionSeekFromEOF(classes.FFmpegMainOptions):
    parameter_name:str = "sseof"
    option_type:classes.FFmpegOptionType = classes.FFmpegOptionType.INPUT



@classes.ffmpegioclass
class FFmpegOptionStats(classes.FFmpegMainOptions):
    parameter_name:str = "stats"
    option_type:classes.FFmpegOptionType = classes.FFmpegOptionType.GLOBAL_OPTIONS



@classes.ffmpegioclass
class FFmpegOptionStatsPeriod(classes.FFmpegMainOptions):
    parameter_name:str = "stats_period"
    option_type:classes.FFmpegOptionType = classes.FFmpegOptionType.GLOBAL_OPTIONS



@classes.ffmpegioclass
class FFmpegOptionStdin(classes.FFmpegMainOptions):
    parameter_name:str = "stdin"
    option_type:classes.FFmpegOptionType = classes.FFmpegOptionType.GLOBAL_OPTIONS



@classes.ffmpegioclass
class FFmpegOptionStreamLoop(classes.FFmpegMainOptions):
    """
    -stream_loop number (input)

    Set number of times input stream shall be looped. Loop 0 means no loop, loop -1 means infinite loop.
    """
    loop:int = 0
    parameter_name:str = "stream_loop"
    option_type:classes.FFmpegOptionType = classes.FFmpegOptionType.INPUT

    @property
    def io_string(
        self,
    )->list:
        """
        -f [format]
        """
        return super().io_string + [
            f"{self.loop:d}",
        ]

    @classmethod
    def create(
        cls,
        loop:int = 0,
        option_type:classes.FFmpegOptionType = classes.FFmpegOptionType.INPUT,
        *args,
        **kwargs,
    ):
        """
        Create an instance of the class using format.

        This class method is necessary because the class inheritance messed up the 
        ordering of parameters of __init__.
        Currently __init__(
            option_type,
            ...
        )
        which makes it hard to call __init__ intuitively.
        """

        return cls(
            loop = loop,
            option_type = option_type,
            *args,
            **kwargs,
        )    


@classes.ffmpegioclass
class FFmpegOptionDuration(classes.FFmpegMainOptions):
    parameter_name:str = "t"
    option_type:classes.FFmpegOptionType = classes.FFmpegOptionType.INPUT_OUTPUT



@classes.ffmpegioclass
class FFmpegOptionTarget(classes.FFmpegMainOptions):
    parameter_name:str = "target"
    option_type:classes.FFmpegOptionType = classes.FFmpegOptionType.OUTPUT



@classes.ffmpegioclass
class FFmpegOptionTimestamp(classes.FFmpegMainOptions):
    parameter_name:str = "timestamp"
    option_type:classes.FFmpegOptionType = classes.FFmpegOptionType.OUTPUT



@classes.ffmpegioclass
class FFmpegOptionTo(classes.FFmpegMainOptions):
    parameter_name:str = "to"
    option_type:classes.FFmpegOptionType = classes.FFmpegOptionType.INPUT_OUTPUT



@classes.ffmpegioclass
class FFmpegOptionOverwrite(classes.FFmpegMainOptions):
    """
    -y (global)

    Overwrite output files without asking.
    """
    parameter_name:str = "y"
    option_type:classes.FFmpegOptionType = classes.FFmpegOptionType.GLOBAL_OPTIONS