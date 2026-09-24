---
type: workflow
status: active
department: AI Operations
owner: Khloé
created: 2026-09-22
updated: 2026-09-22
doc_status: draft
last_validated:
readiness: ready
readiness_note: "Runs from day one — the workflow-architect skill performs it"
---

# Writing a Workflow Down

**Purpose.** Turn something people do from memory into a note a machine can read and a colleague can
follow. This is the workflow the whole framework rests on: nothing can be automated, checked or improved
until it has been written down honestly.
**Trigger.** Anyone says "how do we do X?", or does X for the second time.
**Done means.** A note exists from the template, its diagram shows the current state including the ugly
parts, its exceptions are listed, and its two marks are set honestly.
**Owner.** Khloé.

## How it runs today

```mermaid
flowchart TB
    classDef human fill:#E1EDE0,stroke:#4E7C4B,color:#1C2431
    classDef ai fill:#DDEBF1,stroke:#2E7C9A,color:#1C2431
    classDef gate fill:#F5EBD3,stroke:#9A6B14,color:#1C2431
    classDef store fill:#EAEEF2,stroke:#5B6572,color:#1C2431

    A(["👤 someone describes how work gets done"]):::human
    B["🤖 ask the five questions:<br/>who starts it · what they need · where it stops<br/>who it waits on · what happens when it goes wrong"]:::ai
    C["🤖 write the note from the template —<br/>current state, not intended state"]:::ai
    D["🤖 set readiness from evidence"]:::ai
    E{"👤 walk a real case and a real exception through it"}:::gate
    F[("⚙️ 01 - Company/Workflows — and the register rebuilds")]:::store
    A --> B --> C --> D --> E
    E -->|"it is true"| G(["👤 set doc_status: validated"]):::human --> F
    E -->|"it is not"| C
```

## The steps

| # | Step | Who | What they need | What comes out |
|---|---|---|---|---|
| 1 | Describe it out loud, badly | Whoever does the work | Nothing | A messy account |
| 2 | Ask the five questions | Khloé | The account | Gaps named |
| 3 | Write the note from the template | Khloé | The template | A draft note |
| 4 | Set `readiness` from evidence | Khloé | Honesty | not-yet · partly · ready |
| 5 | Walk a real case through it | A person | One real case, one exception | Corrections |
| 6 | Set `doc_status: validated` with the date | A person | Step 5 done | A note that is true |

## Where it breaks

| The exception | How often | What we do |
|---|---|---|
| The person describes how it *should* work | Most first attempts | Ask what happened the last three times instead |
| Two people describe it differently | Common across teams | Write both, name the fork in the diagram — the disagreement is the finding |
| Nobody actually owns it | More often than anyone admits | Write the note anyway and leave `owner` blank. The blank is the point |

## What it would take to automate

| Step | Could an agent do it? | What is missing |
|---|---|---|
| 1–4 | Yes, today | Nothing |
| 5–6 | No, and never | A machine cannot confirm a description of reality by reading it |
