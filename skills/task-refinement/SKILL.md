---
name: task-refinement
description: Interview the user relentlessly about a plan or design until reaching a shared understanding, resolving each branch of the decision tree. Use every time the user presents any request to implement, fix, add, change, refactor, or build something, stress-test a plan, get challenged on their design, or mentions "/task-refinement".
model: opus
effort: high
defaultMode: plan
---
# Task Refinement Skill

Your job is to reach a precise, shared understanding of the task before any implementation begins.

You are in read-only mode. Do not write, edit, or execute anything.

## Steps

### 1. Explore Before Asking
Before asking the user anything, explore and check if the answer exists in the codebase: existing patterns, error handling conventions, data models, interfaces, test coverage. Only ask what the codebase cannot answer.

### 2. Interview
Interview the user relentlessly about every aspect of this plan or design until reaching a shared understandin. Walk down each branch of the design tree, resolving dependencies one-by-one. After the main interview silently run this checklist and ask about any not yet covered:
- **Failure modes**: what happens when this breaks, times out, or receives bad input?
- **Boundary conditions**: empty state, single item, large input, concurrent access?
- **Rollback**: can this be undone? what is the state if it half-succeeds?
- **Dependencies**: what breaks elsewhere if this changes?
- **Security surface**: does this touch auth, user data, or external input?
- **Simpler alternative**: is there a version that solves 80% of the problem with 20% of the complexity?

### 3. Generate Plan
After the interview, create `%Y%m%d_<short-title-of-task>.md` in the planning directory:

1. **Task Spec**: Define the one-sentence goal, scope (in/out), key decisions, edge cases, and remaining open questions.
2. **Sub-tasks**: Break the work into sequential, isolated implementation steps. Minimize inter-dependencies.

## 4. Finalize
- Present the plan to the user.
- If the plan remains ambiguous, repeat the interview.
- If the user provides feedback, update the plan.
- Only consider the task status "refined" once the user explicitly approves the sub-task list.

## Template: %Y%m%d_<short-name-of-task>.md

```markdown
# Task Refinement: <short-title-of-task>

## Status: in_progress | refined 

## Task Spec
**Task:** [one sentence]
**Scope:** [what is in, what is explicitly out]
**Key decisions:** [answers to the important questions]
**Edge cases:** [list]
**Open questions:** [anything unresolved]

## Sub-tasks
### [ ] <number> <short-sub-task-title>
<self-contained-sub-task-description>

## Deferred
- <list-future-improvements>
```
