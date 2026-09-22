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
  - Where this one stops — the nearby thing people (and its agent) will assume is its and is not
succeeds_when: "One sentence a person outside the department could check."
---

# {{title}}

> One paragraph: what this part of the organisation is for, in the words you would use to a new starter
> on their first morning. Not a mission statement — what it actually does all day.

## What it owns

The list above, in prose. Where a boundary is genuinely unclear, say so here rather than pretending.

## Where it stops

The `not_owned:` list, and it is the more important of the two. **An agent always answers.** Ask one a
question just outside its ground and it will not say "that is not mine" — it will produce something
confident and plausible about a subject it knows nothing about, and you will not be able to tell.
The stop line is what makes the answers you *do* get trustworthy. Between people it does a second job:
the argument about who owns a thing is much cheaper now than in six months.

## Who leads it

One executive, named in `executive:` above. That role note is compiled into the agent that answers for
this department. One department, one executive — a department with two has neither.

## How you know it is working

The `succeeds_when:` line above, expanded: what you would look at, and how often.

## Its workflows

Generated into the register. A department with no workflow is a name, not a department yet.
