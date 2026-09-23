#!/usr/bin/env python3
"""build_picture.py — the site everyone reads, generated from the notes.

Output: 05 - Operations/picture/
    ai_operations.html   the dashboard — what is waiting on a person, and whether the check is green
    agents.html          the executive hierarchy, redrawn from the role notes every build
    workflows.html       every workflow, in department blocks
    projects.html        what is actually being worked on

Four pages, one stylesheet, one nav. Nothing here is a second source of truth: every number is counted
from the notes at build time, and the hierarchy is read from each role's `reports_to` and `department`,
so adding a department and an executive redraws it with no diagram to maintain.
"""
from __future__ import annotations
import io, os, sys, json, html, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import framework as F

E = lambda s: html.escape(str(s), quote=False)
TODAY = datetime.date.today()

PAGES = [("ai_operations.html", "Dashboard"),
         ("agents.html", "Agent organization"),
         ("workflows.html", "Workflows"),
         ("projects.html", "Projects")]

CSS = """
:root{--bg:#F4F5F6;--panel:#FFF;--ink:#14181C;--muted:#5B6672;--rule:#DCE0E4;--accent:#5B4FD1;
 --accent-soft:#ECEAFB;--warn:#8A5A12;--warn-soft:#F6EEDD;--good:#2F6B43;
 --fs:"Segoe UI",system-ui,-apple-system,sans-serif;--fm:"Cascadia Mono",ui-monospace,Consolas,monospace}
@media(prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#121518;--panel:#191D21;--ink:#E7EBEE;
 --muted:#96A0AA;--rule:#2A3037;--accent:#A59CFF;--accent-soft:#232043;--warn:#D8A54A;--warn-soft:#2C2416;--good:#6FBF8B}}
:root[data-theme=dark]{--bg:#121518;--panel:#191D21;--ink:#E7EBEE;--muted:#96A0AA;--rule:#2A3037;
 --accent:#A59CFF;--accent-soft:#232043;--warn:#D8A54A;--warn-soft:#2C2416;--good:#6FBF8B}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:400 15px/1.55 var(--fs)}
a{color:var(--accent);text-decoration:none}
a:hover{text-decoration:underline}
.wrap{max-width:1040px;margin:0 auto;padding:0 20px 56px}
nav{border-bottom:1px solid var(--rule);background:var(--panel);position:sticky;top:0;z-index:5}
nav .in{max-width:1040px;margin:0 auto;padding:0 20px;display:flex;flex-wrap:wrap;gap:2px;align-items:center}
nav a{display:inline-block;padding:14px 14px 11px;font-size:14px;text-decoration:none;color:var(--muted);
 border-bottom:3px solid transparent}
nav a:hover{color:var(--ink)}
nav a.on{color:var(--ink);border-bottom-color:var(--accent);font-weight:600}
.top{display:flex;flex-wrap:wrap;gap:12px;align-items:baseline;justify-content:space-between;
 border-bottom:2px solid var(--ink);padding:36px 0 14px}
h1{font-size:26px;margin:0;letter-spacing:-.01em}
.stamp{font:400 12px/1 var(--fm);color:var(--muted)}
section{margin-top:34px}
h2{font-size:19px;margin:0 0 4px}
.sub{font-size:13px;color:var(--muted);margin:0 0 16px;max-width:70ch}
.grid{display:grid;gap:14px;grid-template-columns:repeat(auto-fit,minmax(260px,1fr))}
.card{background:var(--panel);border:1px solid var(--rule);border-radius:4px;padding:16px 18px}
.card h3{margin:0 0 2px;font-size:16px}
.card .who{font:400 12px/1 var(--fm);color:var(--accent);text-transform:uppercase;letter-spacing:.08em}
.card p{margin:10px 0 0;font-size:14px;color:var(--muted)}
.card ul{margin:10px 0 0;padding-left:18px;font-size:13.5px;color:var(--muted)}
.wait{background:var(--warn-soft);border:1px solid var(--warn);border-radius:4px;padding:16px 18px}
.wait ul{margin:0;padding-left:0;list-style:none}
.wait li{padding:9px 0;border-top:1px solid var(--rule);font-size:14.5px}
.wait li:first-child{border-top:0}
.wait .why{display:block;font-size:13px;color:var(--muted);margin-top:2px}
.none{color:var(--good);font-size:14.5px;margin:0}
table{border-collapse:collapse;width:100%;font-size:14px;min-width:620px}
.tw{overflow-x:auto;background:var(--panel);border:1px solid var(--rule);border-radius:4px;padding:4px 16px}
th{text-align:left;font:500 11px/1.3 var(--fm);letter-spacing:.09em;text-transform:uppercase;
 white-space:nowrap;color:var(--muted);padding:12px 14px 8px 0;border-bottom:1px solid var(--rule)}
td{padding:11px 14px 11px 0;border-bottom:1px solid var(--rule);vertical-align:top}
tr:last-child td{border-bottom:0}
.pill{display:inline-block;font:500 11.5px/1 var(--fm);padding:4px 8px;border-radius:3px;
 background:var(--accent-soft);color:var(--accent);white-space:nowrap}
.pill.warn{background:var(--warn-soft);color:var(--warn)}
.pill.good{background:transparent;color:var(--good);border:1px solid var(--good)}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:1px;background:var(--rule);
 border:1px solid var(--rule);border-radius:4px;overflow:hidden}
.stat{background:var(--panel);padding:14px 16px}
.stat b{display:block;font-size:26px;line-height:1;font-variant-numeric:tabular-nums}
.stat span{display:block;margin-top:6px;font-size:12.5px;color:var(--muted)}
.deptblock{margin-top:26px}
.deptblock .hd{display:flex;flex-wrap:wrap;gap:10px;align-items:baseline;justify-content:space-between;
 border-bottom:1px solid var(--rule);padding-bottom:7px;margin-bottom:12px}
.deptblock .hd h3{margin:0;font-size:17px}
.deptblock .hd .led{font:400 12px/1 var(--fm);color:var(--accent);text-transform:uppercase;letter-spacing:.07em}
.empty{color:var(--muted);font-size:14px;font-style:italic;padding:6px 0}
.chart{background:var(--panel);border:1px solid var(--rule);border-radius:4px;padding:22px 18px;overflow-x:auto}
.chart svg{display:block;margin:0 auto}
.legend{margin-top:10px;font-size:12.5px;color:var(--muted);text-align:center}
footer{margin-top:44px;padding-top:14px;border-top:1px solid var(--rule);font-size:12.5px;color:var(--muted)}
@media print{:root{--bg:#fff;--panel:#fff}nav{display:none}.tw{overflow:visible}table{min-width:0}}
"""


def clip(s, n):
    """Cut on a word boundary — a purpose that ends mid-word reads as a bug, and this page is the product."""
    s = (s or "").strip()
    if len(s) <= n:
        return s or "—"
    return s[:n].rsplit(" ", 1)[0].rstrip(" ,.;:—-") + "…"


def days(d):
    try:
        return (TODAY - datetime.date.fromisoformat(str(d)[:10])).days
    except Exception:
        return None


def nav(active):
    links = "".join(f'<a href="{f}"{" class=on" if f == active else ""}>{E(t)}</a>' for f, t in PAGES)
    return f'<nav><div class="in">{links}</div></nav>'


def shell(title, active, head, body, stamp):
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)}</title><style>{CSS}</style></head><body>
{nav(active)}
<div class="wrap">
<div class="top"><h1>{E(head)}</h1><span class="stamp">{stamp}</span></div>
{body}
<footer>Generated from the notes by <code>build_picture.py</code> — a view, never a second source of
truth. Edit the note that owns the fact and build again. · AI Operations Framework, MeshPro × Expectus</footer>
</div></body></html>"""


def dept_key(d):
    """Head Office first, AI Operations second, then whatever the owner added, alphabetically.
    A department note can set `order:` to place itself."""
    name = d.get("name") or d["_name"]
    default = {"Head Office": 10, "AI Operations": 20}.get(name, 50)
    try:
        o = int(d.get("order") or default)
    except Exception:
        o = default
    return (o, name.lower())


# ---------------------------------------------------------------- the hierarchy
BW, BH, HGAP, VGAP = 178, 58, 22, 48


def tree_svg(roles):
    """Lay the executives out from what each role says about itself.

    The shape comes from `reports_to`; anything reporting to nobody hangs off you. There is no diagram
    to maintain — add a department with an executive and the next build draws it.
    """
    named = {}
    for r in roles:
        named[(r.get("name") or r["_name"]).strip()] = r
    ROOT = "You"
    kids, seen = {}, set()
    for n, r in sorted(named.items()):
        p = (r.get("reports_to") or "").strip()
        kids.setdefault(p if (p in named and p != n) else ROOT, []).append(n)

    pos, cursor, depth_max = {}, [0], [0]

    def place(node, depth):
        if node in seen:                      # a role that reports to something reporting to it
            return None
        seen.add(node)
        depth_max[0] = max(depth_max[0], depth)
        ch = [c for c in kids.get(node, []) if c not in seen]
        if not ch:
            x = cursor[0]
            cursor[0] += BW + HGAP
        else:
            xs = [place(c, depth + 1) for c in ch]
            xs = [x for x in xs if x is not None]
            x = (min(xs) + max(xs)) / 2 if xs else cursor[0]
            if not xs:
                cursor[0] += BW + HGAP
        pos[node] = (x, depth * (BH + VGAP))
        return x

    place(ROOT, 0)
    for n in named:                            # anything a cycle left out still gets drawn
        if n not in pos:
            pos[n] = (cursor[0], (depth_max[0] + 1) * (BH + VGAP))
            cursor[0] += BW + HGAP
            depth_max[0] += 0

    W = max(cursor[0] - HGAP, BW)
    H = (depth_max[0] + 1) * BH + depth_max[0] * VGAP

    out = []
    for parent, ch in kids.items():
        if parent not in pos:
            continue
        px, py = pos[parent]
        drawn = [c for c in ch if c in pos]
        if not drawn:
            continue
        cy = py + BH
        mid = cy + VGAP / 2
        out.append(f'<path d="M{px + BW/2:.1f} {cy} V{mid:.1f}" stroke="var(--rule)" fill="none" stroke-width="1.5"/>')
        xs = [pos[c][0] + BW / 2 for c in drawn]
        if len(drawn) > 1:
            out.append(f'<path d="M{min(xs):.1f} {mid:.1f} H{max(xs):.1f}" stroke="var(--rule)" '
                       f'fill="none" stroke-width="1.5"/>')
        for c in drawn:
            cxx, cyy = pos[c]
            out.append(f'<path d="M{cxx + BW/2:.1f} {mid:.1f} V{cyy:.1f}" stroke="var(--rule)" '
                       f'fill="none" stroke-width="1.5"/>')

    for node, (x, y) in pos.items():
        if node == ROOT:
            out.append(f'<rect x="{x:.1f}" y="{y}" width="{BW}" height="{BH}" rx="6" fill="var(--ink)"/>')
            out.append(f'<text x="{x + BW/2:.1f}" y="{y + BH/2 + 5}" text-anchor="middle" '
                       f'font-family="var(--fs)" font-size="15" font-weight="600" fill="var(--panel)">You</text>')
            continue
        r = named[node]
        sub = r.get("department") or "across all departments"
        out.append(f'<rect x="{x:.1f}" y="{y}" width="{BW}" height="{BH}" rx="6" fill="var(--panel)" '
                   f'stroke="var(--accent)" stroke-width="1.4"/>')
        out.append(f'<text x="{x + BW/2:.1f}" y="{y + 24}" text-anchor="middle" font-family="var(--fs)" '
                   f'font-size="14.5" font-weight="600" fill="var(--ink)">{E(clip(node, 22))}</text>')
        out.append(f'<text x="{x + BW/2:.1f}" y="{y + 42}" text-anchor="middle" font-family="var(--fm)" '
                   f'font-size="11" fill="var(--muted)">{E(clip(sub, 26))}</text>')

    return (f'<svg viewBox="0 0 {W:.0f} {H:.0f}" width="100%" style="max-width:{W:.0f}px;height:auto" '
            f'role="img" aria-label="The executive hierarchy">' + "".join(out) + "</svg>")


# ---------------------------------------------------------------- the build
def build(root):
    roles = F.notes(root, F.ROLES_DIR)
    depts = sorted(F.notes(root, F.DEPTS_DIR), key=dept_key)
    flows = F.notes(root, F.FLOWS_DIR, skip=("Workflows.md",))
    projects = [n for n in F.notes(root, F.WORK_DIR) if n.get("type") != "note" or n.get("outcome")]
    decisions = F.notes(root, F.DECISIONS_DIR)
    everything = F.all_notes(root)
    dept_names = [(d.get("name") or d["_name"]) for d in depts]

    def execs_of(name):
        return [r for r in roles if (r.get("department") or "") == name]

    def flows_of(name):
        return sorted([w for w in flows if (w.get("department") or "") == name], key=lambda x: x["_name"])

    # ---- what is waiting on a person
    waiting = []
    for d in decisions:
        if d.get("status") == "proposed":
            age = days(d.get("created"))
            waiting.append((f"Decision not made: {d['_name']}",
                            "drafted and waiting on you" + (f", {age} days ago" if age else "")
                            + " — until you decide it, everything downstream of it is guessing"))
        r = days(d.get("review_on")) if d.get("review_on") else None
        if r is not None and r >= 0:
            waiting.append((f"Decision due for review: {d['_name']}",
                            f"its review date passed {r} days ago — it may no longer be the right call"))
    for d in depts:
        name = d.get("name") or d["_name"]
        if not execs_of(name):
            waiting.append((f"Department with no executive: {name}",
                            "nobody answers for it, so every question about it comes back to you"))
        if not flows_of(name):
            waiting.append((f"Department with no workflow: {name}",
                            "it is a name until somebody writes down how one piece of its work happens"))
    for w in flows:
        if not w.get("owner"):
            waiting.append((f"Workflow with no owner: {w['_name']}",
                            "nobody is accountable when it goes wrong, so nobody will notice when it does"))
    for p in projects:
        if not p.get("owner"):
            waiting.append((f"Project with no owner: {p['_name']}",
                            "work nobody has agreed to do tends to stay work nobody does"))
        late = days(p.get("due")) if p.get("due") else None
        if late is not None and late > 0 and p.get("status") not in ("done", "archived"):
            waiting.append((f"Project past its date: {p['_name']}",
                            f"due {late} days ago and still open — move the date or move the work"))
    for n in everything:
        if n.get("status") == "draft" and n.get("type") != "workflow":
            age = days(n.get("updated") or n.get("created"))
            if age is not None and age > 21:
                waiting.append((f"Stale draft: {n['_name']}",
                                f"untouched for {age} days — agents read status as fact, so it is "
                                f"misleading rather than merely old"))

    check = {}
    cp = os.path.join(root, F.PICTURE_DIR, "check.json")
    if os.path.exists(cp):
        try:
            check = json.loads(F.read(cp))
        except Exception:
            check = {}
    chk = (f'<span class="pill good">{check.get("passed",0)} checks green</span>'
           if check.get("failed") == 0 else
           f'<span class="pill warn">{check.get("failed","?")} failing</span>') if check else \
          '<span class="pill warn">never run</span>'
    stamp = f"built {TODAY.isoformat()} · {chk}"

    val = sum(1 for w in flows if w.get("doc_status") == "validated")
    run = sum(1 for w in flows if w.get("readiness") == "ready")

    os.makedirs(os.path.join(root, F.PICTURE_DIR), exist_ok=True)
    write = lambda f, s: io.open(os.path.join(root, F.PICTURE_DIR, f), "w",
                                 encoding="utf-8", newline="\n").write(s)

    # ---- 1. the dashboard
    wait_html = ("<ul>" + "".join(
        f"<li><b>{E(t)}</b><span class=why>{E(w)}</span></li>" for t, w in waiting) + "</ul>"
        ) if waiting else ('<p class="none">Nothing is waiting on you. Every department has an executive '
                           'and a workflow, everything written down has an owner, and no decision is sitting unmade.</p>')
    dash = f"""
<section><h2>Waiting on you</h2>
<p class="sub">Named, not counted — with what each one waits for and what happens if nothing is done.</p>
<div class="wait">{wait_html}</div></section>

<section><h2>Where it stands</h2>
<p class="sub">Counted from the notes at build time. Nothing here was typed in.</p>
<div class="stats">
  <div class="stat"><b>{len(depts)}</b><span>department{"" if len(depts)==1 else "s"}</span></div>
  <div class="stat"><b>{len(roles)}</b><span>executives</span></div>
  <div class="stat"><b>{len(flows)}</b><span>workflows written down</span></div>
  <div class="stat"><b>{run}</b><span>running end to end</span></div>
  <div class="stat"><b>{len(projects)}</b><span>project{"" if len(projects)==1 else "s"}</span></div>
  <div class="stat"><b>{len(everything)}</b><span>notes in the vault</span></div>
</div></section>

<section><h2>The rest of the site</h2>
<div class="grid">
  <div class="card"><h3><a href="agents.html">Agent organization</a></h3>
    <p>Who answers for what, drawn from the role notes. Add a department with an executive and it redraws itself.</p></div>
  <div class="card"><h3><a href="workflows.html">Workflows</a></h3>
    <p>Every workflow in its department block, with two marks each: is the note true, and does it run.</p></div>
  <div class="card"><h3><a href="projects.html">Projects</a></h3>
    <p>What is actually being worked on, who owns it, and what is late.</p></div>
</div></section>"""
    write(F.PAGE_DASH, shell("Dashboard — the picture", F.PAGE_DASH,
                             "What needs you, and how it is running", dash, stamp))

    # ---- 2. the organization
    role_cards = ""
    for d in depts:
        name = d.get("name") or d["_name"]
        mine = execs_of(name)
        lead = ", ".join(E(r.get("name", r["_name"])) for r in mine) if mine else \
            '<span style="color:var(--warn)">no executive yet</span>'
        cards = "".join(
            f'<div class="card"><div class="who">{E(r.get("authority","prepare"))}'
            f'{" · " + E(r.get("title")) if r.get("title") and r.get("title") != r.get("name") else ""}</div>'
            f'<h3>{E(r.get("name", r["_name"]))}</h3>'
            f'<p>{E((r.get("owns") or ["—"])[0])}</p>'
            f'<ul>{"".join(f"<li>{E(g)}</li>" for g in (r.get("green_list") or [])[:3])}</ul>'
            f'<p style="margin-top:12px"><b>Stops at:</b> {E((r.get("not_owned") or ["—"])[0])}</p></div>'
            for r in mine)
        role_cards += (f'<div class="deptblock"><div class="hd"><h3>{E(name)}</h3>'
                       f'<span class="led">{lead}</span></div>'
                       f'<p class="sub">{E(d.get("succeeds_when") or "No test of whether it is working — add succeeds_when:")}</p>'
                       f'<div class="grid">{cards or "<p class=empty>Nobody answers for this department yet.</p>"}</div></div>')
    spanning = [r for r in roles if not r.get("department")]
    if spanning:
        cards = "".join(
            f'<div class="card"><div class="who">{E(r.get("authority","prepare"))} · across all</div>'
            f'<h3>{E(r.get("name", r["_name"]))}</h3>'
            f'<p>{E((r.get("owns") or ["—"])[0])}</p></div>' for r in spanning)
        role_cards += (f'<div class="deptblock"><div class="hd"><h3>Across every department</h3>'
                       f'<span class="led">not tied to one</span></div><div class="grid">{cards}</div></div>')

    org = f"""
<section><h2>The hierarchy</h2>
<p class="sub">Read from each role's own note — who it reports to, and which department it answers for.
There is no diagram to maintain: add a department and an executive, rebuild, and it appears here.</p>
<div class="chart">{tree_svg(roles)}</div>
<p class="legend">{len(roles)} executives · {len(depts)} departments · one executive per department</p></section>

<section><h2>What each of them may do</h2>
<p class="sub">Everything off these lists is prepared and handed to a person. The line that matters most
is the last one on each card — where that executive stops.</p>
{role_cards}</section>"""
    write(F.PAGE_AGENTS, shell("Agent organization", F.PAGE_AGENTS, "Who answers for what", org, stamp))

    # ---- 3. workflows, in department blocks
    def wf_table(rows):
        body = "".join(
            '<tr><td><b>{}</b><br><span style="color:var(--muted);font-size:13px">{}</span></td>'
            '<td>{}</td><td>{}</td><td>{}</td></tr>'.format(
                E(w["_name"]), E(clip(F.summary(w["_body"], "Purpose"), 120)), E(w.get("owner") or "—"),
                '<span class="pill good">validated</span>' if w.get("doc_status") == "validated"
                else '<span class="pill">note is a draft</span>',
                {"ready": '<span class="pill good">running</span>',
                 "partly": '<span class="pill warn">partly running</span>'}.get(
                    w.get("readiness"), '<span class="pill">described only</span>'))
            for w in rows)
        return ('<div class="tw"><table><thead><tr><th>Workflow</th><th>Owner</th><th>The note</th>'
                f'<th>The workflow</th></tr></thead><tbody>{body}</tbody></table></div>')

    blocks, placed = "", set()
    for d in depts:
        name = d.get("name") or d["_name"]
        mine = flows_of(name)
        placed.update(id(w) for w in mine)
        lead = ", ".join(E(r.get("name", r["_name"])) for r in execs_of(name)) or "no executive yet"
        r = sum(1 for w in mine if w.get("readiness") == "ready")
        blocks += (f'<div class="deptblock"><div class="hd"><h3>{E(name)}</h3>'
                   f'<span class="led">{lead} · {len(mine)} workflow{"" if len(mine)==1 else "s"}'
                   f'{f", {r} running" if mine else ""}</span></div>'
                   + (wf_table(mine) if mine else
                      '<p class="empty">Nothing written down yet — this department is a name until one is.</p>')
                   + "</div>")
    rest = sorted([w for w in flows if id(w) not in placed], key=lambda x: x["_name"])
    if rest:
        company = [w for w in rest if (w.get("department") or "") == F.COMPANY_WIDE]
        strays = [w for w in rest if w not in company]
        if company:
            blocks += ('<div class="deptblock"><div class="hd"><h3>Company-wide</h3>'
                       '<span class="led">belongs to no single department</span></div>'
                       + wf_table(company) + "</div>")
        if strays:
            blocks += ('<div class="deptblock"><div class="hd"><h3>Department not recognised</h3>'
                       '<span class="led">fix the department: field, or write the note</span></div>'
                       + wf_table(strays) + "</div>")

    wf = f"""
<section><h2>Two marks, not one</h2>
<p class="sub"><b>Validated</b> means a person walked a real case through the note. <b>Running</b> means
the workflow itself works end to end. They go wrong separately, which is why there are two of them.</p>
<div class="stats">
  <div class="stat"><b>{len(flows)}</b><span>written down</span></div>
  <div class="stat"><b>{val}</b><span>validated against a real case</span></div>
  <div class="stat"><b>{run}</b><span>running end to end</span></div>
  <div class="stat"><b>{len(depts)}</b><span>departments</span></div>
</div></section>
<section><h2>By department</h2>{blocks}</section>"""
    write(F.PAGE_FLOWS, shell("Workflows", F.PAGE_FLOWS, "How the work actually happens", wf, stamp))

    # ---- 4. projects
    def pj_table(rows):
        body = ""
        for p in rows:
            late = days(p.get("due")) if p.get("due") else None
            when = (f'<span class="pill warn">{late} days over</span>' if late is not None and late > 0
                    else (E(p.get("due")) if p.get("due") else "—"))
            body += ('<tr><td><b>{}</b><br><span style="color:var(--muted);font-size:13px">{}</span></td>'
                     '<td>{}</td><td>{}</td><td>{}</td></tr>').format(
                E(p["_name"]), E(clip(p.get("outcome") or F.summary(p["_body"], "Outcome"), 110)),
                E(p.get("owner") or "—"), E(p.get("status") or "—"), when)
        return ('<div class="tw"><table><thead><tr><th>Project</th><th>Owner</th><th>Status</th>'
                f'<th>Due</th></tr></thead><tbody>{body}</tbody></table></div>')

    pblocks, pplaced = "", set()
    for d in depts:
        name = d.get("name") or d["_name"]
        mine = sorted([p for p in projects if (p.get("department") or "") == name], key=lambda x: x["_name"])
        pplaced.update(id(p) for p in mine)
        if mine:
            pblocks += (f'<div class="deptblock"><div class="hd"><h3>{E(name)}</h3>'
                        f'<span class="led">{len(mine)} project{"" if len(mine)==1 else "s"}</span></div>'
                        + pj_table(mine) + "</div>")
    loose = sorted([p for p in projects if id(p) not in pplaced], key=lambda x: x["_name"])
    if loose:
        pblocks += ('<div class="deptblock"><div class="hd"><h3>No department named</h3>'
                    '<span class="led">add department: to the note</span></div>' + pj_table(loose) + "</div>")

    pj = f"""
<section><h2>What is actually being worked on</h2>
<p class="sub">Read from <code>02 - Work</code>. A project here is a piece of work with an outcome, an
owner and a way to tell when it is finished — not a list of activities.</p>
{pblocks or '<p class="empty">No projects yet. Ask for <b>Setting Up a Project</b> and the first one gets written properly.</p>'}
</section>"""
    write(F.PAGE_PROJECTS, shell("Projects", F.PAGE_PROJECTS, "The work in flight", pj, stamp))

    # the page used to be index.html; leave no stale copy for somebody to open by mistake
    stale = os.path.join(root, F.PICTURE_DIR, "index.html")
    if os.path.exists(stale):
        os.remove(stale)

    return len(waiting), len(roles), len(flows), len(depts), len(projects)


if __name__ == "__main__":
    root = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    w, r, f, d, p = build(root)
    print(f"site rebuilt — {len(PAGES)} pages · {w} thing{'' if w==1 else 's'} waiting on a person, "
          f"{d} department{'' if d==1 else 's'}, {r} executives, {f} workflows, {p} projects")
    print(f"   {F.PICTURE.replace(os.sep, '/')}  (inside your folder)")
