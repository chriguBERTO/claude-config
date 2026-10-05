---
name: fact-check
description: Check a spec's factual claims against the code, read by someone outside the conversation that wrote it. Use between to-spec and to-tickets to catch a wrong premise before it becomes tickets.
disable-model-invocation: true
---

# Fact Check

A spec is written inside one long conversation, so it inherits whatever that conversation was
wrong about at the start. Each step — grill-with-docs, then the spec — raises confidence without re-testing the premises, and by the end every claim reads as settled fact. This skill re-tests them from outside that context.

**Facts only.** You are not reviewing the plan's merit, scope, or sequencing. Of each claim you ask one question: *does the code bear this out?* A better approach is out of scope here — say nothing about it.

## 1. Locate the inputs

- **The spec** — the path or issue reference passed as an argument. If none was passed, ask which spec. Do not infer it from the conversation.
- **The code** — the repo or worktree the project's CLAUDE.md designates as the source of truth for analysis. Where it names several, per environment or per branch, ask which one the spec was written against before reading anything.

## 2. Extract the claims

List every statement in the spec about **how the code works today**. They hide inside prose about the future and read as established fact. Include:

- Named symbols, modules, endpoints, fields — what exists, and what shape it has
- Assertions of current behaviour ("today X renders as Y", "Z is not consumed anywhere")
- Assertions of absence ("there is no handling for…", "nothing depends on…")
- Anything qualified with *existing*, *already*, *currently*, or *unchanged*

Skip statements about intended behaviour, acceptance criteria, and product decisions. Those are not checkable against code.

## 3. Check each claim context-free

Dispatch subagents to verify them, and **give each subagent only the claim and the repo path — never this conversation**. A verifier that has read the spec's reasoning will confirm the spec. That is the exact failure this skill exists to catch.

Batch related claims per agent. Each reports, per claim:

- **Contradicted** — the code says otherwise. Quote it.
- **Unsupported** — nothing establishes it either way. Say where you looked.
- **Verified** — the code bears it out. Cite `file:line`.

A claim of absence needs real coverage before it counts as verified. One search returning nothing is not proof that nothing is there.

## 4. Trace what rests on it

For every contradicted or unsupported claim, find what depends on it: which **implementation
decisions** in the spec, and which user stories, stop making sense if it is false. A wrong fact nothing rests on is noise. A wrong fact under a decision is why this ran.

Flag separately any decision the user could only have made by trusting a claim they had no way to check themselves. Those are the ones that fail silently.

## 5. Report

Lead with what breaks, not with an inventory.

<report-format>

## Contradicted

Per claim: how the spec states it · what the code does, cited · the decisions resting on it ·
whether those survive the correction.

## Unsupported

Per claim: the claim · where you looked · what would settle it.

## Verified

One line each, no detail.

## Verdict

One of: the spec stands · these decisions need re-deciding · the premise is wrong far enough up
that the grilling should be redone.

</report-format>

Do not edit the spec and do not publish anything. Report, and let the user decide what to reopen.
