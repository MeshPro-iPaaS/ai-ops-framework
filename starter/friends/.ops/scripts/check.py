#!/usr/bin/env python3
"""check.py — sixteen checks that fail the build when the picture and reality disagree.

Run it before you show anyone the page:  python .ops/scripts/check.py
Exit 0 = everything the vault says about itself is true. Exit 1 = it is not, and each failure says why.

These sixteen are the base. Add one the same session you add a rule — a rule with no check decays, quietly,
and you find out months later.
"""
from __future__ import annotations
import io, os, sys, json, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import framework as F

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PASS, FAIL = [], []
ok = lambda m: PASS.append(m)
bad = lambda m: FAIL.append(m)
TODAY = datetime.date.today()

NAMES = {
    1: "the contract is where every session will look for it",
    2: "every role says what it may and may not do",
    3: "every role has a current agent file",
    4: "every workflow carries both of its marks",
    5: "validated means somebody actually walked a case through it",
    6: "the register matches the workflow notes",
    7: "the site was built from the notes as they are now",
    8: "every note can be read by a machine",
    9: "decisions are either decided by somebody, or not decided",
    10: "nothing is filed outside the folders that exist",
    11: "every department has exactly one executive who answers for it",
    12: "every executive leads a department that exists",
    13: "every workflow belongs somewhere",
    14: "the framework's own files are not being read as your notes",
    15: "every project belongs to a department that exists",
    16: "every skill is owned by an executive and says when to use it",
}


def run(root):
    # 1 — the contract
    if os.path.exists(os.path.join(root, "CLAUDE.md")):
        ok(NAMES[1])
    else:
        bad(f"{NAMES[1]} — CLAUDE.md is missing from the vault root, so no session inherits the rules")

    roles = F.notes(root, F.ROLES_DIR)
    depts = F.notes(root, F.DEPTS_DIR)
    flows = F.notes(root, F.FLOWS_DIR, skip=("Workflows.md",))
    dept_names = {(d.get("name") or d["_name"]) for d in depts}

    # 2 — role contracts are complete
    need = ("name", "authority", "reports_to", "owns", "green_list", "never", "writes")
    miss = [(r["_name"], k) for r in roles for k in need if not r.get(k)]
    for n, k in miss:
        bad(f"{NAMES[2]} — role {n!r} has no {k!r}; an agent with an unstated ceiling has no ceiling")
    bad_auth = [r["_name"] for r in roles if r.get("authority") not in F.AUTHORITY]
    for n in bad_auth:
        bad(f"{NAMES[2]} — role {n!r} uses an authority level outside {sorted(F.AUTHORITY)}")
    if roles and not miss and not bad_auth:
        ok(f"{NAMES[2]} ({len(roles)} roles)")
    if not roles:
        bad(f"{NAMES[2]} — there are no roles at all")

    # 3 — agents say what their role notes say. Content, not timestamps: copying a vault resets every
    # mtime, and the timestamp version of this check failed three times on a perfectly correct copy.
    import build_roles as BR
    stale = []
    for r in roles:
        a = os.path.join(root, F.AGENTS_DIR, BR.slug_of(r) + ".md")
        if not os.path.exists(a):
            bad(f"{NAMES[3]} — {r['_name']!r} has no compiled agent; run build_roles.py")
        elif F.read(a).replace("\r\n", "\n") != BR.agent_text(r):
            stale.append(r["_name"])
    for n in stale:
        bad(f"{NAMES[3]} — the agent for {n!r} no longer says what its role note says; run build_roles.py")
    if roles and not stale:
        ok(NAMES[3])

    # 4 — both marks, using the agreed words
    m4 = 0
    for w in flows:
        if w.get("readiness") not in F.READINESS:
            bad(f"{NAMES[4]} — {w['_name']!r} has readiness {w.get('readiness')!r}, not one of {sorted(F.READINESS)}")
            m4 += 1
        if w.get("doc_status") not in F.DOC_STATUS:
            bad(f"{NAMES[4]} — {w['_name']!r} has doc_status {w.get('doc_status')!r}, not one of {sorted(F.DOC_STATUS)}")
            m4 += 1
        if w.get("readiness") in ("partly", "not-yet") and not w.get("readiness_note"):
            bad(f"{NAMES[4]} — {w['_name']!r} is not running and does not say why")
            m4 += 1
    if flows and not m4:
        ok(f"{NAMES[4]} ({len(flows)} workflows)")

    # 5 — validated carries a date
    m5 = [w["_name"] for w in flows if w.get("doc_status") == "validated" and not w.get("last_validated")]
    for n in m5:
        bad(f"{NAMES[5]} — {n!r} says validated with no last_validated date; a claim with no date is not one")
    if not m5:
        ok(NAMES[5])

    # 6 — the register agrees with the notes
    reg = F.read(os.path.join(root, F.REGISTER))
    if not reg:
        bad(f"{NAMES[6]} — there is no register; run build_register.py")
    else:
        missing = [w["_name"] for w in flows if f"[[{w['_name']}]]" not in reg]
        for n in missing:
            bad(f"{NAMES[6]} — {n!r} is written down but not in the register; run build_register.py")
        if not missing:
            ok(f"{NAMES[6]} ({len(flows)} listed)")

    # 7 — the picture is newer than its sources
    pic = os.path.join(root, F.PICTURE)
    gone = [p for p in F.SITE_PAGES if not os.path.exists(os.path.join(root, F.PICTURE_DIR, p))]
    if gone:
        bad(f"{NAMES[7]} — the site is missing {', '.join(gone)}; run build_picture.py")
    elif not os.path.exists(pic):
        bad(f"{NAMES[7]} — the picture has never been built; run build_picture.py")
    else:
        stamp = {}
        bp = os.path.join(root, F.PICTURE_DIR, "build.json")
        if os.path.exists(bp):
            try:
                stamp = json.loads(F.read(bp))
            except Exception:
                stamp = {}
        if stamp.get("sources") == F.source_fingerprint(root):
            ok(NAMES[7])
        elif stamp:
            bad(f"{NAMES[7]} — a note has changed since the site was built; run build_picture.py")
        else:
            bad(f"{NAMES[7]} — the site does not record what it was built from; run build_picture.py")

    # 8 — frontmatter every machine can read
    everything = F.all_notes(root)
    m8 = [(n["_name"], k) for n in everything for k in ("type", "status", "created")
          if not n.get(k) and "Templates" not in n["_path"]]
    for n, k in m8[:8]:
        bad(f"{NAMES[8]} — {n!r} has no {k!r} in its frontmatter")
    if len(m8) > 8:
        bad(f"{NAMES[8]} — and {len(m8)-8} more notes are missing frontmatter")
    if not m8:
        ok(f"{NAMES[8]} ({len(everything)} notes)")

    # 9 — decisions
    m9 = 0
    for d in F.notes(root, F.DECISIONS_DIR):
        if d.get("status") == "decided" and not d.get("decided_by"):
            bad(f"{NAMES[9]} — {d['_name']!r} is decided but nobody is named as having decided it")
            m9 += 1
        if d.get("status") == "proposed" and d.get("decided_by"):
            bad(f"{NAMES[9]} — {d['_name']!r} is still proposed but names who decided it")
            m9 += 1
    if not m9:
        ok(NAMES[9])

    # 10 — nothing outside the folders
    extra = [n for n in sorted(os.listdir(root))
             if os.path.isdir(os.path.join(root, n))
             and n not in F.FOLDERS and not n.startswith((".", "_"))
             and not F.is_source_tree(os.path.join(root, n))]
    for n in extra:
        bad(f"{NAMES[10]} — {n!r} is a folder nobody declared; either add it to the contract or file its contents")
    if not extra:
        ok(f"{NAMES[10]} ({len(F.FOLDERS)} folders)")

    # 11 — one department, one executive. Two is worse than none: with two, each assumes the other did it.
    m11 = 0
    for d in depts:
        name = d.get("name") or d["_name"]
        execs = [r["_name"] for r in roles if (r.get("department") or "") == name
                 and (r.get("kind") or "executive") == "executive"]
        if not execs:
            bad(f"{NAMES[11]} — {name!r} has no executive; every question about it lands back on you")
            m11 += 1
        elif len(execs) > 1:
            bad(f"{NAMES[11]} — {name!r} has {len(execs)} executives ({', '.join(execs)}); "
                f"with two, each will assume the other answered")
            m11 += 1
        for k in ("owns", "succeeds_when"):
            if not d.get(k):
                bad(f"{NAMES[11]} — department {name!r} has no {k!r}; "
                    f"a department that cannot say what it owns or when it is working is a label")
                m11 += 1
    if depts and not m11:
        ok(f"{NAMES[11]} ({len(depts)} departments)")
    if not depts:
        bad(f"{NAMES[11]} — there are no departments; run the workflow 'Setting Up a Department'")

    # 12 — a role pointing at a department that was renamed or deleted is the commonest way this drifts
    m12 = [(r["_name"], r.get("department")) for r in roles
           if r.get("department") and r.get("department") not in dept_names]
    known = {(r.get("name") or r["_name"]) for r in roles}
    for r in roles:
        if (r.get("kind") or "executive") == "specialist":
            boss = (r.get("reports_to") or "").strip()
            if boss not in known:
                bad(f"{NAMES[12]} — specialist {r['_name']!r} reports to {boss or 'nobody'}, "
                    f"and there is no role by that name; a specialist nobody owns is an agent nobody reads")
    for n, d in m12:
        bad(f"{NAMES[12]} — {n!r} leads {d!r}, and there is no department note by that name")
    if not m12:
        e = sum(1 for r in roles if r.get("department") and (r.get("kind") or "executive") == "executive")
        sp = sum(1 for r in roles if (r.get("kind") or "executive") == "specialist")
        ok(f"{NAMES[12]} ({e} executives, {sp} specialist{'' if sp == 1 else 's'}, "
           f"{len(roles) - e - sp} across all departments)")

    # 13 — blank cannot be told apart from forgotten, so company-wide is written, not left empty
    m13 = 0
    for w in flows:
        d = w.get("department")
        if not d:
            bad(f"{NAMES[13]} — {w['_name']!r} names no department; write the department, "
                f"or {F.COMPANY_WIDE!r} if it genuinely belongs to no single one")
            m13 += 1
        elif d != F.COMPANY_WIDE and d not in dept_names:
            bad(f"{NAMES[13]} — {w['_name']!r} belongs to {d!r}, and there is no department note by that name")
            m13 += 1
    if flows and not m13:
        ok(f"{NAMES[13]} ({len(flows)} workflows)")

    # 14 — the framework's own source, wherever it was downloaded to, is machinery and not notes.
    # This check exists because the first real install failed ten of the other thirteen for exactly
    # this reason: the download landed in the vault and every README, SKILL and template in it was
    # read as a note the owner had written badly.
    trees = F.source_trees(root)
    if trees:
        where = ", ".join(os.path.relpath(t, root).replace(os.sep, "/") for t in trees)
        ok(f"{NAMES[14]} — excluded the copy at {where}; delete it whenever you like, "
           f"nothing here reads from it")
    else:
        ok(f"{NAMES[14]} (no copy of it inside the vault)")

    # 15 — a project filed under a department that does not exist is invisible on the Projects page
    projects = F.notes(root, F.WORK_DIR)
    m15 = [(p["_name"], p.get("department")) for p in projects
           if p.get("department") and p.get("department") not in dept_names
           and p.get("department") != F.COMPANY_WIDE]
    for n, d in m15:
        bad(f"{NAMES[15]} — project {n!r} names department {d!r}, and there is no note by that name")
    if not m15:
        ok(f"{NAMES[15]} ({len(projects)} in 02 - Work)")

    # 16 — a skill is a capability the site advertises, so it has to say who reaches for it and when.
    # An unowned skill is not a small untidiness: nothing will ever think to use it, and the catalog
    # claims a capability the organisation does not actually have.
    skills = F.skills(root)
    m16 = 0
    for sk in skills:
        if not (sk.get("description") or "").strip():
            bad(f"{NAMES[16]} — skill {sk['_name']!r} has no description; the description is the only "
                f"thing that decides whether it is ever picked up")
            m16 += 1
        want = (sk.get("owner") or "").strip()
        if not want:
            bad(f"{NAMES[16]} — skill {sk['_name']!r} names no owner; add owner: with an executive's "
                f"name or job title, or nothing will reach for it")
            m16 += 1
        elif not F.owner_of(sk, roles):
            bad(f"{NAMES[16]} — skill {sk['_name']!r} is owned by {want!r}, and there is no role by "
                f"that name or title")
            m16 += 1
    if skills and not m16:
        ok(f"{NAMES[16]} ({len(skills)} skills)")
    if not skills:
        bad(f"{NAMES[16]} — there are no skills at all; the install should have put three in "
            f".claude/skills/")

    return PASS, FAIL


if __name__ == "__main__":
    root = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    p, f = run(root)
    for line in f:
        print("  FAILED:", line)
    print(f"\n{len(p)} checks passed, {len(f)} failed")
    if not f:
        print("Everything the vault says about itself is true.")
    try:
        os.makedirs(os.path.join(root, F.PICTURE_DIR), exist_ok=True)
        io.open(os.path.join(root, F.PICTURE_DIR, "check.json"), "w", encoding="utf-8").write(
            json.dumps({"passed": len(p), "failed": len(f), "ran": TODAY.isoformat()}, indent=1))
    except Exception:
        pass
    sys.exit(1 if f else 0)
