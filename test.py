from pybdinfo import BDInfo, Report

bdinfo = BDInfo()
bdinfo.open(r'D:\demo-bluray.iso')

playlists = bdinfo.get_playlists()
for playlist in playlists:
    print(playlist.to_string())

report = bdinfo.scan_playlists(['00000.mpls'])
print(report.summary())
print(report.detailed())
