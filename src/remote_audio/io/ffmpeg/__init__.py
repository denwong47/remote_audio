from remote_audio.io.ffmpeg.formats import FFMPEG_FORMATS

import remote_audio.io.ffmpeg.classes as classes
import remote_audio.io.ffmpeg.io_protocol as io_protocol
import remote_audio.io.ffmpeg.io_devices as io_devices
import remote_audio.io.ffmpeg.main_options as main_options
import remote_audio.io.ffmpeg.command as command

# if (__name__=="__main__"):
#     _inputformat = main_options.FFmpegOptionFormat.create("mp3", option_type=classes.FFmpegOptionType.INPUT)
#     _input = io_protocol.FFmpegProtocolFile.create('/Users/denwong47/Downloads/karen.mp3')
#     _outputformat = main_options.FFmpegOptionFormat.create("wav", option_type=classes.FFmpegOptionType.OUTPUT)
#     _output = io_protocol.FFmpegProtocolFile.create('/Users/denwong47/Downloads/converted.wav')
#     _nooverwrite = main_options.FFmpegOptionNoOverwrite.create()
#     _overwrite = main_options.FFmpegOptionOverwrite.create()
#     _loop2 = main_options.FFmpegOptionStreamLoop.create(2)

#     _command = command.FFmpegCommand(
#         input = _input,
#         output = _output,
#         options = (
#             _inputformat,
#             _outputformat,
#             _overwrite,
#             _loop2,
#         )
#     )

#     print (_command.run())