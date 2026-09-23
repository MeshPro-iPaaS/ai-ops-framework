# AI Operations Framework

**MeshPro × Expectus** · the base package

A written organisation that keeps itself true. You give it a folder; it gives you roles that can act,
workflows that execute the same way twice, and a picture of your operation that regenerates itself and
**refuses to publish a number it cannot prove**.

This is the **base**. It is deliberately small: one department with an executive, three roles, eight
workflows, four generators, one check suite, one page. No task board, no customer record, no schedules,
no code agents — those are separate packages you add when the base is running and you want more. A setup
that does everything on day one is a setup nobody finishes reading.

**You start with departments.** Name the parts — for a company its divisions, for one person every part of their own job — give each one an executive, and the
agents follow from that. Everything else — workflows, decisions, the weekly rhythm — hangs off an owner,
and a department is where owners come from.

## What you get

| | |
|---|---|
| **A contract** | The operating rules every AI session inherits before it does anything |
| **A folder skeleton** | Eight folders, each with one job, and a rule for what belongs in it |
| **Six templates** | So state is written the same way every time and a machine can read it |
| **A department layer** | One department installed as a worked example, and the workflow for naming your own |
| **Three roles** | Chief of Staff · Operations Executive (the shape every department's executive takes) · Workflow Architect — written contracts compiled into runnable agents |
| **Eight workflows** | Five that keep the vault true, one for naming your departments, two generic examples |
| **Two skills** | Writing a workflow down, and keeping the picture true |
| **Four generators** | Roles → agents · workflows → a register · the vault → a page · the whole thing → a check |
| **One check suite** | Thirteen checks that fail the build when the picture and reality disagree |

## Install

**If you use Claude with a folder connected** — the way most people will — you do not install anything
and you do not type any of this. Make a folder, connect it, and ask in plain words:

> *Set up the AI Operations Framework in this folder — pull it from
> github.com/MeshPro-iPaaS/ai-ops-framework and run the install.*

Claude does the rest. [`docs/START HERE.md`](docs/START%20HERE.md) is the walkthrough, written for
somebody who has never opened a terminal.

**If you would rather run it yourself**, it needs Python 3.10+ and nothing else:

```
python install.py "C:\path\to\your\vault"
```

Your dashboard lands at `05 - Operations/picture/ai_operations.html` — a plain local file, rebuilt from
your notes every time anything changes. The download itself is skipped by every generator and every
check, wherever it ended up, so it is never mistaken for one of your notes.

Either way it creates the folders, copies the contract, templates, departments, roles, workflows and
skills in, compiles the roles into agents, builds the register and the page, and runs the check. It is
idempotent — run it again after any change and it brings everything back in line.

Obsidian is optional but recommended: it is how you read and edit the vault comfortably. The framework
is plain Markdown either way, and nothing depends on a plugin.

## The idea underneath

1. **A fact has exactly one home.** Nothing is true in two places.
2. **Every surface is generated from those homes.** A page nobody could regenerate is a page that will lie.
3. **A check refuses the build when a stated number would be untrue.** Not a warning — a failure.
4. **Only a person publishes, sends, deploys or decides.** The machine prepares; the human commits.

## Showing it to someone

`docs/` holds two decks — a fourteen-slide one for somebody deciding whether to adopt it, and an
seventeen-slide **hands-on** one for a room building it with you, live, in an hour.

The fourteen-slide deck — the four ideas, what lands on disk, and a day-by-day first
fortnight with screenshots of the page the framework generates for itself. Present it as-is, or
run the install against an empty folder and show the real thing.

## Adding more

| Package | What it adds |
|---|---|
| The Rhythm | Daily, weekly and monthly passes · ledgers · the surface that names what waits on a person |
| More Departments | Ready-made department and executive notes — sales, delivery, finance, engineering, marketing — to adapt rather than write |
| The Board | Your task tracker connected, and the discipline that keeps it truthful |
| The Customer Record | Account schema, health, who needs attention and why |
| Revenue | Pipeline, outreach drafting, gap analysis |
| The Workshop | Per-repository agents, lanes, audits |
| Two People | Sharing the vault with a colleague over git, without sharing your own working material |

---

© MeshPro × Expectus. Installed in your vault, owned by you. Nothing here phones home, and nothing stops
working if we stop talking.
