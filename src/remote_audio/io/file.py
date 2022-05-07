#!/usr/bin/env python3

import os, sys
from enum import Enum
import io

from typing import Any, Dict, Tuple, Union

from remote_audio.exceptions import FileIOError, WavFormatError


"""
This module deals with local file I/O, which also includes a range of WAV file specific methods and classes.

For a WAV structure introduction, see
http://soundfile.sapp.org/doc/WaveFormat/
http://www-mmsp.ece.mcgill.ca/Documents/AudioFormats/WAVE/WAVE.html
"""

DEFAULT_FILE_CHUNK_SIZE = 2**20
WAV_MAX_CHUNKSIZE = 0xFFFFFFFF-36

class WavFMTVariant(Enum):
    PCM = 16
    NON_PCM = 18
    EXTENSIBLE = 40

class WavFormatCode(Enum):
    WAVE_FORMAT_PCM         =   0x0001
    WAVE_FORMAT_IEEE_FLOAT  =   0x0003
    WAVE_FORMAT_ALAW        =   0x0006
    WAVE_FORMAT_MULAW       =   0x0007
    WAVE_FORMAT_EXTENSIBLE  =   0xFFFE

class WavHeader(dict):
    """
    A wrapper for dict, for a header of a WAV file.
    Use either:
        _header.get("ChunkSize")
    or
        _header.ChunkSize

    Construct using get_wav_header. Do not build with class.
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
        _transform_enum_fmtvariant = lambda b: WavFMTVariant(_transform_uint_little(b))
        _transform_enum_format = lambda b: WavFormatCode(_transform_uint_little(b))

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
                "transform":    _transform_enum_fmtvariant,
            }
        )
        
        _header.add_chunk(
            data = data,
            **{
                "name":         "AudioFormat",
                "boundary":     (20, 2),
                "transform":    _transform_enum_format,
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

        if (_header.get("Subchunk1Size").value >= 18):
            _header.add_chunk(
                data = data,
                **{
                    "name":         "ExtensionSize",
                    "boundary":     (36, 2),
                    "transform":    _transform_uint_little,
                }
            )

        if (_header.get("Subchunk1Size").value >= 40):
            _header.add_chunk(
                data = data,
                **{
                    "name":         "ValidBitsPerSample",
                    "boundary":     (38, 2),
                    "transform":    _transform_uint_little,
                }
            )

            _header.add_chunk(
                data = data,
                **{
                    "name":         "SpeakerPositionMask",
                    "boundary":     (40, 4),
                    "transform":    _transform_uint_little,
                }
            )

            _header.add_chunk(
                data = data,
                **{
                    "name":         "SubFormatGUID",
                    "boundary":     (44, 16),
                    "transform":    _transform_uint_little,
                }
            )

        _subchunk2_start = _header.get("Subchunk1Size").value+20
        
        _header.add_chunk(
            data = data,
            **{
                "name":         "Subchunk2ID",
                "boundary":     (_subchunk2_start, 4),
                "transform":    _transform_text,
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

    @classmethod
    def new(
        cls,
        size:Union[int, bytes]      = WAV_MAX_CHUNKSIZE,
        ChunkID:str                 = "RIFF",
        ChunkSize:int               = 36,
        Format:str                  = "WAVE",
        Subchunk1ID:str             = "fmt ",
        Subchunk1Size:WavFMTVariant = WavFMTVariant.PCM,
        AudioFormat:WavFormatCode   = WavFormatCode.WAVE_FORMAT_PCM,
        NumChannels:int             = 2,
        SampleRate:int              = 44100,
        ByteRate:int                = None,
        BlockAlign:int              = None,
        BitsPerSample:int           = 16,
        ExtensionSize:int           = None,
        ValidBitsPerSample:int      = None,
        SpeakerPositionMask:int     = None,
        SubFormatGUID:int           = None,
        Subchunk2ID:str             = "data",
        Subchunk2Size:int           = 0,
    ):
        _header = cls()

        # Data Conversions if not the correct types
        if (isinstance(Subchunk1Size, int)):
            Subchunk1Size = WavFMTVariant(Subchunk1Size)

        if (isinstance(AudioFormat, int)):
            AudioFormat = WavFormatCode(AudioFormat)

        if (isinstance(size, bytes)):
            size = len(size)
        elif (size is None):
            size = 0

        # Calculate the correct values if None
        if (isinstance(size, int)):
            Subchunk2Size           = size
            ChunkSize               = Subchunk2Size + Subchunk1Size.value + 20
            
        if (BlockAlign is None):
            BlockAlign = int(NumChannels * BitsPerSample / 8)

        if (ByteRate is None):
            ByteRate = SampleRate * BlockAlign

        # Put data
        _header["ChunkID"]          = ChunkID
        _header["ChunkSize"]        = ChunkSize
        _header["Format"]           = Format
        _header["Subchunk1ID"]      = Subchunk1ID
        _header["Subchunk1Size"]    = Subchunk1Size
        _header["AudioFormat"]      = AudioFormat
        _header["NumChannels"]      = NumChannels
        _header["SampleRate"]       = SampleRate
        _header["ByteRate"]         = ByteRate
        _header["BlockAlign"]       = BlockAlign
        _header["BitsPerSample"]    = BitsPerSample

        if (Subchunk1Size.value >= 18):
            _header["ExtensionSize"]= ExtensionSize
        
        if (Subchunk1Size.value >= 40):
            _header["ValidBitsPerSample"]   = ValidBitsPerSample
            _header["SpeakerPositionMask"]  = SpeakerPositionMask
            _header["SubFormatGUID"]        = SubFormatGUID

        _header["Subchunk2ID"]      = Subchunk2ID
        _header["Subchunk2Size"]    = Subchunk2Size

        return _header


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
    )->bool:
        # This HAS to return a bool.
        return bool(self.is_valid)

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
                self.get("ChunkSize", -1) - self.get("Subchunk2Size", -1)   == self.get("Subchunk1Size").value + 20,
                self.get("Format", None)                                    == "WAVE",
                self.get("Subchunk1ID", None)                               == "fmt ",
                isinstance(self.get("AudioFormat", -1), WavFormatCode),
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
    def construct(
        self
    )->bytes:
        """
        Rebuild a header in bytes.
        """

        _bytes = b""
        _bytes += self.get("ChunkID").encode("utf-8")
        _bytes += self.get("ChunkSize").to_bytes(4, byteorder="little")
        _bytes += self.get("Format").encode("utf-8")
        _bytes += self.get("Subchunk1ID").encode("utf-8")
        _bytes += self.get("Subchunk1Size").value.to_bytes(4, byteorder="little")
        _bytes += self.get("AudioFormat").value.to_bytes(2, byteorder="little")
        _bytes += self.get("NumChannels").to_bytes(2, byteorder="little")
        _bytes += self.get("SampleRate").to_bytes(4, byteorder="little")
        _bytes += self.get("ByteRate").to_bytes(4, byteorder="little")
        _bytes += self.get("BlockAlign").to_bytes(2, byteorder="little")
        _bytes += self.get("BitsPerSample").to_bytes(2, byteorder="little")

        if (self.get("Subchunk1Size").value >= 18):
            _bytes += self.get("ExtensionSize").to_bytes(2, byteorder="little")
        
        if (self.get("Subchunk1Size").value >= 40):
            _bytes += self.get("ValidBitsPerSample").to_bytes(2, byteorder="little")
            _bytes += self.get("SpeakerPositionMask").to_bytes(4, byteorder="little")
            _bytes += self.get("SubFormatGUID").to_bytes(16, byteorder="little")

        _bytes += self.get("Subchunk2ID").encode("utf-8")
        _bytes += self.get("Subchunk2Size").to_bytes(4, byteorder="little")

        return _bytes

def get_file_size(
    path:str,
)->int:
    """
    Get file size from OS.
    """
    try:
        return os.path.getsize(
            path
        )
    except OSError as e:
        return FileIOError(str(e))

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
        return (get_file_size(_path))
            
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

    return WavHeader.from_data(
        data
    )
    

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