#!/usr/bin/env python3

from typing import BinaryIO

import pyaudio

from remote_audio import api


def play_stream(
    io:BinaryIO,
    **kwargs,
):
    _p = api.pya
    pass