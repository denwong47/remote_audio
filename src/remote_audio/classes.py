#!/usr/bin/env python3

import time as timer
import threading
from turtle import st
from typing import Any, Union

import io
import pyaudio

class StreamStatus():
    """
    A simple pointer object to a boolean,
    used to be passed to callback methods for in-callback access to stream status.
    """

    def __init__(
        self,
        timeout:int=None,
        bytes_total:int=None,
    ):
        self.set(True)

        self.bytes_total = bytes_total
        self.bytes_played = 0

        self.timeout = timeout
        self.update_last_data()
        
        self.played(0)

    def __bool__(
        self
    ):
        """
        Evaluates self to False if:
        - status is False or
        - bytes_total is completed
        - data timed out
        """
        # if (self.last_data): print (f"Timeout: {(timer.perf_counter() - self.last_data)/self.timeout:.2%} | Size: {self.bytes_played-self.bytes_total}")

        return all(
            (
                self.status,
                not self.completed,
                not self.timedout,
            )
        )
            
    __nonzero__ = __bool__

    def set(
        self,
        status:bool=True,
    ):
        self.status = status

    def update_last_data(
        self
    ):
        self.last_data = timer.perf_counter()

    def played(
        self,
        bytes_count:int,
    ):
        self.bytes_played += max(0, bytes_count)

        if (bytes_count>0):
            self.update_last_data()

    @property
    def completed(
        self
    ):
        if (isinstance(self.bytes_total, int)):
            return self.bytes_played >= self.bytes_total
        else:
            return None

    @property
    def timedout(
        self
    ):
        if (isinstance(self.timeout, (float, int))):
            return (timer.perf_counter() - self.last_data) >= self.timeout
        else:
            return None

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

    def __init__(
        self,
        stream:pyaudio.Stream,
        timeout:float=None,
        stream_status:StreamStatus=None,
    ):
        self.stream = stream
        self.timeout = timeout

        self.stream_status = stream_status

    def __bool__(self):
        return self.stream_status
    __nonzero__ = __bool__
    
    def __enter__(self):
        self.start()
        return self

    def __exit__(self, type, value, traceback):
        try:
            _lastactive = timer.perf_counter()
            while (
                self.stream_status and \
                type is None # There is no Exception
            ):
                if (self.stream.is_active()):
                    _lastactive = timer.perf_counter()
                
                timer.sleep(0.02)

            self.stream_status.set(False)

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



class BytesLoopIO(io.IOBase):
    def __init__(
        self,
        initial_bytes:Union[
            bytes,
            bytearray
        ]=b""):
        
        self.lock = threading.Lock()
        self._buffer = bytearray(initial_bytes)

    def getbuffer(
        self
    ):
        """
        Return a modifiable view of the buffer
        """
        return memoryview(self._buffer)

    def getvalue(
        self
    ):
        """
        Return the value of the buffer - this is a clone
        """
        return self._buffer

    def read(
        self,
        size:Union[
            int,
            None
        ]=None,
    )->bytearray:
        """
        Read a certain length from the buffer
        """
        with self.lock:
            # We can just pass size=None into [:size]. This actually gives the whole buffer
            _chunk = self._buffer[:size]
            self._buffer = self._buffer[len(_chunk):]

        return bytes(_chunk)

    def write(
        self,
        b:Union[
            bytes,
            bytearray
        ],
    )->None:
        """
        Write to the end of buffer
        """
        with self.lock:
            self._buffer += bytearray(b)