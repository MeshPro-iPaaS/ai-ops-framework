---
name: keeping-the-picture-true
description: Use at the end of any session that changed a note the picture draws from — a role, a workflow, a skill, a decision, the contract — and whenever someone asks whether the picture is current or says it looks wrong. Regenerates the register, the agents and the page, runs the check, and reports what is untrue rather than papering over it.
owner: AI Operations Lead
department: AI Operations
---

# Keeping the picture true

The page everyone reads is generated. Your job is to make it true again, in this order.

## Do this

1. **Find the one note that owns the fact** that changed. The contract's routing table says which. If the
   fact appears in two notes, that is the finding — report it before doing anything else.
2. **Edit that note.** Never a generated file: `01 - Company/Workflows/Workflows.md`, anything under
   `05 - Operations/picture/ai_operations.html` (the dashboard), and everything in `.claude/agents/` are outputs.
3. **Run the generators, in order** — or `python .ops/scripts/rebuild.py`, which runs all three and
   the check for you:
   ```
   python .ops/scripts/build_roles.py
   python .ops/scripts/build_register.py
   python .ops/scripts/build_picture.py
   ```
   A skill counts as a note the picture draws from: `.claude/skills/{name}/SKILL.md` feeds the Skills
   page, and a workflow's `## The steps` table feeds the diagram you get by clicking that workflow.
   Both come from `build_picture.py`, so neither needs anything extra — but neither updates on its own
   either.
4. **Run the check:** `python .ops/scripts/check.py`. It must report **zero failures**.
5. **If something failed, fix the note** the failure names — never the output, and never the check.
6. **Report in plain words**: what changed, what the check said, and what is still untrue. If something
   needs a person, name it — what it is, what it waits for, and what happens if nothing is done. A count
   is not a notification.

## Never

- Publish or send anything. The base framework produces a local page; putting it anywhere is a person's
  decision.
- Report a green check you did not run.
- Edit the check to make it pass.
