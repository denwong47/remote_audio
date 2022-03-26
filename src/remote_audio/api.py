#!/usr/bin/env python3

import pyaudio

from contextlib import redirect_stderr, redirect_stdout

with redirect_stdout(None):
    with redirect_stderr(None):
        pya = pyaudio.PyAudio()