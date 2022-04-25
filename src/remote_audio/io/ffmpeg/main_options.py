#!/usr/bin/env python3

from enum import Enum
from remote_audio.io.ffmpeg import stream_specifier

from remote_audio.io.ffmpeg.formats import FFMPEG_FORMATS
from remote_audio.io.ffmpeg.stream_specifier import FFmpegStreamSpecifier, FFmpegStreamType
import remote_audio.io.ffmpeg.classes as classes

"""
FFmpeg Main options
https://ffmpeg.org/ffmpeg.html#toc-Main-options
"""




@classes.ffmpegioclass
class FFmpegOptionAttach(classes.FFmpegMainOptions):
    """
    -attach filename (output)

    Add an attachment to the output file. This is supported by a few formats like Matroska for e.g. fonts used in rendering subtitles. Attachments are implemented as a specific type of stream, so this option will add a new stream to the file. It is then possible to use per-stream options on this stream in the usual way. Attachment streams created with this option will be created after all the other streams (i.e. those created with -map or automatic mappings).

    Note that for Matroska you also have to set the mimetype metadata tag:

    ffmpeg -i INPUT -attach DejaVuSans.ttf -metadata:s:2 mimetype=application/x-truetype-font out.mkv

    (assuming that the attachment stream will be third in the output file).
    """

    attach_path:str = ""
    parameter_name:str = "attach"
    option_type:classes.FFmpegOptionType = classes.FFmpegOptionType.OUTPUT

    @property
    def io_string(
        self,
    )->list:
        """
        -attach filename (output)
        """
        return super().io_string + [
            f"{self.attach_path:d}",
        ]

    @classmethod
    def create(
        cls,
        attach_path:str,
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
            attach_path = attach_path,
            option_type = option_type,
            *args,
            **kwargs,
        )   


# @classes.ffmpegioclass
# class FFmpegOptionCodec(classes.FFmpegMainOptions):
#     """
#     -c[:stream_specifier] codec (input/output,per-stream)
#     -codec[:stream_specifier] codec (input/output,per-stream)

#     Select an encoder (when used before an output file) or a decoder (when used before an input file) for one or more streams. codec is the name of a decoder/encoder or a special value copy (output only) to indicate that the stream is not to be re-encoded.

#     For example

#     ffmpeg -i INPUT -map 0 -c:v libx264 -c:a copy OUTPUT

#     encodes all video streams with libx264 and copies all audio streams.

#     For each stream, the last matching c option is applied, so

#     ffmpeg -i INPUT -map 0 -c copy -c:v:1 libx264 -c:a:137 libvorbis OUTPUT

#     will copy all the streams except the second video, which will be encoded with libx264, and the 138th audio, which will be encoded with libvorbis.

#     """
#     stream_specifier:FFmpegStreamSpecifier = FFmpegStreamSpecifier()
#     codec:str = "libx264"
#     parameter_name:str = "codec"
#     option_type:classes.FFmpegOptionType = classes.FFmpegOptionType.INPUT_OUTPUT



@classes.ffmpegioclass
class FFmpegOptionDebugTimestamp(classes.FFmpegMainOptions):
    """
    -debug_ts (global)

    Print timestamp information. It is off by default. This option is mostly useful for testing and debugging purposes, and the output format may change from one version to another, so it should not be employed by portable scripts.

    See also the option -fdebug ts.
    """
    parameter_name:str = "debug_ts"
    option_type:classes.FFmpegOptionType = classes.FFmpegOptionType.GLOBAL_OPTIONS



@classes.ffmpegioclass
class FFmpegOptionDispositions(classes.FFmpegMainOptions):
    """
    -dispositions

    Show stream dispositions.
    """

    parameter_name:str = "disposition"
    option_type:classes.FFmpegOptionType = classes.FFmpegOptionType.OUTPUT



@classes.ffmpegioclass
class FFmpegOptionDN(classes.FFmpegMainOptions):
    """
    -dn (input/output)

    As an input option, blocks all data streams of a file from being filtered or being automatically selected or mapped for any output. See -discard option to disable streams individually.

    As an output option, disables data recording i.e. automatic selection or mapping of any data stream. For full manual control see the -map option.
    """

    parameter_name:str = "dn"
    option_type:classes.FFmpegOptionType = classes.FFmpegOptionType.INPUT_OUTPUT



@classes.ffmpegioclass
class FFmpegOptionDumpAttachment(classes.FFmpegMainOptions):
    """
    Extract the matching attachment stream into a file named filename. If filename is empty, then the value of the filename metadata tag will be used.

    E.g. to extract the first attachment to a file named ’out.ttf’:

        ffmpeg -dump_attachment:t:0 out.ttf -i INPUT

    To extract all attachments to files determined by the filename tag:

        ffmpeg -dump_attachment:t "" -i INPUT

    Technical note: attachments are implemented as codec extradata, so this option can actually be used to extract extradata from any stream, not just attachments. 
    """

    attach_path:str = ""
    stream_specifier:FFmpegStreamSpecifier = FFmpegStreamSpecifier()
    parameter_name:str = "dump_attachment"
    option_type:classes.FFmpegOptionType = classes.FFmpegOptionType.INPUT


    @property
    def io_string(
        self,
    )->list:
        _super_io = super().io_string
        _super_io[-1] += self.stream_specifier.as_suffix(":")

        return _super_io + [
            f"{self.attach_path}",
        ]

    @classmethod
    def create(
        cls,
        attach_path:str,
        stream_specifier:FFmpegStreamSpecifier = FFmpegStreamSpecifier(),
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
            attach_path = attach_path,
            stream_specifier = stream_specifier,
            option_type = option_type,
            *args,
            **kwargs,
        )

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
    """
    -filter[:stream_specifier] filtergraph
    """

    filtergraph:str = ""
    stream_specifier:FFmpegStreamSpecifier = FFmpegStreamSpecifier()
    parameter_name:str = "filter"
    option_type:classes.FFmpegOptionType = classes.FFmpegOptionType.OUTPUT

    @property
    def io_string(
        self,
    )->list:
        _super_io = super().io_string
        _super_io[-1] += self.stream_specifier.as_suffix(":")

        return _super_io + [
            f"{self.filtergraph}",
        ]

    @classmethod
    def create(
        cls,
        filtergraph:str,
        stream_specifier:FFmpegStreamSpecifier = FFmpegStreamSpecifier(),
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
            filtergraph = filtergraph,
            stream_specifier = stream_specifier,
            option_type = option_type,
            *args,
            **kwargs,
        )

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