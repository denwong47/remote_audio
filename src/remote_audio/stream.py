#!/usr/bin/env python3

import time as timer
import warnings
from typing import Any, Union


import pyaudio

import remote_audio

DEFAULT_TIMEOUT = 5


class StreamStatus():
    """
    A simple pointer object to a boolean,
    used to be passed to callback methods for in-callback access to stream status.
    """

    def __init__(
        self,
        timeout:int=None,
        io:'remote_audio.io.base_io.StreamIO'=None,
        bytes_total:Union[
            int,
            "remote_audio.io.base_io.StreamIO",
        ]=None,
    ):
        self.set(True)

        self.io = io
        self.bytes_total = bytes_total if bytes_total else (self.io if isinstance(self.io, remote_audio.io.base_io.StreamIO) else None)
        self.bytes_played = 0

        if (self.bytes_total is None and timeout is None):
            warnings.warn(
                RuntimeWarning(
                    "timeout needs to be specified if bytes_total is not; otherwise stream cannot end. Timeout set to default."
                )
            )
            timeout = DEFAULT_TIMEOUT

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
        # if (self.last_data): print (f"Timeout: {timer.perf_counter()-self.last_data:.2f} | Size: {self.bytes_played-self.bytes_total}")

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

    @property
    def bytes_total(
        self,
    ):
        """
        Total number of bytes anticipated, in wave form.

        Return itself if its an int;
        Return current io.bytes_total if its a StreamIO object.

        This is because StreamIO may not know the true length of the data at the start of stream,
        and will only update its .bytes_total when its own streaming ends.

        Hence this property needs to dynamically update.
        """
        if (isinstance(self._bytes_total_origin, remote_audio.io.base_io.StreamIO)):
            return self._bytes_total_origin.bytes_total
        else:
            return self._bytes_total_origin

    @bytes_total.setter
    def bytes_total(
        self,
        value:Union[
            int,
            "remote_audio.io.base_io.StreamIO",
        ]
    ):
        self._bytes_total_origin = value

    @property
    def bytes_written(
        self,
    ):
        """
        Bytes written by `io` so far.

        Only valid if `io` is specified, and it is a `StreamIO` instance.
        """

        if (isinstance(self.io, remote_audio.io.base_io.StreamIO)):
            return self.io.bytes_written
        else:
            return None
    
    @property
    def bytes_buffered(
        self,
    ):
        """
        Bytes that are buffered, but not yet played.

        Only valid if `io` is specified, and it is a `StreamIO` instance.
        """

        if (isinstance(_written := self.bytes_written, int) and isinstance(_played := self.bytes_played, int)):
            return _written - _played
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
        exit_interrupt:bool=False,
    ):
        self.stream = stream
        self.timeout = timeout

        self.stream_status = stream_status

        self.exit_interrupt = exit_interrupt

    def __bool__(self):
        return self.stream_status
    __nonzero__ = __bool__
    
    def __enter__(self):
        self.start()
        return self

    def __exit__(self, type, value, traceback):
        try:
            while (
                self.stream_status and \
                not self.exit_interrupt and \
                type is None # There is no Exception
            ):    
                # Wait it out if stream hasn't finished by end of context
                timer.sleep(0.1)

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




