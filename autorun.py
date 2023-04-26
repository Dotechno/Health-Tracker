# run run.py with while try
import os
import time
import sys
import subprocess


def run():
    while True:
        try:
            subprocess.call("python run.py", shell=True)
        except Exception as e:
            print(e)
            time.sleep(5)
            continue
        break


if __name__ == '__main__':
    run()
