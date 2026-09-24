#!/usr/bin/env python3
"""build_starter.py — produce starter/, a set of vaults that are already installed.

Run this from the repository root whenever anything under framework/ changes:

    python tools/build_starter.py

Why it exists: installing this must never depend on what happens to be on the person's computer.
Plenty of machines have no Python, and plenty of Claude sessions cannot run programs on a person's
computer at all. Both of those turned up in real demos. So the finished vault ships in the repository
and installing it is a copy — which every session can do, on every machine.

One folder per naming scheme, because the alternative was asking a session to rename three executives
across fifteen files by hand in a room full of laptops. A copy cannot be got half right.

The check result is deliberately NOT shipped. A green tick copied from somebody else's machine is
exactly the kind of claim this framework exists to refuse; the dashboard says the check has never run
here, because it has not.
"""
from __future__ import annotations
import io, os, shutil, subprocess, sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(HERE, "starter")
sys.path.insert(0, HERE)
from install import SCHEMES                                     # noqa: E402  the one list of names

README = """---
type: note
status: active
created: 2026-09-24
updated: 2026-09-24
---

# Your vault

> Everything in this folder was copied in by the AI Operations Framework. Open
> `05 - Operations/picture/ai_operations.html` in a browser — that is your dashboard.

Your three executives are called **{names}**.

The check has not run here yet, and the dashboard says so. It runs when a session that can run
programs on this machine runs `.ops/scripts/check.py`. Nothing else needs it: naming departments,
adding executives and specialists, teaching skills and writing workflows down are all notes, and you
can write notes.

*Signage, written by the installer. Edit the folder's contents, not this file.*
"""


def one(key, label, names):
    dst = os.path.join(OUT, key)
    r = subprocess.run([sys.executable, os.path.join(HERE, "install.py"), dst, "--names", key],
                       stdin=subprocess.DEVNULL, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stdout, r.stderr)
        raise SystemExit(f"the {key} install did not finish cleanly — fix that before shipping a starter")

    # no borrowed green tick, and the pages must say so
    for f in ("check.json",):
        p = os.path.join(dst, "05 - Operations", "picture", f)
        if os.path.exists(p):
            os.remove(p)
    subprocess.run([sys.executable, os.path.join(dst, ".ops", "scripts", "build_picture.py"), dst],
                   capture_output=True, text=True)

    for root, dirs, _ in os.walk(dst):
        for d in list(dirs):
            if d == "__pycache__":
                shutil.rmtree(os.path.join(root, d)); dirs.remove(d)

    io.open(os.path.join(dst, "README.md"), "w", encoding="utf-8", newline="\n").write(
        README.format(names=", ".join(names)))
    return sum(len(f) for _, _, f in os.walk(dst))


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    total = 0
    for key, (label, names) in SCHEMES.items():
        n = one(key, label, names)
        total += n
        print(f"  starter/{key:11} {', '.join(names):34} {n} files")
    io.open(os.path.join(OUT, "README.md"), "w", encoding="utf-8", newline="\n").write(
        "# Pre-built vaults\n\n"
        "One folder per naming scheme. **Copy the contents of one of them** into the person's folder —\n"
        "all of it, including the hidden `.claude` and `.ops` folders — and the install is done. No\n"
        "Python, no terminal, nothing to run.\n\n"
        "| Folder | Your three executives are called |\n|---|---|\n"
        + "".join(f"| `{k}/` | {', '.join(v[1])} |\n" for k, v in SCHEMES.items())
        + "\nThey are identical apart from the names. See [`../INSTALL.md`](../INSTALL.md).\n")
    print(f"starter/ rebuilt — {len(SCHEMES)} vaults, {total} files, no check result in any of them")


if __name__ == "__main__":
    main()
