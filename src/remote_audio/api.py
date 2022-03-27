#!/usr/bin/env python3
from contextlib import redirect_stderr, redirect_stdout

import pyaudio


pya = None

def refresh():
    """
    Rebuild PyAudio handle
    """
    
    global pya
    with redirect_stdout(None):
        with redirect_stderr(None):
            pya = pyaudio.PyAudio()


refresh()