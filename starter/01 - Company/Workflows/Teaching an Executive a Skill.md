---
type: workflow
status: active
department: AI Operations
owner: Workflow Architect
created: 2026-09-23
updated: 2026-09-23
doc_status: draft
last_validated:
readiness: ready
---

# Teaching an Executive a Skill

**Purpose.** Give an executive a capability it did not have — a way of doing one thing properly, written
down once and used the same way every time. A skill is the difference between an agent that improvises
and one that follows your method.
**Trigger.** You explain the same approach to an executive twice.
**Done means.** A skill exists in `.claude/skills/`, its executive knows to reach for it, and somebody
has used it once.
**Owner.** Workflow Architect.

## How it runs today

```mermaid
flowchart TB
    classDef human fill:#E1EDE0,stroke:#4E7C4B,color:#1C2431
    classDef ai fill:#DDEBF1,stroke:#2E7C9A,color:#1C2431
    classDef gate fill:#F5EBD3,stroke:#9A6B14,color:#1C2431
    classDef store fill:#EAEEF2,stroke:#5B6572,color:#1C2431

    A(["👤 I keep explaining this the same way"]):::human
    B["🤖 write it down as a skill — when to use it, the steps, where it stops"]:::ai
    C[("⚙️ .claude/skills/{name}/SKILL.md")]:::store
    D["🤖 name it on its executive's role note"]:::ai
    E{"👤 use it once on something real"}:::gate
    F["🤖 fix what the real case showed"]:::ai
    A --> B --> C --> D --> E --> F --> C
```

## The steps

| # | Step | Who | What they need | What comes out |
|---|---|---|---|---|
| 1 | Say what you keep repeating | You | Your own words | The method, out loud |
| 2 | Write it as a skill | Workflow Architect | `_Templates/Skill.md` | `.claude/skills/{name}/SKILL.md` |
| 3 | Say when it applies | Workflow Architect | Step 1 | A description concrete enough to trigger on |
| 4 | Name it on the executive | Workflow Architect | The role note | The executive knows it exists |
| 5 | Use it on something real | You | A live case | Proof, or a list of what it got wrong |
| 6 | Fix what the case showed | Workflow Architect | Step 5 | A skill that survived contact |

## Where it breaks

| The exception | How often | What we do |
|---|---|---|
| The description is vague, so nothing ever triggers it | Most first drafts | Name the situation, not the topic |
| The skill quietly becomes a second copy of a workflow | Common | A workflow is how work moves; a skill is how one step is done well. If it has an owner and a trigger, it is a workflow |
| It is written from how you wish you worked | Always tempting | Write the version that includes the messy part |

## What it would take to automate

| Step | Could an agent do it? | What is missing |
|---|---|---|
| 2, 3, 4, 6 | Yes, today | Nothing |
| 1, 5 | No | What you keep repeating, and whether it worked, are yours |
