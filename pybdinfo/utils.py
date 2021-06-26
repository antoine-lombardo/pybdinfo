import platform, subprocess

def run_exe(args):
    if platform.system() == 'Linux':
        args.insert(0, 'mono')
    return subprocess.Popen(args=args, stdout=subprocess.PIPE, universal_newlines=True)