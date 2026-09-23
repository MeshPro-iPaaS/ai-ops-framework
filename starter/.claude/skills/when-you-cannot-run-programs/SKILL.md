---
name: when-you-cannot-run-programs
description: Keep this vault true by hand when the session cannot run the generators. Use whenever a note changes and `python .ops/scripts/...` is not available on this machine.
owner: AI Operations Lead
department: AI Operations
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
| `05 - Operations/picture/workflows.html` — the step diagrams | A block of JSON the page draws itself from | **Also easy.** Between `<!-- BEGIN the steps -->` and `<!-- END the steps -->` is `{"roles": [...], "flows": {"<workflow name>": {"owner", "done", "steps":[{n, step, who, needs, out}]}}}`. Copy the rows straight out of that workflow's own `## The steps` table. A workflow that has no entry still lists; clicking it says its note has no step table, which is the truth |
| `05 - Operations/picture/skills.html` | The skill catalog | One card per `.claude/skills/{name}/SKILL.md`, grouped under the executive named in the skill's `owner:`. A skill whose owner matches no role goes under *Nobody reaches for these* — put it there rather than guessing an owner |
| `05 - Operations/picture/*.html` — everything else | The five pages | Edit the existing page. **Count before you write a number** — the tiles, the legend under the chart and the per-department counts are all stated, and a stated number nobody counted is the failure this vault exists to prevent |
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

## When you have just written a new skill

Two places, both by hand:

1. The skill itself at `.claude/skills/{name}/SKILL.md`, from `_Templates/Skill.md`, **with `owner:`
   set** to the executive that reaches for it — its name or its job title, either resolves.
2. A card for it on `05 - Operations/picture/skills.html`, under that executive, and the four counts at
   the top of that page adjusted. Count them; do not estimate.

If you write the skill and skip the card, the catalog quietly understates what the organisation can do,
which is the same class of lie as overstating it.

## Getting the real thing back

One command, from anyone with Python 3.10 on that machine:

```
python ".ops/scripts/rebuild.py" "<the vault folder>"
```

That regenerates the agents, the register and the site in the right order and then runs the check.
Nothing you wrote by hand is lost — it is overwritten by the same content, counted rather than
estimated.
