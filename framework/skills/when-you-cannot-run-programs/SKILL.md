---
name: when-you-cannot-run-programs
description: Keep this vault true by hand when the session cannot run the generators. Use whenever a note changes and `python .ops/scripts/...` is not available on this machine.
---

# When you cannot run programs

Some sessions can read and write files on this computer and nothing more. Everything in this vault
still works — it is all plain text — but the four generators and the check cannot run, so the things
they normally produce have to be written by hand. This skill says exactly which files, what goes in
them, and what you must never claim.

## The rule that matters most

**Never state a number you have not counted, and never say the check passed.** The whole point of this
framework is a surface that cannot lie. Writing a generated file by hand is fine; writing *fifteen
checks green* into it when no check ran is not. If you touch the site, leave the check indicator saying
the check has not run — that is the truth.

## What is generated, and what to put in it

| File | What it is | What to do when a note changes |
|---|---|---|
| `.claude/agents/<slug>.md` | One per role note | Rewrite it from the role note: the frontmatter `name` is the role's `slug`, the description is its name, authority, department, first three `owns` and all of `never`. Then the note's body, then the authority section — copy the shape from an agent that is already there |
| `01 - Company/Workflows/Workflows.md` | The register | Between the `BEGIN generated` and `END generated` markers: one section per department, a row per workflow with its owner, whether the note is validated, whether it runs, and its Purpose line |
| `05 - Operations/picture/agents.html` — the hierarchy | A block of JSON the page draws itself from | **This is the easy one.** Between `<!-- BEGIN the hierarchy -->` and `<!-- END the hierarchy -->` is a list of `{name, title, department, reports_to, authority}`. Add, remove or edit an entry and the chart relays itself when the page is opened. There are no coordinates to compute and nothing else in that file to touch |
| `05 - Operations/picture/*.html` — everything else | The four pages | Edit the existing page. **Count before you write a number** — the tiles, the legend under the chart and the per-department counts are all stated, and a stated number nobody counted is the failure this vault exists to prevent |
| `05 - Operations/picture/check.json` | The check result | **Do not write this file.** It is written by the check, and only by the check |

## The order

Role notes first, then the register, then the pages. On the organization page, do the hierarchy data
block first and the counts around it second — the legend under the chart states how many executives and
departments there are, and it does not update itself. A page built before the register is a page
describing a register that no longer exists.

## What to tell the person

Say it plainly, once, rather than quietly doing a worse job:

> This machine cannot run the framework's generators, so I updated the agent file, the register and the
> site by hand. They are correct as far as I can count, but the check has not run — the dashboard says
> so. Anyone who can run programs here can run `.ops/scripts/check.py` and get the guarantee back.

## Getting the real thing back

One command, from anyone with Python 3.10 on that machine:

```
python ".ops/scripts/rebuild.py" "<the vault folder>"
```

That regenerates the agents, the register and the site in the right order and then runs the check.
Nothing you wrote by hand is lost — it is overwritten by the same content, counted rather than
estimated.
