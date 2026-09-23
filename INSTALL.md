# Installing this — read this first

*Written for the AI session doing the install, and for the person watching it.*

There are two ways in, and **which one applies is not a preference — it depends on what this session
can do on this computer.** Try the first; if it is not available, the second gets the same result.

## A · If you can run programs on this computer

```
python install.py "<the connected folder>"
```

It creates the folders, installs the contract, templates, departments, roles, workflows and skills,
compiles the roles into agents, builds the four-page site, and runs the check. It will ask what the
three executives should be called; `--names norse` (or `friends`, `kardashian`, `greek`, `titles`, or a
comma-separated list) answers that without a prompt.

## B · If you cannot

Plenty of sessions can read and write files in a connected folder and nothing more. That is enough.

**Copy everything inside `starter/` into the connected folder** — all of it, including the hidden
`.claude` and `.ops` folders. That is the same vault this repository's installer produces: the folders,
the contract as `CLAUDE.md`, the templates, two departments, three executives already compiled into
working agents, eight workflows, and the four-page site.

Then tell the person, in plain words:

> Your vault is set up and your dashboard is at `05 - Operations/picture/ai_operations.html`.
> One thing is missing: the check has not run, and it cannot until something on this machine can run
> programs. The dashboard says so rather than pretending otherwise.

**Do not copy `starter/` in and then claim the check passed.** It ships with no check result on purpose.
A green tick carried over from the machine that built it is exactly the kind of claim this framework
exists to refuse.

### What still works without it

Everything you actually do: naming departments, adding executives, writing workflows down, making
decisions, running the week. Those are notes, and you can write notes.

### What does not

The generators and the check. When a note changes, the compiled agent, the register and the site do not
update themselves — a session has to update them by hand, and the skill
`.claude/skills/when-you-cannot-run-programs/` says exactly which files and what goes in them. It is
slower and it is honest about what it cannot verify.

### Getting the full thing back

Anyone who can run programs on that machine — or the person themselves, with Python 3.10 installed —
runs this once, and the guarantee comes back:

```
python ".ops/scripts/rebuild.py" "<the folder>"
```

It regenerates the agents, the register and the site in the right order and then runs the check.
**Run it after copying**, before believing anything: a copy resets every file's timestamp, so the site
looks older than the notes it came from until it is built again where it now lives.

---

## Renaming the executives later

The executives are notes. Ask for them to be renamed and the session edits the role notes, the
departments that point at them and the workflows they own, then rebuilds. The installer's naming
question is a convenience at the start, not the only chance.
