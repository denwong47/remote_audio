#!/usr/bin/env python3


from enum import Enum
from typing import Any, Dict, Iterable, Union
import warnings

from remote_audio.io.ffmpeg.formats import FFMPEG_FORMATS
import remote_audio.io.ffmpeg.classes as classes



"""
FFmpeg Stream Specifiers
https://ffmpeg.org/ffmpeg.html#Stream-specifiers-1
"""

class FFmpegStreamType(Enum):
    VIDEO="v"
    VIDEO_NONATTACH="V"
    AUDIO="a"
    SUBTITLE="s"
    DATA="d"
    ATTACHMENT="t"

    def __repr__(self):
        """
        Why doesn't Enum does this automatically????
        """
        return f"{type(self).__name__}.{self.name}"

@classes.ffmpegioclass
class FFmpegStreamSpecifier():
    """
    ```
    FFmpegStreamSpecifier(
        stream_index:int = None
        stream_type:Iterable[Union[str, FFmpegStreamType]] = None
        pid:int = None
        stream_id:int = None
        metadata:Dict[str, Union[str, None]] = None
        usable:bool = False
    )->FFmpegStreamSpecifier
    ```

    Some options are applied per-stream, e.g. bitrate or codec. Stream specifiers are used to precisely specify which stream(s) a given option belongs to.

    A stream specifier is a string generally appended to the option name and separated from it by a colon. E.g. -codec:a:1 ac3 contains the a:1 stream specifier, which matches the second audio stream. Therefore, it would select the ac3 codec for the second audio stream.

    A stream specifier can match several streams, so that the option is applied to all of them. E.g. the stream specifier in -b:a 128k matches all audio streams.

    An empty stream specifier matches all streams. For example, -codec copy or -codec: copy would copy all the streams without reencoding.

    Possible forms of stream specifiers are:

    stream_index
        Matches the stream with this index. E.g. -threads:1 4 would set the thread count for the second stream to 4. If stream_index is used as an additional stream specifier (see below), then it selects stream number stream_index from the matching streams. Stream numbering is based on the order of the streams as detected by libavformat except when a program ID is also specified. In this case it is based on the ordering of the streams in the program. 

    stream_type[:additional_stream_specifier]
        stream_type is one of following: 'v' or 'V' for video, 'a' for audio, 's' for subtitle, 'd' for data, and 't' for attachments. 'v' matches all video streams, 'V' only matches video streams which are not attached pictures, video thumbnails or cover arts. If additional_stream_specifier is used, then it matches streams which both have this type and match the additional_stream_specifier. Otherwise, it matches all streams of the specified type. 
        
    p:program_id[:additional_stream_specifier]
        Matches streams which are in the program with the id program_id. If additional_stream_specifier is used, then it matches streams which both are part of the program and match the additional_stream_specifier.

    #stream_id or i:stream_id
        Match the stream by stream id (e.g. PID in MPEG-TS container). 

    m:key[:value]
        Matches streams with the metadata tag key having the specified value. If value is not given, matches streams that contain the given tag with any value. 

    u
        Matches streams with usable configuration, the codec must be defined and the essential information such as video dimension or audio sample rate must be present.

    Note that in ffmpeg, matching by metadata will only work properly for input files. 
    """
    
    stream_index:int = None
    stream_type:Union[
        str,
        FFmpegStreamType,
        Iterable[
            Union[
                str,
                FFmpegStreamType
            ]
        ]
    ] = None
    pid:int = None
    stream_id:int = None
    metadata:Dict[str, Union[str, None]] = None
    usable:bool = False

    def __str__(self)->str:
        """
        Possible Formats:

        :u
        :m:key[:value]
        :i:stream_id
        :p:pid[:stream_type][:stream_index]
        """

        if (self.usable):
            _return = "u"
        elif (self.metadata):
            _return = f"m:{list(self.metadata.keys())[0]}"
            if (list(self.metadata.values())[0] is not None):
                _return += f":{list(self.metadata.values())[0]}"
        elif (self.stream_id):
            _return = f"i:{self.stream_id:d}"
        else:
            _items = []

            if (self.pid):
                _items.append("p")
                _items.append(f"{self.pid:d}")
            
            if (self.stream_type):
                _items.append(":".join(
                    [stream_type.value for stream_type in self.stream_type],
                ))
            
            # Need to allow for stream_index = 0
            if (self.stream_index is not None):
                _items.append(f"{self.stream_index:d}")
            
            _return = ":".join(
                _items
            )

        return _return

    def __post_init__(self):
        """
        Issue warnings about improper parameters
        """
        # Make stream_type a list - so that s:a:0 can be used.
        if (not isinstance(self.stream_type, (list, tuple))):
            if (isinstance(self.stream_type, str)):
                # Allow for "s:a" etc
                self.stream_type = self.stream_type.split(":")
            elif (self.stream_type is None):
                self.stream_type = []
            else:
                self.stream_type = [self.stream_type, ]
 
        for _id, _stream_type in enumerate(self.stream_type):
            if (isinstance(_stream_type, str)):
                self.stream_type[_id] = FFmpegStreamType(_stream_type)

        if (self.usable):
            if (self.stream_index or \
                self.stream_type or \
                self.pid or \
                self.stream_id or \
                self.metadata):
                
                warnings.warn(
                    UserWarning(
                        f"FFmpegStreamSpecifier :u option does not accept any additional specifiers; the rest will be disregarded."
                    )
                )
        
        elif (self.metadata):
            if (self.stream_index or \
                self.stream_type or \
                self.pid or \
                self.stream_id):
                
                warnings.warn(
                    UserWarning(
                        f"FFmpegStreamSpecifier :m option does not accept any additional specifiers; the rest will be disregarded."
                    )
                )
            elif (len(self.metadata) > 1):
                warnings.warn(
                    UserWarning(
                        f"FFmpegStreamSpecifier :m only accepts one set of key:value; the rest will be disregarded."
                    )
                )
            
        elif (self.stream_id):
            if (self.stream_index or \
                self.stream_type or \
                self.pid or \
                self.metadata):

                warnings.warn(
                    UserWarning(
                        f"FFmpegStreamSpecifier :i option does not accept any additional specifiers; the rest will be disregarded."
                    )
                )
            elif (not isinstance(self.stream_id, int)):
                raise ValueError(
                    f"FFmpegStreamSpecifier :i option expects an int only, {type(self.stream_id).__name__} found."
                )

    def as_suffix(
        self,
        sep:str=":",
    )->str:
        _str = str(self)

        if (_str):
            _str = sep + _str

        return _str