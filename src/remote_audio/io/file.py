#!/usr/bin/env python3

import os, sys
import io
from typing import Any, Dict, Tuple, Union

from remote_audio.exceptions import FileIOError, WavFormatError


class WavHeader(dict):
    """
    A wrapper for dict, for a header of a WAV file.
    Use either:
        _header.get("ChunkSize")
    or
        _header.ChunkSize
    """

    @classmethod
    def from_data(
        cls,
        data:Union[
            bytes, # actual binary data
            str,   # path
            io.IOBase,
        ],
    ):
        """
        Construct instance from data.
        data can be:
        - str: path to WAV file
        - io object: a file like object that can be .read()
        - bytes: raw binary data
        """

        return get_wav_header(
            data=data
        )


    def add_chunk(
        self,
        data:bytes,
        name:str,
        boundary:Tuple[int],
        transform:Any=None,
    ):
        _chunk = data[boundary[0]:boundary[0]+boundary[1]]
        
        self[name] = transform(_chunk)

    def __getattr__(self, name:str):
        """
        Allow self.AttributeName to reference self["AttributeName"]
        """
        return self.get(name, None)


    def __bool__(
        self,
    ):
        return self.is_valid

    @property
    def is_valid(
        self,
    ):
        """
        Basic checks to see if the header makes sense.

        Return True if Yes, otherwise return a False-evaluating Exception ready to be raised.
        """

        if all(
            (
                self.get("ChunkID", None)                                   == "RIFF",
                self.get("ChunkSize", -1) - self.get("Subchunk2Size", -1)   == self.get("Subchunk1Size", -32768) + 20,
                self.get("Format", None)                                    == "WAVE",
                self.get("Subchunk1ID", None)                               == "fmt ",
                self.get("AudioFormat", -1)                                 >= 1,
                self.get("NumChannels", -1)                                 >= 1,
                self.get("BlockAlign", -1)                                  == int(self.get("NumChannels", 0) * self.get("BitsPerSample", 0)/8),
                self.get("ByteRate", -1)                                    == self.get("SampleRate", 0) * self.get("BlockAlign", 0),
                self.get("BitsPerSample", -1) % 8                           == 0,
            )
        ):
            return True
        else:
            return WavFormatError(
                "WAV Header not valid."
            )
    
    @property
    def header_size(
        self,
    )->int:
        """
        Total Header size.
        Could be 44 or 46, depending on Subchunk1Size
        """

        if (_return := self.is_valid):
            return self.get("Subchunk1Size", 16) + 20 + 8 # Count ChunkID and ChunkSize
        else:
            return _return

    @property
    def data_size(
        self
    )->int:
        """
        Actual data chunk size.
        """

        if (_return := self.is_valid):
            return self.get(
                "Subchunk2Size",
                WavFormatError(
                    "WAV Header does not contain Subchunk2Size."
                ),
            )
        else:
            return _return

    @property
    def total_size(
        self
    )->int:
        """
        Entire file size.
        
        This is simply 8 + ChunkSize.
        """

        if (_return := self.is_valid):
            return self.get("ChunkSize", -8) + 8
        else:
            return _return


    #TODO make a construct() method that regenerates the bytes?


def get_wav_file_size(
    data:Union[
        bytes, # actual binary data
        str,   # path
        io.IOBase,
    ],
)->int:
    """
    Whole WAV file size.
    """
    
    if (isinstance(data, str)):
        # Path
        _path = data
        try:
            return os.path.getsize(
                _path
            )
        except OSError as e:
            return FileIOError(str(e))
            
    elif (isinstance(data, bytes)):
        # bytes only, give its length
        return len(data)
    
    elif (isinstance(data, io.IOBase)):
        # IO
        _io = data
        _header = get_wav_header(_io)

        return _header.total_size


 

def get_wav_header(
    data:Union[
        bytes, # actual binary data
        str,   # path
        io.IOBase,
    ],
)->WavHeader:

    """
    Get header data from a file path, an IO object, a set of bytes.

    It is possible for the header to be 44 or 46 bytes -
    for safety we will overread it, then drop excessive data.
    """

    if (isinstance(data, str)):
        # Read data from path if str
        _path = data
        try:
            with open(_path, "rb") as _f:
                data = _f.read(46)
        except(OSError, FileNotFoundError) as e:
            return FileIOError(str(e))

    elif (isinstance(data, io.IOBase)):
        # Get the first 46 bytes
        _io = data
        data = _io.read(46)
        _io.seek(0, io.SEEK_SET)
    
    _transform_text = lambda b: b.decode("utf-8")
    _transform_uint_little = lambda b: int.from_bytes(b, "little", signed=False)

    _header = WavHeader()

    _header.add_chunk(
        data = data,
        **{
            "name":         "ChunkID",
            "boundary":     (0, 4),
            "transform":    _transform_text,
        }
    )
    
    _header.add_chunk(
        data = data,
        **{
            "name":         "ChunkSize",
            "boundary":     (4, 4),
            "transform":    _transform_uint_little,
        }
    )
    
    _header.add_chunk(
        data = data,
        **{
            "name":         "Format",
            "boundary":     (8, 4),
            "transform":    _transform_text,
        }
    )
    
    _header.add_chunk(
        data = data,
        **{
            "name":         "Subchunk1ID",
            "boundary":     (12, 4),
            "transform":    _transform_text,
        }
    )
    
    _header.add_chunk(
        data = data,
        **{
            "name":         "Subchunk1Size",
            "boundary":     (16, 4),
            "transform":    _transform_uint_little,
        }
    )
    
    _header.add_chunk(
        data = data,
        **{
            "name":         "AudioFormat",
            "boundary":     (20, 2),
            "transform":    _transform_uint_little,
        }
    )
    
    _header.add_chunk(
        data = data,
        **{
            "name":         "NumChannels",
            "boundary":     (22, 2),
            "transform":    _transform_uint_little,
        }
    )
    
    _header.add_chunk(
        data = data,
        **{
            "name":         "SampleRate",
            "boundary":     (24, 4),
            "transform":    _transform_uint_little,
        }
    )
    
    _header.add_chunk(
        data = data,
        **{
            "name":         "ByteRate",
            "boundary":     (28, 4),
            "transform":    _transform_uint_little,
        }
    )
    
    _header.add_chunk(
        data = data,
        **{
            "name":         "BlockAlign",
            "boundary":     (32, 2),
            "transform":    _transform_uint_little,
        }
    )
    
    _header.add_chunk(
        data = data,
        **{
            "name":         "BitsPerSample",
            "boundary":     (34, 2),
            "transform":    _transform_uint_little,
        }
    )

    _subchunk2_start = _header.get("Subchunk1Size", 16)+20
    
    _header.add_chunk(
        data = data,
        **{
            "name":         "Subchunk2ID",
            "boundary":     (_subchunk2_start, 4),
            "transform":    _transform_uint_little,
        }
    )
    
    _header.add_chunk(
        data = data,
        **{
            "name":         "Subchunk2Size",
            "boundary":     (_subchunk2_start+4, 4),
            "transform":    _transform_uint_little,
        }
    )

    return _header
    

def get_wav_header_size(
    data:Union[
        bytes, # actual binary data
        str,   # path
        io.IOBase,
    ],
)->int:
    """
    Read the 16th-20th byte (Subchunk1Size)
    to determine if the wav file has a 44-byte or 46-byte header
    """
    _header = get_wav_header(
        data=data,
    )

    return _header.header_size



def get_wav_data_size(
    data:Union[
        bytes, # actual binary data
        str,   # path
        io.IOBase,
    ],
):
    """
    Return the size of a wav file without the 44/46-byte header.
    """

    _header = get_wav_header(
        data=data,
    )

    return _header.data_size