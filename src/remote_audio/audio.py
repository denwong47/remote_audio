#!/usr/bin/env python3
import os, sys
from typing import Any, BinaryIO, Callable, Dict, Union


import pyaudio
import wave

from remote_audio import api, device
import remote_audio
from remote_audio.exceptions import InvalidInputParameters
from remote_audio.stream import AudioStream, StreamStatus, DEFAULT_TIMEOUT

DEFAULT_CHUNK_SIZE = 1024


def create_stream_callback(
    wHnd:wave.Wave_read,
    chunk_size:int=DEFAULT_CHUNK_SIZE,
    stream_status:StreamStatus=None,
    ):
    """
    From a wave_read object, feed chunks of data to the stream.
    To be used with steam_callback in pyaudio methods.
    """

    def wrapper(
        in_data:Union[
            bytes,
            None,
        ],
        frame_count:int,
        time_info:Dict[
            str, Any
        ],
        status_flags:int,
    ):
        _data = wHnd.readframes(chunk_size)

        if (isinstance(stream_status, StreamStatus)):
            # Record amount of bytes played to StreamStatus
            stream_status.played(len(_data))

            _status = pyaudio.paContinue if (_data or stream_status) else pyaudio.paComplete
            if (not stream_status.timedout):
                # arbitarily keeping stream alive by feeding null bytes
                _data += b"\x00"*(chunk_size*wHnd.getnchannels()*wHnd.getsampwidth()-len(_data))
        else:
            _status = pyaudio.paContinue if (_data) else pyaudio.paComplete

        return (_data, _status)

    return wrapper

def start_wav_stream(
    io:Union[
        BinaryIO,
        str,
    ],
    device_index:Union[
        int,
        None
    ]=None,
    chunk_size:int=DEFAULT_CHUNK_SIZE,
    start:bool=True,
    bytes_total:Union[
        int,
        "remote_audio.io.base_io.StreamIO",
        None,
    ]=None,
    timeout:float=DEFAULT_TIMEOUT,
    exit_interrupt:bool=False,
    **kwargs,
)->AudioStream:
    """
    Start an AudioStream from a binary IO object.

    The stream is non-blocking - an AudioStream object will be returned as soon as the stream starts.

    Returns a AudioStream;
    use this function as context manager:
    ```
    with start_wav_stream(io, device_index) as _stream:
        pass
    ```
    """

    _p = api.pya

    _wHnd = wave.open(io, "rb")

    if (bytes_total is None):
        if (isinstance(io, str)):
            # io is a path
            if (os.path.exists(io)):
                # io exists
                # Use get_wav_size - this removes the 44/46-byte header size.
                bytes_total = remote_audio.io.file.get_wav_data_size(io)
        elif (isinstance(io, remote_audio.io.base_io.StreamIO)):
            # io is a StreamIO
            # That means it has .bytes_total,
            # and StreamStatus supports having a StreamIO as bytes_total
            bytes_total = io

    # Initiate a StreamStatus
    _stream_status = StreamStatus(
        io=io,
        bytes_total=bytes_total,
        timeout=timeout,
    )
    
    _stream = _p.open(output_device_index=device_index,
                      format=_p.get_format_from_width(_wHnd.getsampwidth()),
                      channels=_wHnd.getnchannels(),
                      rate=_wHnd.getframerate(),
                      output=True,
                      start=start,
                      stream_callback=create_stream_callback(
                          wHnd=_wHnd,
                          chunk_size=chunk_size,
                          stream_status=_stream_status,
                      ),
                      **kwargs,
    )

    # Return an AudioStream instance that can control the playback within a context.
    return AudioStream(
        _stream,
        timeout=timeout,
        stream_status=_stream_status,
        exit_interrupt=exit_interrupt,
    )

def get_format_class(
    format:str
)->Union[
    "remote_audio.io.base_io.StreamIO",
    None,
]:
    """
    Look for the relevant StreamIO class that corresponds to `format`.
    Returns None if not found.
    """

    format = format.upper()

    _wav_formats = ("WAV", "WAVE")

    if (format in _wav_formats):
        return remote_audio.io.base_io.WaveStreamIO
    else:
        return getattr(remote_audio.classes, f"{format}StreamIO", None)

def play_file(
    path:str,
    format:str=None,
    device_index:Union[
        int,
        None
    ]=None,
    chunk_size:int=DEFAULT_CHUNK_SIZE,
    start:bool=True,
    bytes_total:Union[
        int,
        "remote_audio.io.base_io.StreamIO",
        None,
    ]=None,
    timeout:float=DEFAULT_TIMEOUT,
    exit_interrupt:bool=False,
    callback:Callable[[remote_audio.io.ffmpeg.command.FFmpegCommand, int], None] = None,
    **kwargs,
)->AudioStream:
    """
    Play a local audio file.
    If `format` is not provided, it will use the file suffix.

    Returns a AudioStream;
    use this function as context manager:
    ```
    with play_file("file.mp3", device_index=device_index) as _stream:
        pass
    ```
    """
    if (not format):
        format = path.split(".")[-1]
    _format_class = get_format_class(format)

    if (_format_class):
        _io = _format_class.from_file(
            path =          path,
            callback =      callback,
        )
        
        return start_wav_stream(
            io =            _io,
            device_index =  device_index,
            chunk_size =    chunk_size,
            start =         start,
            bytes_total =   bytes_total,
            timeout =       timeout,
            exit_interrupt= exit_interrupt,
            **kwargs,
        )
    else:
        return InvalidInputParameters(f"{format} is not a valid format.")

def play_http(
    url:str,
    format:str=None,
    device_index:Union[
        int,
        None
    ]=None,
    chunk_size:int=DEFAULT_CHUNK_SIZE,
    start:bool=True,
    bytes_total:Union[
        int,
        "remote_audio.io.base_io.StreamIO",
        None,
    ]=None,
    timeout:float=DEFAULT_TIMEOUT,
    exit_interrupt:bool=False,
    callback:Callable[[remote_audio.io.ffmpeg.command.FFmpegCommand, int], None] = None,
    **kwargs,
)->AudioStream:
    """
    Play an audio file over HTTP.
    If `format` is not provided, it will use the file suffix.

    Returns a AudioStream;
    use this function as context manager:
    ```
    with play_http("https://somedomain.com/file.mp3", device_index=device_index) as _stream:
        pass
    ```
    """

    if (not format):
        format = url.split(".")[-1]
    _format_class = get_format_class(format)

    if (_format_class):
        _io = _format_class.from_http(
            url =           url,
            callback =      callback,
        )
        
        return start_wav_stream(
            io =            _io,
            device_index =  device_index,
            chunk_size =    chunk_size,
            start =         start,
            bytes_total =   bytes_total,
            timeout =       timeout,
            exit_interrupt= exit_interrupt,
            **kwargs,
        )
    else:
        return InvalidInputParameters(f"{format} is not a valid format.")