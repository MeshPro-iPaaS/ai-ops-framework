---
type: workflow
status: active
department: AI Operations
owner: Hephaestus
created: 2026-09-22
updated: 2026-09-22
doc_status: draft
last_validated:
readiness: ready
readiness_note: "Runs from day one — build_register, build_picture and check.py perform it"
---

# Keeping the Picture True

**Purpose.** The page everyone reads rebuilds itself from the notes, and a check refuses it when a
stated number would be untrue. This is the loop the whole framework exists to protect.
**Trigger.** Any change to a note that the picture draws from; and whenever you are about to show anyone
the page.
**Done means.** Every generator has run against the current notes, the check reports zero failures, and
the page you are looking at is the one that was just built.
**Owner.** Athena.

## How it runs today

```mermaid
flowchart TB
    classDef human fill:#E1EDE0,stroke:#4E7C4B,color:#1C2431
    classDef ai fill:#DDEBF1,stroke:#2E7C9A,color:#1C2431
    classDef gate fill:#F5EBD3,stroke:#9A6B14,color:#1C2431
    classDef store fill:#EAEEF2,stroke:#5B6572,color:#1C2431

    A(["👤 you change a note"]):::human
    B["🤖 an agent does green-list work"]:::ai
    S[("⚙️ the notes — the only source")]:::store
    G["🤖 build_roles · build_register · build_picture"]:::ai
    C{"🤖 check.py — zero failures, or stop"}:::gate
    P[("⚙️ 05 - Operations/picture — the page you read")]:::store
    F["🤖 fix the note that is wrong —<br/>never the generated file"]:::ai
    A --> S
    B --> S
    S --> G --> C
    C -->|"0 failures"| P
    C -->|"anything failed"| F --> G
```

## The steps

| # | Step | Who | What they need | What comes out |
|---|---|---|---|---|
| 1 | Change the one note that owns the fact | Anyone | To know which note that is | A changed source |
| 2 | Run the generators | Agent or you | Python | A rebuilt register and page |
| 3 | Run the check | Agent or you | — | Zero failures, or a named untruth |
| 4 | Fix the **note**, not the output | Agent or you | The failure message | A true source |
| 5 | Look at the page | You | — | Confidence it is current |

## Where it breaks

| The exception | How often | What we do |
|---|---|---|
| Someone edits the generated page because it was faster | Once per new person | It is overwritten on the next build. That is the design, not a bug — say so once and move on |
| The check fails on something no script can fix | Weekly at first | It goes on the list of what is waiting on a person, by name |
| The page is built but never looked at | The quiet failure | The page states when it was built. If that date is old, nobody is running the loop |

## What it would take to automate

| Step | Could an agent do it? | What is missing |
|---|---|---|
| 2, 3, 4 | Yes, today | Nothing |
| 5 | No | Looking at it is the human part |
| Running it on a clock | Yes — that is the Rhythm package | Scheduled passes, which the base deliberately leaves out |
