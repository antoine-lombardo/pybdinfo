import os, datetime, platform
from pybdinfo.utils import run_exe

TMP = None
if platform.system() == 'Windows':
    TMP = r'D:\tmp'
elif platform.system() == 'Linux':
    TMP = '/media/ferb/Data/tmp'
if not TMP:
    sys.exit()

class BDInfo():
    def __init__(self):
        self.exec = os.path.normpath(os.path.join(os.path.dirname(__file__), 'binaries/BDInfoCLI-ng_v0.7.5.5/BDInfo.exe'))
        self.path = None
        self.is_iso = False

    def open(self, path):
        if not os.path.exists(path):
            return False
        if os.path.isfile(path) and os.path.splitext(path)[1].lower() != '.iso':
            return False
        if os.path.isfile(path) and os.path.splitext(path)[1].lower() == '.iso':
            self.is_iso = True
        if os.path.isdir(path):
            self.is_iso = False
        self.path = os.path.normpath(path)
        return True

    def get_playlists(self):
        if self.path is None:
            return None
        args = [self.exec, '--list', self.path]
        if self.is_iso:
            args.append(os.path.dirname(self.path))
        process = run_exe(args)
        process.wait()
        started = False
        playlists = []
        while True:
            line = process.stdout.readline()
            if not line:
                break
            elif '#' in line and \
                'Group' in line and \
                'Playlist' in line and \
                'File' in line and \
                'Length' in line and \
                'Estimated Bytes' in line and \
                'Measured Bytes' in line:
                started = True
                continue
            elif started:
                playlist_raw = line.split()
                if len(playlist_raw) == 6:
                    playlists.append(PlaylistOverview(line.split()))
                continue
        return playlists
    
    def scan_playlist(self, playlist, callback = None):
        for element in os.listdir(TMP):
            if os.path.isfile(os.path.join(TMP, element)):
                if element.startswith('BDINFO.') and element.endswith('.txt'):
                    os.remove(os.path.join(TMP, element))
        args = [self.exec, '--mpls', playlist, self.path, TMP]
        process = run_exe(args)
        while process.poll() is None:
            if callback is not None:
                try:
                    line = process.stdout.readline()
                    index_scanning = line.index('Scanning')
                    index_percent = line.index('%')
                    percent = int(line[index_scanning + 8:index_percent].strip())
                    index_m2ts = line.lower().index('m2ts')
                    index_sep = line.rindex('|')
                    elapsed_str = line[index_m2ts + 4:index_sep].strip()
                    remaining_str = line[index_sep + 1:].strip()
                    elapsed = datetime.datetime.strptime(elapsed_str,"%H:%M:%S")
                    remaining = datetime.datetime.strptime(remaining_str,"%H:%M:%S")
                    callback(percent, elapsed, remaining)
                except: continue
        report = []
        for element in os.listdir(TMP):
            if os.path.isfile(os.path.join(TMP, element)):
                if element.startswith('BDINFO.') and element.endswith('.txt'):
                    with open(os.path.join(TMP, element), encoding='utf-8') as file:
                        report = file.read().splitlines()
                    os.remove(os.path.join(TMP, element))
        return PlaylistDetails(report)
        

class PlaylistOverview():
    def __init__(self, infos):
        self.index = int(infos[0])
        self.group = int(infos[1])
        self.file = infos[2].lower()
        self.duration = datetime.datetime.strptime(infos[3],"%H:%M:%S")
        self.size = int(infos[4].replace(',',''))
   
    def to_string(self):
        return 'ID: {} / GROUP: {} / FILE: {} / DURATION: {} / SIZE: {} Bytes'.format(
            str(self.index), str(self.group), self.file, self.duration.strftime("%H:%M:%S"), str(self.size)
        )

class PlaylistDetails():
    def __init__(self, lines):
        self.lines = lines

    def summary(self):
        started = False
        lines = []
        for line in self.lines:
            if line.strip() == 'QUICK SUMMARY:':
                started = True
                continue
            if started and line.strip() != '':
                lines.append(line)
        return '\n'.join(lines)

    def detailed(self):
        started = False
        lines = []
        for line in self.lines:
            if line.strip() == 'DISC INFO:':
                started = True
            if started and line.strip() == '[/code]':
                if lines[-1].strip() == '':
                    return '\n'.join(lines)[:-1]
                else:
                    return '\n'.join(lines)
            elif started:
                lines.append(line)

    def get_infos(self):
        details = self._extract_details_infos()
        title = None
        label = None
        size = None
        protection = None
        version = None
        for line in details:
            if line.startswith('Disc Title:'):
                title = line.replace('Disc Title:', '').strip()
            elif line.startswith('Disc Label:'):
                label = line.replace('Disc Label:', '').strip()
            elif line.startswith('Disc Size:'):
                size = int(line.replace('Disc Size:', '').replace('bytes', '').replace(',', '').strip())
            elif line.startswith('Protection:'):
                protection = line.replace('Protection:', '').strip()
            elif line.startswith('BDInfo:'):
                version = line.replace('BDInfo:', '').strip()
        return Infos(title, label, size, protection, version)

    def get_report(self):
        details = self._extract_details_report()
        name = None
        length = None
        size = None
        bitrate = None
        for line in details:
            if line.startswith('Name:'):
                name = line.replace('Name:', '').strip()
            elif line.startswith('Length:'):
                length = line.replace('Length:', '')
                if '(' in length:
                    length = length[:length.index('(')]
                length = length.strip()
            elif line.startswith('Size:'):
                size = int(line.replace('Size:', '').replace('bytes', '').replace(',', '').strip())
            elif line.startswith('Total Bitrate:'):
                bitrate = float(line.replace('Total Bitrate:', '').replace('Mbps', '').replace(',', '').strip())
        return Report(name, length, size, bitrate)
    

    def get_video_streams(self):
        details = self._extract_details_video()
        headers_line = details[0]
        index_codec = headers_line.index('Codec')
        index_bitrate = headers_line.index('Bitrate')
        index_description = headers_line.index('Description')
        video_tracks = []
        for line in details[2:]:
            codec = line[index_codec:index_bitrate].strip()
            bitrate = float(line[index_bitrate:index_description].replace('kbps', '').strip())
            description = line[index_description:].strip()
            video_tracks.append(VideoTrack(codec, bitrate, description))
        return video_tracks

    def get_audio_streams(self):
        details = self._extract_details_audio()
        headers_line = details[0]
        index_codec = headers_line.index('Codec')
        index_language = headers_line.index('Language')
        index_bitrate = headers_line.index('Bitrate')
        index_description = headers_line.index('Description')
        audio_tracks = []
        for line in details[2:]:
            codec = line[index_codec:index_language].strip()
            language = line[index_language:index_bitrate].strip()
            bitrate = float(line[index_bitrate:index_description].replace('kbps', '').strip())
            description = line[index_description:].strip()
            audio_tracks.append(AudioTrack(codec, language, bitrate, description))
        return audio_tracks

    def get_subtitles_streams(self):
        details = self._extract_details_subtitles()
        headers_line = details[0]
        index_codec = headers_line.index('Codec')
        index_language = headers_line.index('Language')
        index_bitrate = headers_line.index('Bitrate')
        index_description = headers_line.index('Description')
        subtitles_tracks = []
        for line in details[2:]:
            codec = line[index_codec:index_language].strip()
            language = line[index_language:index_bitrate].strip()
            bitrate = float(line[index_bitrate:index_description].replace('kbps', '').strip())
            description = line[index_description:].strip()
            subtitles_tracks.append(SubtitlesTrack(codec, language, bitrate, description))
        return subtitles_tracks

    def get_files(self):
        details = self._extract_details_files()
        headers_line = details[0]
        index_name = headers_line.index('Name')
        index_time_in = headers_line.index('Time In')
        index_length = headers_line.index('Length')
        index_size = headers_line.index('Size')
        index_bitrate = headers_line.index('Total Bitrate')
        files = []
        for line in details[2:]:
            name = line[index_name:index_time_in].strip()
            time_in = line[index_time_in:index_length].strip()
            length = line[index_length:index_size].strip()
            size = int(line[index_size:index_bitrate].replace(',', '').strip())
            bitrate = float(line[index_bitrate:].replace(',', '').strip())
            files.append(File(name, time_in, length, size, bitrate))
        return files

    def get_chapters(self):
        details = self._extract_details_chapters()
        headers_line = details[0]
        index_number = headers_line.index('Number')
        index_time_in = headers_line.index('Time In')
        index_length = headers_line.index('Length')
        index_avg_video_rate = headers_line.index('Avg Video Rate')
        chapters = []
        for line in details[2:]:
            number = int(line[index_number:index_time_in].strip())
            time_in = line[index_time_in:index_length].strip()
            length = line[index_length:index_avg_video_rate].strip()
            chapters.append(Chapter(number, time_in, length))
        return chapters

    def _extract_details(self, line1, line2 = '[/code]'):
        started = False
        lines = []
        for line in self.lines:
            if line.strip() == line1:
                started = True
            elif started and line2 is not None and line.strip() == line2:
                return lines
            elif started and line.strip() != '':
                lines.append(line)
        return lines

    def _extract_details_infos(self):
        return self._extract_details('DISC INFO:', 'PLAYLIST REPORT:')

    def _extract_details_report(self):
        return self._extract_details('PLAYLIST REPORT:', 'VIDEO:')

    def _extract_details_video(self):
        return self._extract_details('VIDEO:', 'AUDIO:')

    def _extract_details_audio(self):
        return self._extract_details('AUDIO:', 'SUBTITLES:')

    def _extract_details_subtitles(self):
        return self._extract_details('SUBTITLES:', 'FILES:')

    def _extract_details_files(self):
        return self._extract_details('FILES:', 'CHAPTERS:')

    def _extract_details_chapters(self):
        return self._extract_details('CHAPTERS:', 'STREAM DIAGNOSTICS:')

    def _extract_details_diagnostic(self):
        return self._extract_details('STREAM DIAGNOSTICS:')

class Infos():
    def __init__(self, title, label, size, protection, version):
        self.title = title
        self.label = label
        self.size = size
        self.protection = protection
        self.version = version

    def to_string(self):
        return 'Disc Title: {}\nDisc Label: {}\nDisc Size: {} bytes\nProtection: {}\nBDInfo: {}' \
            .format(self.title, self.label, str(self.size), self.protection, self.version)

class Report():
    def __init__(self, name, length, size, bitrate):
        self.name = name
        self.length = datetime.datetime.strptime(length,"%H:%M:%S.%f")
        self.size = size
        self.bitrate = bitrate

    def to_string(self):
        return 'Name: {}\nLength: {}\nSize: {} bytes\nTotal Bitrate: {} Mbps' \
            .format(self.name, self.length.strftime("%H:%M:%S.%f"), str(self.size), self.bitrate)

class VideoTrack():
    def __init__(self, codec, bitrate, description):
        self.codec = codec
        self.bitrate = bitrate
        self.description = description

    def to_string(self):
        return '{} / {} kbps / {}'.format(self.codec, str(self.bitrate), self.description)

class AudioTrack():
    def __init__(self, codec, language, bitrate, description):
        self.codec = codec
        self.language = language
        self.bitrate = bitrate
        self.description = description

    def to_string(self):
        return '{} / {} / {} kbps / {}'.format(self.codec, self.language, str(self.bitrate), self.description)

class SubtitlesTrack():
    def __init__(self, codec, language, bitrate, description):
        self.codec = codec
        self.language = language
        self.bitrate = bitrate
        self.description = description

    def to_string(self):
        return '{} / {} / {} kbps / {}'.format(self.codec, self.language, str(self.bitrate), self.description)

class File():
    def __init__(self, name, time_in, length, size, bitrate):
        self.name = name
        self.time_in = datetime.datetime.strptime(time_in,"%H:%M:%S.%f")
        self.length = datetime.datetime.strptime(length,"%H:%M:%S.%f")
        self.size = size
        self.bitrate = bitrate

    def to_string(self):
        return '{} / {} / {} / {} bytes / {} Kbps'.format(self.name, self.time_in.strftime("%H:%M:%S.%f"), self.length.strftime("%H:%M:%S.%f"), str(self.size), str(self.bitrate))

class Chapter():
    def __init__(self, number, time_in, length):
        self.number = number
        self.time_in = datetime.datetime.strptime(time_in,"%H:%M:%S.%f")
        self.length = datetime.datetime.strptime(length,"%H:%M:%S.%f")
    def to_string(self):
        return 'Chapter {} / {} / {}'.format(str(self.number), self.time_in.strftime("%H:%M:%S.%f"), self.length.strftime("%H:%M:%S.%f"))


