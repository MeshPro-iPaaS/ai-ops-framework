# Installing this — read this first

*Written for the AI session doing the install, and for the person watching it.*

**Install it by copying a folder. Do not start by running a program.**

Two real demos have now failed at exactly that: one machine could not run programs at all, and one had
no Python. Both were normal work laptops. So the finished vault ships in this repository and the
install is a copy — which every session can do, on every machine, with nothing installed.

## The install

**1 · Ask what the three executives should be called.** One question, and the only one:

| Say | Your executives are called |
|---|---|
| job titles | Chief of Staff, AI Operations Lead, Workflow Architect |
| Norse | Saga, Völundur, Bragi |
| Friends | Monica, Chandler, Ross |
| the Kardashians | Kourtney, Kim, Khloé |
| Greek | Athena, Hephaestus, Hermes |

**2 · Copy everything inside the matching folder into the person's connected folder** — all of it,
including the hidden `.claude` and `.ops` folders:

| They said | Copy the contents of |
|---|---|
| job titles | `starter/titles/` |
| Norse | `starter/norse/` |
| Friends | `starter/friends/` |
| the Kardashians | `starter/kardashian/` |
| Greek | `starter/greek/` |

The five are identical apart from the names. Each is a complete installed vault: thirteen folders, the
contract as `CLAUDE.md`, nine templates, two departments, three executives already compiled into
working agents, ten workflows, three skills, and the five-page site.

**3 · Tell the person, in plain words:**

> Your vault is set up and your dashboard is at `05 - Operations/picture/ai_operations.html` — open it
> in a browser. One thing is missing: the check has not run, and it cannot until something on this
> machine can run programs. The dashboard says so rather than pretending otherwise.

**Do not claim the check passed.** The starters ship with no check result on purpose. A green tick
carried over from the machine that built them is exactly the kind of claim this framework exists to
refuse.

If they want three names of their own instead, copy `starter/titles/` and then replace the three job
titles everywhere they appear — in `01 - Company/Roles/` (including the filenames, and the `slug:`
field, which must be lowercase ASCII with hyphens), `01 - Company/Departments/`,
`01 - Company/Workflows/`, `.claude/agents/` (including the filenames) and the site's
`agents.html`. Leave every `title:` line alone: that is the job title, and it stays.

## What this gets you, and what it does not

Everything a person actually does is a note, and notes need nothing installed: naming departments,
adding executives and specialists, teaching skills, writing workflows down, making decisions, running
the week.

What needs Python is the machinery that keeps the generated surfaces true: the compiled agents, the
register, the five-page site and the check. Without it, a session updates those by hand, and the skill
at `.claude/skills/when-you-cannot-run-programs/` says exactly which files and what goes in them. Two
of them — the hierarchy on `agents.html` and the step diagrams on `workflows.html` — are blocks of JSON
that the page redraws itself from, so those are an edit to a list rather than a layout to compute.

## Turning the machinery on, later — optional

Nothing above needs this, and the demo does not need it. It buys you the automatic rebuild and the
green check back.

**Where Python 3.10+ already exists**, one line from anywhere:

```
python ".ops/scripts/rebuild.py" "<the folder>"
```

**Where it does not** — which is most work laptops — every vault ships a script that fetches Python's
official *embeddable package*: about 10 MB, no installer, no admin rights, nothing added to `PATH`,
nothing registered with Windows. It lands in `C:\AI\python` and can be deleted at any time.

```
powershell -NoProfile -ExecutionPolicy Bypass -File ".ops\turn-on-the-machinery.ps1"
```

Run with no arguments it finds every vault under `C:\AI`; `-Vault "C:\AI\Your Folder"` names one.
It uses a real Python if it finds one and only downloads when it does not.

Two ways this can fail on a locked-down machine, both worth knowing before a room full of people:
the download can be blocked (a proxy, or python.org not on the allowlist), and `-ExecutionPolicy
Bypass` can itself be refused by group policy. Neither is a problem — the vault carries on working
exactly as it did, with the dashboard saying the check has not run, which is true.

## Installing from source instead

`python install.py "<the folder>" --names norse` builds a vault from `framework/` rather than copying
one. It is what `tools/build_starter.py` uses to produce the five starters. **It is not the install
path for a person's laptop** — it needs Python, which is the thing that keeps not being there.

---

## Renaming the executives later

The executives are notes. Ask for them to be renamed and the session edits the role notes, the
departments that point at them and the workflows they own. The naming question is a convenience at the
start, not the only chance.
