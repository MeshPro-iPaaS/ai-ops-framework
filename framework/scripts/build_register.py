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


def build(root):
    flows = F.notes(root, F.FLOWS_DIR, skip=("Workflows.md",))
    rows = []
    for w in sorted(flows, key=lambda x: x["_name"]):
        rows.append("| [[{}]] | {} | {} | {} | {} |".format(
            w["_name"], w.get("owner") or "—",
            "✅ validated" if w.get("doc_status") == "validated" else "✏️ draft",
            MARK.get(w.get("readiness", ""), "—"),
            F.summary(w["_body"], "Purpose")[:110] or "—"))
    v = sum(1 for w in flows if w.get("doc_status") == "validated")
    r = sum(1 for w in flows if w.get("readiness") == "ready")
    block = "\n".join([
        BEGIN,
        f"*{len(flows)} workflows · {v} validated against a real case · {r} running end to end. "
        f"Generated {datetime.date.today().isoformat()} — edit the workflow notes, not this table.*",
        "",
        "| Workflow | Owner | Note | Workflow | Purpose |",
        "|---|---|---|---|---|",
        *rows, "", END])
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
