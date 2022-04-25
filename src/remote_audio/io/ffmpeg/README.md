# remote_audio.io.ffmpeg

```
    _inputformat = main_options.FFmpegOptionFormat.create("mp3", option_type=classes.FFmpegOptionType.INPUT)
    _input = io_protocol.FFmpegProtocolHTTP.create('some.mp3')
    _outputformat = main_options.FFmpegOptionFormat.create("wav", option_type=classes.FFmpegOptionType.OUTPUT)
    _output = io_protocol.FFmpegProtocolPipe.create()
    _nooverwrite = main_options.FFmpegOptionNoOverwrite.create()
    _overwrite = main_options.FFmpegOptionOverwrite.create()
    _loop2 = main_options.FFmpegOptionStreamLoop.create(2)

    # Convert mp3 into wav, repeating 3 times
    _command = command.FFmpegCommand(
        input = _input,
        output = _output,
        options = (
            _inputformat,
            _outputformat,
            _overwrite,
            _loop2,
        )
    )

    # Pipe wav output into a wave IO object
    _command | some_wave_IO
```
