#!/usr/bin/env python3

from enum import Enum

import remote_audio.io.ffmpeg.classes as classes

"""
FFmpeg Input and Output device options
https://ffmpeg.org/ffmpeg-devices.html

TODO This is INCOMPLETE
"""



class FFmpegDeviceAlsa(classes.FFmpegDevice):
    device_type:classes.FFmpegInputOutputType = classes.FFmpegInputOutputType.INPUT_OUTPUT

    