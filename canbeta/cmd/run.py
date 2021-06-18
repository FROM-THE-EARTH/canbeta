
import argparse
import os
import sys
sys.path.append(os.path.join(os.getcwd()))

from can09.parent.main import run_parent
from can09.child.main import run_child


parser = argparse.ArgumentParser()

parser.add_argument("device", choices=["parent", "child"])

args = parser.parse_args()

if args.device == "parent":
    run_parent()
elif args.device == "child":
    run_child()
else:
    raise ValueError(
        "'device' must be 'parent' or 'child'."
    )