---
type: workflow
status: active
department: Head Office
owner: Athena
created: 2026-09-22
updated: 2026-09-22
doc_status: draft
last_validated:
readiness: ready
readiness_note: "Runs from day one — the contract and the installer perform it"
---

# Changing How You Work

**Purpose.** When the way you work changes, change it in one place and let everything downstream follow —
instead of discovering six months later that three documents describe three different organisations.
**Trigger.** A rule changes, a role changes, a workflow changes, or you decide something that lands on
any of them.
**Done means.** The one note that owns the fact is edited, the installer has run, the check is green, and
one line records what changed and why.
**Owner.** Athena.

## How it runs today

```mermaid
flowchart TB
    classDef human fill:#E1EDE0,stroke:#4E7C4B,color:#1C2431
    classDef ai fill:#DDEBF1,stroke:#2E7C9A,color:#1C2431
    classDef gate fill:#F5EBD3,stroke:#9A6B14,color:#1C2431
    classDef store fill:#EAEEF2,stroke:#5B6572,color:#1C2431

    A(["👤 you say how it should work now"]):::human
    R{"🤖 which note owns this fact?"}:::gate
    C[("⚙️ the contract — a rule")]:::store
    O[("⚙️ a role — what someone may do")]:::store
    W[("⚙️ a workflow — how work moves")]:::store
    I["🤖 run the installer:<br/>roles recompile, register rebuilds, picture rebuilds"]:::ai
    K{"🤖 check.py"}:::gate
    L[("⚙️ one line in the log: what changed, and why")]:::store
    A --> R
    R --> C & O & W
    C & O & W --> I --> K -->|"green"| L
    K -->|"red"| F["🤖 fix the source note"]:::ai --> I
```

## The steps

| # | Step | Who | What they need | What comes out |
|---|---|---|---|---|
| 1 | Say what changed, in plain words | You | — | Intent |
| 2 | Find the **one** note that owns it | Athena | The contract's routing table | A single target |
| 3 | Edit that note, and only that note | Athena | — | A changed source |
| 4 | Run the installer | Agent or you | Python | Everything downstream agrees |
| 5 | Check, then log one line | Athena | — | A green check and a record |

## Where it breaks

| The exception | How often | What we do |
|---|---|---|
| The same rule is written in two places | The classic failure | Delete one. Two copies of a rule is two rules |
| The change is made in the generated output | Early on | It vanishes at the next build; fix the source |
| Nobody logs why | Usually | Six months later nobody remembers, and it gets reverted by someone reasonable |

## What it would take to automate

| Step | Could an agent do it? | What is missing |
|---|---|---|
| 2–5 | Yes, today | Nothing |
| 1 | No | Deciding how you work is not delegable |
