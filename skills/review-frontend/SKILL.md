---
name: review-frontend
description: Orchestrates multi-agent code review. Architect, designer, contradist, security, performance-engineer, and platform-engineer review code from different perspectives. Iterates until all reviewers approve. USE WHEN review code, code review, review changes, review PR, review before merge, check code quality.
---

# Review Workflow

Multi-agent code review. Specialist agents review in parallel, findings are consolidated, fixes applied, cycle repeats until all reviewers approve.

## Agents

| Agent                    | Focus                                                    |
| ------------------------ | -------------------------------------------------------- |
| **architect**            | Architecture, structure, dependency direction            |
| **designer**             | Usability, UI correctness, accessibility, design system  |
| **contradist**           | Over-engineering, unnecessary complexity, scope creep    |
| **security**             | OWASP vulnerabilities, input handling, data exposure     |
| **performance-engineer** | Render efficiency, bundle impact, Web Vitals             |
| **platform-engineer**    | Windows compatibility of Node scripts and build tooling  |

All agents are defined in `.claude/agents/`. Each outputs a numbered finding list or "APPROVED".

## Steps

### 1. Setup

1. Determine base branch (`main` or `master`)
2. Collect changed files: `git diff --name-only <base>...HEAD`
3. Read plan files if they exist in `[.claude|.ai|.cursor]/plans/` (plan.md, architecture.md, ux.md)
4. Ask the user which reviewers to include (default: all applicable). Skip designer if no UI changes; skip platform-engineer if no Node scripts or `tools/` changes.
5. Create `review.md` in the plan directory (format at end of this file)

### 2. Parallel Review

Spawn all selected reviewers in parallel. Each receives:
- The list of changed files (filtered to their domain where applicable)
- Plan files for context (if they exist)

Do NOT repeat each agent's review criteria here — the agents know their job. Only provide context they need: file list, plan docs, and any project-specific specs.

If a finding affects the backend package, the reviewer must note this explicitly (e.g. "impacts backend: API contract change in `shared/types.ts`").

### 3. Consolidate

1. Collect findings from all reviewers
2. Deduplicate overlapping findings
3. Categorize:
   - **Blockers** — must fix (Critical/High)
   - **Improvements** — should fix (Medium)
   - **Suggestions** — optional (Low)
4. Update `review.md`, present summary to user

### 4. User Decision

Present findings and ask what to address:
- All blockers (recommended minimum)
- Blockers + improvements
- Everything
- Custom selection
- None — approve as-is → skip to Step 7

### 5. Fix & Verify

1. Address selected findings
2. Run verification (`@[.claude|.ai|.cursor]/skills/verify.md`) — fix and retry, max 3 attempts, then ask user
3. Run code-simplifier on modified files to reduce complexity without changing behavior
4. Re-verify after simplification; revert simplifications that break verification

### 6. Re-Review

1. Re-run only reviewers whose findings were addressed
2. If new blockers → return to Step 4
3. If no blockers → proceed to Step 7
4. After 3 iterations, ask user whether to continue or accept

### 7. Approve

1. Final verification pass
2. Update `review.md`: mark approved, record final status per reviewer
3. Present summary: iterations, findings addressed vs. deferred, outstanding suggestions
4. Ask: "Ready to commit?"

## review.md Format

```markdown
# Review: <feature>
## Status: in_progress | approved
## Context
- **Branch:** <branch>
- **Reviewers:** <list>
- **Changed Files:** <count>

## Iteration 1
### Blockers
- [ ] [<reviewer>] <finding> — `<file>` — <description>
### Improvements
- [ ] [<reviewer>] <finding> — `<file>` — <description>
### Suggestions
- [ ] [<reviewer>] <finding> — `<file>` — <description>
### Decision: <what user chose>
### Fixes: <what was fixed>

## Final Status
| Reviewer | Status | Notes |
| --- | --- | --- |
| architect | approved | |

## Deferred
- <suggestion for future>
```

## Rules

- Run reviewers in parallel, never sequentially
- Present findings to user before fixing — user owns the final call
- Re-run affected reviewers after fixes
- Track iterations in review.md
- Run verification after every fix cycle
- Max 3 iterations without user confirmation
- Only blockers are mandatory; never block on suggestions
