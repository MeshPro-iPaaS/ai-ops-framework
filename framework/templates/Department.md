---
type: department
status: active
name: {{title}}
slug:
executive:
owner:
created: {{date}}
updated: {{date}}
owns:
  - The first thing this department is accountable for
  - The second
not_owned:
  - Something people will assume belongs here and does not — name it, or you will argue about it later
succeeds_when: "One sentence a person outside the department could check."
---

# {{title}}

> One paragraph: what this part of the organisation is for, in the words you would use to a new starter
> on their first morning. Not a mission statement — what it actually does all day.

## What it owns

The list above, in prose. Where a boundary is genuinely unclear, say so here rather than pretending.

## Who leads it

One executive, named in `executive:` above. That role note is compiled into the agent that answers for
this department. One department, one executive — a department with two has neither.

## How you know it is working

The `succeeds_when:` line above, expanded: what you would look at, and how often.

## Its workflows

Generated into the register. A department with no workflow is a name, not a department yet.
