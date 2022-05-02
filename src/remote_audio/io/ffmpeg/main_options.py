#!/usr/bin/env python3

from enum import Enum
import shlex
from typing import Any, Dict, Iterable

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
    `-attach filename (output)`

    Add an attachment to the output file. This is supported by a few formats like Matroska for e.g. fonts used in rendering subtitles. Attachments are implemented as a specific type of stream, so this option will add a new stream to the file. It is then possible to use per-stream options on this stream in the usual way. Attachment streams created with this option will be created after all the other streams (i.e. those created with -map or automatic mappings).

    Note that for Matroska you also have to set the mimetype metadata tag:

    ```
        ffmpeg -i INPUT -attach DejaVuSans.ttf -metadata:s:2 mimetype=application/x-truetype-font out.mkv
    ```
    

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
        `-attach filename (output)`
        """
        return super().io_string + [
            f"{shlex.quote(str(self.attach_path))}",
        ]

    @classmethod
    def create(
        cls,
        attach_path:str,
        # option_type:classes.FFmpegOptionType = classes.FFmpegOptionType.OUTPUT,
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
            # option_type = option_type,
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
    `-debug_ts (global)`

    Print timestamp information. It is off by default. This option is mostly useful for testing and debugging purposes, and the output format may change from one version to another, so it should not be employed by portable scripts.

    See also the option `-fdebug` ts.
    """
    parameter_name:str = "debug_ts"
    option_type:classes.FFmpegOptionType = classes.FFmpegOptionType.GLOBAL_OPTIONS



@classes.ffmpegioclass
class FFmpegOptionDispositions(classes.FFmpegMainOptions):
    """
    `-dispositions`

    Show stream dispositions.
    """

    parameter_name:str = "disposition"
    option_type:classes.FFmpegOptionType = classes.FFmpegOptionType.OUTPUT



@classes.ffmpegioclass
class FFmpegOptionDN(classes.FFmpegMainOptions):
    """
    `-dn (input/output)`

    As an input option, blocks all data streams of a file from being filtered or being automatically selected or mapped for any output. See `-discard` option to disable streams individually.

    As an output option, disables data recording i.e. automatic selection or mapping of any data stream. For full manual control see the `-map` option.
    """

    parameter_name:str = "dn"
    option_type:classes.FFmpegOptionType = classes.FFmpegOptionType.INPUT_OUTPUT



@classes.ffmpegioclass
class FFmpegOptionDumpAttachment(classes.FFmpegMainOptions):
    """
    Extract the matching attachment stream into a file named filename. If filename is empty, then the value of the filename metadata tag will be used.

    E.g. to extract the first attachment to a file named ’out.ttf’:
    ```
        ffmpeg -dump_attachment:t:0 out.ttf -i INPUT
    ```

    To extract all attachments to files determined by the filename tag:
    ```
        ffmpeg -dump_attachment:t "" -i INPUT
    ```

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
            f"{shlex.quote(str(self.attach_path))}",
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
    `-f fmt (input/output)`

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
            shlex.quote(str(self.format)),
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
    `-filter[:stream_specifier] filtergraph`

    Create the filtergraph specified by filtergraph and use it to filter the stream.

    filtergraph is a description of the filtergraph to apply to the stream, and must have a single input and a single output of the same type of the stream. In the filtergraph, the input is associated to the label in, and the output to the label out. See the ffmpeg-filters manual for more information about the filtergraph syntax.

    See the `-filter_complex` option if you want to create filtergraphs with multiple inputs and/or outputs.
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
            f"{shlex.quote(str(self.filtergraph))}",
        ]

    @classmethod
    def create(
        cls,
        filtergraph:str,
        stream_specifier:FFmpegStreamSpecifier = FFmpegStreamSpecifier(),
        # option_type:classes.FFmpegOptionType = classes.FFmpegOptionType.OUTPUT,
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
            # option_type = option_type,
            *args,
            **kwargs,
        )

@classes.ffmpegioclass
class FFmpegOptionFilterScript(classes.FFmpegMainOptions):
    """
    `-filter_script[:stream_specifier] filename (output,per-stream)`
    
    This option is similar to -filter, the only difference is that its argument is the name of the file from which a filtergraph description is to be read. 
    """

    filename:str = ""
    stream_specifier:FFmpegStreamSpecifier = FFmpegStreamSpecifier()
    parameter_name:str = "filter_script"
    option_type:classes.FFmpegOptionType = classes.FFmpegOptionType.OUTPUT


    @property
    def io_string(
        self,
    )->list:
        _super_io = super().io_string
        _super_io[-1] += self.stream_specifier.as_suffix(":")

        return _super_io + [
            f"{shlex.quote(str(self.filename))}",
        ]

    @classmethod
    def create(
        cls,
        filename:str,
        stream_specifier:FFmpegStreamSpecifier = FFmpegStreamSpecifier(),
        # option_type:classes.FFmpegOptionType = classes.FFmpegOptionType.OUTPUT,
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
            filename = filename,
            stream_specifier = stream_specifier,
            # option_type = option_type,
            *args,
            **kwargs,
        )

@classes.ffmpegioclass
class FFmpegOptionFilterThreads(classes.FFmpegMainOptions):
    """
    `-filter_threads nb_threads (global)`

    Defines how many threads are used to process a filter pipeline. Each pipeline will produce a thread pool with this many threads available for parallel processing. The default is the number of available CPUs. 
    """

    nb_threads:int = None
    parameter_name:str = "filter_threads"
    option_type:classes.FFmpegOptionType = classes.FFmpegOptionType.GLOBAL_OPTIONS

    @property
    def io_string(
        self,
    )->list:
        _super_io = super().io_string

        return _super_io + [
            f"{shlex.quote(str(self.nb_threads))}",
        ]

    @classmethod
    def create(
        cls,
        nb_threads:int,
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
            nb_threads = nb_threads,
            *args,
            **kwargs,
        )

@classes.ffmpegioclass
class FFmpegOptionFrames(classes.FFmpegMainOptions):
    """
    `-frames[:stream_specifier] framecount (output,per-stream)`

    Stop writing to the stream after framecount frames.
    """
    framecount:int = None
    stream_specifier:FFmpegStreamSpecifier = FFmpegStreamSpecifier()
    parameter_name:str = "frames"
    option_type:classes.FFmpegOptionType = classes.FFmpegOptionType.OUTPUT
    
    @property
    def io_string(
        self,
    )->list:
        _super_io = super().io_string
        _super_io[-1] += self.stream_specifier.as_suffix(":")

        return _super_io + [
            f"{shlex.quote(str(self.framecount))}",
        ]

    @classmethod
    def create(
        cls,
        framecount:int,
        stream_specifier:FFmpegStreamSpecifier = FFmpegStreamSpecifier(),
        # option_type:classes.FFmpegOptionType = classes.FFmpegOptionType.OUTPUT,
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
            framecount = framecount,
            stream_specifier = stream_specifier,
            # option_type = option_type,
            *args,
            **kwargs,
        )

@classes.ffmpegioclass
class FFmpegOptionFileSize(classes.FFmpegMainOptions):
    """
    `-fs limit_size (output)`

    Set the file size limit, expressed in bytes. No further chunk of bytes is written after the limit is exceeded. The size of the output file is slightly more than the requested file size. 
    """
    limit_size:int = None
    parameter_name:str = "fs"
    option_type:classes.FFmpegOptionType = classes.FFmpegOptionType.OUTPUT

    @property
    def io_string(
        self,
    )->list:
        _super_io = super().io_string

        return _super_io + [
            f"{shlex.quote(str(self.limit_size))}",
        ]

    @classmethod
    def create(
        cls,
        limit_size:int,
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
            limit_size = limit_size,
            *args,
            **kwargs,
        )

    

@classes.ffmpegioclass
class FFmpegOptionInputTimestampOffset(classes.FFmpegMainOptions):
    """
    `-itsoffset offset (input)`

    Set the input time offset.

    offset must be a time duration specification, see (ffmpeg-utils)the Time duration section in the ffmpeg-utils(1) manual.

    The offset is added to the timestamps of the input files. Specifying a positive offset means that the corresponding streams are delayed by the time duration specified in offset.
    """
    offset:int = None
    parameter_name:str = "itsoffset"
    option_type:classes.FFmpegOptionType = classes.FFmpegOptionType.INPUT
    
    @property
    def io_string(
        self,
    )->list:
        _super_io = super().io_string

        return _super_io + [
            f"{shlex.quote(str(self.offset))}",
        ]

    @classmethod
    def create(
        cls,
        offset:int,
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
            offset = offset,
            *args,
            **kwargs,
        )


@classes.ffmpegioclass
class FFmpegOptionInputTimestampRescale(classes.FFmpegMainOptions):
    """
    `-itsscale scale (input,per-stream)`

    Rescale input timestamps. scale should be a floating point number. 
    """
    scale:float = None
    stream_specifier:FFmpegStreamSpecifier = FFmpegStreamSpecifier()
    parameter_name:str = "itsscale"
    option_type:classes.FFmpegOptionType = classes.FFmpegOptionType.INPUT

    @property
    def io_string(
        self,
    )->list:
        _super_io = super().io_string
        _super_io[-1] += self.stream_specifier.as_suffix(":")

        return _super_io + [
            f"{shlex.quote(str(self.scale))}",
        ]

    @classmethod
    def create(
        cls,
        scale:float,
        stream_specifier:FFmpegStreamSpecifier = FFmpegStreamSpecifier(),
        # option_type:classes.FFmpegOptionType = classes.FFmpegOptionType.OUTPUT,
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
            scale = scale,
            stream_specifier = stream_specifier,
            # option_type = option_type,
            *args,
            **kwargs,
        )

@classes.ffmpegioclass
class FFmpegOptionMetadata(classes.FFmpegMainOptions):    
    """
    `-metadata[:metadata_specifier] key=value (output,per-metadata)`

    Set a metadata key/value pair.

    An optional metadata_specifier may be given to set metadata on streams, chapters or programs. See -map_metadata documentation for details.

    This option overrides metadata set with -map_metadata. It is also possible to delete metadata by using an empty value.

    For example, for setting the title in the output file:
    
    ```
        ffmpeg -i in.avi -metadata title="my title" out.flv
    ```
    OR
    ```
    FFmpegCommand(
        input = FFmpegProtocolFile.create("in.avi"),
        output = FFmpegProtocolFile.create("out.avi"),
        options = [
            FFmpegOptionMetadata.create({
                "title":"my title"
            })
        ]
    )
    ```

    To set the language of the first audio stream:

    ```
        ffmpeg -i INPUT -metadata:s:a:0 language=eng OUTPUT
    ```
    OR
    ```
    FFmpegCommand(
        input = FFmpegProtocolFile.create(INPUT),
        output = FFmpegProtocolFile.create(OUTPUT),
        metadata_specifier = FFmpegStreamSpecifier(
            stream_index = 0,
            stream_type="s:a"
        ),
        options = [
            FFmpegOptionMetadata.create({
                "language":"eng"
            })
        ]
    )
    ```
    """
    metadata:Dict[str, Any] = None
    metadata_specifier:FFmpegStreamSpecifier = FFmpegStreamSpecifier()
    parameter_name:str = "metadata"
    option_type:classes.FFmpegOptionType = classes.FFmpegOptionType.OUTPUT

    @property
    def io_string(
        self,
    )->list:
        _super_io = super().io_string
        _super_io[-1] += self.metadata_specifier.as_suffix(":")

        return _super_io + [
            f"{key}={shlex.quote(value)}" for key,value in zip(self.metadata.keys(), self.metadata.values())
        ]

    @classmethod
    def create(
        cls,
        metadata:Dict[str, Any] = {},
        metadata_specifier:FFmpegStreamSpecifier = FFmpegStreamSpecifier(),
        # option_type:classes.FFmpegOptionType = classes.FFmpegOptionType.OUTPUT,
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
            metadata = metadata,
            metadata_specifier = metadata_specifier,
            # option_type = option_type,
            *args,
            **kwargs,
        )


@classes.ffmpegioclass
class FFmpegOptionNoOverwrite(classes.FFmpegMainOptions):
    """
    `-n (global)`

    Do not overwrite output files, and exit immediately if a specified output file already exists.
    """
    parameter_name:str = "n"
    option_type:classes.FFmpegOptionType = classes.FFmpegOptionType.GLOBAL_OPTIONS


@classes.ffmpegioclass
class FFmpegOptionPreset(classes.FFmpegMainOptions):
    """
    `-pre[:stream_specifier] preset_name (output,per-stream)`

    Specify the preset for matching stream(s).
    """
    preset_name:str = None
    stream_specifier:FFmpegStreamSpecifier = FFmpegStreamSpecifier()
    parameter_name:str = "pre"
    option_type:classes.FFmpegOptionType = classes.FFmpegOptionType.OUTPUT

    @property
    def io_string(
        self,
    )->list:
        _super_io = super().io_string
        _super_io[-1] += self.stream_specifier.as_suffix(":")

        return _super_io + [
            f"{shlex.quote(str(self.preset_name))}",
        ]

    @classmethod
    def create(
        cls,
        preset_name:str,
        stream_specifier:FFmpegStreamSpecifier = FFmpegStreamSpecifier(),
        # option_type:classes.FFmpegOptionType = classes.FFmpegOptionType.OUTPUT,
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
            preset_name = preset_name,
            stream_specifier = stream_specifier,
            # option_type = option_type,
            *args,
            **kwargs,
        )


@classes.ffmpegioclass
class FFmpegOptionProgram(classes.FFmpegMainOptions):
    """
    `-program [title=title:][program_num=program_num:]st=stream[:st=stream...] (output)`

    Creates a program with the specified title, program_num and adds the specified stream(s) to it.
    """
    streams:Iterable[FFmpegStreamSpecifier] = None
    title:str = None
    program_num:int = None
    parameter_name:str = "program"
    option_type:classes.FFmpegOptionType = classes.FFmpegOptionType.OUTPUT

    @property
    def io_string(
        self,
    )->list:
        _super_io = super().io_string

        _program_items = []
        if (self.title is not None):
            _program_items.append(f"title={shlex.quote(self.title)}")

        if (self.program_num is not None):
            _program_items.append(f"program_num={self.program_num:d}")

        _program_items += [
            f"st={stream.as_suffix('')}" for stream in self.streams
        ]

        return _super_io + [
            ":".join(_program_items)
        ]

    @classmethod
    def create(
        cls,
        streams:Iterable[FFmpegStreamSpecifier],
        title:str = None,
        program_num:int = None,
        # option_type:classes.FFmpegOptionType = classes.FFmpegOptionType.OUTPUT,
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

        if (isinstance(streams, FFmpegStreamSpecifier)):
            streams = [streams,]

        return cls(
            streams = streams,
            title = title,
            program_num = program_num,
            # option_type = option_type,
            *args,
            **kwargs,
        )

@classes.ffmpegioclass
class FFmpegOptionProgress(classes.FFmpegMainOptions):
    """
    `-progress url (global)`

    Send program-friendly progress information to url.

    Progress information is written periodically and at the end of the encoding process. It is made of "key=value" lines. key consists of only alphanumeric characters. The last key of a sequence of progress information is always "progress".

    The update period is set using `FFmpegOptionStatsPeriod`. 
    """
    url:str = None
    parameter_name:str = "progress"
    option_type:classes.FFmpegOptionType = classes.FFmpegOptionType.GLOBAL_OPTIONS

    @property
    def io_string(
        self,
    )->list:
        _super_io = super().io_string
        
        return _super_io + [
            f"{shlex.quote(str(self.url))}",
        ]

    @classmethod
    def create(
        cls,
        url:str,
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
            url = url,
            *args,
            **kwargs,
        )

    

@classes.ffmpegioclass
class FFmpegOptionQScale(classes.FFmpegMainOptions):
    """
    `-q[:stream_specifier] q (output,per-stream)`
    `-qscale[:stream_specifier] q (output,per-stream)`

    Use fixed quality scale (VBR). The meaning of q/qscale is codec-dependent. If qscale is used without a stream_specifier then it applies only to the video stream, this is to maintain compatibility with previous behavior and as specifying the same codec specific value to 2 different codecs that is audio and video generally is not what is intended when no stream_specifier is used.
    """
    q:str = None
    stream_specifier:FFmpegStreamSpecifier = FFmpegStreamSpecifier()
    parameter_name:str = "qscale"
    option_type:classes.FFmpegOptionType = classes.FFmpegOptionType.OUTPUT
    

    @property
    def io_string(
        self,
    )->list:
        _super_io = super().io_string
        _super_io[-1] += self.stream_specifier.as_suffix(":")
        
        return _super_io + [
            f"{shlex.quote(str(self.q))}",
        ]

    @classmethod
    def create(
        cls,
        q:str,
        stream_specifier:FFmpegStreamSpecifier = FFmpegStreamSpecifier(),
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
            q = q,
            stream_specifier = stream_specifier,
            *args,
            **kwargs,
        )


@classes.ffmpegioclass
class FFmpegOptionRecastMedia(classes.FFmpegMainOptions):
    """
    `-recast_media (global)`

    Allow forcing a decoder of a different media type than the one detected or designated by the demuxer. Useful for decoding media data muxed as data streams.
    """
    parameter_name:str = "recast_media"
    option_type:classes.FFmpegOptionType = classes.FFmpegOptionType.GLOBAL_OPTIONS



@classes.ffmpegioclass
class FFmpegOptionReinitFilter(classes.FFmpegMainOptions):
    """
    `-reinit_filter[:stream_specifier] integer (input,per-stream)`

    This boolean option determines if the filtergraph(s) to which this stream is fed gets reinitialized when input frame parameters change mid-stream. This option is enabled by default as most video and all audio filters cannot handle deviation in input frame properties. Upon reinitialization, existing filter state is lost, like e.g. the frame count n reference available in some filters. Any frames buffered at time of reinitialization are lost. The properties where a change triggers reinitialization are, for video, frame resolution or pixel format; for audio, sample format, sample rate, channel count or channel layout.
    """
    integer:int = None
    parameter_name:str = "reinit_filter"
    stream_specifier:FFmpegStreamSpecifier = FFmpegStreamSpecifier()
    option_type:classes.FFmpegOptionType = classes.FFmpegOptionType.INPUT

    @property
    def io_string(
        self,
    )->list:
        _super_io = super().io_string
        _super_io[-1] += self.stream_specifier.as_suffix(":")
        
        return _super_io + [
            f"{shlex.quote(str(self.integer))}",
        ]

    @classmethod
    def create(
        cls,
        integer:int,
        stream_specifier:FFmpegStreamSpecifier = FFmpegStreamSpecifier(),
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
            integer = integer,
            stream_specifier = stream_specifier,
            *args,
            **kwargs,
        )


@classes.ffmpegioclass
class FFmpegOptionSeek(classes.FFmpegMainOptions):
    """
    `-ss position (input/output)`

    When used as an input option (before -i), seeks in this input file to position. Note that in most formats it is not possible to seek exactly, so ffmpeg will seek to the closest seek point before position. When transcoding and -accurate_seek is enabled (the default), this extra segment between the seek point and position will be decoded and discarded. When doing stream copy or when -noaccurate_seek is used, it will be preserved.

    When used as an output option (before an output url), decodes but discards input until the timestamps reach position.

    position must be a time duration specification, see (ffmpeg-utils)the Time duration section in the ffmpeg-utils(1) manual.
    """
    position:str = None
    parameter_name:str = "ss"
    option_type:classes.FFmpegOptionType = classes.FFmpegOptionType.INPUT_OUTPUT

    @property
    def io_string(
        self,
    )->list:
        _super_io = super().io_string
        
        return _super_io + [
            f"{shlex.quote(str(self.position))}",
        ]

    @classmethod
    def create(
        cls,
        position:str,
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
            position = position,
            option_type = option_type,
            *args,
            **kwargs,
        )


@classes.ffmpegioclass
class FFmpegOptionSeekFromEOF(classes.FFmpegMainOptions):
    """
    `-sseof position (input)`

    Like the -ss option but relative to the "end of file". That is negative values are earlier in the file, 0 is at EOF.
    """
    position:str = None
    parameter_name:str = "sseof"
    option_type:classes.FFmpegOptionType = classes.FFmpegOptionType.INPUT

    @property
    def io_string(
        self,
    )->list:
        _super_io = super().io_string
        
        return _super_io + [
            f"{shlex.quote(str(self.position))}",
        ]

    @classmethod
    def create(
        cls,
        position:str,
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
            position = position,
            *args,
            **kwargs,
        )


@classes.ffmpegioclass
class FFmpegOptionStats(classes.FFmpegMainOptions):
    """
    `-stats (global)`

    Print encoding progress/statistics.
    It is on by default, to explicitly disable it you need to specify `-nostats`.
    """
    parameter_name:str = "stats"
    option_type:classes.FFmpegOptionType = classes.FFmpegOptionType.GLOBAL_OPTIONS


@classes.ffmpegioclass
class FFmpegOptionStatsPeriod(classes.FFmpegMainOptions):
    """
    `-stats_period time (global)`

    Set period at which encoding progress/statistics are updated. Default is 0.5 seconds.
    """
    time:float = None
    parameter_name:str = "stats_period"
    option_type:classes.FFmpegOptionType = classes.FFmpegOptionType.GLOBAL_OPTIONS

    @property
    def io_string(
        self,
    )->list:
        _super_io = super().io_string
        
        return _super_io + [
            f"{shlex.quote(str(self.time))}",
        ]

    @classmethod
    def create(
        cls,
        time:float,
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
            time = time,
            *args,
            **kwargs,
        )


@classes.ffmpegioclass
class FFmpegOptionStdin(classes.FFmpegMainOptions):
    """
    `-stdin`

    Enable interaction on standard input. On by default unless standard input is used as an input. To explicitly disable interaction you need to specify -nostdin.

    Disabling interaction on standard input is useful, for example, if ffmpeg is in the background process group. Roughly the same result can be achieved with `ffmpeg ... < /dev/null` but it requires a shell.
    """
    parameter_name:str = "stdin"
    option_type:classes.FFmpegOptionType = classes.FFmpegOptionType.GLOBAL_OPTIONS



@classes.ffmpegioclass
class FFmpegOptionStreamLoop(classes.FFmpegMainOptions):
    """
    `-stream_loop number (input)`

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
            f"{shlex.quote(str(self.loop))}",
        ]

    @classmethod
    def create(
        cls,
        loop:int = 0,
        # option_type:classes.FFmpegOptionType = classes.FFmpegOptionType.INPUT,
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
            # option_type = option_type,
            *args,
            **kwargs,
        )    


@classes.ffmpegioclass
class FFmpegOptionDuration(classes.FFmpegMainOptions):
    """
    `-t duration (input/output)`

    When used as an input option (before `-i`), limit the duration of data read from the input file.

    When used as an output option (before an output url), stop writing the output after its duration reaches duration.

    duration must be a time duration specification, see (ffmpeg-utils)the Time duration section in the ffmpeg-utils(1) manual.

    `-to` and `-t` are mutually exclusive and `-t` has priority.
    """
    duration:str = None
    parameter_name:str = "t"
    option_type:classes.FFmpegOptionType = classes.FFmpegOptionType.INPUT_OUTPUT

    @property
    def io_string(
        self,
    )->list:
        return super().io_string + [
            f"{shlex.quote(str(self.duration))}",
        ]

    @classmethod
    def create(
        cls,
        duration:str,
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
            duration = duration,
            option_type = option_type,
            *args,
            **kwargs,
        )    

    

@classes.ffmpegioclass
class FFmpegOptionTarget(classes.FFmpegMainOptions):
    """
    `-target type (output)`

    Specify target file type (`vcd`, `svcd`, `dvd`, `dv`, `dv50`). type may be prefixed with `pal-`, `ntsc-` or `film-` to use the corresponding standard. All the format options (bitrate, codecs, buffer sizes) are then set automatically. You can just type:

    ```
        ffmpeg -i myfile.avi -target vcd /tmp/vcd.mpg
    ```

    Nevertheless you can specify additional options as long as you know they do not conflict with the standard, as in:

    ```
        ffmpeg -i myfile.avi -target vcd -bf 2 /tmp/vcd.mpg
    ```

    The parameters set for each target are as follows.

    VCD

    pal:
    ```
    -f vcd -muxrate 1411200 -muxpreload 0.44 -packetsize 2324
    -s 352x288 -r 25
    -codec:v mpeg1video -g 15 -b:v 1150k -maxrate:v 1150v -minrate:v 1150k -bufsize:v 327680
    -ar 44100 -ac 2
    -codec:a mp2 -b:a 224k
    ```

    ntsc:
    ```
    -f vcd -muxrate 1411200 -muxpreload 0.44 -packetsize 2324
    -s 352x240 -r 30000/1001
    -codec:v mpeg1video -g 18 -b:v 1150k -maxrate:v 1150v -minrate:v 1150k -bufsize:v 327680
    -ar 44100 -ac 2
    -codec:a mp2 -b:a 224k
    ```

    film:
    ```
    -f vcd -muxrate 1411200 -muxpreload 0.44 -packetsize 2324
    -s 352x240 -r 24000/1001
    -codec:v mpeg1video -g 18 -b:v 1150k -maxrate:v 1150v -minrate:v 1150k -bufsize:v 327680
    -ar 44100 -ac 2
    -codec:a mp2 -b:a 224k
    ```

    SVCD

    pal:
    ```
    -f svcd -packetsize 2324
    -s 480x576 -pix_fmt yuv420p -r 25
    -codec:v mpeg2video -g 15 -b:v 2040k -maxrate:v 2516k -minrate:v 0 -bufsize:v 1835008 -scan_offset 1
    -ar 44100
    -codec:a mp2 -b:a 224k
    ```

    ntsc:
    ```
    -f svcd -packetsize 2324
    -s 480x480 -pix_fmt yuv420p -r 30000/1001
    -codec:v mpeg2video -g 18 -b:v 2040k -maxrate:v 2516k -minrate:v 0 -bufsize:v 1835008 -scan_offset 1
    -ar 44100
    -codec:a mp2 -b:a 224k
    ```

    film:
    ```
    -f svcd -packetsize 2324
    -s 480x480 -pix_fmt yuv420p -r 24000/1001
    -codec:v mpeg2video -g 18 -b:v 2040k -maxrate:v 2516k -minrate:v 0 -bufsize:v 1835008 -scan_offset 1
    -ar 44100
    -codec:a mp2 -b:a 224k
    ```

    DVD

    pal:
    ```
    -f dvd -muxrate 10080k -packetsize 2048
    -s 720x576 -pix_fmt yuv420p -r 25
    -codec:v mpeg2video -g 15 -b:v 6000k -maxrate:v 9000k -minrate:v 0 -bufsize:v 1835008
    -ar 48000
    -codec:a ac3 -b:a 448k
    ```

    ntsc:
    ```
    -f dvd -muxrate 10080k -packetsize 2048
    -s 720x480 -pix_fmt yuv420p -r 30000/1001
    -codec:v mpeg2video -g 18 -b:v 6000k -maxrate:v 9000k -minrate:v 0 -bufsize:v 1835008
    -ar 48000
    -codec:a ac3 -b:a 448k
    ```

    film:
    ```
    -f dvd -muxrate 10080k -packetsize 2048
    -s 720x480 -pix_fmt yuv420p -r 24000/1001
    -codec:v mpeg2video -g 18 -b:v 6000k -maxrate:v 9000k -minrate:v 0 -bufsize:v 1835008
    -ar 48000
    -codec:a ac3 -b:a 448k
    ```

    DV
    ```
    pal:
    -f dv
    -s 720x576 -pix_fmt yuv420p -r 25
    -ar 48000 -ac 2

    ntsc:
    -f dv
    -s 720x480 -pix_fmt yuv411p -r 30000/1001
    -ar 48000 -ac 2

    film:
    -f dv
    -s 720x480 -pix_fmt yuv411p -r 24000/1001
    -ar 48000 -ac 2
    ```

    The `dv50` target is identical to the `dv` target except that the pixel format set is `yuv422p` for all three standards.

    Any user-set value for a parameter above will override the target preset value. In that case, the output may not comply with the target standard.
    """
    type:str = None
    parameter_name:str = "target"
    option_type:classes.FFmpegOptionType = classes.FFmpegOptionType.OUTPUT

    @property
    def io_string(
        self,
    )->list:
        return super().io_string + [
            f"{shlex.quote(str(self.type))}",
        ]

    @classmethod
    def create(
        cls,
        type:str,
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
            type = type,
            *args,
            **kwargs,
        )    
    

@classes.ffmpegioclass
class FFmpegOptionTimestamp(classes.FFmpegMainOptions):
    """
    `-timestamp date (output)`

    Set the recording timestamp in the container.

    date must be a date specification, see (ffmpeg-utils)the Date section in the ffmpeg-utils(1) manual.
    """
    date:str = None
    parameter_name:str = "timestamp"
    option_type:classes.FFmpegOptionType = classes.FFmpegOptionType.OUTPUT

    @property
    def io_string(
        self,
    )->list:
        return super().io_string + [
            f"{shlex.quote(str(self.date))}",
        ]

    @classmethod
    def create(
        cls,
        date:str,
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
            date = date,
            *args,
            **kwargs,
        )    
    

@classes.ffmpegioclass
class FFmpegOptionTo(classes.FFmpegMainOptions):
    """
    `-to position (input/output)`

    Stop writing the output or reading the input at position. position must be a time duration specification, see (ffmpeg-utils)the Time duration section in the ffmpeg-utils(1) manual.

    `-to` and `-t` are mutually exclusive and `-t` has priority.
    """
    position:str = None
    parameter_name:str = "to"
    option_type:classes.FFmpegOptionType = classes.FFmpegOptionType.INPUT_OUTPUT

    @property
    def io_string(
        self,
    )->list:
        _super_io = super().io_string
        
        return _super_io + [
            f"{shlex.quote(str(self.position))}",
        ]

    @classmethod
    def create(
        cls,
        position:str,
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
            position = position,
            *args,
            **kwargs,
        )

@classes.ffmpegioclass
class FFmpegOptionOverwrite(classes.FFmpegMainOptions):
    """
    `-y (global)`

    Overwrite output files without asking.
    """
    parameter_name:str = "y"
    option_type:classes.FFmpegOptionType = classes.FFmpegOptionType.GLOBAL_OPTIONS