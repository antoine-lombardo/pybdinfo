import os, datetime, platform, json
from pybdinfo.utils import run_exe
from pybdinfo.languages import lang_to_code, code_to_lang
from pybdinfo.codecs import name_to_codec
from pybdinfo.video_description import extract_videoformat, extract_framerate, extract_aspectratio, extract_profile, extract_level

class BDInfo():
    def __init__(self, tmp_dir):
        self.tmp_dir = tmp_dir
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
        for element in os.listdir(self.tmp_dir):
            if os.path.isfile(os.path.join(self.tmp_dir, element)):
                if element.startswith('BDINFO.') and element.endswith('.txt'):
                    os.remove(os.path.join(self.tmp_dir, element))
        args = [self.exec, '--mplsjson', playlist, self.path, self.tmp_dir]
        process = run_exe(args)
        json_str = None
        while True:
            line = process.stdout.readline()
            if line == '':
                break
            if line.startswith('JSON:'):
                json_str = line
            if callback is not None:
                try:
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
                except: 
                    continue
        process.wait()
        # Report
        report = []
        for element in os.listdir(self.tmp_dir):
            if os.path.isfile(os.path.join(self.tmp_dir, element)):
                if element.startswith('BDINFO.') and element.endswith('.txt'):
                    with open(os.path.join(self.tmp_dir, element), encoding='utf-8') as file:
                        report = file.read().splitlines()
                    os.remove(os.path.join(self.tmp_dir, element))

        # Object
        if json_str == None:
            bdrom = None
        else:
            bdrom = json.loads(json_str[5:])
        return Report(report, bdrom, playlist)
        

class PlaylistOverview():
    def __init__(self, infos):
        self.index = int(infos[0])
        self.group = int(infos[1])
        self.file = infos[2].lower()
        self.duration = datetime.datetime.strptime(infos[3],"%H:%M:%S")
        self.size = int(infos[4].replace(',',''))
   
    def __str__(self):
        return 'ID: {} / GROUP: {} / FILE: {} / DURATION: {} / SIZE: {} Bytes'.format(
            str(self.index), str(self.group), self.file, self.duration.strftime("%H:%M:%S"), str(self.size)
        )

class Report():
    def __init__(self, lines, object, playlist):
        self.lines = lines
        self.object = object
        self.playlist = playlist
        self.playlist_object = self.object['PlaylistFiles'][playlist.upper()]

    @classmethod
    def open(cls, path):
        if not os.path.exists(path) or not os.path.isfile(path):
            raise
        with open(path, 'r', encoding='utf-8') as file:
            obj = json.load(file)
        return cls(obj['lines'], obj['object'], obj['playlist'])

    def __str__(self):
        return self.summary()

    def full(self):
        return '\n'.join(self.lines)

    def export(self, path):
        if os.path.exists(path) and os.path.isfile(path):
            os.remove(path)
        with open(path, 'w', encoding='utf-8') as file:
            for line in self.lines:
                file.write(line + '\n')

    def save(self, path):
        obj = {
            'lines': self.lines,
            'object': self.object,
            'playlist': self.playlist
        }
        if os.path.exists(path) and os.path.isfile(path):
            os.remove(path)
        with open(path, 'w', encoding='utf-8') as file:
            json.dump(obj, file)

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

    def chapters(self):
        chapters = []
        for seconds in self.playlist_object['Chapters']:
            chapters.append(datetime.timedelta(seconds=seconds))
        return chapters

    def streams(self):
        return self.playlist_object['Streams']

    def video_streams(self):
        return self.playlist_object['VideoStreams']

    def audio_streams(self):
        return self.playlist_object['AudioStreams']

    def text_streams(self):
        return self.playlist_object['TextStreams']

    def graphics_streams(self):
        return self.playlist_object['GraphicsStreams']