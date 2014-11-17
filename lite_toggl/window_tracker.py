import subprocess
import os
import time

def shellCommand(args):
    return subprocess.Popen(args, stdout=subprocess.PIPE).stdout.read()

def currentWindowTitle():
    exe = os.path.dirname(os.path.abspath(__file__)) + "/current_window_title.sh"
    return subprocess.check_output(exe).rstrip()

if __name__ == "__main__":
    while True:
        print currentWindowTitle()
        time.sleep(1)
