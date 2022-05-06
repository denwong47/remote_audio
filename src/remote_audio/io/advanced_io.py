from socket import timeout
from typing import Any, Callable, Dict, Iterable, Union
import warnings
from numpy import byte

import remote_audio.io.base_io
import remote_audio.io.http as http
import remote_audio.io.file as file
import remote_audio.io.ffmpeg.command as command
import remote_audio.io.ffmpeg.classes as classes
import remote_audio.io.ffmpeg.io_protocol as io_protocol
import remote_audio.io.ffmpeg.main_options as main_options
from remote_audio.exceptions import InvalidInputParameters

# This module depends on complete initialisation of remote_audio.io; hence it cannot be be called from remote_audio.io.__init__.py.
# However it can be referenced from remote_audio.classes, which is where you should use all the classes.

class FFmpegStreamIO(remote_audio.io.base_io.StreamIO):
    """
    An IO File-like object class for any audio files, that allows both .read() and .write().
    When it .write() data, it sfeeds the data into FFmpeg first to convert to WAV, then write the stdout instead.
    Suitable for AudioStreaming over slow I/O.
    """
    def __init__(
        self,
        initial_bytes:bytes = b"",
        format:str = "mp3",
        kind:str = "pipe",
        input_params:Dict[str, Any] = {
            "path":None,
            "url":None,
            "timeout":None,
        },
        bytes_total:int = None,             # Optional - does not affect the class
        callback:Callable[[command.FFmpegCommand, int], None] = None,
        *args,
        **kwargs,
    ):
        self.format = format
        self.kind = kind
        self.input_params = input_params
        self.command = None

        self.callback = callback if (callable(callback)) else None

        kind_check = {
            "pipe":tuple(),
            "file":("path",),
            "http":(
                "url",
                # "timeout",
            ),
        }
        # Check kind is correct
        if (not self.kind in kind_check.keys()):
            raise InvalidInputParameters(
                f"{type(self).__name__} class only accepts kind being {' | '.join(kind_check.keys())}."
            )

        # Check all input_params are present
        if (not all(
            map(
                lambda key: self.input_params.get(key, None),
                kind_check.get(self.kind),
            )
        )):
            raise InvalidInputParameters(
                f"{type(self).__name__} class requires input_params with keys {', '.join(kind_check.get(self.kind))}, some of which are missing."
            )

        # Set the header to maximum size - otherwise wHnd won't even return any frames.
        _header = file.WavHeader.new(file.WAV_MAX_CHUNKSIZE)  # Problem - we don't know how long the file will be prior to complete conversion.
        # We are writing a WAV header - so this needs to be super().write(), not self.write()
        
        # Get super class to init
        super().__init__(
            initial_bytes=b"", # We haven't written the wave header yet, feed it nothing
            bytes_total=bytes_total,
            *args,
            **kwargs,
        )

        # Now write the header
        super().write(_header.construct())
            
        self.get_command()
        self.write(b=initial_bytes)


    def get_command(
        self
    )->command.FFmpegCommand:
        
        if (not isinstance(self.command, command.FFmpegCommand)):
            
            # rw_timeout - not seems to be supported by FFmpeg!!
            # timeout = self.input_params.get("timeout")
            # if (not isinstance(timeout, (float, int))):
            #     timeout = http.DEFAULT_HTTP_TIMEOUT

            # rw_timeout = timeout * 1000000

            input_mapper = {
                "pipe":lambda: io_protocol.FFmpegProtocolPipe.create(
                    pipe=0
                ),
                "file":lambda: io_protocol.FFmpegProtocolFile.create(
                    path=self.input_params.get("path")
                ),
                "http":lambda: io_protocol.FFmpegProtocolHTTP.create(
                    url=self.input_params.get("url"),
                    # rw_timeout=rw_timeout,
                ),
            }
            
            self.command = command.FFmpegCommand(
                input  = input_mapper.get(self.kind)(),
                output = io_protocol.FFmpegProtocolPipe.create(pipe=1),
                options = [
                    # Convert from provided format
                    main_options.FFmpegOptionFormat.create(
                        format = self.format,
                        option_type = classes.FFmpegOptionType.INPUT,
                    ),
                    # Convert to s16le
                    main_options.FFmpegOptionFormat.create(
                        format = "s16le",
                        option_type = classes.FFmpegOptionType.OUTPUT,
                    ),
                ]
            )

            super_instance = super()
            
            def _stream_callback(
                command:command.FFmpegCommand,
                bytes_total:int,
            ):
                self.bytes_total = bytes_total
                if (callable(self.callback)):
                    self.callback(command, bytes_total)
                
            self.command.start()
            
            self.command.stream_stdout(
                super_instance,
                callback=_stream_callback,
            )
        return self.command
    
    def write(
        self,
        b:bytes,
        *args,
        **kwargs,
    ):
        """
        Append bytes to the back of the buffer within thread lock.
        
        As input bytes are a different format as output,
        the input bytes will be fed through a FFmpegCommand to convert to WAV,
        before feeding through super().wrtie().
        """

        if (self.kind == "pipe" or True):
            self.get_command().stream_stdin(b)
        # else:
        #     warnings.warn(
        #         UserWarning(
        #             f"{type(self).__name__} class only support .write() if its kind=pipe. {len(b):,} bytes of data is discarded."
        #         )
        #     )

    @classmethod
    def from_file(
        cls,
        path:str,
        format:str,
        callback:Callable[[command.FFmpegCommand, int], None] = None,
    ):
        bytes_total = file.get_file_size(path)

        if (not isinstance(bytes_total, Exception)):
            _io = cls(
                format = format,
                kind = "file",
                initial_bytes = b"",
                # bytes_total = bytes_total, # DON'T DO THIS - This is the MP3 size, not WAV size!
                input_params = {
                    "path": path,
                },
                callback = callback,
            )
                
            return _io
        else:
            return bytes_total

    @classmethod
    def from_http(
        cls,
        url:str,
        format:str,
        # timeout:float = http.DEFAULT_HTTP_TIMEOUT, # rw_timeout does not work on ffmpeg!!
        bytes_total:int = None,
        callback:Callable[[command.FFmpegCommand, int], None] = None,
        **kwargs,
    )->Union[
        "FFmpegStreamIO",
        Exception,
    ]:
        _io = cls(
            format = format,
            kind = "http",
            initial_bytes = b"",
            bytes_total = bytes_total,
            input_params = {
                "url": url,
                # "timeout": timeout,
            },
            callback = callback,
        )
        
        return _io

def FFmpegStreamFormatDecorator(
    format:str
)->type:
    """
    Function for creating multiple classes 
    """
    
    class _streamIOProxyClass(FFmpegStreamIO):
        def __init__(
            self,
            initial_bytes:bytes = b"",
            kind:str = "pipe",
            input_params:Dict[str, Any] = {
                "path":None,
                "url":None,
                "timeout":None,
            },
            bytes_total:int = None,             # Optional - does not affect the class
            callback:Callable[[command.FFmpegCommand, int], None] = None,
            *args,
            **kwargs,
        )->None:
            # When the super().from_http() calls cls.__init__,
            # it will inevitably include format=.
            # However when cls.__init__ is called, it calls the
            # subclass instead, forcing format= into kwargs.
            # This will result in format being mentioned twice below.
            # Lets kill one of it.

            kwargs["format"] = format

            super().__init__(
                initial_bytes   = initial_bytes,
                # format          = format,
                kind            = kind,
                input_params    = input_params,
                bytes_total     = bytes_total,
                callback        = callback,
                *args,
                **kwargs,
            )

        @classmethod
        def from_file(
            cls,
            path:str,
            callback:Callable[[command.FFmpegCommand, int], None] = None,
        )->Union[
            FFmpegStreamIO,
            Exception,
        ]:
            return super(_streamIOProxyClass, cls).from_file(
                path            = path,
                format          = format,
                callback        = callback,
            )
        
        @classmethod
        def from_http(
            cls,
            url:str,
            # timeout:float = http.DEFAULT_HTTP_TIMEOUT, # rw_timeout does not work on ffmpeg!!
            bytes_total:int = None,
            callback:Callable[[command.FFmpegCommand, int], None] = None,
            **kwargs,
        )->Union[
            FFmpegStreamIO,
            Exception,
        ]:            
            return super(_streamIOProxyClass, cls).from_http(
                url             = url,
                format          = format,
                # timeout         = timeout,
                bytes_total     = bytes_total,
                callback        = callback,
                **kwargs,
            )

    # Dynamically generate class through the proxy class
    return type(
        f"{format.upper()}StreamIO",
        (_streamIOProxyClass, ),
        dict(_streamIOProxyClass.__dict__),
    )


# Generate all the dynamic types
_3DOSTRStreamIO = FFmpegStreamFormatDecorator("3dostr")
_3G2StreamIO = FFmpegStreamFormatDecorator("3g2")
_3GPStreamIO = FFmpegStreamFormatDecorator("3gp")
_4XMStreamIO = FFmpegStreamFormatDecorator("4xm")
A64StreamIO = FFmpegStreamFormatDecorator("a64")
AAStreamIO = FFmpegStreamFormatDecorator("aa")
AACStreamIO = FFmpegStreamFormatDecorator("aac")
AAXStreamIO = FFmpegStreamFormatDecorator("aax")
AC3StreamIO = FFmpegStreamFormatDecorator("ac3")
ACEStreamIO = FFmpegStreamFormatDecorator("ace")
ACMStreamIO = FFmpegStreamFormatDecorator("acm")
ACTStreamIO = FFmpegStreamFormatDecorator("act")
ADFStreamIO = FFmpegStreamFormatDecorator("adf")
ADPStreamIO = FFmpegStreamFormatDecorator("adp")
ADSStreamIO = FFmpegStreamFormatDecorator("ads")
ADTSStreamIO = FFmpegStreamFormatDecorator("adts")
ADXStreamIO = FFmpegStreamFormatDecorator("adx")
AEAStreamIO = FFmpegStreamFormatDecorator("aea")
AFCStreamIO = FFmpegStreamFormatDecorator("afc")
AIFFStreamIO = FFmpegStreamFormatDecorator("aiff")
AIXStreamIO = FFmpegStreamFormatDecorator("aix")
ALAWStreamIO = FFmpegStreamFormatDecorator("alaw")
ALIAS_PIXStreamIO = FFmpegStreamFormatDecorator("alias_pix")
ALPStreamIO = FFmpegStreamFormatDecorator("alp")
AMRStreamIO = FFmpegStreamFormatDecorator("amr")
AMRNBStreamIO = FFmpegStreamFormatDecorator("amrnb")
AMRWBStreamIO = FFmpegStreamFormatDecorator("amrwb")
AMVStreamIO = FFmpegStreamFormatDecorator("amv")
ANMStreamIO = FFmpegStreamFormatDecorator("anm")
APCStreamIO = FFmpegStreamFormatDecorator("apc")
APEStreamIO = FFmpegStreamFormatDecorator("ape")
APMStreamIO = FFmpegStreamFormatDecorator("apm")
APNGStreamIO = FFmpegStreamFormatDecorator("apng")
APTXStreamIO = FFmpegStreamFormatDecorator("aptx")
APTX_HDStreamIO = FFmpegStreamFormatDecorator("aptx_hd")
AQTITLEStreamIO = FFmpegStreamFormatDecorator("aqtitle")
ARGO_ASFStreamIO = FFmpegStreamFormatDecorator("argo_asf")
ARGO_BRPStreamIO = FFmpegStreamFormatDecorator("argo_brp")
ARGO_CVGStreamIO = FFmpegStreamFormatDecorator("argo_cvg")
ASFStreamIO = FFmpegStreamFormatDecorator("asf")
ASF_OStreamIO = FFmpegStreamFormatDecorator("asf_o")
ASF_STREAMStreamIO = FFmpegStreamFormatDecorator("asf_stream")
ASSStreamIO = FFmpegStreamFormatDecorator("ass")
ASTStreamIO = FFmpegStreamFormatDecorator("ast")
AUStreamIO = FFmpegStreamFormatDecorator("au")
AUDIOTOOLBOXStreamIO = FFmpegStreamFormatDecorator("audiotoolbox")
AV1StreamIO = FFmpegStreamFormatDecorator("av1")
AVFOUNDATIONStreamIO = FFmpegStreamFormatDecorator("avfoundation")
AVIStreamIO = FFmpegStreamFormatDecorator("avi")
AVM2StreamIO = FFmpegStreamFormatDecorator("avm2")
AVRStreamIO = FFmpegStreamFormatDecorator("avr")
AVSStreamIO = FFmpegStreamFormatDecorator("avs")
AVS2StreamIO = FFmpegStreamFormatDecorator("avs2")
AVS3StreamIO = FFmpegStreamFormatDecorator("avs3")
BETHSOFTVIDStreamIO = FFmpegStreamFormatDecorator("bethsoftvid")
BFIStreamIO = FFmpegStreamFormatDecorator("bfi")
BFSTMStreamIO = FFmpegStreamFormatDecorator("bfstm")
BINStreamIO = FFmpegStreamFormatDecorator("bin")
BINKStreamIO = FFmpegStreamFormatDecorator("bink")
BINKAStreamIO = FFmpegStreamFormatDecorator("binka")
BITStreamIO = FFmpegStreamFormatDecorator("bit")
BITPACKEDStreamIO = FFmpegStreamFormatDecorator("bitpacked")
BMP_PIPEStreamIO = FFmpegStreamFormatDecorator("bmp_pipe")
BMVStreamIO = FFmpegStreamFormatDecorator("bmv")
BOAStreamIO = FFmpegStreamFormatDecorator("boa")
BRENDER_PIXStreamIO = FFmpegStreamFormatDecorator("brender_pix")
BRSTMStreamIO = FFmpegStreamFormatDecorator("brstm")
C93StreamIO = FFmpegStreamFormatDecorator("c93")
CAFStreamIO = FFmpegStreamFormatDecorator("caf")
CAVSVIDEOStreamIO = FFmpegStreamFormatDecorator("cavsvideo")
CDGStreamIO = FFmpegStreamFormatDecorator("cdg")
CDXLStreamIO = FFmpegStreamFormatDecorator("cdxl")
CINEStreamIO = FFmpegStreamFormatDecorator("cine")
CODEC2StreamIO = FFmpegStreamFormatDecorator("codec2")
CODEC2RAWStreamIO = FFmpegStreamFormatDecorator("codec2raw")
CONCATStreamIO = FFmpegStreamFormatDecorator("concat")
CRCStreamIO = FFmpegStreamFormatDecorator("crc")
CRI_PIPEStreamIO = FFmpegStreamFormatDecorator("cri_pipe")
DASHStreamIO = FFmpegStreamFormatDecorator("dash")
DATAStreamIO = FFmpegStreamFormatDecorator("data")
DAUDStreamIO = FFmpegStreamFormatDecorator("daud")
DCSTRStreamIO = FFmpegStreamFormatDecorator("dcstr")
DDS_PIPEStreamIO = FFmpegStreamFormatDecorator("dds_pipe")
DERFStreamIO = FFmpegStreamFormatDecorator("derf")
DFAStreamIO = FFmpegStreamFormatDecorator("dfa")
DHAVStreamIO = FFmpegStreamFormatDecorator("dhav")
DIRACStreamIO = FFmpegStreamFormatDecorator("dirac")
DNXHDStreamIO = FFmpegStreamFormatDecorator("dnxhd")
DPX_PIPEStreamIO = FFmpegStreamFormatDecorator("dpx_pipe")
DSFStreamIO = FFmpegStreamFormatDecorator("dsf")
DSICINStreamIO = FFmpegStreamFormatDecorator("dsicin")
DSSStreamIO = FFmpegStreamFormatDecorator("dss")
DTSStreamIO = FFmpegStreamFormatDecorator("dts")
DTSHDStreamIO = FFmpegStreamFormatDecorator("dtshd")
DVStreamIO = FFmpegStreamFormatDecorator("dv")
DVBSUBStreamIO = FFmpegStreamFormatDecorator("dvbsub")
DVBTXTStreamIO = FFmpegStreamFormatDecorator("dvbtxt")
DVDStreamIO = FFmpegStreamFormatDecorator("dvd")
DXAStreamIO = FFmpegStreamFormatDecorator("dxa")
EAStreamIO = FFmpegStreamFormatDecorator("ea")
EA_CDATAStreamIO = FFmpegStreamFormatDecorator("ea_cdata")
EAC3StreamIO = FFmpegStreamFormatDecorator("eac3")
EPAFStreamIO = FFmpegStreamFormatDecorator("epaf")
EXR_PIPEStreamIO = FFmpegStreamFormatDecorator("exr_pipe")
F32BEStreamIO = FFmpegStreamFormatDecorator("f32be")
F32LEStreamIO = FFmpegStreamFormatDecorator("f32le")
F4VStreamIO = FFmpegStreamFormatDecorator("f4v")
F64BEStreamIO = FFmpegStreamFormatDecorator("f64be")
F64LEStreamIO = FFmpegStreamFormatDecorator("f64le")
FFMETADATAStreamIO = FFmpegStreamFormatDecorator("ffmetadata")
FIFOStreamIO = FFmpegStreamFormatDecorator("fifo")
FIFO_TESTStreamIO = FFmpegStreamFormatDecorator("fifo_test")
FILM_CPKStreamIO = FFmpegStreamFormatDecorator("film_cpk")
FILMSTRIPStreamIO = FFmpegStreamFormatDecorator("filmstrip")
FITSStreamIO = FFmpegStreamFormatDecorator("fits")
FLACStreamIO = FFmpegStreamFormatDecorator("flac")
FLICStreamIO = FFmpegStreamFormatDecorator("flic")
FLVStreamIO = FFmpegStreamFormatDecorator("flv")
FRAMECRCStreamIO = FFmpegStreamFormatDecorator("framecrc")
FRAMEHASHStreamIO = FFmpegStreamFormatDecorator("framehash")
FRAMEMD5StreamIO = FFmpegStreamFormatDecorator("framemd5")
FRMStreamIO = FFmpegStreamFormatDecorator("frm")
FSBStreamIO = FFmpegStreamFormatDecorator("fsb")
FWSEStreamIO = FFmpegStreamFormatDecorator("fwse")
G722StreamIO = FFmpegStreamFormatDecorator("g722")
G723_1StreamIO = FFmpegStreamFormatDecorator("g723_1")
G726StreamIO = FFmpegStreamFormatDecorator("g726")
G726LEStreamIO = FFmpegStreamFormatDecorator("g726le")
G729StreamIO = FFmpegStreamFormatDecorator("g729")
GDVStreamIO = FFmpegStreamFormatDecorator("gdv")
GEM_PIPEStreamIO = FFmpegStreamFormatDecorator("gem_pipe")
GENHStreamIO = FFmpegStreamFormatDecorator("genh")
GIFStreamIO = FFmpegStreamFormatDecorator("gif")
GIF_PIPEStreamIO = FFmpegStreamFormatDecorator("gif_pipe")
GSMStreamIO = FFmpegStreamFormatDecorator("gsm")
GXFStreamIO = FFmpegStreamFormatDecorator("gxf")
H261StreamIO = FFmpegStreamFormatDecorator("h261")
H263StreamIO = FFmpegStreamFormatDecorator("h263")
H264StreamIO = FFmpegStreamFormatDecorator("h264")
HASHStreamIO = FFmpegStreamFormatDecorator("hash")
HCAStreamIO = FFmpegStreamFormatDecorator("hca")
HCOMStreamIO = FFmpegStreamFormatDecorator("hcom")
HDSStreamIO = FFmpegStreamFormatDecorator("hds")
HEVCStreamIO = FFmpegStreamFormatDecorator("hevc")
HLSStreamIO = FFmpegStreamFormatDecorator("hls")
HNMStreamIO = FFmpegStreamFormatDecorator("hnm")
ICOStreamIO = FFmpegStreamFormatDecorator("ico")
IDCINStreamIO = FFmpegStreamFormatDecorator("idcin")
IDFStreamIO = FFmpegStreamFormatDecorator("idf")
IFFStreamIO = FFmpegStreamFormatDecorator("iff")
IFVStreamIO = FFmpegStreamFormatDecorator("ifv")
ILBCStreamIO = FFmpegStreamFormatDecorator("ilbc")
IMAGE2StreamIO = FFmpegStreamFormatDecorator("image2")
IMAGE2PIPEStreamIO = FFmpegStreamFormatDecorator("image2pipe")
IMFStreamIO = FFmpegStreamFormatDecorator("imf")
INGENIENTStreamIO = FFmpegStreamFormatDecorator("ingenient")
IPMOVIEStreamIO = FFmpegStreamFormatDecorator("ipmovie")
IPODStreamIO = FFmpegStreamFormatDecorator("ipod")
IPUStreamIO = FFmpegStreamFormatDecorator("ipu")
IRCAMStreamIO = FFmpegStreamFormatDecorator("ircam")
ISMVStreamIO = FFmpegStreamFormatDecorator("ismv")
ISSStreamIO = FFmpegStreamFormatDecorator("iss")
IV8StreamIO = FFmpegStreamFormatDecorator("iv8")
IVFStreamIO = FFmpegStreamFormatDecorator("ivf")
IVRStreamIO = FFmpegStreamFormatDecorator("ivr")
J2K_PIPEStreamIO = FFmpegStreamFormatDecorator("j2k_pipe")
JACOSUBStreamIO = FFmpegStreamFormatDecorator("jacosub")
JPEG_PIPEStreamIO = FFmpegStreamFormatDecorator("jpeg_pipe")
JPEGLS_PIPEStreamIO = FFmpegStreamFormatDecorator("jpegls_pipe")
JVStreamIO = FFmpegStreamFormatDecorator("jv")
KUXStreamIO = FFmpegStreamFormatDecorator("kux")
KVAGStreamIO = FFmpegStreamFormatDecorator("kvag")
LATMStreamIO = FFmpegStreamFormatDecorator("latm")
LAVFIStreamIO = FFmpegStreamFormatDecorator("lavfi")
LIVE_FLVStreamIO = FFmpegStreamFormatDecorator("live_flv")
LMLM4StreamIO = FFmpegStreamFormatDecorator("lmlm4")
LOASStreamIO = FFmpegStreamFormatDecorator("loas")
LRCStreamIO = FFmpegStreamFormatDecorator("lrc")
LUODATStreamIO = FFmpegStreamFormatDecorator("luodat")
LVFStreamIO = FFmpegStreamFormatDecorator("lvf")
LXFStreamIO = FFmpegStreamFormatDecorator("lxf")
M4VStreamIO = FFmpegStreamFormatDecorator("m4v")
MATROSKAStreamIO = FFmpegStreamFormatDecorator("matroska")
MATROSKAStreamIO = FFmpegStreamFormatDecorator("matroska")
WEBMStreamIO = FFmpegStreamFormatDecorator("webm")
MCAStreamIO = FFmpegStreamFormatDecorator("mca")
MCCStreamIO = FFmpegStreamFormatDecorator("mcc")
MD5StreamIO = FFmpegStreamFormatDecorator("md5")
MGSTSStreamIO = FFmpegStreamFormatDecorator("mgsts")
MICRODVDStreamIO = FFmpegStreamFormatDecorator("microdvd")
MJPEGStreamIO = FFmpegStreamFormatDecorator("mjpeg")
MJPEG_2000StreamIO = FFmpegStreamFormatDecorator("mjpeg_2000")
MKVTIMESTAMP_V2StreamIO = FFmpegStreamFormatDecorator("mkvtimestamp_v2")
MLPStreamIO = FFmpegStreamFormatDecorator("mlp")
MLVStreamIO = FFmpegStreamFormatDecorator("mlv")
MMStreamIO = FFmpegStreamFormatDecorator("mm")
MMFStreamIO = FFmpegStreamFormatDecorator("mmf")
MODSStreamIO = FFmpegStreamFormatDecorator("mods")
MOFLEXStreamIO = FFmpegStreamFormatDecorator("moflex")
MOVStreamIO = FFmpegStreamFormatDecorator("mov")
MOVStreamIO = FFmpegStreamFormatDecorator("mov")
MP4StreamIO = FFmpegStreamFormatDecorator("mp4")
M4AStreamIO = FFmpegStreamFormatDecorator("m4a")
_3GPStreamIO = FFmpegStreamFormatDecorator("3gp")
_3G2StreamIO = FFmpegStreamFormatDecorator("3g2")
MJ2StreamIO = FFmpegStreamFormatDecorator("mj2")
MP2StreamIO = FFmpegStreamFormatDecorator("mp2")
MP3StreamIO = FFmpegStreamFormatDecorator("mp3")
MP4StreamIO = FFmpegStreamFormatDecorator("mp4")
MPCStreamIO = FFmpegStreamFormatDecorator("mpc")
MPC8StreamIO = FFmpegStreamFormatDecorator("mpc8")
MPEGStreamIO = FFmpegStreamFormatDecorator("mpeg")
MPEG1VIDEOStreamIO = FFmpegStreamFormatDecorator("mpeg1video")
MPEG2VIDEOStreamIO = FFmpegStreamFormatDecorator("mpeg2video")
MPEGTSStreamIO = FFmpegStreamFormatDecorator("mpegts")
MPEGTSRAWStreamIO = FFmpegStreamFormatDecorator("mpegtsraw")
MPEGVIDEOStreamIO = FFmpegStreamFormatDecorator("mpegvideo")
MPJPEGStreamIO = FFmpegStreamFormatDecorator("mpjpeg")
MPL2StreamIO = FFmpegStreamFormatDecorator("mpl2")
MPSUBStreamIO = FFmpegStreamFormatDecorator("mpsub")
MSFStreamIO = FFmpegStreamFormatDecorator("msf")
MSNWCTCPStreamIO = FFmpegStreamFormatDecorator("msnwctcp")
MSPStreamIO = FFmpegStreamFormatDecorator("msp")
MTAFStreamIO = FFmpegStreamFormatDecorator("mtaf")
MTVStreamIO = FFmpegStreamFormatDecorator("mtv")
MULAWStreamIO = FFmpegStreamFormatDecorator("mulaw")
MUSXStreamIO = FFmpegStreamFormatDecorator("musx")
MVStreamIO = FFmpegStreamFormatDecorator("mv")
MVIStreamIO = FFmpegStreamFormatDecorator("mvi")
MXFStreamIO = FFmpegStreamFormatDecorator("mxf")
MXF_D10StreamIO = FFmpegStreamFormatDecorator("mxf_d10")
MXF_OPATOMStreamIO = FFmpegStreamFormatDecorator("mxf_opatom")
MXGStreamIO = FFmpegStreamFormatDecorator("mxg")
NCStreamIO = FFmpegStreamFormatDecorator("nc")
NISTSPHEREStreamIO = FFmpegStreamFormatDecorator("nistsphere")
NSPStreamIO = FFmpegStreamFormatDecorator("nsp")
NSVStreamIO = FFmpegStreamFormatDecorator("nsv")
NULLStreamIO = FFmpegStreamFormatDecorator("null")
NUTStreamIO = FFmpegStreamFormatDecorator("nut")
NUVStreamIO = FFmpegStreamFormatDecorator("nuv")
OBUStreamIO = FFmpegStreamFormatDecorator("obu")
OGAStreamIO = FFmpegStreamFormatDecorator("oga")
OGGStreamIO = FFmpegStreamFormatDecorator("ogg")
OGVStreamIO = FFmpegStreamFormatDecorator("ogv")
OMAStreamIO = FFmpegStreamFormatDecorator("oma")
OPUSStreamIO = FFmpegStreamFormatDecorator("opus")
PAFStreamIO = FFmpegStreamFormatDecorator("paf")
PAM_PIPEStreamIO = FFmpegStreamFormatDecorator("pam_pipe")
PBM_PIPEStreamIO = FFmpegStreamFormatDecorator("pbm_pipe")
PCX_PIPEStreamIO = FFmpegStreamFormatDecorator("pcx_pipe")
PGM_PIPEStreamIO = FFmpegStreamFormatDecorator("pgm_pipe")
PGMYUV_PIPEStreamIO = FFmpegStreamFormatDecorator("pgmyuv_pipe")
PGX_PIPEStreamIO = FFmpegStreamFormatDecorator("pgx_pipe")
PHOTOCD_PIPEStreamIO = FFmpegStreamFormatDecorator("photocd_pipe")
PICTOR_PIPEStreamIO = FFmpegStreamFormatDecorator("pictor_pipe")
PJSStreamIO = FFmpegStreamFormatDecorator("pjs")
PMPStreamIO = FFmpegStreamFormatDecorator("pmp")
PNG_PIPEStreamIO = FFmpegStreamFormatDecorator("png_pipe")
PP_BNKStreamIO = FFmpegStreamFormatDecorator("pp_bnk")
PPM_PIPEStreamIO = FFmpegStreamFormatDecorator("ppm_pipe")
PSD_PIPEStreamIO = FFmpegStreamFormatDecorator("psd_pipe")
PSPStreamIO = FFmpegStreamFormatDecorator("psp")
PSXSTRStreamIO = FFmpegStreamFormatDecorator("psxstr")
PVAStreamIO = FFmpegStreamFormatDecorator("pva")
PVFStreamIO = FFmpegStreamFormatDecorator("pvf")
QCPStreamIO = FFmpegStreamFormatDecorator("qcp")
QDRAW_PIPEStreamIO = FFmpegStreamFormatDecorator("qdraw_pipe")
R3DStreamIO = FFmpegStreamFormatDecorator("r3d")
RAWVIDEOStreamIO = FFmpegStreamFormatDecorator("rawvideo")
REALTEXTStreamIO = FFmpegStreamFormatDecorator("realtext")
REDSPARKStreamIO = FFmpegStreamFormatDecorator("redspark")
RL2StreamIO = FFmpegStreamFormatDecorator("rl2")
RMStreamIO = FFmpegStreamFormatDecorator("rm")
ROQStreamIO = FFmpegStreamFormatDecorator("roq")
RPLStreamIO = FFmpegStreamFormatDecorator("rpl")
RSDStreamIO = FFmpegStreamFormatDecorator("rsd")
RSOStreamIO = FFmpegStreamFormatDecorator("rso")
RTPStreamIO = FFmpegStreamFormatDecorator("rtp")
RTP_MPEGTSStreamIO = FFmpegStreamFormatDecorator("rtp_mpegts")
RTSPStreamIO = FFmpegStreamFormatDecorator("rtsp")
S16BEStreamIO = FFmpegStreamFormatDecorator("s16be")
S16LEStreamIO = FFmpegStreamFormatDecorator("s16le")
S24BEStreamIO = FFmpegStreamFormatDecorator("s24be")
S24LEStreamIO = FFmpegStreamFormatDecorator("s24le")
S32BEStreamIO = FFmpegStreamFormatDecorator("s32be")
S32LEStreamIO = FFmpegStreamFormatDecorator("s32le")
S337MStreamIO = FFmpegStreamFormatDecorator("s337m")
S8StreamIO = FFmpegStreamFormatDecorator("s8")
SAMIStreamIO = FFmpegStreamFormatDecorator("sami")
SAPStreamIO = FFmpegStreamFormatDecorator("sap")
SBCStreamIO = FFmpegStreamFormatDecorator("sbc")
SBGStreamIO = FFmpegStreamFormatDecorator("sbg")
SCCStreamIO = FFmpegStreamFormatDecorator("scc")
SCDStreamIO = FFmpegStreamFormatDecorator("scd")
SDLStreamIO = FFmpegStreamFormatDecorator("sdl")
SDL2StreamIO = FFmpegStreamFormatDecorator("sdl2")
SDPStreamIO = FFmpegStreamFormatDecorator("sdp")
SDR2StreamIO = FFmpegStreamFormatDecorator("sdr2")
SDSStreamIO = FFmpegStreamFormatDecorator("sds")
SDXStreamIO = FFmpegStreamFormatDecorator("sdx")
SEGMENTStreamIO = FFmpegStreamFormatDecorator("segment")
SERStreamIO = FFmpegStreamFormatDecorator("ser")
SGAStreamIO = FFmpegStreamFormatDecorator("sga")
SGI_PIPEStreamIO = FFmpegStreamFormatDecorator("sgi_pipe")
SHNStreamIO = FFmpegStreamFormatDecorator("shn")
SIFFStreamIO = FFmpegStreamFormatDecorator("siff")
SIMBIOSIS_IMXStreamIO = FFmpegStreamFormatDecorator("simbiosis_imx")
SLNStreamIO = FFmpegStreamFormatDecorator("sln")
SMJPEGStreamIO = FFmpegStreamFormatDecorator("smjpeg")
SMKStreamIO = FFmpegStreamFormatDecorator("smk")
SMOOTHSTREAMINGStreamIO = FFmpegStreamFormatDecorator("smoothstreaming")
SMUSHStreamIO = FFmpegStreamFormatDecorator("smush")
SOLStreamIO = FFmpegStreamFormatDecorator("sol")
SOXStreamIO = FFmpegStreamFormatDecorator("sox")
SPDIFStreamIO = FFmpegStreamFormatDecorator("spdif")
SPXStreamIO = FFmpegStreamFormatDecorator("spx")
SRTStreamIO = FFmpegStreamFormatDecorator("srt")
STLStreamIO = FFmpegStreamFormatDecorator("stl")
STREAM_SEGMENTStreamIO = FFmpegStreamFormatDecorator("stream_segment")
SSEGMENTStreamIO = FFmpegStreamFormatDecorator("ssegment")
STREAMHASHStreamIO = FFmpegStreamFormatDecorator("streamhash")
SUBVIEWERStreamIO = FFmpegStreamFormatDecorator("subviewer")
SUBVIEWER1StreamIO = FFmpegStreamFormatDecorator("subviewer1")
SUNRAST_PIPEStreamIO = FFmpegStreamFormatDecorator("sunrast_pipe")
SUPStreamIO = FFmpegStreamFormatDecorator("sup")
SVAGStreamIO = FFmpegStreamFormatDecorator("svag")
SVCDStreamIO = FFmpegStreamFormatDecorator("svcd")
SVG_PIPEStreamIO = FFmpegStreamFormatDecorator("svg_pipe")
SVSStreamIO = FFmpegStreamFormatDecorator("svs")
SWFStreamIO = FFmpegStreamFormatDecorator("swf")
TAKStreamIO = FFmpegStreamFormatDecorator("tak")
TEDCAPTIONSStreamIO = FFmpegStreamFormatDecorator("tedcaptions")
TEEStreamIO = FFmpegStreamFormatDecorator("tee")
THPStreamIO = FFmpegStreamFormatDecorator("thp")
TIERTEXSEQStreamIO = FFmpegStreamFormatDecorator("tiertexseq")
TIFF_PIPEStreamIO = FFmpegStreamFormatDecorator("tiff_pipe")
TMVStreamIO = FFmpegStreamFormatDecorator("tmv")
TRUEHDStreamIO = FFmpegStreamFormatDecorator("truehd")
TTAStreamIO = FFmpegStreamFormatDecorator("tta")
TTMLStreamIO = FFmpegStreamFormatDecorator("ttml")
TTYStreamIO = FFmpegStreamFormatDecorator("tty")
TXDStreamIO = FFmpegStreamFormatDecorator("txd")
TYStreamIO = FFmpegStreamFormatDecorator("ty")
U16BEStreamIO = FFmpegStreamFormatDecorator("u16be")
U16LEStreamIO = FFmpegStreamFormatDecorator("u16le")
U24BEStreamIO = FFmpegStreamFormatDecorator("u24be")
U24LEStreamIO = FFmpegStreamFormatDecorator("u24le")
U32BEStreamIO = FFmpegStreamFormatDecorator("u32be")
U32LEStreamIO = FFmpegStreamFormatDecorator("u32le")
U8StreamIO = FFmpegStreamFormatDecorator("u8")
UNCODEDFRAMECRCStreamIO = FFmpegStreamFormatDecorator("uncodedframecrc")
V210StreamIO = FFmpegStreamFormatDecorator("v210")
V210XStreamIO = FFmpegStreamFormatDecorator("v210x")
VAGStreamIO = FFmpegStreamFormatDecorator("vag")
VC1StreamIO = FFmpegStreamFormatDecorator("vc1")
VC1TESTStreamIO = FFmpegStreamFormatDecorator("vc1test")
VCDStreamIO = FFmpegStreamFormatDecorator("vcd")
VIDCStreamIO = FFmpegStreamFormatDecorator("vidc")
VIVIDASStreamIO = FFmpegStreamFormatDecorator("vividas")
VIVOStreamIO = FFmpegStreamFormatDecorator("vivo")
VMDStreamIO = FFmpegStreamFormatDecorator("vmd")
VOBStreamIO = FFmpegStreamFormatDecorator("vob")
VOBSUBStreamIO = FFmpegStreamFormatDecorator("vobsub")
VOCStreamIO = FFmpegStreamFormatDecorator("voc")
VPKStreamIO = FFmpegStreamFormatDecorator("vpk")
VPLAYERStreamIO = FFmpegStreamFormatDecorator("vplayer")
VQFStreamIO = FFmpegStreamFormatDecorator("vqf")
W64StreamIO = FFmpegStreamFormatDecorator("w64")
WAVStreamIO = FFmpegStreamFormatDecorator("wav")
WC3MOVIEStreamIO = FFmpegStreamFormatDecorator("wc3movie")
WEBMStreamIO = FFmpegStreamFormatDecorator("webm")
WEBM_CHUNKStreamIO = FFmpegStreamFormatDecorator("webm_chunk")
WEBM_DASH_MANIFESTStreamIO = FFmpegStreamFormatDecorator("webm_dash_manifest")
WEBPStreamIO = FFmpegStreamFormatDecorator("webp")
WEBP_PIPEStreamIO = FFmpegStreamFormatDecorator("webp_pipe")
WEBVTTStreamIO = FFmpegStreamFormatDecorator("webvtt")
WSAUDStreamIO = FFmpegStreamFormatDecorator("wsaud")
WSDStreamIO = FFmpegStreamFormatDecorator("wsd")
WSVQAStreamIO = FFmpegStreamFormatDecorator("wsvqa")
WTVStreamIO = FFmpegStreamFormatDecorator("wtv")
WVStreamIO = FFmpegStreamFormatDecorator("wv")
WVEStreamIO = FFmpegStreamFormatDecorator("wve")
X11GRABStreamIO = FFmpegStreamFormatDecorator("x11grab")
XAStreamIO = FFmpegStreamFormatDecorator("xa")
XBINStreamIO = FFmpegStreamFormatDecorator("xbin")
XBM_PIPEStreamIO = FFmpegStreamFormatDecorator("xbm_pipe")
XMVStreamIO = FFmpegStreamFormatDecorator("xmv")
XPM_PIPEStreamIO = FFmpegStreamFormatDecorator("xpm_pipe")
XVAGStreamIO = FFmpegStreamFormatDecorator("xvag")
XWD_PIPEStreamIO = FFmpegStreamFormatDecorator("xwd_pipe")
XWMAStreamIO = FFmpegStreamFormatDecorator("xwma")
YOPStreamIO = FFmpegStreamFormatDecorator("yop")
YUV4MPEGPIPEStreamIO = FFmpegStreamFormatDecorator("yuv4mpegpipe")
