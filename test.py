from pybdinfo import BDInfo, Report
from tqdm import tqdm
import os, platform, sys, progressbar

pbar = None
data_dir = None
if platform.system() == 'Windows':
    data_dir = 'D:\\'
elif platform.system() == 'Linux':
    data_dir = '/media/ferb/Data/'
if not data_dir:
    sys.exit()

iso_file = os.path.join(data_dir, 'Ip.Man.Kung.Fu.Master.2019.BluRay.1080p.AVC.DTS-HD.MA5.1-CHDBits.iso')
report_path = r'C:\Users\Ferb\Desktop\report.txt'

def progress_callback(percent, elapsed, remaining):
    global pbar
    if pbar is None:
        pbar = progressbar.ProgressBar(max_value=100)
    pbar.update(percent)

# START HERE

if not os.path.exists(report_path) or not os.path.isfile(report_path):
    
    # List playlists
    print('Listing playlists...')
    bdinfo = BDInfo(os.path.join(data_dir, 'tmp'))
    bdinfo.open(iso_file)
    print('  Done!')

    # Show playlists available
    print('\nPlaylists available:')
    for playlist in bdinfo.get_playlists():
        print('  {}'.format(str(playlist)))

    # Scan specific playlist
    playlist_to_scan = bdinfo.get_playlists()[0]
    print('\nScanning playlist "{}"...'.format(playlist_to_scan.file))
    report = bdinfo.scan_playlist(playlist_to_scan.file, progress_callback)
    progressbar.streams.flush()
    pbar = None
    print('  Done!')

    # Export report
    export_path = r'C:\Users\Ferb\Desktop\bdinfo.txt'
    print('\nExporting report to "{}"...'.format(export_path))
    report.export(export_path)
    print('  Done!')

    # Save report ()
    print('\nSaving report to "{}"...'.format(report_path))
    report.save(report_path)
    print('  Done!')


else:
    report = Report.open(report_path)


# Show overview
print('\nPlaylist summary:'.format(report_path))
for line in str(report).split('\n'):
    print('  {}'.format(line))

# Show some infos
print('\nNumber of streams: {}'.format(str(len(report.streams()))))
print('->Video streams...: {}'.format(str(len(report.video_streams()))))
print('->Audio streams...: {}'.format(str(len(report.audio_streams()))))
print('->Text streams....: {}'.format(str(len(report.text_streams()))))
print('->Graphics streams: {}'.format(str(len(report.graphics_streams()))))

print('\nChapters:')
count = 0
for chapter in report.chapters():
    print('Chapter {}: {}'.format(str(count), str(chapter)))
    count += 1