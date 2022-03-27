#!/usr/bin/env python3
import os, sys
from contextlib import redirect_stderr, redirect_stdout

import pyaudio


pya = None

def refresh():
    """
    Rebuild PyAudio handle
    """
    
    global pya
    with redirect_stdout(open(os.devnull, 'w')):
        with redirect_stderr(open(os.devnull, 'w')):
            pya = pyaudio.PyAudio()


refresh()