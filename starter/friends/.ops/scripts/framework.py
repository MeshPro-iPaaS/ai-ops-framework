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
PAGE_SKILLS = "skills.html"
SITE_PAGES = (PAGE_DASH, PAGE_AGENTS, PAGE_SKILLS, PAGE_FLOWS, PAGE_PROJECTS)
PICTURE = os.path.join(PICTURE_DIR, PAGE_DASH)   # the page you open first
REGISTER = os.path.join(FLOWS_DIR, "Workflows.md")
AGENTS_DIR = os.path.join(".claude", "agents")
SKILLS_DIR = os.path.join(".claude", "skills")

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


# ---------------------------------------------------------------- skills
# A skill is a folder with a SKILL.md in it, not a note in the vault tree, so it needs its own reader.
# Its owner is written as a role's name or as a job title: the installer renames executives, and a
# skill that named "Chief of Staff" would otherwise point at nobody the moment somebody chose Norse
# gods. Matching on either means the pointer survives the rename without a migration.
def skills(root):
    out = []
    base = os.path.join(root, SKILLS_DIR)
    if not os.path.isdir(base):
        return out
    for slug in sorted(os.listdir(base)):
        p = os.path.join(base, slug, "SKILL.md")
        if not os.path.isfile(p):
            continue
        fm, body = split(read(p))
        fm["_path"] = p.replace(os.sep, "/")
        fm["_slug"] = slug
        fm["_name"] = fm.get("name") or slug
        fm["_body"] = body
        fm["_stops"] = section(body, "Where it stops") or section(body, "Never")
        fm["_when"] = section(body, "When to use it")
        out.append(fm)
    return out


def owner_of(skill, roles):
    """The role a skill belongs to, matched on its name or on its job title."""
    want = (skill.get("owner") or "").strip()
    if not want:
        return None
    for r in roles:
        if (r.get("name") or r["_name"]).strip() == want:
            return r
    for r in roles:
        if (r.get("title") or "").strip() == want:
            return r
    return None


def section(body, heading):
    """The prose under a `## heading`, up to the next heading of the same level."""
    m = re.search(r"^##\s+" + re.escape(heading) + r"\s*$(.*?)(?=^##\s|\Z)", body, re.S | re.M)
    if not m:
        return ""
    text = re.sub(r"^\s*[-*]\s+", "", m.group(1).strip(), flags=re.M)
    text = re.sub(r"`([^`]*)`", r"\1", text)
    return " ".join(text.split())


# ---------------------------------------------------------------- workflow steps
# Every workflow note carries a `## The steps` table. The site draws it, so the table is the single
# place the steps are written: there is no second copy in a diagram to fall out of step with it.
STEP_HEADS = ("step", "who", "what they need", "what comes out")


def steps(body):
    """The rows of the `## The steps` table, as {n, step, who, needs, out}."""
    block = re.search(r"^##\s+The steps\s*$(.*?)(?=^##\s|\Z)", body, re.S | re.M)
    if not block:
        return []
    rows = []
    for line in block.group(1).split("\n"):
        line = line.strip()
        if not line.startswith("|") or set(line) <= set("|-: "):
            continue
        cells = [c.strip().replace("`", "") for c in line.strip("|").split("|")]
        if len(cells) < 2:
            continue
        low = [c.lower() for c in cells]
        if any(h in low for h in STEP_HEADS):
            continue
        n = cells[0]
        rest = cells[1:]
        if not n.isdigit():
            rest = cells
            n = str(len(rows) + 1)
        while len(rest) < 4:
            rest.append("")
        if not rest[0]:
            continue
        rows.append({"n": n, "step": rest[0], "who": rest[1], "needs": rest[2], "out": rest[3]})
    return rows


# ---------------------------------------------------------------- is the site current
# "Was the page built after the notes?" used to be answered with timestamps, and copying a vault
# resets every timestamp — so a perfectly correct copy reported itself stale. This answers the same
# question with content, which survives being copied, zipped, synced or restored from a backup.
def source_fingerprint(root):
    import hashlib
    h = hashlib.sha256()
    paths = sorted(
        glob.glob(os.path.join(root, "01 - Company", "**", "*.md"), recursive=True)
        + glob.glob(os.path.join(root, WORK_DIR, "**", "*.md"), recursive=True)
        + glob.glob(os.path.join(root, SKILLS_DIR, "*", "SKILL.md")),
        key=lambda p: os.path.relpath(p, root).replace(os.sep, "/").lower())
    for p in paths:
        rel = os.path.relpath(p, root).replace(os.sep, "/")
        if rel.endswith(REGISTER.replace(os.sep, "/")):
            continue          # generated from the very notes we are hashing
        h.update(rel.encode("utf-8"))
        h.update(b"\0")
        h.update(read(p).replace("\r\n", "\n").encode("utf-8"))
        h.update(b"\0")
    return h.hexdigest()
