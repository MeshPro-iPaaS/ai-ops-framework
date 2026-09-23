# Start here

*You will not type a single command. You will not install Python, git, or anything else. If you can
make a folder and write a sentence, you can do all of this.*

**About twenty minutes**, and at the end you will have an organisation that writes itself down: named
departments, an executive for each one that can actually do work, and a page that refuses to tell you
something untrue.

---

## What you need

| | |
|---|---|
| **Claude, on your computer** | The desktop app. This is where you do everything |
| **A folder** | Under `C:\AI` — `C:\AI\My Second Brain` is fine. Empty is fine. This becomes your vault |
| **Obsidian** *(recommended, not required)* | Free. It is how you read and edit the vault comfortably. Everything works without it; it is just nicer with it |

Your vault is **your second brain**: the place your organisation's facts live, so that you and Claude
are looking at the same thing tomorrow as today. Nothing is uploaded anywhere. The folder stays on your
computer and it is plain text you can read with Notepad.

---

## 1 · Make the folder

Make an empty folder under `C:\AI` and give it your own name, or your team's. Everything AI-related
lives in one place that way, which matters the first time you go looking for it.

That is the whole of step one.

## 2 · Make a project in Claude, and connect the folder to it

In Claude, create a **project** for your company — call it whatever you call the company.

Then **connect the folder** you just made to that project. Claude will ask you to confirm; say yes.

> **Why a project?** Because a project remembers. Everything you do inside it reads and writes the
> same folder, so the conversation you have next week starts where this one ended instead of starting
> from nothing. One project, one company, one folder.

## 3 · Ask for the setup

Write this to Claude, in the project, in exactly these words or your own:

> **Set up the AI Operations Framework in my connected folder. Pull it from
> github.com/MeshPro-iPaaS/ai-ops-framework and run the install, then tell me what it made.**

Claude fetches the framework, installs it into your folder and runs the check. It takes about a minute.
When it finishes you have thirteen folders, a contract, templates, two departments, three roles compiled
into working agents, ten workflows, three skills, and a five-page site — dashboard, agent organization,
skills, workflows and projects — in `05 - Operations/picture/`. Open **`ai_operations.html`** first.

**Claude will ask what to call your executives**: their job titles, or Norse mythology, Friends, the
Kardashians, Greek, or three names of your own. It changes nothing except what they are called, and a
name you chose is one you will actually talk to. The job titles stay in the notes either way.

The download itself usually ends up inside your folder. That is fine: every generator and every check
skips it on sight, so it is never read as one of your notes, and you can delete it once the install has
run. `.ops/framework-source/` is the tidy place for it if you would rather keep it.

> **If Claude says it cannot run programs on your computer** — some setups can only read and write
> files — say: *then copy everything in the starter folder into mine instead.* You get exactly the same
> vault. The one difference: the check cannot run, and the dashboard will say so rather than pretend.
> Everything you actually do today — departments, executives, workflows — works either way.

> **If Claude says it cannot reach the address** — some company networks block it — download the
> repository as a ZIP in your browser instead, unzip it anywhere, and say: *install the framework from
> the folder I just unzipped into my vault folder.* Same result.

## 4 · Look at what you got

Ask:

> **Open the picture and tell me what it says.**

It is `05 - Operations/picture/ai_operations.html`, a plain file in your own folder. Bookmark it —
the other three pages are linked across the top.

The page lists what is waiting on a person, the departments and who answers for each, and every workflow
with two marks: whether the *note* has been checked against a real case, and whether the *workflow*
actually runs. They go wrong separately, which is why there are two.

It will tell you something uncomfortable straight away — probably that you have one department and no
real workflows yet. That is correct, and it is the point: **the page never says something it cannot
prove.**

## 5 · Name your departments — this is the real first step

Say:

> **Walk me through Setting Up a Department. My organisation has these parts: …**

and then name them the way you say them out loud. *Sales. Delivery. The money stuff. The client stuff.*
Three to six. Not twelve.

Claude writes one note per department — what it owns, what it explicitly does **not** own, and one
sentence saying how you would know it is working — then gives each one an **executive**: a role note
that gets compiled into an agent that answers for that department and nothing else.

That is your executive layer. Adding a department later is the same sentence again.

> **Two rules worth arguing about now rather than in six months.** One department, one executive — with
> two, each assumes the other answered. And the same person can be behind several departments: the
> department is the unit of *accountability*, not of headcount.

## 6 · Write down one workflow — the one that annoys you most

Not your most important process. The one that goes wrong most often. Say:

> **Let's write down how [the thing] actually happens today, including the parts that are a mess.**

Claude asks you questions and writes the note: what triggers it, what "done" means, who owns it, the
steps, **where it breaks**, and what an agent could take over. It marks it as a draft and as not-yet
running, because you have not walked a real case through it yet.

Do that once — one real case, start to finish — and tell Claude it held up. Only then does it become
validated, and only a person can say so.

## 7 · Ask for the truth, on a schedule

Once a week:

> **Run my week: what finished, what is stale, what is waiting on me?**

Everything answers from the notes. If the notes are wrong, the answer is wrong — which is exactly why
the check exists, and why it fails the build rather than warning you.

---

## The four ideas, in one breath

1. **A fact has one home.** If it is true in two places, one of them is lying and you cannot tell which.
2. **Every surface is generated.** The page, the register, the agents. Never edit those — edit the note.
3. **A check fails the build on a false claim.** Not a warning. A failure.
4. **Only a person publishes, sends, deploys or decides.** The machine prepares; you commit.

## What to do when something is wrong

Tell Claude in plain words. *"That's not how it works — we do X first."* It changes the note that owns
the fact and rebuilds everything downstream. You never edit the page; the page is a view.

If a session ever answers you with a command to type, that session is wrong. Say so.

---

*AI Operations Framework — MeshPro × Expectus. Installed in your vault, owned by you. Nothing here
phones home, and nothing stops working if we stop talking.*
