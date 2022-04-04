import remote_audio
from remote_audio.device import AudioDevice

from tqdm import tqdm
import time as timer

# Initialise an WaveStreamIO from http location.
# This will start a threading task in the background to download and write the IO already.
_io = remote_audio.io.classes.WaveStreamIO.from_http(
    "",
)

print ("IO Initialised")



# Start a the audio stream as a context.
# The playing of the audio is non-blocking until the context exits.
with AudioDevice.default(output=True).start_wav_stream(
    _io,
    timeout=10,
    bytes_total=_io.bytes_total,
    exit_interrupt=False,
) as _stream1:
    
    # Inside this context, nothing actually needs to be done.
    # Everything here is simply for the progress bar.
    _pbar = tqdm(total =_io.bytes_total)

    _start = timer.perf_counter()
    
    while (_stream1.stream_status):
        _pbar.n = (_io.bytes_written - _stream1.stream_status.bytes_played)
        _pbar.set_description(f"Time {timer.perf_counter()-_start:,.2f}s, Buffer Fullness")
        _pbar.update()
        timer.sleep(0.1)

    _pbar.close()