---
type: workflow
status: active
owner:
created: {{date}}
updated: {{date}}
doc_status: draft
last_validated:
readiness: not-yet
readiness_note: "why it is not yet running end to end"
---

# {{title}}

**Purpose.** What this workflow is for, in one or two sentences.
**Trigger.** What starts it.
**Done means.** How you know it finished — a condition, not a feeling.
**Owner.** Who is accountable when it goes wrong.

## How it runs today

Draw the current state, not the intended one. If a step is a person copying something by hand, draw the
person copying something by hand.

```mermaid
flowchart TB
    classDef human fill:#E1EDE0,stroke:#4E7C4B,color:#1C2431
    classDef ai fill:#DDEBF1,stroke:#2E7C9A,color:#1C2431
    classDef gate fill:#F5EBD3,stroke:#9A6B14,color:#1C2431
    classDef store fill:#EAEEF2,stroke:#5B6572,color:#1C2431

    A(["👤 what starts it"]):::human --> B["🤖 the first step"]:::ai
    B --> C{"👤 the gate that needs a person"}:::gate
    C --> D[("⚙️ where the result lands")]:::store
```

## The steps

| # | Step | Who | What they need | What comes out |
|---|---|---|---|---|
| 1 | | | | |

## Where it breaks

| The exception | How often | What we do |
|---|---|---|

## What it would take to automate

| Step | Could an agent do it? | What is missing |
|---|---|---|

## Improvements proposed

Kept separate from the current state on purpose. A proposal is not a description.
