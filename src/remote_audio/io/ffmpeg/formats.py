#!/usr/bin/env python3

"""
All FFmpeg accepted formats,
libavformat    59. 16.100 / 59. 16.100
"""

FFMPEG_FORMATS = {
    "3dostr":{
        "description":"3DO STR",
        "demux":True,
        "mux":False,
    },
    "3g2":{
        "description":"3GP2 (3GPP2 file format)",
        "demux":False,
        "mux":True,
    },
    "3gp":{
        "description":"3GP (3GPP file format)",
        "demux":False,
        "mux":True,
    },
    "4xm":{
        "description":"4X Technologies",
        "demux":True,
        "mux":False,
    },
    "a64":{
        "description":"a64 - video for Commodore 64",
        "demux":False,
        "mux":True,
    },
    "aa":{
        "description":"Audible AA format files",
        "demux":True,
        "mux":False,
    },
    "aac":{
        "description":"raw ADTS AAC (Advanced Audio Coding)",
        "demux":True,
        "mux":False,
    },
    "aax":{
        "description":"CRI AAX",
        "demux":True,
        "mux":False,
    },
    "ac3":{
        "description":"raw AC-3",
        "demux":True,
        "mux":True,
    },
    "ace":{
        "description":"tri-Ace Audio Container",
        "demux":True,
        "mux":False,
    },
    "acm":{
        "description":"Interplay ACM",
        "demux":True,
        "mux":False,
    },
    "act":{
        "description":"ACT Voice file format",
        "demux":True,
        "mux":False,
    },
    "adf":{
        "description":"Artworx Data Format",
        "demux":True,
        "mux":False,
    },
    "adp":{
        "description":"ADP",
        "demux":True,
        "mux":False,
    },
    "ads":{
        "description":"Sony PS2 ADS",
        "demux":True,
        "mux":False,
    },
    "adts":{
        "description":"ADTS AAC (Advanced Audio Coding)",
        "demux":False,
        "mux":True,
    },
    "adx":{
        "description":"CRI ADX",
        "demux":True,
        "mux":True,
    },
    "aea":{
        "description":"MD STUDIO audio",
        "demux":True,
        "mux":False,
    },
    "afc":{
        "description":"AFC",
        "demux":True,
        "mux":False,
    },
    "aiff":{
        "description":"Audio IFF",
        "demux":True,
        "mux":True,
    },
    "aix":{
        "description":"CRI AIX",
        "demux":True,
        "mux":False,
    },
    "alaw":{
        "description":"PCM A-law",
        "demux":True,
        "mux":True,
    },
    "alias_pix":{
        "description":"Alias/Wavefront PIX image",
        "demux":True,
        "mux":False,
    },
    "alp":{
        "description":"LEGO Racers ALP",
        "demux":True,
        "mux":True,
    },
    "amr":{
        "description":"3GPP AMR",
        "demux":True,
        "mux":True,
    },
    "amrnb":{
        "description":"raw AMR-NB",
        "demux":True,
        "mux":False,
    },
    "amrwb":{
        "description":"raw AMR-WB",
        "demux":True,
        "mux":False,
    },
    "amv":{
        "description":"AMV",
        "demux":False,
        "mux":True,
    },
    "anm":{
        "description":"Deluxe Paint Animation",
        "demux":True,
        "mux":False,
    },
    "apc":{
        "description":"CRYO APC",
        "demux":True,
        "mux":False,
    },
    "ape":{
        "description":"Monkey's Audio",
        "demux":True,
        "mux":False,
    },
    "apm":{
        "description":"Ubisoft Rayman 2 APM",
        "demux":True,
        "mux":True,
    },
    "apng":{
        "description":"Animated Portable Network Graphics",
        "demux":True,
        "mux":True,
    },
    "aptx":{
        "description":"raw aptX (Audio Processing Technology for Bluetooth)",
        "demux":True,
        "mux":True,
    },
    "aptx_hd":{
        "description":"raw aptX HD (Audio Processing Technology for Bluetooth)",
        "demux":True,
        "mux":True,
    },
    "aqtitle":{
        "description":"AQTitle subtitles",
        "demux":True,
        "mux":False,
    },
    "argo_asf":{
        "description":"Argonaut Games ASF",
        "demux":True,
        "mux":True,
    },
    "argo_brp":{
        "description":"Argonaut Games BRP",
        "demux":True,
        "mux":False,
    },
    "argo_cvg":{
        "description":"Argonaut Games CVG",
        "demux":True,
        "mux":True,
    },
    "asf":{
        "description":"ASF (Advanced / Active Streaming Format)",
        "demux":True,
        "mux":True,
    },
    "asf_o":{
        "description":"ASF (Advanced / Active Streaming Format)",
        "demux":True,
        "mux":False,
    },
    "asf_stream":{
        "description":"ASF (Advanced / Active Streaming Format)",
        "demux":False,
        "mux":True,
    },
    "ass":{
        "description":"SSA (SubStation Alpha) subtitle",
        "demux":True,
        "mux":True,
    },
    "ast":{
        "description":"AST (Audio Stream)",
        "demux":True,
        "mux":True,
    },
    "au":{
        "description":"Sun AU",
        "demux":True,
        "mux":True,
    },
    "audiotoolbox":{
        "description":"AudioToolbox output device",
        "demux":False,
        "mux":True,
    },
    "av1":{
        "description":"AV1 Annex B",
        "demux":True,
        "mux":False,
    },
    "avfoundation":{
        "description":"AVFoundation input device",
        "demux":True,
        "mux":False,
    },
    "avi":{
        "description":"AVI (Audio Video Interleaved)",
        "demux":True,
        "mux":True,
    },
    "avm2":{
        "description":"SWF (ShockWave Flash) (AVM2)",
        "demux":False,
        "mux":True,
    },
    "avr":{
        "description":"AVR (Audio Visual Research)",
        "demux":True,
        "mux":False,
    },
    "avs":{
        "description":"Argonaut Games Creature Shock",
        "demux":True,
        "mux":False,
    },
    "avs2":{
        "description":"raw AVS2-P2/IEEE1857.4 video",
        "demux":True,
        "mux":True,
    },
    "avs3":{
        "description":"AVS3-P2/IEEE1857.10",
        "demux":True,
        "mux":True,
    },
    "bethsoftvid":{
        "description":"Bethesda Softworks VID",
        "demux":True,
        "mux":False,
    },
    "bfi":{
        "description":"Brute Force & Ignorance",
        "demux":True,
        "mux":False,
    },
    "bfstm":{
        "description":"BFSTM (Binary Cafe Stream)",
        "demux":True,
        "mux":False,
    },
    "bin":{
        "description":"Binary text",
        "demux":True,
        "mux":False,
    },
    "bink":{
        "description":"Bink",
        "demux":True,
        "mux":False,
    },
    "binka":{
        "description":"Bink Audio",
        "demux":True,
        "mux":False,
    },
    "bit":{
        "description":"G.729 BIT file format",
        "demux":True,
        "mux":True,
    },
    "bitpacked":{
        "description":"Bitpacked",
        "demux":True,
        "mux":False,
    },
    "bmp_pipe":{
        "description":"piped bmp sequence",
        "demux":True,
        "mux":False,
    },
    "bmv":{
        "description":"Discworld II BMV",
        "demux":True,
        "mux":False,
    },
    "boa":{
        "description":"Black Ops Audio",
        "demux":True,
        "mux":False,
    },
    "brender_pix":{
        "description":"BRender PIX image",
        "demux":True,
        "mux":False,
    },
    "brstm":{
        "description":"BRSTM (Binary Revolution Stream)",
        "demux":True,
        "mux":False,
    },
    "c93":{
        "description":"Interplay C93",
        "demux":True,
        "mux":False,
    },
    "caf":{
        "description":"Apple CAF (Core Audio Format)",
        "demux":True,
        "mux":True,
    },
    "cavsvideo":{
        "description":"raw Chinese AVS (Audio Video Standard) video",
        "demux":True,
        "mux":True,
    },
    "cdg":{
        "description":"CD Graphics",
        "demux":True,
        "mux":False,
    },
    "cdxl":{
        "description":"Commodore CDXL video",
        "demux":True,
        "mux":False,
    },
    "cine":{
        "description":"Phantom Cine",
        "demux":True,
        "mux":False,
    },
    "codec2":{
        "description":"codec2 .c2 muxer",
        "demux":True,
        "mux":True,
    },
    "codec2raw":{
        "description":"raw codec2 muxer",
        "demux":True,
        "mux":True,
    },
    "concat":{
        "description":"Virtual concatenation script",
        "demux":True,
        "mux":False,
    },
    "crc":{
        "description":"CRC testing",
        "demux":False,
        "mux":True,
    },
    "cri_pipe":{
        "description":"piped cri sequence",
        "demux":True,
        "mux":False,
    },
    "dash":{
        "description":"DASH Muxer",
        "demux":True,
        "mux":True,
    },
    "data":{
        "description":"raw data",
        "demux":True,
        "mux":True,
    },
    "daud":{
        "description":"D-Cinema audio",
        "demux":True,
        "mux":True,
    },
    "dcstr":{
        "description":"Sega DC STR",
        "demux":True,
        "mux":False,
    },
    "dds_pipe":{
        "description":"piped dds sequence",
        "demux":True,
        "mux":False,
    },
    "derf":{
        "description":"Xilam DERF",
        "demux":True,
        "mux":False,
    },
    "dfa":{
        "description":"Chronomaster DFA",
        "demux":True,
        "mux":False,
    },
    "dhav":{
        "description":"Video DAV",
        "demux":True,
        "mux":False,
    },
    "dirac":{
        "description":"raw Dirac",
        "demux":True,
        "mux":True,
    },
    "dnxhd":{
        "description":"raw DNxHD (SMPTE VC-3)",
        "demux":True,
        "mux":True,
    },
    "dpx_pipe":{
        "description":"piped dpx sequence",
        "demux":True,
        "mux":False,
    },
    "dsf":{
        "description":"DSD Stream File (DSF)",
        "demux":True,
        "mux":False,
    },
    "dsicin":{
        "description":"Delphine Software International CIN",
        "demux":True,
        "mux":False,
    },
    "dss":{
        "description":"Digital Speech Standard (DSS)",
        "demux":True,
        "mux":False,
    },
    "dts":{
        "description":"raw DTS",
        "demux":True,
        "mux":True,
    },
    "dtshd":{
        "description":"raw DTS-HD",
        "demux":True,
        "mux":False,
    },
    "dv":{
        "description":"DV (Digital Video)",
        "demux":True,
        "mux":True,
    },
    "dvbsub":{
        "description":"raw dvbsub",
        "demux":True,
        "mux":False,
    },
    "dvbtxt":{
        "description":"dvbtxt",
        "demux":True,
        "mux":False,
    },
    "dvd":{
        "description":"MPEG-2 PS (DVD VOB)",
        "demux":False,
        "mux":True,
    },
    "dxa":{
        "description":"DXA",
        "demux":True,
        "mux":False,
    },
    "ea":{
        "description":"Electronic Arts Multimedia",
        "demux":True,
        "mux":False,
    },
    "ea_cdata":{
        "description":"Electronic Arts cdata",
        "demux":True,
        "mux":False,
    },
    "eac3":{
        "description":"raw E-AC-3",
        "demux":True,
        "mux":True,
    },
    "epaf":{
        "description":"Ensoniq Paris Audio File",
        "demux":True,
        "mux":False,
    },
    "exr_pipe":{
        "description":"piped exr sequence",
        "demux":True,
        "mux":False,
    },
    "f32be":{
        "description":"PCM 32-bit floating-point big-endian",
        "demux":True,
        "mux":True,
    },
    "f32le":{
        "description":"PCM 32-bit floating-point little-endian",
        "demux":True,
        "mux":True,
    },
    "f4v":{
        "description":"F4V Adobe Flash Video",
        "demux":False,
        "mux":True,
    },
    "f64be":{
        "description":"PCM 64-bit floating-point big-endian",
        "demux":True,
        "mux":True,
    },
    "f64le":{
        "description":"PCM 64-bit floating-point little-endian",
        "demux":True,
        "mux":True,
    },
    "ffmetadata":{
        "description":"FFmpeg metadata in text",
        "demux":True,
        "mux":True,
    },
    "fifo":{
        "description":"FIFO queue pseudo-muxer",
        "demux":False,
        "mux":True,
    },
    "fifo_test":{
        "description":"Fifo test muxer",
        "demux":False,
        "mux":True,
    },
    "film_cpk":{
        "description":"Sega FILM / CPK",
        "demux":True,
        "mux":True,
    },
    "filmstrip":{
        "description":"Adobe Filmstrip",
        "demux":True,
        "mux":True,
    },
    "fits":{
        "description":"Flexible Image Transport System",
        "demux":True,
        "mux":True,
    },
    "flac":{
        "description":"raw FLAC",
        "demux":True,
        "mux":True,
    },
    "flic":{
        "description":"FLI/FLC/FLX animation",
        "demux":True,
        "mux":False,
    },
    "flv":{
        "description":"FLV (Flash Video)",
        "demux":True,
        "mux":True,
    },
    "framecrc":{
        "description":"framecrc testing",
        "demux":False,
        "mux":True,
    },
    "framehash":{
        "description":"Per-frame hash testing",
        "demux":False,
        "mux":True,
    },
    "framemd5":{
        "description":"Per-frame MD5 testing",
        "demux":False,
        "mux":True,
    },
    "frm":{
        "description":"Megalux Frame",
        "demux":True,
        "mux":False,
    },
    "fsb":{
        "description":"FMOD Sample Bank",
        "demux":True,
        "mux":False,
    },
    "fwse":{
        "description":"Capcom's MT Framework sound",
        "demux":True,
        "mux":False,
    },
    "g722":{
        "description":"raw G.722",
        "demux":True,
        "mux":True,
    },
    "g723_1":{
        "description":"raw G.723.1",
        "demux":True,
        "mux":True,
    },
    "g726":{
        "description":"raw big-endian G.726 (left-justified)",
        "demux":True,
        "mux":True,
    },
    "g726le":{
        "description":"raw little-endian G.726 (right-justified)",
        "demux":True,
        "mux":True,
    },
    "g729":{
        "description":"G.729 raw format demuxer",
        "demux":True,
        "mux":False,
    },
    "gdv":{
        "description":"Gremlin Digital Video",
        "demux":True,
        "mux":False,
    },
    "gem_pipe":{
        "description":"piped gem sequence",
        "demux":True,
        "mux":False,
    },
    "genh":{
        "description":"GENeric Header",
        "demux":True,
        "mux":False,
    },
    "gif":{
        "description":"CompuServe Graphics Interchange Format (GIF)",
        "demux":True,
        "mux":True,
    },
    "gif_pipe":{
        "description":"piped gif sequence",
        "demux":True,
        "mux":False,
    },
    "gsm":{
        "description":"raw GSM",
        "demux":True,
        "mux":True,
    },
    "gxf":{
        "description":"GXF (General eXchange Format)",
        "demux":True,
        "mux":True,
    },
    "h261":{
        "description":"raw H.261",
        "demux":True,
        "mux":True,
    },
    "h263":{
        "description":"raw H.263",
        "demux":True,
        "mux":True,
    },
    "h264":{
        "description":"raw H.264 video",
        "demux":True,
        "mux":True,
    },
    "hash":{
        "description":"Hash testing",
        "demux":False,
        "mux":True,
    },
    "hca":{
        "description":"CRI HCA",
        "demux":True,
        "mux":False,
    },
    "hcom":{
        "description":"Macintosh HCOM",
        "demux":True,
        "mux":False,
    },
    "hds":{
        "description":"HDS Muxer",
        "demux":False,
        "mux":True,
    },
    "hevc":{
        "description":"raw HEVC video",
        "demux":True,
        "mux":True,
    },
    "hls":{
        "description":"Apple HTTP Live Streaming",
        "demux":True,
        "mux":True,
    },
    "hnm":{
        "description":"Cryo HNM v4",
        "demux":True,
        "mux":False,
    },
    "ico":{
        "description":"Microsoft Windows ICO",
        "demux":True,
        "mux":True,
    },
    "idcin":{
        "description":"id Cinematic",
        "demux":True,
        "mux":False,
    },
    "idf":{
        "description":"iCE Draw File",
        "demux":True,
        "mux":False,
    },
    "iff":{
        "description":"IFF (Interchange File Format)",
        "demux":True,
        "mux":False,
    },
    "ifv":{
        "description":"IFV CCTV DVR",
        "demux":True,
        "mux":False,
    },
    "ilbc":{
        "description":"iLBC storage",
        "demux":True,
        "mux":True,
    },
    "image2":{
        "description":"image2 sequence",
        "demux":True,
        "mux":True,
    },
    "image2pipe":{
        "description":"piped image2 sequence",
        "demux":True,
        "mux":True,
    },
    "imf":{
        "description":"IMF (Interoperable Master Format)",
        "demux":True,
        "mux":False,
    },
    "ingenient":{
        "description":"raw Ingenient MJPEG",
        "demux":True,
        "mux":False,
    },
    "ipmovie":{
        "description":"Interplay MVE",
        "demux":True,
        "mux":False,
    },
    "ipod":{
        "description":"iPod H.264 MP4 (MPEG-4 Part 14)",
        "demux":False,
        "mux":True,
    },
    "ipu":{
        "description":"raw IPU Video",
        "demux":True,
        "mux":False,
    },
    "ircam":{
        "description":"Berkeley/IRCAM/CARL Sound Format",
        "demux":True,
        "mux":True,
    },
    "ismv":{
        "description":"ISMV/ISMA (Smooth Streaming)",
        "demux":False,
        "mux":True,
    },
    "iss":{
        "description":"Funcom ISS",
        "demux":True,
        "mux":False,
    },
    "iv8":{
        "description":"IndigoVision 8000 video",
        "demux":True,
        "mux":False,
    },
    "ivf":{
        "description":"On2 IVF",
        "demux":True,
        "mux":True,
    },
    "ivr":{
        "description":"IVR (Internet Video Recording)",
        "demux":True,
        "mux":False,
    },
    "j2k_pipe":{
        "description":"piped j2k sequence",
        "demux":True,
        "mux":False,
    },
    "jacosub":{
        "description":"JACOsub subtitle format",
        "demux":True,
        "mux":True,
    },
    "jpeg_pipe":{
        "description":"piped jpeg sequence",
        "demux":True,
        "mux":False,
    },
    "jpegls_pipe":{
        "description":"piped jpegls sequence",
        "demux":True,
        "mux":False,
    },
    "jv":{
        "description":"Bitmap Brothers JV",
        "demux":True,
        "mux":False,
    },
    "kux":{
        "description":"KUX (YouKu)",
        "demux":True,
        "mux":False,
    },
    "kvag":{
        "description":"Simon & Schuster Interactive VAG",
        "demux":True,
        "mux":True,
    },
    "latm":{
        "description":"LOAS/LATM",
        "demux":False,
        "mux":True,
    },
    "lavfi":{
        "description":"Libavfilter virtual input device",
        "demux":True,
        "mux":False,
    },
    "live_flv":{
        "description":"live RTMP FLV (Flash Video)",
        "demux":True,
        "mux":False,
    },
    "lmlm4":{
        "description":"raw lmlm4",
        "demux":True,
        "mux":False,
    },
    "loas":{
        "description":"LOAS AudioSyncStream",
        "demux":True,
        "mux":False,
    },
    "lrc":{
        "description":"LRC lyrics",
        "demux":True,
        "mux":True,
    },
    "luodat":{
        "description":"Video CCTV DAT",
        "demux":True,
        "mux":False,
    },
    "lvf":{
        "description":"LVF",
        "demux":True,
        "mux":False,
    },
    "lxf":{
        "description":"VR native stream (LXF)",
        "demux":True,
        "mux":False,
    },
    "m4v":{
        "description":"raw MPEG-4 video",
        "demux":True,
        "mux":True,
    },
    "matroska":{
        "description":"Matroska",
        "demux":False,
        "mux":True,
    },
    "matroska,webm":{
        "description":"Matroska / WebM",
        "demux":True,
        "mux":False,
    },
    "mca":{
        "description":"MCA Audio Format",
        "demux":True,
        "mux":False,
    },
    "mcc":{
        "description":"MacCaption",
        "demux":True,
        "mux":False,
    },
    "md5":{
        "description":"MD5 testing",
        "demux":False,
        "mux":True,
    },
    "mgsts":{
        "description":"Metal Gear Solid: The Twin Snakes",
        "demux":True,
        "mux":False,
    },
    "microdvd":{
        "description":"MicroDVD subtitle format",
        "demux":True,
        "mux":True,
    },
    "mjpeg":{
        "description":"raw MJPEG video",
        "demux":True,
        "mux":True,
    },
    "mjpeg_2000":{
        "description":"raw MJPEG 2000 video",
        "demux":True,
        "mux":False,
    },
    "mkvtimestamp_v2":{
        "description":"extract pts as timecode v2 format, as defined by mkvtoolnix",
        "demux":False,
        "mux":True,
    },
    "mlp":{
        "description":"raw MLP",
        "demux":True,
        "mux":True,
    },
    "mlv":{
        "description":"Magic Lantern Video (MLV)",
        "demux":True,
        "mux":False,
    },
    "mm":{
        "description":"American Laser Games MM",
        "demux":True,
        "mux":False,
    },
    "mmf":{
        "description":"Yamaha SMAF",
        "demux":True,
        "mux":True,
    },
    "mods":{
        "description":"MobiClip MODS",
        "demux":True,
        "mux":False,
    },
    "moflex":{
        "description":"MobiClip MOFLEX",
        "demux":True,
        "mux":False,
    },
    "mov":{
        "description":"QuickTime / MOV",
        "demux":False,
        "mux":True,
    },
    "mov,mp4,m4a,3gp,3g2,mj2":{
        "description":"QuickTime / MOV",
        "demux":True,
        "mux":False,
    },
    "mp2":{
        "description":"MP2 (MPEG audio layer 2)",
        "demux":False,
        "mux":True,
    },
    "mp3":{
        "description":"MP3 (MPEG audio layer 3)",
        "demux":True,
        "mux":True,
    },
    "mp4":{
        "description":"MP4 (MPEG-4 Part 14)",
        "demux":False,
        "mux":True,
    },
    "mpc":{
        "description":"Musepack",
        "demux":True,
        "mux":False,
    },
    "mpc8":{
        "description":"Musepack SV8",
        "demux":True,
        "mux":False,
    },
    "mpeg":{
        "description":"MPEG-1 Systems / MPEG program stream",
        "demux":True,
        "mux":True,
    },
    "mpeg1video":{
        "description":"raw MPEG-1 video",
        "demux":False,
        "mux":True,
    },
    "mpeg2video":{
        "description":"raw MPEG-2 video",
        "demux":False,
        "mux":True,
    },
    "mpegts":{
        "description":"MPEG-TS (MPEG-2 Transport Stream)",
        "demux":True,
        "mux":True,
    },
    "mpegtsraw":{
        "description":"raw MPEG-TS (MPEG-2 Transport Stream)",
        "demux":True,
        "mux":False,
    },
    "mpegvideo":{
        "description":"raw MPEG video",
        "demux":True,
        "mux":False,
    },
    "mpjpeg":{
        "description":"MIME multipart JPEG",
        "demux":True,
        "mux":True,
    },
    "mpl2":{
        "description":"MPL2 subtitles",
        "demux":True,
        "mux":False,
    },
    "mpsub":{
        "description":"MPlayer subtitles",
        "demux":True,
        "mux":False,
    },
    "msf":{
        "description":"Sony PS3 MSF",
        "demux":True,
        "mux":False,
    },
    "msnwctcp":{
        "description":"MSN TCP Webcam stream",
        "demux":True,
        "mux":False,
    },
    "msp":{
        "description":"Microsoft Paint (MSP))",
        "demux":True,
        "mux":False,
    },
    "mtaf":{
        "description":"Konami PS2 MTAF",
        "demux":True,
        "mux":False,
    },
    "mtv":{
        "description":"MTV",
        "demux":True,
        "mux":False,
    },
    "mulaw":{
        "description":"PCM mu-law",
        "demux":True,
        "mux":True,
    },
    "musx":{
        "description":"Eurocom MUSX",
        "demux":True,
        "mux":False,
    },
    "mv":{
        "description":"Silicon Graphics Movie",
        "demux":True,
        "mux":False,
    },
    "mvi":{
        "description":"Motion Pixels MVI",
        "demux":True,
        "mux":False,
    },
    "mxf":{
        "description":"MXF (Material eXchange Format)",
        "demux":True,
        "mux":True,
    },
    "mxf_d10":{
        "description":"MXF (Material eXchange Format) D-10 Mapping",
        "demux":False,
        "mux":True,
    },
    "mxf_opatom":{
        "description":"MXF (Material eXchange Format) Operational Pattern Atom",
        "demux":False,
        "mux":True,
    },
    "mxg":{
        "description":"MxPEG clip",
        "demux":True,
        "mux":False,
    },
    "nc":{
        "description":"NC camera feed",
        "demux":True,
        "mux":False,
    },
    "nistsphere":{
        "description":"NIST SPeech HEader REsources",
        "demux":True,
        "mux":False,
    },
    "nsp":{
        "description":"Computerized Speech Lab NSP",
        "demux":True,
        "mux":False,
    },
    "nsv":{
        "description":"Nullsoft Streaming Video",
        "demux":True,
        "mux":False,
    },
    "null":{
        "description":"raw null video",
        "demux":False,
        "mux":True,
    },
    "nut":{
        "description":"NUT",
        "demux":True,
        "mux":True,
    },
    "nuv":{
        "description":"NuppelVideo",
        "demux":True,
        "mux":False,
    },
    "obu":{
        "description":"AV1 low overhead OBU",
        "demux":True,
        "mux":True,
    },
    "oga":{
        "description":"Ogg Audio",
        "demux":False,
        "mux":True,
    },
    "ogg":{
        "description":"Ogg",
        "demux":True,
        "mux":True,
    },
    "ogv":{
        "description":"Ogg Video",
        "demux":False,
        "mux":True,
    },
    "oma":{
        "description":"Sony OpenMG audio",
        "demux":True,
        "mux":True,
    },
    "opus":{
        "description":"Ogg Opus",
        "demux":False,
        "mux":True,
    },
    "paf":{
        "description":"Amazing Studio Packed Animation File",
        "demux":True,
        "mux":False,
    },
    "pam_pipe":{
        "description":"piped pam sequence",
        "demux":True,
        "mux":False,
    },
    "pbm_pipe":{
        "description":"piped pbm sequence",
        "demux":True,
        "mux":False,
    },
    "pcx_pipe":{
        "description":"piped pcx sequence",
        "demux":True,
        "mux":False,
    },
    "pgm_pipe":{
        "description":"piped pgm sequence",
        "demux":True,
        "mux":False,
    },
    "pgmyuv_pipe":{
        "description":"piped pgmyuv sequence",
        "demux":True,
        "mux":False,
    },
    "pgx_pipe":{
        "description":"piped pgx sequence",
        "demux":True,
        "mux":False,
    },
    "photocd_pipe":{
        "description":"piped photocd sequence",
        "demux":True,
        "mux":False,
    },
    "pictor_pipe":{
        "description":"piped pictor sequence",
        "demux":True,
        "mux":False,
    },
    "pjs":{
        "description":"PJS (Phoenix Japanimation Society) subtitles",
        "demux":True,
        "mux":False,
    },
    "pmp":{
        "description":"Playstation Portable PMP",
        "demux":True,
        "mux":False,
    },
    "png_pipe":{
        "description":"piped png sequence",
        "demux":True,
        "mux":False,
    },
    "pp_bnk":{
        "description":"Pro Pinball Series Soundbank",
        "demux":True,
        "mux":False,
    },
    "ppm_pipe":{
        "description":"piped ppm sequence",
        "demux":True,
        "mux":False,
    },
    "psd_pipe":{
        "description":"piped psd sequence",
        "demux":True,
        "mux":False,
    },
    "psp":{
        "description":"PSP MP4 (MPEG-4 Part 14)",
        "demux":False,
        "mux":True,
    },
    "psxstr":{
        "description":"Sony Playstation STR",
        "demux":True,
        "mux":False,
    },
    "pva":{
        "description":"TechnoTrend PVA",
        "demux":True,
        "mux":False,
    },
    "pvf":{
        "description":"PVF (Portable Voice Format)",
        "demux":True,
        "mux":False,
    },
    "qcp":{
        "description":"QCP",
        "demux":True,
        "mux":False,
    },
    "qdraw_pipe":{
        "description":"piped qdraw sequence",
        "demux":True,
        "mux":False,
    },
    "r3d":{
        "description":"REDCODE R3D",
        "demux":True,
        "mux":False,
    },
    "rawvideo":{
        "description":"raw video",
        "demux":True,
        "mux":True,
    },
    "realtext":{
        "description":"RealText subtitle format",
        "demux":True,
        "mux":False,
    },
    "redspark":{
        "description":"RedSpark",
        "demux":True,
        "mux":False,
    },
    "rl2":{
        "description":"RL2",
        "demux":True,
        "mux":False,
    },
    "rm":{
        "description":"RealMedia",
        "demux":True,
        "mux":True,
    },
    "roq":{
        "description":"raw id RoQ",
        "demux":True,
        "mux":True,
    },
    "rpl":{
        "description":"RPL / ARMovie",
        "demux":True,
        "mux":False,
    },
    "rsd":{
        "description":"GameCube RSD",
        "demux":True,
        "mux":False,
    },
    "rso":{
        "description":"Lego Mindstorms RSO",
        "demux":True,
        "mux":True,
    },
    "rtp":{
        "description":"RTP output",
        "demux":True,
        "mux":True,
    },
    "rtp_mpegts":{
        "description":"RTP/mpegts output format",
        "demux":False,
        "mux":True,
    },
    "rtsp":{
        "description":"RTSP output",
        "demux":True,
        "mux":True,
    },
    "s16be":{
        "description":"PCM signed 16-bit big-endian",
        "demux":True,
        "mux":True,
    },
    "s16le":{
        "description":"PCM signed 16-bit little-endian",
        "demux":True,
        "mux":True,
    },
    "s24be":{
        "description":"PCM signed 24-bit big-endian",
        "demux":True,
        "mux":True,
    },
    "s24le":{
        "description":"PCM signed 24-bit little-endian",
        "demux":True,
        "mux":True,
    },
    "s32be":{
        "description":"PCM signed 32-bit big-endian",
        "demux":True,
        "mux":True,
    },
    "s32le":{
        "description":"PCM signed 32-bit little-endian",
        "demux":True,
        "mux":True,
    },
    "s337m":{
        "description":"SMPTE 337M",
        "demux":True,
        "mux":False,
    },
    "s8":{
        "description":"PCM signed 8-bit",
        "demux":True,
        "mux":True,
    },
    "sami":{
        "description":"SAMI subtitle format",
        "demux":True,
        "mux":False,
    },
    "sap":{
        "description":"SAP output",
        "demux":True,
        "mux":True,
    },
    "sbc":{
        "description":"raw SBC",
        "demux":True,
        "mux":True,
    },
    "sbg":{
        "description":"SBaGen binaural beats script",
        "demux":True,
        "mux":False,
    },
    "scc":{
        "description":"Scenarist Closed Captions",
        "demux":True,
        "mux":True,
    },
    "scd":{
        "description":"Square Enix SCD",
        "demux":True,
        "mux":False,
    },
    "sdl,sdl2":{
        "description":"SDL2 output device",
        "demux":False,
        "mux":True,
    },
    "sdp":{
        "description":"SDP",
        "demux":True,
        "mux":False,
    },
    "sdr2":{
        "description":"SDR2",
        "demux":True,
        "mux":False,
    },
    "sds":{
        "description":"MIDI Sample Dump Standard",
        "demux":True,
        "mux":False,
    },
    "sdx":{
        "description":"Sample Dump eXchange",
        "demux":True,
        "mux":False,
    },
    "segment":{
        "description":"segment",
        "demux":False,
        "mux":True,
    },
    "ser":{
        "description":"SER (Simple uncompressed video format for astronomical capturing)",
        "demux":True,
        "mux":False,
    },
    "sga":{
        "description":"Digital Pictures SGA",
        "demux":True,
        "mux":False,
    },
    "sgi_pipe":{
        "description":"piped sgi sequence",
        "demux":True,
        "mux":False,
    },
    "shn":{
        "description":"raw Shorten",
        "demux":True,
        "mux":False,
    },
    "siff":{
        "description":"Beam Software SIFF",
        "demux":True,
        "mux":False,
    },
    "simbiosis_imx":{
        "description":"Simbiosis Interactive IMX",
        "demux":True,
        "mux":False,
    },
    "sln":{
        "description":"Asterisk raw pcm",
        "demux":True,
        "mux":False,
    },
    "smjpeg":{
        "description":"Loki SDL MJPEG",
        "demux":True,
        "mux":True,
    },
    "smk":{
        "description":"Smacker",
        "demux":True,
        "mux":False,
    },
    "smoothstreaming":{
        "description":"Smooth Streaming Muxer",
        "demux":False,
        "mux":True,
    },
    "smush":{
        "description":"LucasArts Smush",
        "demux":True,
        "mux":False,
    },
    "sol":{
        "description":"Sierra SOL",
        "demux":True,
        "mux":False,
    },
    "sox":{
        "description":"SoX native",
        "demux":True,
        "mux":True,
    },
    "spdif":{
        "description":"IEC 61937 (used on S/PDIF - IEC958)",
        "demux":True,
        "mux":True,
    },
    "spx":{
        "description":"Ogg Speex",
        "demux":False,
        "mux":True,
    },
    "srt":{
        "description":"SubRip subtitle",
        "demux":True,
        "mux":True,
    },
    "stl":{
        "description":"Spruce subtitle format",
        "demux":True,
        "mux":False,
    },
    "stream_segment,ssegment":{
        "description":"streaming segment muxer",
        "demux":False,
        "mux":True,
    },
    "streamhash":{
        "description":"Per-stream hash testing",
        "demux":False,
        "mux":True,
    },
    "subviewer":{
        "description":"SubViewer subtitle format",
        "demux":True,
        "mux":False,
    },
    "subviewer1":{
        "description":"SubViewer v1 subtitle format",
        "demux":True,
        "mux":False,
    },
    "sunrast_pipe":{
        "description":"piped sunrast sequence",
        "demux":True,
        "mux":False,
    },
    "sup":{
        "description":"raw HDMV Presentation Graphic Stream subtitles",
        "demux":True,
        "mux":True,
    },
    "svag":{
        "description":"Konami PS2 SVAG",
        "demux":True,
        "mux":False,
    },
    "svcd":{
        "description":"MPEG-2 PS (SVCD)",
        "demux":False,
        "mux":True,
    },
    "svg_pipe":{
        "description":"piped svg sequence",
        "demux":True,
        "mux":False,
    },
    "svs":{
        "description":"Square SVS",
        "demux":True,
        "mux":False,
    },
    "swf":{
        "description":"SWF (ShockWave Flash)",
        "demux":True,
        "mux":True,
    },
    "tak":{
        "description":"raw TAK",
        "demux":True,
        "mux":False,
    },
    "tedcaptions":{
        "description":"TED Talks captions",
        "demux":True,
        "mux":False,
    },
    "tee":{
        "description":"Multiple muxer tee",
        "demux":False,
        "mux":True,
    },
    "thp":{
        "description":"THP",
        "demux":True,
        "mux":False,
    },
    "tiertexseq":{
        "description":"Tiertex Limited SEQ",
        "demux":True,
        "mux":False,
    },
    "tiff_pipe":{
        "description":"piped tiff sequence",
        "demux":True,
        "mux":False,
    },
    "tmv":{
        "description":"8088flex TMV",
        "demux":True,
        "mux":False,
    },
    "truehd":{
        "description":"raw TrueHD",
        "demux":True,
        "mux":True,
    },
    "tta":{
        "description":"TTA (True Audio)",
        "demux":True,
        "mux":True,
    },
    "ttml":{
        "description":"TTML subtitle",
        "demux":False,
        "mux":True,
    },
    "tty":{
        "description":"Tele-typewriter",
        "demux":True,
        "mux":False,
    },
    "txd":{
        "description":"Renderware TeXture Dictionary",
        "demux":True,
        "mux":False,
    },
    "ty":{
        "description":"TiVo TY Stream",
        "demux":True,
        "mux":False,
    },
    "u16be":{
        "description":"PCM unsigned 16-bit big-endian",
        "demux":True,
        "mux":True,
    },
    "u16le":{
        "description":"PCM unsigned 16-bit little-endian",
        "demux":True,
        "mux":True,
    },
    "u24be":{
        "description":"PCM unsigned 24-bit big-endian",
        "demux":True,
        "mux":True,
    },
    "u24le":{
        "description":"PCM unsigned 24-bit little-endian",
        "demux":True,
        "mux":True,
    },
    "u32be":{
        "description":"PCM unsigned 32-bit big-endian",
        "demux":True,
        "mux":True,
    },
    "u32le":{
        "description":"PCM unsigned 32-bit little-endian",
        "demux":True,
        "mux":True,
    },
    "u8":{
        "description":"PCM unsigned 8-bit",
        "demux":True,
        "mux":True,
    },
    "uncodedframecrc":{
        "description":"uncoded framecrc testing",
        "demux":False,
        "mux":True,
    },
    "v210":{
        "description":"Uncompressed 4:2:2 10-bit",
        "demux":True,
        "mux":False,
    },
    "v210x":{
        "description":"Uncompressed 4:2:2 10-bit",
        "demux":True,
        "mux":False,
    },
    "vag":{
        "description":"Sony PS2 VAG",
        "demux":True,
        "mux":False,
    },
    "vc1":{
        "description":"raw VC-1 video",
        "demux":True,
        "mux":True,
    },
    "vc1test":{
        "description":"VC-1 test bitstream",
        "demux":True,
        "mux":True,
    },
    "vcd":{
        "description":"MPEG-1 Systems / MPEG program stream (VCD)",
        "demux":False,
        "mux":True,
    },
    "vidc":{
        "description":"PCM Archimedes VIDC",
        "demux":True,
        "mux":True,
    },
    "vividas":{
        "description":"Vividas VIV",
        "demux":True,
        "mux":False,
    },
    "vivo":{
        "description":"Vivo",
        "demux":True,
        "mux":False,
    },
    "vmd":{
        "description":"Sierra VMD",
        "demux":True,
        "mux":False,
    },
    "vob":{
        "description":"MPEG-2 PS (VOB)",
        "demux":False,
        "mux":True,
    },
    "vobsub":{
        "description":"VobSub subtitle format",
        "demux":True,
        "mux":False,
    },
    "voc":{
        "description":"Creative Voice",
        "demux":True,
        "mux":True,
    },
    "vpk":{
        "description":"Sony PS2 VPK",
        "demux":True,
        "mux":False,
    },
    "vplayer":{
        "description":"VPlayer subtitles",
        "demux":True,
        "mux":False,
    },
    "vqf":{
        "description":"Nippon Telegraph and Telephone Corporation (NTT) TwinVQ",
        "demux":True,
        "mux":False,
    },
    "w64":{
        "description":"Sony Wave64",
        "demux":True,
        "mux":True,
    },
    "wav":{
        "description":"WAV / WAVE (Waveform Audio)",
        "demux":True,
        "mux":True,
    },
    "wc3movie":{
        "description":"Wing Commander III movie",
        "demux":True,
        "mux":False,
    },
    "webm":{
        "description":"WebM",
        "demux":False,
        "mux":True,
    },
    "webm_chunk":{
        "description":"WebM Chunk Muxer",
        "demux":False,
        "mux":True,
    },
    "webm_dash_manifest":{
        "description":"WebM DASH Manifest",
        "demux":True,
        "mux":True,
    },
    "webp":{
        "description":"WebP",
        "demux":False,
        "mux":True,
    },
    "webp_pipe":{
        "description":"piped webp sequence",
        "demux":True,
        "mux":False,
    },
    "webvtt":{
        "description":"WebVTT subtitle",
        "demux":True,
        "mux":True,
    },
    "wsaud":{
        "description":"Westwood Studios audio",
        "demux":True,
        "mux":True,
    },
    "wsd":{
        "description":"Wideband Single-bit Data (WSD)",
        "demux":True,
        "mux":False,
    },
    "wsvqa":{
        "description":"Westwood Studios VQA",
        "demux":True,
        "mux":False,
    },
    "wtv":{
        "description":"Windows Television (WTV)",
        "demux":True,
        "mux":True,
    },
    "wv":{
        "description":"raw WavPack",
        "demux":True,
        "mux":True,
    },
    "wve":{
        "description":"Psion 3 audio",
        "demux":True,
        "mux":False,
    },
    "x11grab":{
        "description":"X11 screen capture, using XCB",
        "demux":True,
        "mux":False,
    },
    "xa":{
        "description":"Maxis XA",
        "demux":True,
        "mux":False,
    },
    "xbin":{
        "description":"eXtended BINary text (XBIN)",
        "demux":True,
        "mux":False,
    },
    "xbm_pipe":{
        "description":"piped xbm sequence",
        "demux":True,
        "mux":False,
    },
    "xmv":{
        "description":"Microsoft XMV",
        "demux":True,
        "mux":False,
    },
    "xpm_pipe":{
        "description":"piped xpm sequence",
        "demux":True,
        "mux":False,
    },
    "xvag":{
        "description":"Sony PS3 XVAG",
        "demux":True,
        "mux":False,
    },
    "xwd_pipe":{
        "description":"piped xwd sequence",
        "demux":True,
        "mux":False,
    },
    "xwma":{
        "description":"Microsoft xWMA",
        "demux":True,
        "mux":False,
    },
    "yop":{
        "description":"Psygnosis YOP",
        "demux":True,
        "mux":False,
    },
    "yuv4mpegpipe":{
        "description":"YUV4MPEG pipe",
        "demux":True,
        "mux":True,
    },
}