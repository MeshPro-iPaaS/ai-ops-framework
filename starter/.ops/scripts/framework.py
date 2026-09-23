"""Shared reading helpers. Every generator and the check use these, so there is one parser."""
from __future__ import annotations
import io, os, re, glob

FOLDERS = ["00 - Inbox", "01 - Company", "02 - Work", "03 - People",
           "04 - Knowledge", "05 - Operations", "06 - Daily", "_Templates"]
DEPTS_DIR = os.path.join("01 - Company", "Departments")
ROLES_DIR = os.path.join("01 - Company", "Roles")
FLOWS_DIR = os.path.join("01 - Company", "Workflows")
DECISIONS_DIR = os.path.join("01 - Company", "Decisions")
WORK_DIR = "02 - Work"
PICTURE_DIR = os.path.join("05 - Operations", "picture")
PAGE_DASH = "ai_operations.html"
PAGE_AGENTS = "agents.html"
PAGE_FLOWS = "workflows.html"
PAGE_PROJECTS = "projects.html"
SITE_PAGES = (PAGE_DASH, PAGE_AGENTS, PAGE_FLOWS, PAGE_PROJECTS)
PICTURE = os.path.join(PICTURE_DIR, PAGE_DASH)   # the page you open first
REGISTER = os.path.join(FLOWS_DIR, "Workflows.md")
AGENTS_DIR = os.path.join(".claude", "agents")

READINESS = {"not-yet", "partly", "ready"}
DOC_STATUS = {"draft", "validated"}
AUTHORITY = {"observe", "recommend", "prepare", "execute"}

# A workflow that belongs to no single department says so in this word rather than leaving the
# field blank, because blank cannot be told apart from forgotten.
COMPANY_WIDE = "company"


def read(p):
    try:
        return io.open(p, encoding="utf-8").read()
    except Exception:
        return ""


def split(text):
    """frontmatter dict (flat scalars + simple lists), body"""
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.S)
    if not m:
        return {}, text
    fm, body, key = {}, m.group(2), None
    for line in m.group(1).split("\n"):
        if re.match(r"^\s*-\s+", line) and key:
            fm.setdefault(key, []).append(re.sub(r"^\s*-\s+", "", line).strip().strip('"'))
            continue
        k = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if k:
            key = k.group(1)
            v = k.group(2).strip().strip('"')
            fm[key] = v if v else []
    return fm, body


def note(p):
    fm, body = split(read(p))
    fm["_path"] = p.replace(os.sep, "/")
    fm["_name"] = os.path.basename(p)[:-3]
    fm["_body"] = body
    return fm


# Every folder carries a README.md saying what belongs in it. It is signage, not content: it is never a
# role, a workflow or a note that needs frontmatter, and the first install proved the point by compiling
# one into an agent called "README".
SIGNAGE = {"README.md", "CLAUDE.md"}

# Folders that are machinery, not notes.
SKIP_DIRS = {".claude", ".ops", ".git", ".obsidian", "picture", "__pycache__", "node_modules"}


def is_source_tree(d):
    """True if d is a copy of this framework's own repository.

    The download usually lands *inside* the vault — that is the natural thing for a session to do
    with a folder it has just been handed, and for a while it was what our own guide said to do.
    Its files are not the user's notes. Read as notes they fail ten of the thirteen checks, and the
    first thing a new owner sees is a wall of red about files they never wrote. So the rule lives
    here, in the one parser everything shares, rather than in an instruction somebody can not follow.
    """
    return (os.path.isfile(os.path.join(d, "install.py"))
            and os.path.isfile(os.path.join(d, "framework", "vault", "CONTRACT.md")))


def source_trees(root):
    """Every copy of the framework's own source sitting inside the vault, outermost first."""
    found = []
    for r, dirs, _ in os.walk(root):
        dirs[:] = [x for x in dirs if x not in SKIP_DIRS]
        for x in list(dirs):
            p = os.path.join(r, x)
            if is_source_tree(p):
                found.append(p.replace(os.sep, "/"))
                dirs.remove(x)
    return sorted(found)


def notes(root, sub, skip=()):
    out = []
    for p in sorted(glob.glob(os.path.join(root, sub, "*.md"))):
        if os.path.basename(p) in skip or os.path.basename(p) in SIGNAGE:
            continue
        out.append(note(p))
    return out


def first_diagram(body):
    m = re.search(r"```mermaid\n(.*?)\n```", body, re.S)
    return m.group(1) if m else ""


def summary(body, label):
    m = re.search(r"\*\*" + re.escape(label) + r"\.\*\*\s*(.+?)(?=\s\*\*[A-Z]|\n\n|\Z)", body, re.S)
    return " ".join(m.group(1).split()) if m else ""


def all_notes(root):
    out = []
    for r, d, f in os.walk(root):
        d[:] = [x for x in d
                if x not in SKIP_DIRS and not is_source_tree(os.path.join(r, x))]
        for n in f:
            if n.endswith(".md") and n not in SIGNAGE:
                out.append(note(os.path.join(r, n)))
    return out
