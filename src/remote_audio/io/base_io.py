import asyncio

import io
import threading
import time as timer
from typing import Any, Callable, Dict, Iterable, Union

import remote_audio
import remote_audio.io.file as file
import remote_audio.io.http as http
import remote_audio.exceptions as exceptions


class StreamIO(io.BytesIO):
    """
    An IO File-like object class that allows both .read() and .write().
    
    Typically .read() and .write() requests are done by different threads;
    this class is thread-safe by putting a threading.Lock.
    There is performance degradation in the short blocking time.
    
    """

    def __init__(
        self,
        initial_bytes:bytes = b"",
        bytes_total:int = None,             # Optional - does not affect the class
        *args,
        **kwargs,
    ):
        self.lock = threading.Lock()
        self.bytes_written = 0
        self.bytes_total = bytes_total

        super().__init__(*args, **kwargs)   # Do not put the initial_bytes in - otherwise bytes_written will be wrong

        if (initial_bytes):
            self.write(initial_bytes)

        pass

    def read(
        self,
        *args,
        **kwargs,
    ):
        """
        Read bytes within thread lock.
        """

        with self.lock:
            return super().read(*args, **kwargs)
            

    def write(
        self,
        b:bytes,
        *args,
        **kwargs,
    ):
        """
        Append bytes to the back of the buffer within thread lock.
        
        It uses .tell() to recall the current .read() position,
        then restore it after writing.

        During this time, the thread is locked hence no .read() is possible.
        """

        with self.lock:
            _pos = self.tell()
            self.seek(0, io.SEEK_END)

            _return = super().write(b, *args, **kwargs)

            self.seek(_pos, io.SEEK_SET)

            self.bytes_written += len(b)

        return _return
    
    def await_data(
        self,
        size:int=2**10,
        timeout:float=3,
        interval:float=0.2,
        callback:Callable[["StreamIO", int], None]=None,
    ):
        """
        A blocking function that only finish when either
        - "size" amount of bytes had been written, or
        - timeout has lapsed
        """
        _start = timer.perf_counter()

        while (
            (timer.perf_counter() < (_start+timeout)) and \
            self.bytes_written < size
        ):
            if (callable(callback)):
                callback(
                    self,
                    self.bytes_written,
                )

            timer.sleep(interval)


class WaveStreamIO(StreamIO):
    """
    An IO File-like object class for WAV files only that allows both .read() and .write().
    Suitable for AudioStreaming over slow I/O.

    When initialised, it accepts as initial_bytes:
    - str: path to WAV file
    - io object: a file like object that can be .read()
    - bytes: raw binary data
    
    Then it will check the header of the WAV file;
    - if valid, returns an IO object that already have the header buffered.
    - if invalid, returns a FileIOError or WavFormatError instance.
    """

    def __new__(
        cls,
        initial_bytes:Union[
            bytes,
            str,
            io.IOBase
        ]=b"",
        bytes_total:int = None,
        *args,
        **kwargs,
    )->"WaveStreamIO":
        """
        Prior to constructing the instance,
        check if header is valid
        """

        _header = file.WavHeader.from_data(
            initial_bytes,
        )
        
        if (_header):
            # Header is valid

            return super(WaveStreamIO, cls).__new__(
                cls,
                *args,
                **kwargs,
            )
        else:
            # Return the exception
            return _header.is_valid
    
    def __init__(
        self,
        initial_bytes:Union[
            bytes,
            str,
            io.IOBase,
        ],
        bytes_total:int = None,
        *args,
        **kwargs
    )->None:
        """
        Get the header of the WAV file and buffer it already.
        This allow wave.open() to initialise immediately;
        otherwise wave will throw EOFError without the header.
        """

        super().__init__(
            initial_bytes = initial_bytes,
            bytes_total = bytes_total,
            *args,
            **kwargs,
        )

    @classmethod
    def from_file(
        cls,
        path:str,
        chunk_size:int=file.DEFAULT_FILE_CHUNK_SIZE,
        callback:Callable[["remote_audio.io.ffmpeg.command.FFmpegCommand", int], None] = None,
    ):
        """
        Play a WAV file from local file.

        Uses threading to load the file in chunks - does not read the whole file in one block.
        This allows for slow I/O like memory cards or network storages to not block execution.
        """

        # This is a bit weird, but we ought to at least get the header of the file through before we start a stream.
        # So we should at least read the first 44 bytes of the file, and feed it as initial_bytes.
        chunk_size = max(chunk_size, 44)
        _size = file.get_file_size(path=path)

        if (_size):
            _f = open(path, "r+b")
            
            try:
                _initial_bytes = _f.read(chunk_size)
                _io = cls(
                    initial_bytes = _initial_bytes,
                    bytes_total = _size,
                )

            except (
                    IOError,
                    OSError,
                    FileNotFoundError,
                ) as e:
                _f.close()
                return exceptions.FileIOError(f"Fails to read header from {path}.")

            # This is the function to hand off to threading
            def _iter_callback(
                gen:Callable[[], bytes],
                push_data:Callable[[bytes,], None],
            ):
                bytes_total = len(_initial_bytes)
                try:
                    # Different from HTTP - gen is a callable here
                    while (_data := gen()):
                        bytes_total += len(_data)
                        push_data(_data)

                    if (callback):
                        callback(
                            None, # None instead of FFmpegCommand - we didn't use one
                            bytes_total,
                        )

                except (
                    IOError,
                    OSError,
                    FileNotFoundError,
                ) as e:
                    pass
                finally:
                    _f.close()

            # Fire and forget: start piping file to IO
            threading.Thread(target=lambda : _iter_callback(
                        gen = lambda : _f.read(chunk_size),
                        push_data = _io.write,
                    )).start()

            return _io
        else:
            return exceptions.FileIOError(f"{path} not readable.")

    @classmethod
    def from_http(
        cls,
        url:str,
        timeout:float = http.DEFAULT_HTTP_TIMEOUT,
        chunk_size:int = http.DEFAULT_HTTP_CHUNK_SIZE,
        params:Dict[str, Any]={},
        callback:Callable[["remote_audio.io.ffmpeg.command.FFmpegCommand", int], None] = None,
        **kwargs,
    )->Union[
        "WaveStreamIO",
        Exception,
    ]:
        """
        Play a WAV file from HTTP address.

        Uses threading to load the request in chunks - does not read the whole file in one block.
        This allows for slow connection to not block exeuction.
        """

        # Request returned 200 OK
        _data_generator = http.iter_http_data(
            url = url,
            params = params,
            timeout = timeout,
            chunk_size = max(46, chunk_size), # chunk_size cannot be smaller than a single header
            **kwargs,
        )

        if (_data_generator):
            # If a valid generator was returned

            _data_chunk = next(_data_generator)
            _header = file.WavHeader.from_data(_data_chunk)

            if (_header):
                # If the header is complete and valid, build our WaveStreamIO object
                _io = cls(
                    initial_bytes = _data_chunk,
                    bytes_total = _header.data_size,
                )
                
            else:
                # If the header it not valid, it will be an Exception already detailing what went wrong
                return _header
        
            # Loop for rest of generator to download data
            def _iter_callback(
                gen:Iterable[bytes],
                push_data:Callable[[bytes], None],
            )->None:
                bytes_total = 0
                for _data_chunk in gen:
                    # Thread?
                    bytes_total += len(_data_chunk)
                    push_data(_data_chunk)
                
                if (callback):
                    callback(
                        None, # None instead of FFmpegCommand - we didn't use one
                        bytes_total,
                    )

            # Fire and forget: start downloading
            threading.Thread(target=lambda : _iter_callback(
                        gen = _data_generator,
                        push_data = _io.write,
                    )).start()
            
            return _io
    
        else:
            return _data_generator

