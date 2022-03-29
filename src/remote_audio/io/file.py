#!/usr/bin/env python3

import os, sys

from remote_audio.exceptions import FileIOError

def get_file_size(
    path:str,
)->int:
    try:
        return os.path.getsize(
            path
        )
    except OSError as e:
        return FileIOError(str(e))

def get_wav_size(
    path:str,
):
    """
    Return the size of a wav file without the 44/46-byte header.
    """

    _file_size = get_file_size(path)
    _wav_header_size = get_wav_header_size(path)
    
    if (_file_size and _wav_header_size):
        return _file_size - _wav_header_size
    else:
        return _file_size and _wav_header_size

def get_wav_header_size(
    path:str,
)->int:
    """
    Read the 16th-20th byte (Subchunk1Size)
    to determine if the wav file has a 44-byte or 46-byte header
    """
    try:
        with open(path, "r+b") as _f:
            _f.seek(16)
            _subchunk1bytes = _f.read(4)
            _subchunk1size = int.from_bytes(_subchunk1bytes, "little", signed=False)

            if (_subchunk1size < 16):
                return FileIOError(f"File {path} does not appear to be a wav file.")
            else:
                return _subchunk1size + 28

    except(OSError, FileNotFoundError) as e:
        return FileIOError(str(e))