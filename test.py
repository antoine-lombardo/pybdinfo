from pybdinfo import BDInfo, PlaylistDetails
import os, platform, sys

data_dir = None
if platform.system() == 'Windows':
    data_dir = 'D:\\'
elif platform.system() == 'Linux':
    data_dir = '/media/ferb/Data/'
if not data_dir:
    sys.exit()

iso_file = os.path.join(data_dir + 'Ip.Man.Kung.Fu.Master.2019.BluRay.1080p.AVC.DTS-HD.MA5.1-CHDBits.iso')
report_file = os.path.join(data_dir + 'BDINFO.Ip.Man.Kung.Fu.Master.2019.BluRay.1080p.AVC.DTS-HD.MA5.1-CHDBits.txt')


def progress_callback(percent, elapsed, remaining):
    print('{}%, {} / {}'.format(str(percent), elapsed.strftime("%H:%M:%S"), remaining.strftime("%H:%M:%S")))

bdinfo = BDInfo()
bdinfo.open(iso_file)

for playlist in bdinfo.get_playlists():
    print(playlist.to_string())


bdinfo.scan_playlist(bdinfo.get_playlists()[0].file, progress_callback)



report = None
with open(report_file, encoding='utf-8') as file:
    report = PlaylistDetails(file.read().splitlines())

for video_track in report.get_video_streams():
    print(video_track.to_string())

for audio_track in report.get_audio_streams():
    print(audio_track.to_string())

for subtitles_track in report.get_subtitles_streams():
    print(subtitles_track.to_string())

for file in report.get_files():
    print(file.to_string())

for chapter in report.get_chapters():
    print(chapter.to_string())

print(report.get_infos().to_string())

print(report.get_report().to_string())
