#!/usr/bin/env python3

import pyaudio
import wave
import os, sys
import time as timer
import logging
import contextlib

logging.getLogger().setLevel(logging.DEBUG)

def main():
    logging.info(f"Using Python {'.'.join([ str(_) for _ in sys.version_info[:3]])}")

    CHUNK = 1024

    if len(sys.argv) < 2:
        print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
        sys.exit(-1)

    logging.debug("Opening wave I/O object...")
    wf = wave.open(sys.argv[1], 'rb')

    logging.debug("Initiating PyAudio object...")
    with contextlib.redirect_stderr(open(os.devnull, 'w')):
        p = pyaudio.PyAudio()

    logging.debug("Creating PyAudio stream...")
    logging.debug(f"{'format =':12s}{p.get_format_from_width(wf.getsampwidth())}")
    logging.debug(f"{'channels =':12s}{wf.getnchannels()}")
    logging.debug(f"{'rate =':12s}{wf.getframerate()}")
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    logging.debug(f"Reading first chunk of {CHUNK:,} bytes...")

    _count = 0
    while data := wf.readframes(CHUNK):
        stream.write(data)
        _count += 1
        logging.debug(f"Reading chunk #{_count:,} of {CHUNK:,} bytes...")

    logging.debug(f"Stopping stream...")
    stream.stop_stream()
    logging.debug(f"Closing steam...")
    stream.close()

    logging.debug(f"Terminating PyAudio object...")
    p.terminate()

    logging.debug(f"Complete.")


if (__name__=="__main__"):
    main()