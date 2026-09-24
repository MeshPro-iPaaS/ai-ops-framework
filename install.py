#!/usr/bin/env python3
"""
install.py — AI Operations Framework (MeshPro x Expectus), base package.

    python install.py "C:\\path\\to\\your\\vault" [--names norse]

Creates the folders, installs the contract, templates, departments, roles, workflows and skills, compiles the roles
into runnable agents, builds the register and the page, and runs the check. Idempotent: run it again
after any change and everything downstream comes back into line.

It never overwrites a note you have edited. Templates, scripts and skills are framework files and are
always refreshed; your contract, roles and workflows are copied in once and then left alone, because
after the first install they are yours.
"""
from __future__ import annotations
import io, os, re, sys, shutil, subprocess, datetime

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
FW = os.path.join(HERE, "framework")
TODAY = datetime.date.today().isoformat()

# What the three installed executives are called. The job titles are the default and are perfectly
# good; people remember a name far better than a title, and an executive somebody has named is one
# they actually talk to. The titles stay in the notes either way, so nothing is lost.
TITLES = ["Chief of Staff", "AI Operations Lead", "Workflow Architect"]
SCHEMES = {
    "titles":     ("their job titles",        TITLES),
    "norse":      ("Norse mythology",         ["Saga", "Völundur", "Bragi"]),
    "friends":    ("Friends",                 ["Monica", "Chandler", "Ross"]),
    "kardashian": ("the Kardashians",         ["Kourtney", "Kim", "Khloé"]),
    "greek":      ("Greek mythology",         ["Athena", "Hephaestus", "Hermes"]),
}

FOLDERS = {
    "00 - Inbox": "Anything not yet filed. This folder is emptied, not stored.",
    "01 - Company": "How the organisation works: decisions, roles, workflows, the weekly record.",
    "01 - Company/Decisions": "One note per decision. An agent may draft everything except the decision.",
    "01 - Company/Departments": "One note per department. Each names one executive who answers for it.",
    "01 - Company/Roles": "One note per role. Edit these, never the compiled agents in .claude/agents.",
    "01 - Company/Workflows": "One note per workflow, named by what it does. Workflows.md is generated.",
    "01 - Company/Weekly": "One note per week: what finished, what is stale, what is next.",
    "02 - Work": "The things you are actually doing — projects and initiatives.",
    "03 - People": "Colleagues, customers, partners: whoever you keep a record about.",
    "04 - Knowledge": "Reference material that stays true regardless of what you are doing this week.",
    "05 - Operations": "The generated picture and the lists of what is waiting. "
                       "Your dashboard is picture/ai_operations.html — open it in a browser.",
    "06 - Daily": "The day log. Append-only, and never a source of truth.",
    "_Templates": "The shapes every new note is made from.",
}


def say(step, msg):
    print(f"  {step}. {msg}")


# Agent filenames want plain ASCII — Völundur is a fine name and a poor filename.
FOLD = {"á": "a", "à": "a", "ä": "a", "å": "a", "â": "a", "é": "e", "è": "e", "ë": "e", "ê": "e",
        "í": "i", "ì": "i", "ï": "i", "î": "i", "ó": "o", "ò": "o", "ö": "o", "ø": "o", "ô": "o",
        "ú": "u", "ù": "u", "ü": "u", "û": "u", "ý": "y", "ñ": "n", "ç": "c", "þ": "th",
        "ð": "d", "æ": "ae", "ß": "ss"}


def slugify(name):
    out = []
    for ch in name.lower():
        for c in FOLD.get(ch, ch):                 # a fold can be two letters: þ is th, æ is ae
            out.append(c if (c.isalnum() and c.isascii()) else "-")
    return re.sub(r"-+", "-", "".join(out)).strip("-") or "role"


def choose_scheme(arg):
    """Returns {job title: name}. Empty means leave the titles alone."""
    if arg:
        key = arg.strip().lower()
        if key in SCHEMES:
            return dict(zip(TITLES, SCHEMES[key][1]))
        names = [n.strip() for n in arg.split(",") if n.strip()]
        if len(names) >= len(TITLES):
            return dict(zip(TITLES, names))
        print(f"  (I do not know the naming scheme {arg!r}, and it is not a list of "
              f"{len(TITLES)} names — keeping the job titles.)")
        return {}
    if not sys.stdin.isatty():          # a session is running this, not a person at a keyboard
        return {}
    print("\nWhat should your three executives be called?\n")
    keys = list(SCHEMES)
    for i, k in enumerate(keys, 1):
        label, names = SCHEMES[k]
        print(f"  {i}. {label:22} {', '.join(names)}")
    print(f"  {len(keys)+1}. something else       type {len(TITLES)} names, comma separated\n")
    try:
        answer = input("  Choose a number, or type your own names: ").strip()
    except EOFError:
        return {}
    if not answer:
        return {}
    if answer.isdigit() and 1 <= int(answer) <= len(keys):
        return dict(zip(TITLES, SCHEMES[keys[int(answer) - 1]][1]))
    return choose_scheme(answer) if "," in answer else {}


def apply_naming(vault, mapping):
    """Rename the executives everywhere at once — the role notes, the departments that point at them,
    and the workflows they own. Done before anything is compiled, so nothing downstream ever sees the
    old name. The job title stays on each role as `title:`."""
    if not mapping:
        return []
    folders = [os.path.join(vault, "01 - Company", d) for d in ("Roles", "Departments", "Workflows")]
    pairs = sorted(mapping.items(), key=lambda kv: -len(kv[0]))   # longest first, so no partial hits
    for folder in folders:
        for f in sorted(os.listdir(folder)) if os.path.isdir(folder) else []:
            if not f.endswith(".md"):
                continue
            path = os.path.join(folder, f)
            lines = io.open(path, encoding="utf-8").read().split("\n")
            for i, line in enumerate(lines):
                if line.startswith("title:"):      # the job title is the one thing that must not move
                    continue
                for old, new in pairs:
                    line = line.replace(old, new)
                lines[i] = line
            io.open(path, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
    roles = os.path.join(vault, "01 - Company", "Roles")
    for old, new in pairs:
        src, dst = os.path.join(roles, old + ".md"), os.path.join(roles, new + ".md")
        if old != new and os.path.exists(src) and not os.path.exists(dst):
            os.rename(src, dst)
    for f in sorted(os.listdir(roles)):
        if not f.endswith(".md"):
            continue
        path = os.path.join(roles, f)
        text = io.open(path, encoding="utf-8").read()
        m = re.search(r"^name:\s*(.+)$", text, re.M)
        if m:
            text = re.sub(r"^slug:.*$", "slug: " + slugify(m.group(1).strip()), text, count=1, flags=re.M)
            io.open(path, "w", encoding="utf-8", newline="\n").write(text)
    return [f"{old} is {new}" for old, new in mapping.items() if old != new]


def title_of(path):
    m = re.search(r"^title:\s*(.+)$", io.open(path, encoding="utf-8").read(), re.M)
    return m.group(1).strip() if m else ""


def titles_present(folder):
    """The job titles already installed, whatever the executives have since been renamed to.

    Without this, a second run re-adds 'Chief of Staff.md' beside the 'Saga.md' it became, and the
    check quite rightly complains that the department now has two executives.
    """
    out = set()
    if os.path.isdir(folder):
        for f in sorted(os.listdir(folder)):
            if f.endswith(".md"):
                t = title_of(os.path.join(folder, f))
                if t:
                    out.add(t)
    return out


def copy_once(src, dst):
    """Framework content that becomes yours: copied on the first install, never overwritten after."""
    if os.path.exists(dst):
        return False
    shutil.copy2(src, dst)
    return True


def main(vault, names=None):
    vault = os.path.abspath(vault)
    fresh = not os.path.exists(os.path.join(vault, "CLAUDE.md"))
    print(f"\nAI Operations Framework — base package")
    print(f"{'installing into' if fresh else 'updating'}: {vault}\n")

    # 1. folders, each with a note saying what belongs in it
    os.makedirs(vault, exist_ok=True)
    made = 0
    for rel, why in FOLDERS.items():
        d = os.path.join(vault, rel)
        if not os.path.isdir(d):
            os.makedirs(d, exist_ok=True)
            made += 1
        readme = os.path.join(d, "README.md")
        # Always rewritten: this is signage the framework owns, not a note you wrote. Copy-once left
        # old installs describing the folder the way it worked two versions ago.
        io.open(readme, "w", encoding="utf-8", newline="\n").write(
            f"---\ntype: note\nstatus: active\ncreated: {TODAY}\nupdated: {TODAY}\n---\n\n"
            f"# {os.path.basename(rel)}\n\n> {why}\n\n"
            f"*Signage, written by the installer. Edit the folder's contents, not this file.*\n")
    say(1, f"{len(FOLDERS)} folders in place ({made} created), each saying what belongs in it")

    # 2. the contract
    n = copy_once(os.path.join(FW, "vault", "CONTRACT.md"), os.path.join(vault, "CLAUDE.md"))
    say(2, "contract installed as CLAUDE.md" if n else "contract left alone — it is yours now")

    # 3. templates (always refreshed: framework files)
    for f in sorted(os.listdir(os.path.join(FW, "templates"))):
        shutil.copy2(os.path.join(FW, "templates", f), os.path.join(vault, "_Templates", f))
    say(3, f"{len(os.listdir(os.path.join(FW,'templates')))} templates refreshed")

    # 4. departments, roles and workflows (copied once, then yours)
    d = sum(copy_once(os.path.join(FW, "departments", f),
                      os.path.join(vault, "01 - Company", "Departments", f))
            for f in sorted(os.listdir(os.path.join(FW, "departments"))))
    roles_dir = os.path.join(vault, "01 - Company", "Roles")
    have = titles_present(roles_dir)
    r = sum(copy_once(os.path.join(FW, "roles", f), os.path.join(roles_dir, f))
            for f in sorted(os.listdir(os.path.join(FW, "roles")))
            if title_of(os.path.join(FW, "roles", f)) not in have)
    w = sum(copy_once(os.path.join(FW, "processes", f), os.path.join(vault, "01 - Company", "Workflows", f))
            for f in sorted(os.listdir(os.path.join(FW, "processes"))))
    say(4, f"{d} departments, {r} roles and {w} workflows installed" if (d or r or w) else
        "departments, roles and workflows left alone — yours to edit")

    # 4b. name the executives, before anything is compiled from them
    if fresh:
        renamed = apply_naming(vault, choose_scheme(names))
        if renamed:
            say("4b", "your executives: " + " · ".join(renamed))

    # 5. skills and scripts (always refreshed)
    sk = os.path.join(vault, ".claude", "skills")
    os.makedirs(sk, exist_ok=True)
    for d in sorted(os.listdir(os.path.join(FW, "skills"))):
        shutil.rmtree(os.path.join(sk, d), ignore_errors=True)
        shutil.copytree(os.path.join(FW, "skills", d), os.path.join(sk, d))
    ops = os.path.join(vault, ".ops", "scripts")
    os.makedirs(ops, exist_ok=True)
    for f in sorted(os.listdir(os.path.join(FW, "scripts"))):
        if f.endswith(".py"):
            shutil.copy2(os.path.join(FW, "scripts", f), os.path.join(ops, f))
    # the opt-in helper that turns the machinery on where there is no Python — it has to travel with
    # the vault, because the vault is often all the person has
    opsdir = os.path.join(vault, ".ops")
    for f in sorted(os.listdir(os.path.join(FW, "ops"))) if os.path.isdir(os.path.join(FW, "ops")) else []:
        shutil.copy2(os.path.join(FW, "ops", f), os.path.join(opsdir, f))
    say(5, f"{len(os.listdir(os.path.join(FW,'skills')))} skills and "
           f"{len([f for f in os.listdir(ops) if f.endswith('.py')])} scripts installed")

    # 6-8. generate
    for i, script in enumerate(("build_roles.py", "build_register.py", "build_picture.py"), start=6):
        out = subprocess.run([sys.executable, os.path.join(ops, script), vault],
                             capture_output=True, text=True)
        say(i, (out.stdout or out.stderr).strip().splitlines()[0] if (out.stdout or out.stderr)
            else f"{script} ran")

    # 9. check
    out = subprocess.run([sys.executable, os.path.join(ops, "check.py"), vault],
                         capture_output=True, text=True)
    # the check writes its result next to the picture; rebuild once more so the page carries it
    # rather than saying "never run" on a vault where it has just run
    subprocess.run([sys.executable, os.path.join(ops, "build_picture.py"), vault],
                   capture_output=True, text=True)
    print()
    print(out.stdout.strip())
    print()

    # If the download landed inside the vault — which is what usually happens — say so plainly.
    # Nothing reads from it, but it is clutter and people wonder whether it is meant to be there.
    sys.path.insert(0, ops)
    try:
        import framework as _F
        inside = _F.source_trees(vault)
    except Exception:
        inside = []
    if inside:
        for t in inside:
            print(f"Your copy of the framework is at {os.path.relpath(t, vault)} — it is excluded "
                  f"from your notes and your checks. Delete it whenever you like.")
        print()

    # Both: the absolute path with a link you can click, and the path inside the folder. The
    # absolute one is what a person needs to actually find the file; the relative one still matters
    # when this ran somewhere other than the laptop, because then the absolute one names a place
    # that is not theirs, and the relative one is the part they can recognise.
    dash = "05 - Operations/picture/ai_operations.html"
    sys.path.insert(0, ops)
    try:
        import framework as _FW
        where = _FW.say_where(vault, "Your dashboard — open it in a browser")
    except Exception:
        where = f"Your dashboard — open it in a browser:\n   {os.path.join(vault, dash)}"
    if out.returncode == 0:
        print(where)
        print(f"   inside your folder: {dash}")
        print()
        print("Then open the vault folder in Obsidian, and connect it in Claude.")
        print()
        print("First thing to do: name your departments. Ask Claude to walk you through")
        print("'Setting Up a Department' — it is the workflow the rest of the layer hangs off.")
    else:
        print("The check found something untrue. Fix the note it names, then run this again.")
        print(where)
    print(f"\nAI Operations Framework, base package — MeshPro x Expectus\n")
    return out.returncode


if __name__ == "__main__":
    args, scheme, skip = [], None, False
    for i, a in enumerate(sys.argv[1:]):
        if skip:
            skip = False
            continue
        if a == "--names":
            scheme = sys.argv[i + 2] if i + 2 < len(sys.argv) else None
            skip = True
        elif a.startswith("--names="):
            scheme = a.split("=", 1)[1]
        elif not a.startswith("--"):
            args.append(a)
    if not args:
        print(__doc__)
        print("Naming schemes: " + ", ".join(SCHEMES) + " — or a comma-separated list of your own.")
        sys.exit(2)
    sys.exit(main(args[0], scheme))
