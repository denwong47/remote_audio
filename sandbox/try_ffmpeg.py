
import os, sys
from tqdm import tqdm

import remote_audio
from remote_audio.device import AudioDevice
from remote_audio.io.ffmpeg import  FFmpegCommand, \
                                    FFmpegProtocolHTTP, \
                                    FFmpegProtocolFile, \
                                    FFmpegProtocolPipe, \
                                    FFmpegOptionFormat
import shell
from shell.classes import ShellCommand
import time as timer

"""
Testing ffmpeg HTTP streaming to WAV stdout pipe, which is then taken up by AudioDevice.start_wav_stream.
"""

if (__name__ =="__main__"):
    if (shell.api.ShellCommandExists("ffmpeg -h")):
        _url = os.getenv("REMOTE_MP3_URL", None)

        if (_url is None):
            print ("REMOTE_MP3_URL is not set. Provide the url of the mp3 to be played.")
            sys.exit(1)

        # Set the header to maximum size - otherwise wHnd won't even return any frames.
        _header = remote_audio.io.file.WavHeader.new(remote_audio.io.file.WAV_MAX_CHUNKSIZE)  # Problem - we don't know how long the file will be prior to complete conversion.

        # Doesn't matter if we don't set the bytes_total; we'll set it in the callback.
        _io = remote_audio.io.classes.WaveStreamIO(
            _header.construct(),
            bytes_total = None,
        )

        # If Hifi Berry is present, use it first. Otherwise, use the default output device.
        _device = remote_audio.device.AudioDevice.find_first(name="berry") or \
                  remote_audio.device.AudioDevice.default(output=True)

        with FFmpegCommand(
            input=FFmpegProtocolHTTP.create(_url),
            output=FFmpegProtocolPipe.create(),
            options=[
                FFmpegOptionFormat.create("mp3", "input"),
                FFmpegOptionFormat.create("s16le", "output"),
            ],
        ) as _sc:
            with _device.start_wav_stream(
                _io,
                timeout=30,
                bytes_total=_io.bytes_total,
                exit_interrupt=False,
            ) as _stream1:

                _pbar = tqdm(total =_io.bytes_total)

                def _stream_callback(
                    command:ShellCommand,
                    bytes_total:int,
                ):
                    _stream1.stream_status.bytes_total = bytes_total
                    _pbar.total = bytes_total
                    _pbar.update()

                _sc.stream_stdout(
                    _io,
                    callback=_stream_callback
                )

                

                _start = timer.perf_counter()
                
                while (_stream1.stream_status):
                    _pbar.n = (_io.bytes_written - _stream1.stream_status.bytes_played)
                    _pbar.set_description(f"Time {timer.perf_counter()-_start:,.2f}s, Buffer Fullness")
                    _pbar.update()
                    timer.sleep(0.2)

                _pbar.close()
    else:
        raise OSError("ffmpeg is not installed.")
