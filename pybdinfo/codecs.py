from enum import Enum

class Codecs(Enum):
    MPEG1_VIDEO = 0
    MPEG2_VIDEO = 1
    AVC_VIDEO = 2
    MVC_VIDEO = 3
    HEVC_VIDEO = 4
    VC1_VIDEO = 5
    MPEG1_AUDIO = 6
    MPEG2_AUDIO = 7
    LPCM_AUDIO = 8
    AC3_AUDIO = 9
    AC3_EX_AUDIO = 10
    AC3_PLUS_AUDIO = 11
    AC3_PLUS_ATMOS_AUDIO = 12
    AC3_TRUE_HD_AUDIO = 13
    AC3_TRUE_HD_ATMOS_AUDIO = 14
    DTS_AUDIO = 15
    DTS_ES_AUDIO = 16
    DTS_HD_AUDIO = 17
    DTS_HD_SECONDARY_AUDIO = 18
    DTS_HD_MASTER_AUDIO = 19
    DTS_X_AUDIO = 20
    PRESENTATION_GRAPHICS = 21
    INTERACTIVE_GRAPHICS = 22
    SUBTITLE = 23
    UNKNOWN = 99

codecs = {
    Codecs.MPEG1_VIDEO: {'name': 'MPEG-1 Video', 'alt_name': 'MPEG-1', 'short_name': 'MPEG-1'},
    Codecs.MPEG2_VIDEO: {'name': 'MPEG-2 Video', 'alt_name': 'MPEG-2', 'short_name': 'MPEG-2'},
    Codecs.AVC_VIDEO: {'name': 'MPEG-4 AVC Video', 'alt_name': 'AVC', 'short_name': 'AVC'},
    Codecs.MVC_VIDEO: {'name': 'MPEG-4 MVC Video', 'alt_name': 'MVC', 'short_name': 'MVC'},
    Codecs.HEVC_VIDEO: {'name': 'HEVC Video', 'alt_name': 'HEVC', 'short_name': 'HEVC'},
    Codecs.VC1_VIDEO: {'name': 'VC-1 Video', 'alt_name': 'VC-1', 'short_name': 'VC-1'},
    Codecs.MPEG1_AUDIO: {'name': 'MP1 Audio', 'alt_name': 'MP1', 'short_name': 'MP1'},
    Codecs.MPEG2_AUDIO: {'name': 'MP2 Audio', 'alt_name': 'MP2', 'short_name': 'MP2'},
    Codecs.LPCM_AUDIO: {'name': 'LPCM Audio', 'alt_name': 'LPCM', 'short_name': 'LPCM'},
    Codecs.AC3_AUDIO: {'name': 'Dolby Digital Audio', 'alt_name': 'DD AC3', 'short_name': 'AC3'},
    Codecs.AC3_EX_AUDIO: {'name': 'Dolby Digital EX Audio', 'alt_name': 'DD AC3', 'short_name': 'AC3-EX'},
    Codecs.AC3_PLUS_AUDIO: {'name': 'Dolby Digital Plus Audio', 'alt_name': 'DD AC3+', 'short_name': 'AC3+'},
    Codecs.AC3_PLUS_ATMOS_AUDIO: {'name': 'Dolby Digital Plus/Atmos Audio', 'alt_name': 'DD AC3+', 'short_name': 'AC3+'},
    Codecs.AC3_TRUE_HD_AUDIO: {'name': 'Dolby TrueHD Audio', 'alt_name': 'Dolby TrueHD', 'short_name': 'TrueHD'},
    Codecs.AC3_TRUE_HD_ATMOS_AUDIO: {'name': 'Dolby TrueHD/Atmos Audio', 'alt_name': 'Dolby TrueHD', 'short_name': 'TrueHD'},
    Codecs.DTS_AUDIO: {'name': 'DTS Audio', 'alt_name': 'DTS', 'short_name': 'DTS'},
    Codecs.DTS_ES_AUDIO: {'name': 'DTS-ES Audio', 'alt_name': 'DTS', 'short_name': 'DTS-ES'},
    Codecs.DTS_HD_AUDIO: {'name': 'DTS-HD High-Res Audio', 'alt_name': 'DTS-HD Hi-Res', 'short_name': 'DTS-HD HR'},
    Codecs.DTS_HD_SECONDARY_AUDIO: {'name': 'DTS Express', 'alt_name': 'DTS Express', 'short_name': 'DTS Express'},
    Codecs.DTS_HD_MASTER_AUDIO: {'name': 'DTS-HD Master Audio', 'alt_name': 'DTS-HD Master', 'short_name': 'DTS-HD MA'},
    Codecs.DTS_X_AUDIO: {'name': 'DTS:X', 'alt_name': 'DTS-HD Master', 'short_name': 'DTS-HD MA'},
    Codecs.PRESENTATION_GRAPHICS: {'name': 'Presentation Graphics', 'alt_name': 'PGS', 'short_name': 'PGS'},
    Codecs.INTERACTIVE_GRAPHICS: {'name': 'Interactive Graphics', 'alt_name': 'IGS', 'short_name': 'IGS'},
    Codecs.SUBTITLE: {'name': 'Subtitle', 'alt_name': 'SUB', 'short_name': 'SUB'},
    Codecs.UNKNOWN: {'name': 'UNKNOWN', 'alt_name': 'UNKNOWN', 'short_name': 'UNKNOWN'},
}

def name_to_codec(name):
    for codec, infos in codecs.items():
        if name == infos['name']:
            return codec
    for codec, infos in codecs.items():
        if name == infos['short_name']:
            return codec
    for codec, infos in codecs.items():
        if name == infos['alt_name']:
            return codec
    return Codecs.UNKNOWN