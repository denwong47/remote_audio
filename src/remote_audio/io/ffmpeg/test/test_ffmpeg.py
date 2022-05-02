from datetime import datetime
import shlex

import quicktest as unittest

from remote_audio.io.ffmpeg.stream_specifier import FFmpegStreamSpecifier, \
                                                    FFmpegStreamType
import remote_audio.io.ffmpeg.classes as classes
import remote_audio.io.ffmpeg.main_options as main_options


class TestFFmpeg(unittest.TestCase):
    def test_main_options(self):
        """
        Test all FFmpegMainOptions to ensure .io_string is producing what we expected.
        """

        _attach_path = "./test.ttf"
        _format = "mp3"
        _filter = "loudnorm"
        _filename = "./test.mp3"
        _nb_threads = 6
        _framecount = 5000
        _limit_size = 2**20
        _offset = 8192
        _scale = 1.5
        _title = "My Video Title"
        _metadata = {
                    "title":_title,
                    "language":"eng",
                    "mimetype":"video/mp4",
                }
        _metadata_list = [
            f"{key}={shlex.quote(str(value))}" \
                for key, value in zip(_metadata.keys(), _metadata.values())
        ]
        _preset_name = "vcd"
        _program_num = 16
        _url = "https://www.example.com/sample.wav"
        _q = 0
        _pid = 16384
        _integer = 64
        _position = "00:11:22.3456"
        _time = 1.2345
        _duration = _position
        _type = "svcd"
        _date = datetime.utcnow().isoformat()

        _option = main_options.FFmpegOptionAttach.create(
                attach_path = _attach_path,
            )
        _answer = ["-"+_option.parameter_name,_attach_path]
        self.assertListEqual(_option.io_string, _answer)


        _option = main_options.FFmpegOptionDebugTimestamp.create(
            )
        _answer = ["-"+_option.parameter_name]
        self.assertListEqual(_option.io_string, _answer)

        _option = main_options.FFmpegOptionDispositions.create(
            )
        _answer = ["-"+_option.parameter_name]
        self.assertListEqual(_option.io_string, _answer)

        _option = main_options.FFmpegOptionDN.create(
            )
        _answer = ["-"+_option.parameter_name]
        self.assertListEqual(_option.io_string, _answer)
            
        _option = main_options.FFmpegOptionDumpAttachment.create(
                attach_path = _attach_path,
                stream_specifier= FFmpegStreamSpecifier(),
                option_type= classes.FFmpegOptionType.INPUT,
            )
        _answer = ["-"+_option.parameter_name, _attach_path]
        self.assertListEqual(_option.io_string, _answer)


        _option = main_options.FFmpegOptionFormat.create(
                format=_format,
                option_type= classes.FFmpegOptionType.INPUT,
            )
        _answer = ["-"+_option.parameter_name, _format]
        self.assertListEqual(_option.io_string, _answer)

        _option = main_options.FFmpegOptionFilter.create(
                filtergraph=_filter,
                stream_specifier= FFmpegStreamSpecifier(0, "a"),
            )
        _answer = ["-"+_option.parameter_name+":a:0", _filter]
        self.assertListEqual(_option.io_string, _answer)

        _option = main_options.FFmpegOptionFilterScript.create(
                filename=_filename,
                stream_specifier= FFmpegStreamSpecifier(0, "a"),
            )
        _answer = ["-"+_option.parameter_name+":a:0", _filename]
        self.assertListEqual(_option.io_string, _answer)

        _option = main_options.FFmpegOptionFilterThreads.create(
                _nb_threads,
            )
        _answer = ["-"+_option.parameter_name, str(_nb_threads)]
        self.assertListEqual(_option.io_string, _answer)

        _option = main_options.FFmpegOptionFrames.create(
                framecount=_framecount,
                stream_specifier= FFmpegStreamSpecifier(1, "v"),
            )
        _answer = ["-"+_option.parameter_name+":v:1", str(_framecount)]
        self.assertListEqual(_option.io_string, _answer)

        _option = main_options.FFmpegOptionFileSize.create(
                limit_size=_limit_size,
            )
        _answer = ["-"+_option.parameter_name, str(_limit_size)]
        self.assertListEqual(_option.io_string, _answer)

        _option = main_options.FFmpegOptionInputTimestampOffset.create(
                offset=_offset,
            )
        _answer = ["-"+_option.parameter_name, str(_offset)]
        self.assertListEqual(_option.io_string, _answer)

        _option = main_options.FFmpegOptionInputTimestampRescale.create(
                scale=_scale,
                stream_specifier= FFmpegStreamSpecifier(),
            )
        _answer = ["-"+_option.parameter_name, str(_scale)]
        self.assertListEqual(_option.io_string, _answer)

        _option = main_options.FFmpegOptionMetadata.create(
                metadata = _metadata,
                metadata_specifier= FFmpegStreamSpecifier(
                    10,
                    [ 
                        FFmpegStreamType.SUBTITLE,
                        FFmpegStreamType.AUDIO,
                    ]
                ),
            )
        _answer = [
            "-"+_option.parameter_name+":s:a:10",
            *_metadata_list,
        ]
        self.assertListEqual(_option.io_string, _answer)

        _option = main_options.FFmpegOptionNoOverwrite.create(
            )
        _answer = ["-"+_option.parameter_name]
        self.assertListEqual(_option.io_string, _answer)

        _option = main_options.FFmpegOptionPreset.create(
                preset_name=_preset_name,
                stream_specifier= FFmpegStreamSpecifier(0, FFmpegStreamType.AUDIO),
            )
        _answer = ["-"+_option.parameter_name+":a:0", _preset_name]
        self.assertListEqual(_option.io_string, _answer)

        _option = main_options.FFmpegOptionProgram.create(
                streams=[
                    FFmpegStreamSpecifier(0, FFmpegStreamType.AUDIO),
                    FFmpegStreamSpecifier(1, FFmpegStreamType.VIDEO),
                    FFmpegStreamSpecifier(2, [FFmpegStreamType.SUBTITLE, FFmpegStreamType.VIDEO]),
                ],
                title= _title,
                program_num= _program_num,
            )
        _answer = [
            "-"+_option.parameter_name,
            ":".join([
                f"title={shlex.quote(_title)}",
                f"program_num={str(_program_num)}",
                "st=a:0",
                "st=v:1",
                "st=s:v:2",
            ])
        ]
        self.assertListEqual(_option.io_string, _answer)

        _option = main_options.FFmpegOptionProgress.create(
                url=_url,
            )
        _answer = ["-"+_option.parameter_name, _url]
        self.assertListEqual(_option.io_string, _answer)

        _option = main_options.FFmpegOptionQScale.create(
                q=_q,
                stream_specifier= FFmpegStreamSpecifier(pid=_pid),
            )
        _answer = ["-"+_option.parameter_name+f":p:{_pid:d}", str(_q)]
        self.assertListEqual(_option.io_string, _answer)

        _option = main_options.FFmpegOptionRecastMedia.create(
            )
        _answer = ["-"+_option.parameter_name]
        self.assertListEqual(_option.io_string, _answer)

        _option = main_options.FFmpegOptionReinitFilter.create(
                integer=_integer,
                stream_specifier= FFmpegStreamSpecifier(),
            )
        _answer = ["-"+_option.parameter_name, str(_integer)]
        self.assertListEqual(_option.io_string, _answer)

        _option = main_options.FFmpegOptionSeek.create(
                position=_position,
                option_type= classes.FFmpegOptionType.INPUT,
            )
        _answer = ["-"+_option.parameter_name, _position]
        self.assertListEqual(_option.io_string, _answer)

        _option = main_options.FFmpegOptionSeekFromEOF.create(
                position=_position,
            )
        _answer = ["-"+_option.parameter_name, _position]
        self.assertListEqual(_option.io_string, _answer)

        _option = main_options.FFmpegOptionStats.create(
            )
        _answer = ["-"+_option.parameter_name]
        self.assertListEqual(_option.io_string, _answer)

        _option = main_options.FFmpegOptionStatsPeriod.create(
                time=_time,
            )
        _answer = ["-"+_option.parameter_name, str(_time)]
        self.assertListEqual(_option.io_string, _answer)

        _option = main_options.FFmpegOptionStdin.create(
            )
        _answer = ["-"+_option.parameter_name]
        self.assertListEqual(_option.io_string, _answer)

        _option = main_options.FFmpegOptionStreamLoop.create(
                loop= 0,
                # option_type= classes.FFmpegOptionType.INPUT,
            )
        _answer = ["-"+_option.parameter_name, str(0)]
        self.assertListEqual(_option.io_string, _answer)

        _option = main_options.FFmpegOptionDuration.create(
                duration=_duration,
                option_type= classes.FFmpegOptionType.INPUT,
            )
        _answer = ["-"+_option.parameter_name, _duration]
        self.assertListEqual(_option.io_string, _answer)

        _option = main_options.FFmpegOptionTarget.create(
                type=_type,
            )
        _answer = ["-"+_option.parameter_name, _type]
        self.assertListEqual(_option.io_string, _answer)

        _option = main_options.FFmpegOptionTimestamp.create(
                date=_date,
            )
        _answer = ["-"+_option.parameter_name, _date]
        self.assertListEqual(_option.io_string, _answer)

        _option = main_options.FFmpegOptionTo.create(
                position=_position,
            )
        _answer = ["-"+_option.parameter_name, _position]
        self.assertListEqual(_option.io_string, _answer)

        _option = main_options.FFmpegOptionOverwrite.create(
            )
        _answer = ["-"+_option.parameter_name]
        self.assertListEqual(_option.io_string, _answer)


if (__name__=="__main__"):
    unittest.main()