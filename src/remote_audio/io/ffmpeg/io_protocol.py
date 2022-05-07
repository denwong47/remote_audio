#!/usr/bin/env python3
import os
import re
from typing import Any, Union

import remote_audio.io.ffmpeg.classes as classes
from remote_audio.exceptions import InvalidInputParameters

"""
FFmpeg Input and Output protocols
https://ffmpeg.org/ffmpeg-protocols.html

TODO This is INCOMPLETE
"""

@classes.ffmpegioclass
class FFmpegProtocolFile(classes.FFmpegProtocol):
    """
    File access protocol.
    https://ffmpeg.org/ffmpeg-protocols.html#file

    Read from or write to a file.

    Use with FFmpegProtocolFile.create();
    calling __init__() of the class is not user-friendly.
    """

    path:str = "./"

    truncate:int = None
    blocksize:int = None
    follow:int = None
    seekable:int = None

    option_type:classes.FFmpegOptionType = classes.FFmpegOptionType.INPUT_OUTPUT

    options_list:tuple = (
        "rw_timeout",
        "truncate",
        "blocksize",
        "follow",
        "seekable",
    )

    @classmethod
    def create(
        cls,
        path:str,
        *args,
        **kwargs,
    )->"FFmpegProtocolFile":
        """
        Create an instance of the class using path alone.

        This class method is necessary because the class inheritance messed up the 
        ordering of parameters of __init__.
        Currently __init__(
            option_type,
            rw_timeout,
            ...
        )
        which makes it hard to call __init__ intuitively.
        """

        return cls(
            path=path,
            *args,
            **kwargs,
        )

    @property
    def io_string(
        self
    )->list:
        return [f"file:{self.path}"]

    @property
    def exists(self):
        return os.path.exists(self.path)


@classes.ffmpegioclass
class FFmpegProtocolData(classes.FFmpegProtocol):
    """
    Data in-line in the URI.
    https://ffmpeg.org/ffmpeg-protocols.html#data

    Example: "data:image/gif;base64,R0lGODdhCAAIAMIEAAAAAAAA//8AAP//AP///////////////ywAAAAACAAIAAADF0gEDLojDgdGiJdJqUX02iB4E8Q9jUMkADs="

    Use with FFmpegProtocolData.from_data();
    calling __init__() of the class is not user-friendly.

    See http://en.wikipedia.org/wiki/Data_URI_scheme. 
    """

    mime_type:str= "audio"
    mime_subtype:str = "mpeg"
    encoding:str = "base64"
    raw_data:str = ""

    option_type:classes.FFmpegOptionType = classes.FFmpegOptionType.INPUT

    options_list:tuple = (
        "rw_timeout",
    )

    @property
    def io_string(self)->list:
        return [self.data]

    @property
    def mime(self):
        if (self.mime_type is None or \
            self.mime_subtype is None):
            return ""
        else:
            return f"{self.mime_type}/{self.mime_subtype}"

    @mime.setter
    def mime(
        self,
        value:str,
    ):
        _pattern = re.compile(
            r"^(?P<mime_type>\w+)/(?P<mime_subtype>\w+)$"
        )
        
        _parsed = _pattern.match(value)

        if (_parsed):
            self.mime_type = _parsed.group("mime_type")
            self.mime_subtype = _parsed.group("mime_subtype")
        else:
            raise InvalidInputParameters(
                f"'{value}' is not a valid mime_type format."
            )
    
    @property
    def data(self):
        return f"data:{self.mime}{(';'+self.encoding) if (self.encoding) else ''},{self.raw_data}"

    @data.setter
    def data(
        self,
        value:str,
    ):
        _pattern = re.compile(
            r"^data:(?:(?P<mime_type>\w+)/(?P<mime_subtype>[\w\-\+]+))?(?:;(?P<encoding>\w+))?,(?P<raw_data>.+)$"
        )
        
        _parsed = _pattern.match(value)

        if (_parsed):
            self.mime_type = _parsed.group("mime_type")
            self.mime_subtype = _parsed.group("mime_subtype")
            self.encoding = _parsed.group("encoding")
            self.raw_data = _parsed.group("raw_data")

        else:
            raise InvalidInputParameters(
                f"'{value}' is not a valid data chunk."
            )

    @classmethod
    def from_data(
        cls,
        data:str,
        *args,
        **kwargs,
    )->"FFmpegProtocolData":
        """
        Create an instance of the class using data alone.
        
        This class method is necessary because the class inheritance messed up the 
        ordering of parameters of __init__.
        Currently __init__(
            option_type,
            rw_timeout,
            ...
        )
        which makes it hard to call __init__ intuitively.
        """

        _instance = cls(
            *args,
            **kwargs,
        )
        _instance.data = data

        return _instance

    create = from_data

@classes.ffmpegioclass
class FFmpegProtocolHTTP(classes.FFmpegProtocol):
    """
    HTTP (Hyper Text Transfer Protocol).
    https://ffmpeg.org/ffmpeg-protocols.html#http

    Streams a file over HTTP.

    Use with FFmpegProtocolHTTP.create();
    calling __init__() of the class is not user-friendly.
    """
    url:str = "http://localhost"

    seekable:int = None
    chunked_post:int = None
    content_type:str = None
    http_proxy:str = None
    headers:str = None
    multiple_requests:int = None
    post_data:str = None
    referer:str = None
    user_agent:str = None
    reconnect_at_eof:bool = None
    reconnect_streamed:bool = None
    reconnect_on_network_error:bool = None
    reconnect_on_http_error:bool = None
    reconnect_delay_max:int = None
    mime_type:str = None
    http_version:str = None
    icy:int = None
    icy_metadata_headers:str = None
    icy_metadata_packet:str = None
    cookies:str = None
    offset:int = None
    end_offset:int = None
    method:str = None
    listen:int = None
    send_expect_100:int = None
    auth_type:str = None
    
    option_type:classes.FFmpegOptionType = \
        classes.FFmpegOptionType.INPUT # -listen is not supported yet

    options_list:tuple = (
        "rw_timeout",
        "seekable",
        "chunked_post",
        "content_type",
        "http_proxy",
        "headers",
        "multiple_requests",
        "post_data",
        "referer",
        "user_agent",
        "reconnect_at_eof",
        "reconnect_streamed",
        "reconnect_on_network_error",
        "reconnect_on_http_error",
        "reconnect_delay_max",
        "mime_type",
        "http_version",
        "icy",
        "icy_metadata_headers",
        "icy_metadata_packet",
        "cookies",
        "offset",
        "end_offset",
        "method",
        "listen",
        "send_expect_100",
        "auth_type",
    )

    @property
    def io_string(
        self
    )->list:
        """
        Return the input/output part of command line.
        Checks if url begins with http[s]://.
        """
        _pattern = re.compile(r"^https?://.+")

        if (_pattern.match(self.url)):
            return [self.url]
        else:
            # Assume HTTPS automatically
            return [f"https://{self.url}"]


    @classmethod
    def create(
        cls,
        url:str,
        *args,
        **kwargs,
    )->"FFmpegProtocolFile":
        """
        Create an instance of the class using path alone.

        This class method is necessary because the class inheritance messed up the 
        ordering of parameters of __init__.
        Currently __init__(
            option_type,
            rw_timeout,
            ...
        )
        which makes it hard to call __init__ intuitively.
        """

        return cls(
            url=url,
            *args,
            **kwargs,
        )


@classes.ffmpegioclass
class FFmpegProtocolPipe(classes.FFmpegProtocol):
    """
    UNIX pipe access protocol.

    Read and write from UNIX pipes. 
    https://ffmpeg.org/ffmpeg-protocols.html#pipe

    The accepted syntax is:

        pipe:[number]

    number is the number corresponding to the file descriptor of the pipe (e.g. 0 for stdin, 1 for stdout, 2 for stderr). If number is not specified, by default the stdout file descriptor will be used for writing, stdin for reading. 


    Use with FFmpegProtocolPipe.create();
    calling __init__() of the class is not user-friendly.
    """

    pipe:Union[int, str] = ""   # default to positional pipe, otherwise 0 = stdin, 1 = stdout, 2 = stderr
    
    blocksize:int = None

    option_type:classes.FFmpegOptionType = \
        classes.FFmpegOptionType.INPUT_OUTPUT # -listen is not supported yet

    options_list:tuple = (
        "rw_timeout",
        "blocksize",
    )

    def __post_init__(
        self,
    ) -> None:
        if (isinstance(self.pipe, str)):
            _pipe_mapper = {
                "stdin":0,
                "stdout":1,
                "stderr":2,
            }
            
            # Map the pipe if found in mapper, otherwise leave it be.
            self.pipe = _pipe_mapper.get(self.pipe.lower(), self.pipe)

    @property
    def io_string(
        self,
    )->list:
        return [f"pipe:{self.pipe}"]


    @classmethod
    def create(
        cls,
        pipe:Union[
            str,
            int,
        ]="",
        *args,
        **kwargs,
    )->"FFmpegProtocolPipe":
        """
        Create an instance of the class using path alone.

        This class method is necessary because the class inheritance messed up the 
        ordering of parameters of __init__.
        Currently __init__(
            option_type,
            rw_timeout,
            ...
        )
        which makes it hard to call __init__ intuitively.
        """

        return cls(
            pipe=pipe,
            *args,
            **kwargs,
        )

# TODO add support for other protocols