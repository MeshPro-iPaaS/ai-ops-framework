#!/usr/bin/env python3
"""build_register.py — the workflow register, written from the workflow notes themselves.

Source: 01 - Company/Workflows/*.md   Output: the generated block inside Workflows.md
"""
from __future__ import annotations
import io, os, re, sys, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import framework as F

BEGIN = "<!-- BEGIN generated — build_register.py -->"
END = "<!-- END generated -->"
MARK = {"ready": "🟢 running", "partly": "🟡 partly", "not-yet": "⚪ described"}


def row(w):
    return "| [[{}]] | {} | {} | {} | {} |".format(
        w["_name"], w.get("owner") or "—",
        "✅ validated" if w.get("doc_status") == "validated" else "✏️ draft",
        MARK.get(w.get("readiness", ""), "—"),
        F.summary(w["_body"], "Purpose")[:110] or "—")


def build(root):
    flows = F.notes(root, F.FLOWS_DIR, skip=("Workflows.md",))
    depts = F.notes(root, F.DEPTS_DIR)

    # Grouped by department, because that is how anyone actually looks for a workflow: they know whose
    # job it is before they know what it is called. A department with no workflow is listed anyway —
    # the empty group is the point, not an omission.
    groups, seen = [], set()
    for d in sorted(depts, key=lambda x: x.get("name") or x["_name"]):
        name = d.get("name") or d["_name"]
        mine = sorted([w for w in flows if (w.get("department") or "") == name], key=lambda x: x["_name"])
        seen.update(id(w) for w in mine)
        groups.append((name, mine))
    company = sorted([w for w in flows if (w.get("department") or "") == F.COMPANY_WIDE],
                     key=lambda x: x["_name"])
    seen.update(id(w) for w in company)
    homeless = sorted([w for w in flows if id(w) not in seen], key=lambda x: x["_name"])

    body = []
    for name, mine in groups:
        body += ["", f"### {name}", ""]
        body += (["| Workflow | Owner | Note | Workflow | Purpose |", "|---|---|---|---|---|"]
                 + [row(w) for w in mine]) if mine else \
                ["*No workflow written down yet — this department is a name until one is.*"]
    if company:
        body += ["", "### Company-wide", "",
                 "| Workflow | Owner | Note | Workflow | Purpose |", "|---|---|---|---|---|"] \
                + [row(w) for w in company]
    if homeless:
        body += ["", "### Department not recognised", "",
                 "*These name a department that has no note. Fix the `department:` field or write the note.*", "",
                 "| Workflow | Owner | Note | Workflow | Purpose |", "|---|---|---|---|---|"] \
                + [row(w) for w in homeless]

    v = sum(1 for w in flows if w.get("doc_status") == "validated")
    r = sum(1 for w in flows if w.get("readiness") == "ready")
    block = "\n".join([
        BEGIN,
        f"*{len(flows)} workflows across {len(depts)} department{'' if len(depts)==1 else 's'} · "
        f"{v} validated against a real case · {r} running end to end. "
        f"Generated {datetime.date.today().isoformat()} — edit the workflow notes, not this table.*",
        *body, "", END])
    p = os.path.join(root, F.REGISTER)
    if os.path.exists(p):
        cur = F.read(p)
        new = re.sub(re.escape(BEGIN) + r".*?" + re.escape(END), block, cur, flags=re.S) \
            if BEGIN in cur else cur.rstrip("\n") + "\n\n" + block + "\n"
    else:
        new = ("---\ntype: note\nstatus: active\nowner: Chief of Staff\n"
               f"created: {datetime.date.today().isoformat()}\nupdated: {datetime.date.today().isoformat()}\n---\n\n"
               "# Workflows\n\n> Every workflow written down, with two marks each: whether the **note** has been "
               "validated against a real case, and whether the **workflow** actually runs. They go wrong "
               "separately, which is why there are two.\n\n" + block + "\n")
    io.open(p, "w", encoding="utf-8", newline="\n").write(new)
    return len(flows), v, r


if __name__ == "__main__":
    root = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    n, v, r = build(root)
    print(f"register rebuilt — {n} workflows, {v} validated, {r} running end to end")
