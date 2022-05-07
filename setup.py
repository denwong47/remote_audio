import setuptools
setuptools.setup()


import shell
if (not shell.ShellCommandExists(["ffmpeg", "-h"])):
    print ("FFmpeg is required for non-Wave file functions; please consult https://ffmpeg.org for more information.")
else:
    print ("FFmpeg found.")