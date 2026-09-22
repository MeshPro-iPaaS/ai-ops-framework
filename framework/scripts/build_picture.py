#!/usr/bin/env python3
"""build_picture.py — the one page everyone reads, generated from the notes.

Output: 05 - Operations/picture/index.html  (open it in a browser; it is a plain local file)

It states four things and nothing it cannot prove: what is waiting on a person, who the roles are and
what each may do unsupervised, every workflow with its two marks, and whether the check was green the
last time it ran. Every number here is counted from the notes at build time.
"""
from __future__ import annotations
import io, os, sys, json, html, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import framework as F

E = lambda s: html.escape(str(s), quote=False)
TODAY = datetime.date.today()

CSS = """
:root{--bg:#F4F5F6;--panel:#FFF;--ink:#14181C;--muted:#5B6672;--rule:#DCE0E4;--accent:#1F5B6B;
 --accent-soft:#E4EEF1;--warn:#8A5A12;--warn-soft:#F6EEDD;--good:#2F6B43;
 --fs:"Segoe UI",system-ui,-apple-system,sans-serif;--fm:"Cascadia Mono",ui-monospace,Consolas,monospace}
@media(prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#121518;--panel:#191D21;--ink:#E7EBEE;
 --muted:#96A0AA;--rule:#2A3037;--accent:#6FB6C9;--accent-soft:#1B2C33;--warn:#D8A54A;--warn-soft:#2C2416;--good:#6FBF8B}}
:root[data-theme=dark]{--bg:#121518;--panel:#191D21;--ink:#E7EBEE;--muted:#96A0AA;--rule:#2A3037;
 --accent:#6FB6C9;--accent-soft:#1B2C33;--warn:#D8A54A;--warn-soft:#2C2416;--good:#6FBF8B}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:400 15px/1.55 var(--fs)}
.wrap{max-width:1000px;margin:0 auto;padding-block:40px;padding-left:20px;padding-right:20px}
.top{display:flex;flex-wrap:wrap;gap:12px;align-items:baseline;justify-content:space-between;
 border-bottom:2px solid var(--ink);padding-bottom:14px}
h1{font-size:27px;margin:0;letter-spacing:-.01em}
.stamp{font:400 12px/1 var(--fm);color:var(--muted)}
section{margin-top:38px}
h2{font-size:19px;margin:0 0 4px}
.sub{font-size:13px;color:var(--muted);margin:0 0 16px}
.grid{display:grid;gap:14px;grid-template-columns:repeat(auto-fit,minmax(260px,1fr))}
.card{background:var(--panel);border:1px solid var(--rule);border-radius:4px;padding:16px 18px}
.card h3{margin:0 0 2px;font-size:16px}
.card .who{font:400 12px/1 var(--fm);color:var(--accent);text-transform:uppercase;letter-spacing:.08em}
.card p{margin:10px 0 0;font-size:14px;color:var(--muted)}
.card ul{margin:10px 0 0;padding-left:18px;font-size:13.5px;color:var(--muted)}
.wait{background:var(--warn-soft);border:1px solid var(--warn);border-radius:4px;padding:16px 18px}
.wait ul{margin:10px 0 0;padding-left:0;list-style:none}
.wait li{padding:8px 0;border-top:1px solid var(--rule);font-size:14.5px}
.wait li:first-child{border-top:0}
.wait .why{display:block;font-size:13px;color:var(--muted);margin-top:2px}
.none{color:var(--good);font-size:14.5px;margin:8px 0 0}
table{border-collapse:collapse;width:100%;font-size:14px;min-width:620px}
.tw{overflow-x:auto;background:var(--panel);border:1px solid var(--rule);border-radius:4px;padding:4px 16px}
th{text-align:left;font:500 11px/1.3 var(--fm);letter-spacing:.09em;text-transform:uppercase;
 color:var(--muted);padding:12px 14px 8px 0;border-bottom:1px solid var(--rule)}
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
footer{margin-top:44px;padding-top:14px;border-top:1px solid var(--rule);font-size:12.5px;color:var(--muted)}
@media print{:root{--bg:#fff;--panel:#fff}.tw{overflow:visible}table{min-width:0}}
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


def build(root):
    roles = F.notes(root, F.ROLES_DIR)
    flows = F.notes(root, F.FLOWS_DIR, skip=("Workflows.md",))
    decisions = F.notes(root, F.DECISIONS_DIR)
    everything = F.all_notes(root)

    waiting = []
    for d in decisions:
        if d.get("status") == "proposed":
            age = days(d.get("created"))
            waiting.append((f"Decision not made: {d['_name']}",
                            "drafted and waiting on you" + (f", {age} days ago" if age else "")
                            + " — until you decide it, everything downstream of it is guessing"))
    for d in decisions:
        r = days(d.get("review_on")) if d.get("review_on") else None
        if r is not None and r >= 0:
            waiting.append((f"Decision due for review: {d['_name']}",
                            f"its review date passed {r} days ago — it may no longer be the right call"))
    for w in flows:
        if not w.get("owner"):
            waiting.append((f"Workflow with no owner: {w['_name']}",
                            "nobody is accountable when it goes wrong, so nobody will notice when it does"))
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

    val = sum(1 for w in flows if w.get("doc_status") == "validated")
    run = sum(1 for w in flows if w.get("readiness") == "ready")

    wait_html = ("<ul>" + "".join(
        f"<li><b>{E(t)}</b><span class=why>{E(w)}</span></li>" for t, w in waiting) + "</ul>"
        ) if waiting else '<p class="none">Nothing is waiting on you. Everything written down has an owner and a decision.</p>'

    role_cards = "".join(
        f'<div class="card"><div class="who">{E(r.get("authority","prepare"))}</div>'
        f'<h3>{E(r.get("name", r["_name"]))}</h3>'
        f'<p>{E((r.get("owns") or ["—"])[0])}</p>'
        f'<ul>{"".join(f"<li>{E(g)}</li>" for g in (r.get("green_list") or [])[:3])}</ul></div>'
        for r in roles)

    flow_rows = "".join(
        '<tr><td><b>{}</b><br><span style="color:var(--muted);font-size:13px">{}</span></td>'
        '<td>{}</td><td>{}</td><td>{}</td></tr>'.format(
            E(w["_name"]), E(clip(F.summary(w["_body"], "Purpose"), 120)), E(w.get("owner") or "—"),
            '<span class="pill good">validated</span>' if w.get("doc_status") == "validated"
            else '<span class="pill">note is a draft</span>',
            {"ready": '<span class="pill good">running</span>',
             "partly": '<span class="pill warn">partly running</span>'}.get(
                w.get("readiness"), '<span class="pill">described only</span>'))
        for w in sorted(flows, key=lambda x: x["_name"]))

    chk = (f'<span class="pill good">{check.get("passed",0)} checks green</span>'
           if check.get("failed") == 0 else
           f'<span class="pill warn">{check.get("failed","?")} failing</span>') if check else \
          '<span class="pill warn">never run</span>'

    page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(os.path.basename(os.path.abspath(root)))} — the picture</title><style>{CSS}</style></head><body>
<div class="wrap">
<div class="top"><h1>What needs you, and how it is running</h1>
<span class="stamp">built {TODAY.isoformat()} · {chk}</span></div>

<section><h2>Waiting on you</h2>
<p class="sub">Named, not counted — with what each one waits for and what happens if nothing is done.</p>
<div class="wait">{wait_html}</div></section>

<section><h2>Who can act, and how far</h2>
<p class="sub">{len(roles)} roles, compiled from their notes. Everything off these lists is prepared and handed to a person.</p>
<div class="grid">{role_cards}</div></section>

<section><h2>Workflows</h2>
<p class="sub">Two marks each. <b>Validated</b> means a person walked a real case through the note. <b>Running</b>
means the workflow itself works end to end. They go wrong separately.</p>
<div class="stats" style="margin-bottom:14px">
  <div class="stat"><b>{len(flows)}</b><span>written down</span></div>
  <div class="stat"><b>{val}</b><span>validated against a real case</span></div>
  <div class="stat"><b>{run}</b><span>running end to end</span></div>
  <div class="stat"><b>{len(everything)}</b><span>notes in the vault</span></div>
</div>
<div class="tw"><table><thead><tr><th>Workflow</th><th>Owner</th><th>The note</th><th>The workflow</th></tr></thead>
<tbody>{flow_rows}</tbody></table></div></section>

<footer>Generated from the notes by <code>build_picture.py</code> — a view, never a second source of truth.
Edit the note that owns the fact and build again. · AI Operations Framework, MeshPro × Expectus</footer>
</div></body></html>"""
    os.makedirs(os.path.join(root, F.PICTURE_DIR), exist_ok=True)
    io.open(os.path.join(root, F.PICTURE_DIR, "index.html"), "w", encoding="utf-8", newline="\n").write(page)
    return len(waiting), len(roles), len(flows)


if __name__ == "__main__":
    root = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    w, r, f = build(root)
    print(f"picture rebuilt — {w} thing{'' if w==1 else 's'} waiting on a person, {r} roles, {f} workflows")
