# remote_audio
This library is designed for use with macOS and Linux, providing various audio related functions in a Pythonic implementation. There is specific focus on playing various formats of audio over HTTP.

All playbacks are designed to be:
- streaming - playback shall start from the first chunk of data, not waiting for the entirety of it.
- non-blocking - the methods starting a playback shall not block the execution of subsequent code.
- controllable - the streaming and playing in the background can be controlled using Python context manager, so there is full control over when the playing stop and ends.

```
README WIP
```

This library uses
- `ffmpeg`
- `portaudio`
- `espeak` in case of Linux, and the built-in `say` on macOS.
The above packgaes needs to be separately installed/compiled; they cannot be installed as `pip` dependencies.

------

### *Note for macOS installations*
- *Compiling portaudio with clang-13+ will cause errors; use `brew install portaudio` to complete install.*
- *When installing PyAudio, gcc may not be able to find the portaudio library; you may require setting environmental variables for `gcc`:*
```shell
export C_INCLUDE_PATH=/System/Volumes/Data/opt/homebrew/Cellar/portaudio/{version_number}/include
export LIBRARY_PATH=/System/Volumes/Data/opt/homebrew/Cellar/portaudio/{version_number}/lib
```
------

## How it works

At the heart of it, this library works on a few layers:
```
    web -> requests -> ffmpeg -> StreamIO -> AudioDevice/portaudio
       http       mp3 etc.   s16le       wave
```
Consider the whole process a continueous IO pipe, with one `stdout` piping into the `stdin` of the next layer.

In the simpliest form:
```python
import remote_audio
import time
with remote_audio.device.AudioDevice.default().play_http("https://somedomain.com/file.mp3") as _stream:
    # Stuff to do while audio is still playing;
    # if this context finishes before the audio ends, it will block until it does

    # OPTIONAL:
    while _stream.stream_status:
        print (f"Buffer remaining: {_stream.stream_status.bytes_buffered:,} bytes")
        time.sleep(0.5)

# Stuff to do when audio stops
```
will stream and play an mp3 file on the default audio device.

------

# High Level APIs

### remote_audio.device
#### remote_audio.device.AudioDevice

```python
class remote_audio.device.AudioDevice(
    device_index:int,
    **kwargs,
)
```

##### Properties
- `.device_index:int`
- `.signature:remote_audio.device.DeviceHostAPISignature`
- `.properties:Dict[str, Any]`
- `.canInput:bool`
- `.canOutput:bool`

##### Methods
```python
@classmethod
def remote_audio.device.AudioDevice.by_device_index(
    device_index:int=0,
    **kwargs,
)->"AudioDevice"
```
Class method.
Return the `AudioDevice` by `device_index`.

```python
@classmethod
def remote_audio.device.AudioDevice.by_host_api_device_index(
    signature:Union[
        DeviceHostAPISignature,
        Tuple[int, int],
    ]=None,
    host_api_index:int=0,
    host_api_device_index:int=0,
)->"AudioDevice"
```
Class method.
Return the `AudioDevice` by `host_api_index` and `host_api_device_index`.

Typically there is only one `host_api_index` - `0` - unless there are multiple audio API active.

```python
@classmethod
def remote_audio.device.AudioDevice.default(
    input:bool=False,
    output:bool=True,
)->"AudioDevice"
```
Class method.
Return the system default `AudioDevice`.

```python
@classmethod
def remote_audio.device.AudioDevice.list()->Iterable[
    "AudioDevice"
]
```
Class method.
Return a `list` of all `AudioDevice` listed by `portaudio`.

```python
@classmethod
def remote_audio.device.AudioDevice.find(
    input:bool=False,
    output:bool=True,
    name:Union[
        re.Pattern,
        str,
    ]=None,
)->Iterable[
    "AudioDevice"
]
```
Class method.
Return a `list` of `AudioDevice` that satisfy the criteria:
- whether the `AudioDevice` `canInput`;
- whether the `AudioDevice` `canOutput`;
- whether the `AudioDevice`'s name satisfy the supplied Regex pattern or `str`.

```python
@classmethod
def remote_audio.device.AudioDevice.find_first(
    *args,
    **kwargs,
)->"AudioDevice"
```
Class method.
Just like `.find()`, but returns the first `AudioDevice` only.

```python
def start_wav_stream(
    self,
    io:BinaryIO,
    chunk_size:int=1024,
    start:bool=True,
    bytes_total:int=None,
    timeout:float=None,
    exit_interrupt:bool=False,
    **kwargs,
)->remote_audio.stream.AudioStream
```
Instance method.

Start a non-blocking streaming playback of wave file (header included) from `io`. `io` needs to be an IO-like object with `.read()` method that returns a `bytes` object. It can be standard `io.BinaryIO` objects, `wave.Wave_read` objects generated from `wave.open()`, or specific to this library, any subclass of `remote_audio.classes.StreamIO`, e.g. `remote_audio.classes.WaveStreamIO` and `remote_audio.classes.MP3StreamIO`.

Returns a `remote_audio.stream.AudioStream` object, which can be used as a context manager:
```python
with remote_audio.device.AudioDevice.default().start_wav_stream(io_obj, exit_interrupt=False):
    # code here will execute, then block and wait for AudioStream.
    # check status of AudioStream with AudioStream.stream_status.

# code here will only execute when AudioStream has finished.
```

```python
with remote_audio.device.AudioDevice.default().start_wav_stream(io_obj, exit_interrupt=True):
    # code here will execute, then interrupt and stop AudioStream if its not finished.
    # check status of AudioStream with AudioStream.stream_status.

# code here will execute immediately following the above, but the AudioStream would be interrupted and stopped at this point.
```

## remote_audio.classes

### remote_audio.io.ffmpeg.StreamIO
```python
class remote_audio.io.ffmpeg.StreamIO(
    initial_bytes:bytes = b"",
    bytes_total:int = None,
)
```
An IO File-like object class that allows both .read() from the head and .write() to the tail by two different threads simultaneously, without having to manually manipulate the pointer. \
**NOTE** This is done by a threading lock - so technically it is not *read* and *write* at the same time.

This is a subclass of `io.BytesIO`, for the purpose of `isinstance` checking; however it is not recommended to use any attributes of the superclass.

`bytes_total` is not used in the class itself; it is optional at initialisation. Some subclasses will update this variable when the full size becomes available (e.g. over HTTP or FFmpeg conversion)

##### Methods
- `.read()`
- `.write(b:bytes)`
- `.tell()`\
Apart from the threading lock, these behave exactly identical to the superclass of `io.BytesIO`.

### remote_audio.io.ffmpeg.WaveStreamIO

### remote_audio.io.ffmpeg.MP3StreamIO

------

# Low Level APIs
## remote_audio.audio

## remote_audio.stream

## remote_audio.io

## remote_audio.io.ffmpeg
### remote_audio.io.ffmpeg.FFmpegCommand
```python
class remote_audio.io.ffmpeg.FFmpegCommand(
        input:classes.FFmpegOption,
        output:classes.FFmpegOption,
        options:Iterable[classes.FFmpegOption]=[],
        ignore_codes:list=[],
        timeout:float=None,
)
```
Sub-class of `ShellPipe` and `ShellCommand`; see https://www.github.com/denwong47/shell for details.

------

# Exceptions
## remote_audio.exceptions