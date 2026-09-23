#!/usr/bin/env python3
"""
install.py — AI Operations Framework (MeshPro x Expectus), base package.

    python install.py "C:\\path\\to\\your\\vault"

Creates the folders, installs the contract, templates, departments, roles, workflows and skills, compiles the roles
into runnable agents, builds the register and the page, and runs the check. Idempotent: run it again
after any change and everything downstream comes back into line.

It never overwrites a note you have edited. Templates, scripts and skills are framework files and are
always refreshed; your contract, roles and workflows are copied in once and then left alone, because
after the first install they are yours.
"""
from __future__ import annotations
import io, os, sys, shutil, subprocess, datetime

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
FW = os.path.join(HERE, "framework")
TODAY = datetime.date.today().isoformat()

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


def copy_once(src, dst):
    """Framework content that becomes yours: copied on the first install, never overwritten after."""
    if os.path.exists(dst):
        return False
    shutil.copy2(src, dst)
    return True


def main(vault):
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
    r = sum(copy_once(os.path.join(FW, "roles", f), os.path.join(vault, "01 - Company", "Roles", f))
            for f in sorted(os.listdir(os.path.join(FW, "roles"))))
    w = sum(copy_once(os.path.join(FW, "processes", f), os.path.join(vault, "01 - Company", "Workflows", f))
            for f in sorted(os.listdir(os.path.join(FW, "processes"))))
    say(4, f"{d} department, {r} roles and {w} workflows installed" if (d or r or w) else
        "departments, roles and workflows left alone — yours to edit")

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

    # Relative, because the install frequently runs inside Claude's own copy of the folder: an
    # absolute path there names somewhere that does not exist on the laptop, and anyone watching
    # reads that as a broken install.
    dash = "05 - Operations/picture/ai_operations.html"
    if out.returncode == 0:
        print("Your dashboard, inside your folder — open it in a browser:")
        print(f"   {dash}")
        print()
        print("Then open the vault folder in Obsidian, and connect it in Claude.")
        print()
        print("First thing to do: name your departments. Ask Claude to walk you through")
        print("'Setting Up a Department' — it is the workflow the rest of the layer hangs off.")
    else:
        print("The check found something untrue. Fix the note it names, then run this again.")
        print(f"The dashboard, such as it is: {dash}")
    print(f"\nAI Operations Framework, base package — MeshPro x Expectus\n")
    return out.returncode


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
