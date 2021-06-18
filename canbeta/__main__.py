
import argparse
import subprocess
import os
import sys
sys.path.append(os.path.join(os.getcwd()))

PATH_CMD_RUN = os.path.join(os.getcwd(), "can09", "cmd", "run.py")

parser = argparse.ArgumentParser()
parser.add_argument("command", choices=["run"])
parser.add_argument("args")

args = parser.parse_args()

if args.command == "run":
    subprocess.run(["python", PATH_CMD_RUN, args.args])
    