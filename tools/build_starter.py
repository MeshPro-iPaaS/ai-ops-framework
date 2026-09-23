#!/usr/bin/env python3
"""build_starter.py — produce starter/, a vault that is already installed.

Run this from the repository root whenever anything under framework/ changes:

    python tools/build_starter.py

Why it exists: not every Claude session can run programs on the person's computer. Plenty can read
and write files in a connected folder and nothing more. For those, `install.py` is unreachable and the
whole product would be too — so the finished result ships in the repository and the install becomes a
copy, which any session can do.

The check result is deliberately NOT shipped. A green tick copied from somebody else's machine is
exactly the kind of claim this framework exists to refuse; the dashboard says the check has never run
here, because it has not.
"""
from __future__ import annotations
import io, os, shutil, subprocess, sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(HERE, "starter")


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    r = subprocess.run([sys.executable, os.path.join(HERE, "install.py"), OUT],
                       stdin=subprocess.DEVNULL, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stdout, r.stderr)
        raise SystemExit("the install did not finish cleanly — fix that before shipping a starter")

    # no borrowed green tick
    chk = os.path.join(OUT, "05 - Operations", "picture", "check.json")
    if os.path.exists(chk):
        os.remove(chk)
    # rebuild the pages so they say the check has never run, which is true of a copied vault
    subprocess.run([sys.executable, os.path.join(OUT, ".ops", "scripts", "build_picture.py"), OUT],
                   capture_output=True, text=True)

    for root, dirs, files in os.walk(OUT):
        for d in list(dirs):
            if d == "__pycache__":
                shutil.rmtree(os.path.join(root, d)); dirs.remove(d)

    io.open(os.path.join(OUT, "README.md"), "w", encoding="utf-8", newline="\n").write(
        "---\ntype: note\nstatus: active\ncreated: 2026-09-23\nupdated: 2026-09-23\n---\n\n"
        "# Your vault\n\n"
        "> Everything in this folder was copied in by the AI Operations Framework. Open\n"
        "> `05 - Operations/picture/ai_operations.html` in a browser — that is your dashboard.\n\n"
        "The check has not run here yet, and the dashboard says so. It runs when a session that can\n"
        "run programs on this machine runs `.ops/scripts/check.py`. Everything else works without it.\n\n"
        "*Signage, written by the installer. Edit the folder's contents, not this file.*\n")

    n = sum(len(f) for _, _, f in os.walk(OUT))
    print(f"starter/ rebuilt — {n} files, no check result, dashboard says never run")


if __name__ == "__main__":
    main()
