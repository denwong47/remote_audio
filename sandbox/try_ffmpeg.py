from tqdm import tqdm

import remote_audio
from remote_audio.device import AudioDevice
import shell
from shell.classes import ShellCommand
import time as timer

"""
Testing ffmpeg HTTP streaming to WAV stdout pipe, which is then taken up by AudioDevice.start_wav_stream.
"""

if (__name__ =="__main__"):
    if (shell.api.ShellCommandExists("ffmpeg -h")):
        _url = ""

        # Set the header to maximum size - otherwise wHnd won't even return any frames.
        _header = remote_audio.io.file.WavHeader.new(remote_audio.io.file.WAV_MAX_CHUNKSIZE)  # Problem - we don't know how long the file will be prior to complete conversion.

        # Doesn't matter if we don't set the bytes_total; we'll set it in the callback.
        _io = remote_audio.io.classes.WaveStreamIO(
            _header.construct(),
            bytes_total = None,
        )

        with ShellCommand(f"ffmpeg -f mp3 -i {_url} -f s16le pipe:1", output=bytes) as _sc:
            with AudioDevice.default(output=True).start_wav_stream(
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