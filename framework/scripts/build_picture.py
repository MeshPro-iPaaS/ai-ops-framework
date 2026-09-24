#!/usr/bin/env python3
"""build_picture.py — the site everyone reads, generated from the notes.

Output: 05 - Operations/picture/
    ai_operations.html   the dashboard — what is waiting on a person, and whether the check is green
    agents.html          the executive hierarchy, redrawn from the role notes every build
    skills.html          the skill catalog, read from .claude/skills and grouped by who reaches for it
    workflows.html       every workflow, in department blocks; click one to see its steps drawn
    projects.html        what is actually being worked on

Five pages, one stylesheet, one nav. Nothing here is a second source of truth: every number is counted
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
         ("skills.html", "Skills"),
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
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(112px,1fr));gap:1px;background:var(--rule);
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
.skill{background:var(--panel);border:1px solid var(--rule);border-radius:4px;padding:16px 18px}
.skill h3{margin:0;font-size:16px}
.skill .slug{font:400 11.5px/1 var(--fm);color:var(--muted);margin-top:4px;display:block}
.skill p{margin:10px 0 0;font-size:13.5px;color:var(--muted)}
.skill .stop{margin-top:11px;padding-top:9px;border-top:1px solid var(--rule);font-size:13px;color:var(--muted)}
.skill.orphan{border-style:dashed}
tr[data-flow]{cursor:pointer}
tr[data-flow] td:first-child b{position:relative;padding-left:16px;display:inline-block}
tr[data-flow] td:first-child b::before{content:"";position:absolute;left:0;top:5px;width:0;height:0;
 border:5px solid transparent;border-left-color:var(--accent);transition:transform .12s;
 transform-origin:3px 5px}
tr[data-flow].open td:first-child b::before{transform:rotate(90deg)}
tr[data-flow]:hover td{background:var(--accent-soft)}
tr.detail>td{padding:0 0 18px;border-bottom:1px solid var(--rule)}
.flowbox{padding:4px 0 0}
ol.flow{list-style:none;margin:6px 0 0;padding:0 0 0 4px}
ol.flow li{position:relative;padding:0 0 16px 44px;min-height:30px}
ol.flow li::before{content:"";position:absolute;left:13px;top:26px;bottom:-4px;width:2px;background:var(--rule)}
ol.flow li:last-child::before{display:none}
.fnum{position:absolute;left:0;top:0;width:28px;height:28px;border-radius:50%;display:flex;
 align-items:center;justify-content:center;font:600 12.5px/1 var(--fm);background:var(--accent-soft);
 color:var(--accent);border:1px solid var(--accent)}
li.person .fnum{background:transparent;color:var(--muted);border-color:var(--muted)}
li.done .fnum{background:transparent;color:var(--good);border-color:var(--good)}
.fbody b{display:block;font-size:14.5px;line-height:1.35}
.fwho{display:inline-block;margin-top:3px;font:400 11.5px/1 var(--fm);text-transform:uppercase;
 letter-spacing:.07em;color:var(--accent)}
li.person .fwho{color:var(--muted)}
.fio{display:block;margin-top:4px;font-size:13px;color:var(--muted)}
.flowlegend{margin:14px 0 0;font-size:12.5px;color:var(--muted)}
footer{margin-top:44px;padding-top:14px;border-top:1px solid var(--rule);font-size:12.5px;color:var(--muted)}
@media print{:root{--bg:#fff;--panel:#fff}nav{display:none}.tw{overflow:visible}table{min-width:0}
 tr.detail>td{display:table-cell}[hidden]{display:revert!important}}
"""


def plain(s):
    """Markdown code ticks are punctuation in the note and noise on the page."""
    return (s or "").replace("`", "")


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


WHERE = ""          # set at build time: the absolute path of this vault's dashboard


def shell(title, active, head, body, stamp):
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)}</title><style>{CSS}</style></head><body>
{nav(active)}
<div class="wrap">
<div class="top"><h1>{E(head)}</h1><span class="stamp">{stamp}</span></div>
{body}
<footer>Generated from the notes by <code>build_picture.py</code> — a view, never a second source of
truth. Edit the note that owns the fact and build again. · AI Operations Framework, MeshPro × Expectus
<br><span style="opacity:.8">This page is a file on your own computer: <code>{E(WHERE)}</code></span></footer>
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
# The chart is drawn by the page, from a block of data the page carries. That is deliberate: plenty of
# machines cannot run these generators at all, and on those a session has to keep the site true by hand.
# Rewriting five lines of JSON is something a session does reliably; recomputing SVG coordinates is not.
ORG_JS = """
(function(){
  var el=document.getElementById('org-data'); if(!el) return;
  var data=JSON.parse(el.textContent||el.innerText), ROOT='You';
  var BW=188,BH=58,HG=22,VG=48;
  var named={}; data.forEach(function(r){ if(r&&r.name) named[r.name]=r; });
  var kids={};
  Object.keys(named).sort().forEach(function(n){
    var p=(named[n].reports_to||'').toString().trim();
    var key=(named[p]&&p!==n)?p:ROOT;
    (kids[key]=kids[key]||[]).push(n);
  });
  var pos={},seen={},cursor=0,maxd=0;
  function place(node,d){
    if(seen[node]) return null;
    seen[node]=1; if(d>maxd) maxd=d;
    var ch=(kids[node]||[]).filter(function(c){return !seen[c];}), x;
    if(!ch.length){ x=cursor; cursor+=BW+HG; }
    else{
      var xs=ch.map(function(c){return place(c,d+1);}).filter(function(v){return v!==null;});
      if(xs.length){ x=(Math.min.apply(null,xs)+Math.max.apply(null,xs))/2; }
      else { x=cursor; cursor+=BW+HG; }
    }
    pos[node]=[x,d*(BH+VG)];
    return x;
  }
  place(ROOT,0);
  Object.keys(named).forEach(function(n){
    if(!(n in pos)){ pos[n]=[cursor,(maxd+1)*(BH+VG)]; cursor+=BW+HG; }
  });
  var W=Math.max(cursor-HG,BW), H=(maxd+1)*BH+maxd*VG, out=[];
  function line(d){ out.push('<path d="'+d+'" stroke="var(--rule)" fill="none" stroke-width="1.5"/>'); }
  Object.keys(kids).forEach(function(parent){
    if(!(parent in pos)) return;
    var drawn=kids[parent].filter(function(c){return c in pos;});
    if(!drawn.length) return;
    var px=pos[parent][0], py=pos[parent][1], cy=py+BH, mid=cy+VG/2;
    line('M'+(px+BW/2)+' '+cy+' V'+mid);
    var xs=drawn.map(function(c){return pos[c][0]+BW/2;});
    if(drawn.length>1) line('M'+Math.min.apply(null,xs)+' '+mid+' H'+Math.max.apply(null,xs));
    drawn.forEach(function(c){ line('M'+(pos[c][0]+BW/2)+' '+mid+' V'+pos[c][1]); });
  });
  function esc(t){ return String(t).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }
  function clip(t,n){ t=String(t||''); return t.length<=n?t:t.slice(0,n).replace(/\s+\S*$/,'')+'\u2026'; }
  Object.keys(pos).forEach(function(node){
    var x=pos[node][0], y=pos[node][1];
    if(node===ROOT){
      out.push('<rect x="'+x+'" y="'+y+'" width="'+BW+'" height="'+BH+'" rx="6" fill="var(--ink)"/>');
      out.push('<text x="'+(x+BW/2)+'" y="'+(y+BH/2+5)+'" text-anchor="middle" font-size="15" font-weight="600" fill="var(--panel)">You</text>');
      return;
    }
    var r=named[node]||{}, spec=(r.kind==='specialist');
    var sub=spec?(r.department||'specialist'):(r.department||'across all departments');
    out.push('<rect x="'+x+'" y="'+y+'" width="'+BW+'" height="'+BH+'" rx="6" fill="var(--panel)" stroke="'+
             (spec?'var(--rule)':'var(--accent)')+'" stroke-width="'+(spec?1:1.4)+'"'+
             (spec?' stroke-dasharray="4 3"':'')+'/>');
    out.push('<text x="'+(x+BW/2)+'" y="'+(y+24)+'" text-anchor="middle" font-size="14.5" font-weight="600" fill="var(--ink)">'+esc(clip(node,22))+'</text>');
    out.push('<text x="'+(x+BW/2)+'" y="'+(y+42)+'" text-anchor="middle" font-family="var(--fm)" font-size="11" fill="var(--muted)">'+esc(clip(sub,26))+'</text>');
  });
  document.getElementById('org-chart').innerHTML =
    '<svg viewBox="0 0 '+W+' '+H+'" width="100%" style="max-width:'+W+'px;height:auto" '+
    'font-family="var(--fs)" role="img" aria-label="The executive hierarchy">'+out.join('')+'</svg>';
})();
"""


def org_block(roles):
    """The hierarchy as data plus the few lines that draw it.

    A session with no way to run these generators keeps the chart true by editing the JSON between the
    markers below — name, title, department, reports_to — and the page redraws itself. Nothing else on
    the page needs touching, and there are no coordinates to get wrong.
    """
    data = [{"name": (r.get("name") or r["_name"]),
             "title": r.get("title") or "",
             "department": r.get("department") or "",
             "reports_to": r.get("reports_to") or "",
             "authority": r.get("authority") or "",
             "kind": r.get("kind") or "executive"} for r in roles]
    blob = json.dumps(data, ensure_ascii=False, indent=1).replace("</", "<\\/")
    return ('<!-- BEGIN the hierarchy — edit this list and the chart redraws itself -->\n'
            f'<script type="application/json" id="org-data">{blob}</script>\n'
            '<!-- END the hierarchy -->\n'
            '<div id="org-chart"></div>\n'
            f'<script>{ORG_JS}</script>')


# ---------------------------------------------------------------- the step diagrams
# Same bargain as the hierarchy: the page carries the steps as data and draws them itself. The steps
# are read out of each workflow note's own step table, so there is no diagram anywhere that can drift
# away from the table — and a session that cannot run these generators keeps the picture true by
# editing a list, not by computing a layout.
FLOW_JS = """
(function(){
  var el=document.getElementById('flow-data'); if(!el) return;
  var d=JSON.parse(el.textContent||el.innerText), flows=d.flows||{}, people=d.roles||[];
  function esc(t){ return String(t==null?'':t).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }
  function draw(key){
    var f=flows[key];
    if(!f) return '<p class="empty">Nothing to draw for this one.</p>';
    if(!f.steps||!f.steps.length)
      return '<p class="empty">This note has no step table yet, so there is nothing to draw. '+
             'Ask for <b>Writing a Workflow Down</b> and the steps get written properly.</p>';
    var h='<ol class="flow">';
    f.steps.forEach(function(s){
      var agent = people.indexOf(String(s.who||'').trim())>=0;
      h+='<li class="'+(agent?'agent':'person')+'"><span class="fnum">'+esc(s.n)+'</span><div class="fbody"><b>'+esc(s.step)+'</b>';
      if(s.who) h+='<span class="fwho">'+esc(s.who)+'</span>';
      if(s.needs||s.out) h+='<span class="fio">'+esc(s.needs||'—')+'  →  '+esc(s.out||'—')+'</span>';
      h+='</div></li>';
    });
    if(f.done) h+='<li class="done"><span class="fnum">✓</span><div class="fbody"><b>Done means</b><span class="fio">'+esc(f.done)+'</span></div></li>';
    h+='</ol>';
    h+='<p class="flowlegend">Read from this workflow’s own step table. A filled number is a step an '+
       'agent can take; an outlined one waits on a person.'+(f.owner?' Owner: <b>'+esc(f.owner)+'</b>.':'')+'</p>';
    return h;
  }
  function toggle(tr){
    var det=tr.nextElementSibling;
    if(!det||det.className.indexOf('detail')<0) return;
    if(det.hasAttribute('hidden')){
      if(!det.getAttribute('data-drawn')){
        det.getElementsByClassName('flowbox')[0].innerHTML=draw(tr.getAttribute('data-flow'));
        det.setAttribute('data-drawn','1');
      }
      det.removeAttribute('hidden'); tr.className='open'; tr.setAttribute('aria-expanded','true');
    } else {
      det.setAttribute('hidden',''); tr.className=''; tr.setAttribute('aria-expanded','false');
    }
  }
  function rowOf(n){ while(n&&n.nodeName!=='TR'){ n=n.parentNode; } return (n&&n.getAttribute&&n.getAttribute('data-flow'))?n:null; }
  document.addEventListener('click',function(e){ var tr=rowOf(e.target); if(tr) toggle(tr); });
  document.addEventListener('keydown',function(e){
    if(e.key!=='Enter'&&e.key!==' ') return;
    var tr=rowOf(e.target); if(tr){ e.preventDefault(); toggle(tr); }
  });
})();
"""


def flow_block(flows, roles):
    """Every workflow's steps as data, plus the few lines that draw them."""
    data = {"roles": sorted({(r.get("name") or r["_name"]) for r in roles}
                            | {(r.get("title") or "") for r in roles} - {""}),
            "flows": {w["_name"]: {"owner": w.get("owner") or "",
                                   "done": plain(F.summary(w["_body"], "Done means")),
                                   "steps": F.steps(w["_body"])} for w in flows}}
    blob = json.dumps(data, ensure_ascii=False, indent=1).replace("</", "<\\/")
    return ('<!-- BEGIN the steps — edit this list and the step diagrams redraw themselves -->\n'
            f'<script type="application/json" id="flow-data">{blob}</script>\n'
            '<!-- END the steps -->\n'
            f'<script>{FLOW_JS}</script>')


# ---------------------------------------------------------------- the build
def build(root):
    global WHERE
    WHERE = F.dashboard_where(root)[0]
    roles = F.notes(root, F.ROLES_DIR)
    depts = sorted(F.notes(root, F.DEPTS_DIR), key=dept_key)
    flows = F.notes(root, F.FLOWS_DIR, skip=("Workflows.md",))
    projects = [n for n in F.notes(root, F.WORK_DIR) if n.get("type") != "note" or n.get("outcome")]
    decisions = F.notes(root, F.DECISIONS_DIR)
    skills = F.skills(root)
    everything = F.all_notes(root)
    dept_names = [(d.get("name") or d["_name"]) for d in depts]

    def is_exec(r):
        return (r.get("kind") or "executive") == "executive"

    execs = [r for r in roles if is_exec(r)]
    specialists = [r for r in roles if not is_exec(r)]

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
    for sk in skills:
        if not F.owner_of(sk, roles):
            waiting.append((f"Skill nobody reaches for: {sk['_name']}",
                            "no executive owns it" + (f" ({sk.get('owner')} is not a role)" if sk.get("owner")
                                                      else ", so nothing will ever think to use it")))
        if not (sk.get("description") or "").strip():
            waiting.append((f"Skill with no trigger: {sk['_name']}",
                            "its description is what decides whether it gets picked up at all, and it is empty"))
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
  <div class="stat"><b>{len(execs)}</b><span>executive{"" if len(execs)==1 else "s"}</span></div>
  <div class="stat"><b>{len(specialists)}</b><span>specialist{"" if len(specialists)==1 else "s"}</span></div>
  <div class="stat"><b>{len(skills)}</b><span>skill{"" if len(skills)==1 else "s"}</span></div>
  <div class="stat"><b>{len(flows)}</b><span>workflows written down</span></div>
  <div class="stat"><b>{run}</b><span>running end to end</span></div>
  <div class="stat"><b>{len(projects)}</b><span>project{"" if len(projects)==1 else "s"}</span></div>
  <div class="stat"><b>{len(everything)}</b><span>notes in the vault</span></div>
</div></section>

<section><h2>The rest of the site</h2>
<div class="grid">
  <div class="card"><h3><a href="agents.html">Agent organization</a></h3>
    <p>Who answers for what, drawn from the role notes. Add a department with an executive and it redraws itself.</p></div>
  <div class="card"><h3><a href="skills.html">Skills</a></h3>
    <p>What each executive knows how to do, read from the skill folder. Teach one and it appears here.</p></div>
  <div class="card"><h3><a href="workflows.html">Workflows</a></h3>
    <p>Every workflow in its department block, with two marks each. Click one to see its steps drawn.</p></div>
  <div class="card"><h3><a href="projects.html">Projects</a></h3>
    <p>What is actually being worked on, who owns it, and what is late.</p></div>
</div></section>"""
    write(F.PAGE_DASH, shell("Dashboard — the picture", F.PAGE_DASH,
                             "What needs you, and how it is running", dash, stamp))

    # ---- 2. the organization
    role_cards = ""
    for d in depts:
        name = d.get("name") or d["_name"]
        mine = [r for r in execs_of(name) if (r.get("kind") or "executive") == "executive"]
        spec = [r for r in roles if (r.get("department") or "") == name
                and (r.get("kind") or "executive") == "specialist"]
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
        if spec:
            cards += ('<div class="card" style="border-style:dashed">'
                      '<div class="who">specialists</div><h3>Working under ' +
                      E(mine[0].get("name", mine[0]["_name"]) if mine else name) + '</h3><ul>' +
                      "".join(f'<li><b>{E(r.get("name", r["_name"]))}</b> — '
                              f'{E((r.get("owns") or ["—"])[0])}</li>' for r in spec) + '</ul></div>')
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
<div class="chart">{org_block(roles)}</div>
<p class="legend">{len(execs)} executive{"" if len(execs)==1 else "s"} · {len(depts)} department{"" if len(depts)==1 else "s"} ·
{len(specialists)} specialist{"" if len(specialists)==1 else "s"}, shown dashed, each reporting to one of them</p></section>

<section><h2>What each of them may do</h2>
<p class="sub">Everything off these lists is prepared and handed to a person. The line that matters most
is the last one on each card — where that executive stops.</p>
{role_cards}</section>"""
    write(F.PAGE_AGENTS, shell("Agent organization", F.PAGE_AGENTS, "Who answers for what", org, stamp))


    # ---- 3. the skill catalog
    def skill_card(sk, owner):
        stop = sk.get("_stops") or ""
        when = sk.get("_when") or ""
        return (f'<div class="skill{"" if owner else " orphan"}">'
                f'<h3>{E(sk["_name"])}</h3>'
                f'<span class="slug">.claude/skills/{E(sk["_slug"])}/</span>'
                f'<p>{E(clip(plain(sk.get("description") or when) or "No description — nothing will trigger it.", 260))}</p>'
                + (f'<p class="stop"><b>Stops at:</b> {E(clip(plain(stop), 180))}</p>' if stop else "")
                + '</div>')

    owned = {}
    orphans = []
    for sk in sorted(skills, key=lambda x: x["_name"].lower()):
        o = F.owner_of(sk, roles)
        if o:
            owned.setdefault(o.get("name") or o["_name"], []).append(sk)
        else:
            orphans.append(sk)

    sk_blocks = ""
    for d in depts:
        name = d.get("name") or d["_name"]
        here = [(r, owned.get(r.get("name") or r["_name"], [])) for r in execs_of(name)]
        here = [(r, v) for r, v in here if v]
        if not here:
            continue
        cnt = sum(len(v) for _, v in here)
        sk_blocks += (f'<div class="deptblock"><div class="hd"><h3>{E(name)}</h3>'
                      f'<span class="led">{cnt} skill{"" if cnt == 1 else "s"}</span></div>')
        for r, v in here:
            rn = r.get("name") or r["_name"]
            sk_blocks += (f'<p class="sub" style="margin:10px 0 8px"><b>{E(rn)}</b> reaches for '
                          f'{"this one" if len(v) == 1 else f"these {len(v)}"}</p>'
                          f'<div class="grid">{"".join(skill_card(x, r) for x in v)}</div>')
        sk_blocks += "</div>"
    spanning_sk = [(r, owned.get(r.get("name") or r["_name"], []))
                   for r in roles if not r.get("department")]
    spanning_sk = [(r, v) for r, v in spanning_sk if v]
    for r, v in spanning_sk:
        rn = r.get("name") or r["_name"]
        sk_blocks += (f'<div class="deptblock"><div class="hd"><h3>{E(rn)}</h3>'
                      f'<span class="led">across every department · {len(v)} skill'
                      f'{"" if len(v) == 1 else "s"}</span></div>'
                      f'<div class="grid">{"".join(skill_card(x, r) for x in v)}</div></div>')
    if orphans:
        sk_blocks += ('<div class="deptblock"><div class="hd"><h3>Nobody reaches for these</h3>'
                      '<span class="led">add owner: to the skill, or a name that matches a role</span>'
                      '</div><div class="grid">'
                      + "".join(skill_card(x, None) for x in orphans) + "</div></div>")

    sk_page = f"""
<section><h2>One method, written down once</h2>
<p class="sub">A skill is one method, written down once: when to use it, how it goes, and where it stops.
Read from <code>.claude/skills/</code> every time this site is built — teach an executive a skill and it
is here on the next build, with no list to keep up to date.</p>
<div class="stats">
  <div class="stat"><b>{len(skills)}</b><span>skill{"" if len(skills) == 1 else "s"}</span></div>
  <div class="stat"><b>{len(skills) - len(orphans)}</b><span>owned by an executive</span></div>
  <div class="stat"><b>{len(orphans)}</b><span>nobody reaches for</span></div>
  <div class="stat"><b>{len(owned)}</b><span>executive{"" if len(owned) == 1 else "s"} with one</span></div>
</div></section>

<section><h2>By who reaches for it</h2>
{sk_blocks or '<p class="empty">No skills yet. Ask for <b>Teaching an Executive a Skill</b> and the first one gets written properly.</p>'}
</section>"""
    write(F.PAGE_SKILLS, shell("Skills", F.PAGE_SKILLS, "What each executive knows how to do",
                               sk_page, stamp))

    # ---- 4. workflows, in department blocks
    def wf_table(rows):
        body = ""
        for w in rows:
            n = len(F.steps(w["_body"]))
            body += (
                '<tr data-flow="{k}" tabindex="0" role="button" aria-expanded="false">'
                '<td><b>{}</b><br><span style="color:var(--muted);font-size:13px">{}</span></td>'
                '<td>{}</td><td>{}</td><td>{}</td></tr>'
                '<tr class="detail" hidden><td colspan="4"><div class="flowbox"></div></td></tr>'
            ).format(
                E(w["_name"]), E(clip(F.summary(w["_body"], "Purpose"), 120)), E(w.get("owner") or "—"),
                '<span class="pill good">validated</span>' if w.get("doc_status") == "validated"
                else '<span class="pill">note is a draft</span>',
                {"ready": '<span class="pill good">running</span>',
                 "partly": '<span class="pill warn">partly running</span>'}.get(
                    w.get("readiness"), '<span class="pill">described only</span>'),
                k=html.escape(w["_name"], quote=True))
            del n
        return ('<div class="tw"><table><thead><tr><th>Workflow</th><th>Owner</th><th>The note</th>'
                f'<th>The workflow</th></tr></thead><tbody>{body}</tbody></table></div>')

    blocks, placed = "", set()
    for d in depts:
        name = d.get("name") or d["_name"]
        mine = flows_of(name)
        placed.update(id(w) for w in mine)
        heads = [r for r in execs_of(name) if is_exec(r)]
        helpers = [r for r in execs_of(name) if not is_exec(r)]
        lead = ", ".join(E(r.get("name", r["_name"])) for r in heads) or "no executive yet"
        if helpers:
            lead += f' +{len(helpers)} specialist' + ("" if len(helpers) == 1 else "s")
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
<section><h2>By department</h2>
<p class="sub">Click any workflow to see its steps drawn — read straight out of that note\u2019s own step
table, so the picture cannot say something the note does not.</p>
{blocks}</section>
{flow_block(flows, roles)}"""
    write(F.PAGE_FLOWS, shell("Workflows", F.PAGE_FLOWS, "How the work actually happens", wf, stamp))

    # ---- 5. projects
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

    # what the site was built from, so the check can ask the question by content and not by clock
    io.open(os.path.join(root, F.PICTURE_DIR, "build.json"), "w", encoding="utf-8",
            newline="\n").write(json.dumps({"built": TODAY.isoformat(),
                                            "sources": F.source_fingerprint(root)}, indent=1))

    # the page used to be index.html; leave no stale copy for somebody to open by mistake
    stale = os.path.join(root, F.PICTURE_DIR, "index.html")
    if os.path.exists(stale):
        os.remove(stale)

    return len(waiting), (len(execs), len(specialists)), len(flows), len(depts), len(projects), len(skills)


if __name__ == "__main__":
    root = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    w, (ex, sp), f, d, p, sk = build(root)
    print(f"site rebuilt — {len(PAGES)} pages · {w} thing{'' if w==1 else 's'} waiting on a person, "
          f"{d} department{'' if d==1 else 's'}, {ex} executives, {sp} specialist{'' if sp==1 else 's'}, "
          f"{sk} skills, {f} workflows, {p} projects")
    print(F.say_where(root))
