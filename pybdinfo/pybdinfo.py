import os, subprocess, datetime

TMP = r'D:\tmp'

class BDInfo():
    def __init__(self):
        self.exec = os.path.normpath(os.path.join(os.path.dirname(__file__), 'binaries/BDInfoCLI-ng_v0.7.5.5/BDInfo.exe'))
        self.path = None
        self.is_iso = False

    def test(self):
        process = subprocess.Popen(self.exec, shell=True, stdout=subprocess.PIPE)
        process.wait()
        print(process.returncode)

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
        process = subprocess.Popen(args=args, shell=True, stdout=subprocess.PIPE)
        process.wait()
        started = False
        playlists = []
        while True:
            line = process.stdout.readline()
            if not line:
                break
            elif '#' in line.decode() and \
                'Group' in line.decode() and \
                'Playlist' in line.decode() and \
                'File' in line.decode() and \
                'Length' in line.decode() and \
                'Estimated Bytes' in line.decode() and \
                'Measured Bytes' in line.decode():
                started = True
                continue
            elif started:
                playlist_raw = line.decode().split()
                if len(playlist_raw) == 6:
                    playlists.append(PlaylistOverview(line.decode().split()))
                continue
        return playlists
    
    def scan_playlists(self, playlists):
        for element in os.listdir(TMP):
            if os.path.isfile(os.path.join(TMP, element)):
                if element.startswith('BDINFO.') and element.endswith('.txt'):
                    os.remove(os.path.join(TMP, element))
        args = [self.exec, '--mpls', ','.join(playlists), self.path, TMP]
        process = subprocess.Popen(args=args, shell=True, stdout=subprocess.PIPE)
        process.wait()
        report = []
        for element in os.listdir(TMP):
            if os.path.isfile(os.path.join(TMP, element)):
                if element.startswith('BDINFO.') and element.endswith('.txt'):
                    with open(os.path.join(TMP, element), encoding='utf-8') as file:
                        report = file.read().splitlines()
                    os.remove(os.path.join(TMP, element))
        return Report(report)
        

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

class Report():
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