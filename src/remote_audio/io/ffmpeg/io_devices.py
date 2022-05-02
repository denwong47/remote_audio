#!/usr/bin/env python3

from enum import Enum

import remote_audio.io.ffmpeg.classes as classes

"""
FFmpeg Input and Output device options
https://ffmpeg.org/ffmpeg-devices.html

TODO This is INCOMPLETE
"""


@classes.ffmpegioclass
class FFmpegDeviceAlsa(classes.FFmpegDevice):
    hw_id:str = None
    
    sample_rate:int = None
    channels:int = None

    option_type:classes.FFmpegOptionType = classes.FFmpegOptionType.INPUT_OUTPUT

    options_list:tuple = (
        "sample_rate",
        "channels",
    )

    