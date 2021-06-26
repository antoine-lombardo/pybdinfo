from pybdinfo import BDInfo, PlaylistDetails
import os

def progress_callback(percent, elapsed, remaining):
    print('{}%, {} / {}'.format(str(percent), elapsed.strftime("%H:%M:%S"), remaining.strftime("%H:%M:%S")))

bdinfo = BDInfo()
bdinfo.open(r'D:\Ip.Man.Kung.Fu.Master.2019.BluRay.1080p.AVC.DTS-HD.MA5.1-CHDBits.iso')

bdinfo.scan_playlist('00000.mpls', progress_callback)



report = None
with open(r'D:\BDINFO.Ip.Man.Kung.Fu.Master.2019.BluRay.1080p.AVC.DTS-HD.MA5.1-CHDBits.txt', encoding='utf-8') as file:
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
