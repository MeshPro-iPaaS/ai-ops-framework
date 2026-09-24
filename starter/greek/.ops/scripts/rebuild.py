#!/usr/bin/env python3
"""rebuild.py — regenerate everything from the notes, in the right order, then check it.

    python .ops/scripts/rebuild.py "<the vault folder>"

The order is not arbitrary: agents come from the role notes, the register comes from the workflow
notes, the site reads both, and the check measures the result. Run it after anything changes, and
after copying a vault from somewhere else — a copy resets every file's timestamp, so the site looks
older than the notes it was built from until it is built again here.
"""
from __future__ import annotations
import os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
STEPS = ["build_roles.py", "build_register.py", "build_picture.py"]


def main(root):
    for s in STEPS:
        r = subprocess.run([sys.executable, os.path.join(HERE, s), root], capture_output=True, text=True)
        out = (r.stdout or r.stderr).strip().splitlines()
        print("  " + (out[0] if out else s))
        if r.returncode != 0:
            print("\n".join(out[1:]))
            return r.returncode
    chk = subprocess.run([sys.executable, os.path.join(HERE, "check.py"), root],
                         capture_output=True, text=True)
    print()
    print(chk.stdout.strip())
    # the page is built before the check runs, so build it once more to carry the result
    subprocess.run([sys.executable, os.path.join(HERE, "build_picture.py"), root],
                   capture_output=True, text=True)
    return chk.returncode


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.getcwd()))
