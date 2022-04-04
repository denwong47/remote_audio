import asyncio

import io
import threading
import time as timer
from typing import Any, Callable, Dict, Iterable, Union

import remote_audio.io.file as file
import remote_audio.io.http as http





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

        # _header = file.WavHeader.from_data(
        #     initial_bytes,
        # )

        # - Do we need below?
        #   We can start the stream with a minimum of 44 bytes,
        #   but if initial_bytes is more than that we should just feed the whole thing through?

        # # TODO make a file.WavHeader.construct() method that regenerates the bytes?
        # _header_size = _header.header_size
        # if (isinstance(initial_bytes, bytes)):
        #     _data = initial_bytes[:_header_size]
        # elif (isinstance(initial_bytes, str)):
        #     with open(initial_bytes, "rb") as _f:
        #         _data = _f.read(_header_size)
        # elif (isinstance(initial_bytes, io.IOBase)):
        #     _data = initial_bytes.read(_header_size)

        super().__init__(
            initial_bytes = initial_bytes,
            bytes_total = bytes_total,
            *args,
            **kwargs,
        )

    @classmethod
    def from_http(
        cls,
        url:str,
        timeout:float = http.DEFAULT_HTTP_TIMEOUT,
        chunk_size:int = http.DEFAULT_HTTP_CHUNK_SIZE,
        params:Dict[str, Any]={},
        **kwargs,
    )->Union[
        "WaveStreamIO",
        Exception,
    ]:
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
                callback:Callable[[bytes], None],
            )->None:
                for _data_chunk in gen:
                    # Thread?
                    callback(_data_chunk)

            # Fire and forget: start downloading
            threading.Thread(target=lambda : _iter_callback(
                        gen = _data_generator,
                        callback = _io.write,
                    )).start()
            
            return _io
    
        else:
            return _data_generator