#!/usr/bin/env python3

from enum import Enum

import remote_audio.io.ffmpeg.classes as classes

"""
FFmpeg Input and Output protocols
https://ffmpeg.org/ffmpeg-protocols.html

TODO This is INCOMPLETE
"""

class FFmpegProtocolFile(classes.FFmpegProtocol):
    pass

class FFmpegProtocolData(classes.FFmpegProtocol):
    pass

class FFmpegProtocolHTTP(classes.FFmpegProtocol):
    pass

class FFmpegProtocolPipe(classes.FFmpegProtocol):
    pass

# TODO add support for other protocols