#!/usr/bin/env python3
import os, sys
from typing import Any, BinaryIO, Dict, Union


import pyaudio
import wave

from remote_audio import api
import remote_audio
from remote_audio.classes import AudioStream, StreamStatus

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
    bytes_total:int=None,
    timeout:float=None,
    exit_interrupt:bool=False,
    **kwargs,
)->AudioStream:
    """
    Start an AudioStream from a binary IO object.

    The stream is non-blocking - an AudioStream object will be returned as soon as the stream starts.
    """

    _p = api.pya

    _wHnd = wave.open(io, "rb")

    if (not bytes_total):
        if (isinstance(io, str)):
            # io is a path
            if (os.path.exists(io)):
                # io exists
                # Use get_wav_size - this removes the 44/46-byte header size.
                bytes_total = remote_audio.io.file.get_wav_data_size(io)

    # Initiate a StreamStatus
    _stream_status = StreamStatus(
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