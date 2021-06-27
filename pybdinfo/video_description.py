from enum import Enum

class VideoFormat(Enum):
    Unknown = 0
    VIDEOFORMAT_480i = 1
    VIDEOFORMAT_576i = 2
    VIDEOFORMAT_480p = 3
    VIDEOFORMAT_1080i = 4
    VIDEOFORMAT_720p = 5
    VIDEOFORMAT_1080p = 6
    VIDEOFORMAT_576p = 7
    VIDEOFORMAT_2160p = 8

videoformats = {
    VideoFormat.VIDEOFORMAT_480i: {'name': '480i', 'interlaced': True},
    VideoFormat.VIDEOFORMAT_576i: {'name': '576i', 'interlaced': True},
    VideoFormat.VIDEOFORMAT_480p: {'name': '480p', 'interlaced': False},
    VideoFormat.VIDEOFORMAT_1080i: {'name': '1080i', 'interlaced': True},
    VideoFormat.VIDEOFORMAT_720p: {'name': '720p', 'interlaced': False},
    VideoFormat.VIDEOFORMAT_1080p: {'name': '1080p', 'interlaced': False},
    VideoFormat.VIDEOFORMAT_576p: {'name': '576p', 'interlaced': False},
    VideoFormat.VIDEOFORMAT_2160p: {'name': '2160p', 'interlaced': False},
}

def extract_videoformat(desc: str):
    for videoformat, infos in videoformats.items():
        if infos['name'] in desc:
            return videoformat
    return VideoFormat.Unknown


class FrameRate(Enum):
    Unknown = 0
    FRAMERATE_23_976 = 1
    FRAMERATE_24 = 2
    FRAMERATE_25 = 3
    FRAMERATE_29_97 = 4
    FRAMERATE_50 = 6
    FRAMERATE_59_94 = 7

framerates = {
    FrameRate.FRAMERATE_23_976: {'name': '23.976 fps', 'enum': 24000, 'denom': 1001},
    FrameRate.FRAMERATE_24: {'name': '24 fps', 'enum': 24000, 'denom': 1000},
    FrameRate.FRAMERATE_25: {'name': '25 fps', 'enum': 25000, 'denom': 1000},
    FrameRate.FRAMERATE_29_97: {'name': '29.970 fps', 'enum': 30000, 'denom': 1001},
    FrameRate.FRAMERATE_50: {'name': '50 fps', 'enum': 50000, 'denom': 1000},
    FrameRate.FRAMERATE_59_94: {'name': '59.940 fps', 'enum': 60000, 'denom': 1001},
}

def extract_framerate(desc: str):
    for framerate, infos in framerates.items():
        if infos['name'] in desc:
            return framerate
    return FrameRate.Unknown


class AspectRatios(Enum):
    Unknown = 0
    ASPECT_4_3 = 2
    ASPECT_16_9 = 3
    ASPECT_2_21 = 4

aspectratios = {
    AspectRatios.ASPECT_4_3: {'name': '4:3'},
    AspectRatios.ASPECT_16_9: {'name': '16:9'},
    AspectRatios.ASPECT_2_21: {'name': '2.21:1'},
}

def extract_aspectratio(desc: str):
    for aspectratio, infos in aspectratios.items():
        if infos['name'] in desc:
            return aspectratio
    return AspectRatios.Unknown


class Profiles(Enum):
    Unknown = 0
    BASELINE = 1
    MAIN = 2
    EXTENDED = 3
    HIGH = 4
    HIGH_10 = 5
    HIGH_4_2_2 = 6
    HIGH_4_4_4 = 7

profiles = {
    Profiles.BASELINE: {'name': 'Baseline Profile'},
    Profiles.MAIN: {'name': 'Main Profile'},
    Profiles.EXTENDED: {'name': 'Extended Profile'},
    Profiles.HIGH: {'name': 'High Profile'},
    Profiles.HIGH_10: {'name': 'High 10 Profile'},
    Profiles.HIGH_4_2_2: {'name': 'High 4:2:2 Profile'},
    Profiles.HIGH_4_4_4: {'name': 'High 4:4:4 Profile'},
    Profiles.Unknown: {'name': 'Unknown Profile'},
}

def extract_profile(desc: str):
    for profile, infos in profiles.items():
        if infos['name'] in desc:
            return profile
    return Profiles.Unknown

def extract_level(desc: str):
    profile = extract_profile(desc)
    if profile == Profiles.Unknown:
        return ''
    try:
        index = desc.index(profiles[profile]['name']) + len(profiles[profile]['name'])
        new_desc = desc[index:].strip()
        if '/' in new_desc:
            new_desc = new_desc[:new_desc.index('/')].strip()
        return new_desc
    except:
        return ''
