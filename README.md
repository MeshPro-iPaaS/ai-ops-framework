# AI Operations Framework

**MeshPro × Expectus** · the base package

A written organisation that keeps itself true. You give it a folder; it gives you roles that can act,
workflows that execute the same way twice, and a picture of your operation that regenerates itself and
**refuses to publish a number it cannot prove**.

This is the **base**. It is deliberately small: three roles, six workflows, four generators, one check
suite, one page. No task board, no customer record, no schedules, no code agents — those are separate
packages you add when the base is running and you want more. A setup that does everything on day one is a
setup nobody finishes reading.

## What you get

| | |
|---|---|
| **A contract** | The operating rules every AI session inherits before it does anything |
| **A folder skeleton** | Eight folders, each with one job, and a rule for what belongs in it |
| **Five templates** | So state is written the same way every time and a machine can read it |
| **Three roles** | Chief of Staff, Domain Lead, Workflow Architect — written contracts compiled into runnable agents |
| **Six workflows** | Five that keep the vault true, one generic project workflow as a worked example |
| **Two skills** | Writing a workflow down, and keeping the picture true |
| **Four generators** | Roles → agents · workflows → a register · the vault → a page · the whole thing → a check |
| **One check suite** | Ten checks that fail the build when the picture and reality disagree |

## Install

Requires Python 3.10+ and, optionally, Obsidian to read the vault comfortably.

```
python install.py "C:\path\to\your\vault"
```

That creates the folders, copies the contract, templates, roles, workflows and skills in, compiles the
roles into agents, builds the register and the page, and runs the check. It is idempotent — run it again
after any change and it brings everything back in line.

## The idea underneath

1. **A fact has exactly one home.** Nothing is true in two places.
2. **Every surface is generated from those homes.** A page nobody could regenerate is a page that will lie.
3. **A check refuses the build when a stated number would be untrue.** Not a warning — a failure.
4. **Only a person publishes, sends, deploys or decides.** The machine prepares; the human commits.

## Adding more

| Package | What it adds |
|---|---|
| The Rhythm | Daily, weekly and monthly passes · ledgers · the surface that names what waits on a person |
| The Board | Your task tracker connected, and the discipline that keeps it truthful |
| The Customer Record | Account schema, health, who needs attention and why |
| Revenue | Pipeline, outreach drafting, gap analysis |
| The Workshop | Per-repository agents, lanes, audits |
| Two People | Sharing the vault with a colleague over git, without sharing your own working material |

---

© MeshPro × Expectus. Installed in your vault, owned by you. Nothing here phones home, and nothing stops
working if we stop talking.
