import os
import time as timer

from tqdm import tqdm

from remote_audio.device import AudioDevice
from remote_audio.classes import MP3StreamIO


# _io = FFmpegStreamIO.from_file(
#     _url = os.getenv("LOCAL_MP3_PATH", None),
#     format="mp3",
# )
_url = os.getenv("REMOTE_MP3_URL", None)

# If Hifi Berry is present, use it first. Otherwise, use the default output device.
_device = AudioDevice.find_first(name="berry") or \
          AudioDevice.default(output=True)

with _device.play_http(
    _url,
    timeout=30,
    bytes_total=None,
    exit_interrupt=False,
) as _stream1:
    _pbar = tqdm(total =_stream1.stream_status.bytes_total)

    _start = timer.perf_counter()

    while (_stream1.stream_status):
        _pbar.n = _stream1.stream_status.bytes_buffered
        _pbar.total = _stream1.stream_status.bytes_total
        # _stream1.stream_status.bytes_total = _io.bytes_total
        _pbar.set_description(f"Time {timer.perf_counter()-_start:,.2f}s, Buffer Fullness, total {_stream1.stream_status.bytes_total}")
        _pbar.update()
        timer.sleep(0.2)
