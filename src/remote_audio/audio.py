#!/usr/bin/env python3
import time as timer
from typing import Any, BinaryIO, Dict, Union


import pyaudio
import wave

from remote_audio import api


DEFAULT_CHUNK_SIZE = 1024

class AudioStream():
    """
    AudioStream wrapper for non-blocking pyaudio.Stream objects.

    You can use it as a context manager,
    i.e.
            with AudioDevice.find_first(name="Buds").start_wav_stream(
                _f1
            ) as _stream1:
                pass

    Which with only complete the context when the full audio clip had been played.

    Or:
    Use it with .start() and .stop() manually.
    """

    def __init__(self, stream:pyaudio.Stream):
        self.stream = stream

    def __bool__(self):
        return self.stream.is_active()
    __nonzero__ = __bool__
    
    def __enter__(self):
        self.start()
        return self

    def __exit__(self, type, value, traceback):
        
        try:
            while (self.stream.is_active()):
                timer.sleep(0.02)

        except OSError as e:
            pass

        self.stop()


    def start(self):
        self.stream.start_stream()

    def stop(self):
        try:
            self.stream.stop_stream()
            self.stream.close()
        except OSError as e:
            pass

def create_stream_callback(
    wHnd:wave.Wave_read,
    chunk_size:int=DEFAULT_CHUNK_SIZE,
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

        return (_data, pyaudio.paContinue if _data else pyaudio.paComplete)

    return wrapper

def start_wav_stream(
    io:BinaryIO,
    device_index:Union[
        int,
        None
    ]=None,
    chunk_size:int=DEFAULT_CHUNK_SIZE,
    **kwargs,
)->AudioStream:
    _p = api.pya
    
    _wHnd = wave.open(io, "rb")

    # _stream = _p.open(output_device_index=device_index,
    #                   format=_p.get_format_from_width(_wHnd.getsampwidth()),
    #                   channels=_wHnd.getnchannels(),
    #                   rate=_wHnd.getframerate(),
    #                   output=True,
    #                   start=True,
    #                   stream_callback=None, # We need to call stream.write, can't use nonblocking
    #                   )

    # _chunk_count = 0
    
    # while (_data := _wHnd.readframes(chunk_size)):
    #     try:
    #         _stream.write(_data)
    #         _chunk_count += 1
    #     except KeyboardInterrupt as e:
    #         break

    # _stream.stop_stream()
    # _stream.close()

    _stream = _p.open(output_device_index=device_index,
                      format=_p.get_format_from_width(_wHnd.getsampwidth()),
                      channels=_wHnd.getnchannels(),
                      rate=_wHnd.getframerate(),
                      output=True,
                      start=True,
                      stream_callback=create_stream_callback(_wHnd)
    )

    return AudioStream(_stream)