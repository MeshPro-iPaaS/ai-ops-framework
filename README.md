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
| **A department layer** | **Head Office** and **AI Operations** installed, each with one executive, and the workflow for naming your own |
| **Three executives** | Chief of Staff, an AI Operations Lead and a Workflow Architect — written contracts compiled into runnable agents. **Name them what you like at install**: job titles, Norse, Friends, the Kardashians, Greek, or your own list |
| **Eight workflows** | Five that keep the vault true, one for naming your departments, two generic examples |
| **Three skills** | Writing a workflow down, keeping the picture true, and keeping it true by hand when nothing can run |
| **Four generators** | Roles → agents · workflows → a register · the vault → a page · the whole thing → a check |
| **A five-page site** | Dashboard · Agent organization · Skills · Workflows · Projects. The hierarchy redraws itself whenever you add a department and an executive, the skill catalog reads itself off `.claude/skills/`, and clicking a workflow draws its steps |
| **One check suite** | Sixteen checks that fail the build when the picture and reality disagree |

## Install

> **If you are an AI session setting this up for somebody: read [`INSTALL.md`](INSTALL.md) first.**
> It is one path, and it is a copy. Do not start by running a program — two real demos failed there,
> one on a machine with no Python and one where the session could not run anything at all.

**Make a folder, connect it in Claude, and ask in plain words:**

> *Set up the AI Operations Framework in this folder, from
> github.com/MeshPro-iPaaS/ai-ops-framework.*

Claude asks one question — what to call your three executives — and copies the matching pre-built
vault out of [`starter/`](starter/) into your folder. Nothing is installed and nothing is run, so it
works the same on a locked-down work laptop as on a developer's machine.
[`docs/START HERE.md`](docs/START%20HERE.md) is the walkthrough, written for somebody who has never
opened a terminal.

Your site lands in `05 - Operations/picture/` — five plain local files. Open `ai_operations.html`
first. The download itself is skipped by every generator and every check, wherever it ended up, so it
is never mistaken for one of your notes.

**The generators are optional.** Every day-to-day thing — naming departments, adding executives and
specialists, teaching skills, writing workflows down — is a note, and needs nothing installed. What
Python buys you is the machinery that keeps the generated surfaces true automatically: the compiled
agents, the register, the site and the check.

Every vault ships `\.ops\turn-on-the-machinery.ps1`, which uses a real Python if the machine has one
and otherwise fetches Python's official embeddable package — about 10 MB, no installer, no admin
rights, nothing added to `PATH` — and runs the rebuild with that. Where even that is blocked, a
session keeps the generated surfaces true by hand, and the skill
`.claude/skills/when-you-cannot-run-programs/` says exactly how; the hierarchy and the step diagrams
redraw themselves from a block of JSON in the page, so those two are an edit to a list.

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
