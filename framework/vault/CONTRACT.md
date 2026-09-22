# CLAUDE.md — the operating contract

*Installed by the AI Operations Framework (MeshPro × Expectus). Yours to edit — this file is the one
place the rules live, and every AI session in this vault reads it before doing anything.*

## The four rules

1. **A fact has exactly one home.** One note owns it. If you find the same fact in two places, one of
   them is wrong and you cannot tell which — fix that before anything else.
2. **Every surface is generated from those homes.** The register, the page, the agent files. Never edit a
   generated file: edit the note that owns the fact and re-run the generator.
3. **A check refuses the build when a stated number would be untrue.** If the page would say nine and
   render seven, the build fails. Run `python .ops/scripts/check.py` before you publish anything.
4. **Only a person publishes, sends, deploys or decides.** Agents prepare. You commit.

## Where things go

| You are adding… | It goes in… | From the template |
|---|---|---|
| A decision you made | `01 - Company/Decisions/DR — {Title}.md` | `Decision.md` |
| How a piece of work actually happens | `01 - Company/Workflows/{Human name}.md` | `Workflow.md` |
| A role an agent plays | `01 - Company/Roles/{Name}.md` | — (see the three installed) |
| A project or initiative | `02 - Work/{Name}.md` | `Note.md` |
| A person, customer or partner | `03 - People/{Name}.md` | `Note.md` |
| Reference material | `04 - Knowledge/{Topic}.md` | `Note.md` |
| Today's log | `06 - Daily/YYYY-MM-DD.md` | `Daily.md` |
| A week's plan or review | `01 - Company/Weekly/YYYY-Www.md` | `Weekly.md` |
| Something you have not filed yet | `00 - Inbox/` | — |

Generated, never edited by hand: `01 - Company/Workflows/Workflows.md` (the register),
`05 - Operations/picture/` (the page), `.ops/agents/` (the compiled roles).

## Frontmatter

Every note carries it. Machines can only read state that is written the same way every time.

```yaml
---
type: workflow | decision | role | project | person | knowledge | daily | weekly | note
status: draft | active | decided | archived
owner: Name            # who decides about this note, not who typed it
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

Workflows carry two more marks, and they answer different questions:

- `doc_status: draft | validated` — is the **note** true? Only a person who has walked a real case
  through it may set `validated`, and they add `last_validated: YYYY-MM-DD` when they do.
- `readiness: not-yet | partly | ready` — is the **workflow** actually running end to end?

A documented organisation is not the same as a working one. Two marks, because they go wrong separately.

## How you talk to it

In plain language. Say what you want; the roles are routed to by intent, not by a command you have to
remember. If a session ever answers you with syntax to type, that session is wrong.

## What is never automatic

Publishing anything outward. Sending anything a customer sees. Deploying. Spending money. Changing a
credential. Deleting. Anything you cannot undo. Agents prepare all of it and stop; you decide.

**Unattended work reads and writes text in this vault, and nothing else.** That restraint is what makes
the rest safe to run when nobody is watching.

## When something is stale

A note left `draft` for three weeks is not neutral — agents read status as fact, so a stale note actively
misleads. Give it a disposition: promote it, archive it, or delete it.

## Changing this file

This contract is the source. When you change how you work, change it here first, then run the installer
so everything downstream agrees. If this file and any other copy of a rule disagree, **this file is
right and the other copy is stale.**
