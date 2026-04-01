---
name: review-backend
description: Orchestrates multi-agent backend API code review. Architect, contradist, security-backend, performance-backend, data-integrity, and reliability review code from different perspectives. Iterates until all reviewers approve. USE WHEN review backend, review API, review backend code, backend code review, review before merge backend, check API quality.
---

# Review Workflow

Multi-agent backend code review. Specialist agents review in parallel, findings are consolidated, fixes applied, cycle repeats until all reviewers approve. Covers Python (FastAPI) and Go API codebases.

## Agents

| Agent                    | Focus                                                                    |
| ------------------------ | ------------------------------------------------------------------------ |
| **architect**            | Architecture, structure, dependency direction                            |
| **contradist**           | Over-engineering, unnecessary complexity, scope creep                    |
| **security-backend**     | OWASP API Top 10, injection, auth/authz, secrets, input validation, CORS |
| **performance-backend**  | Query efficiency, connection management, async/concurrency               |
| **data-integrity**       | Schema migrations, validation gaps, transaction safety                   |
| **reliability**          | Error handling, resilience, observability, degradation                   |

All agents are defined in `.claude/agents/`. Each outputs a numbered finding list or "APPROVED".

## Steps

### 1. Setup

1. Determine base branch (`main` or `master`)
2. Collect changed files: `git diff --name-only <base>...HEAD`
3. Read plan files if they exist in `[.claude|.ai|.cursor]/plans/` (plan.md, architecture.md)
4. Ask the user which reviewers to include (default: all applicable). Skip data-integrity if no schema/migration changes; skip reliability if changes are trivial.
5. Create `review_backend_%Y%m%d.md` in the plan directory (format at end of this file)

### 2. Parallel Review

Spawn all selected reviewers in parallel. Each receives:
- The list of changed files (filtered to their domain where applicable)
- Plan files for context (if they exist)

Do NOT repeat each agent's review criteria here — the agents know their job. Only provide context they need: file list, plan docs, and any project-specific specs.

If a finding affects the frontend package, the reviewer must note this explicitly (e.g. "impacts frontend: response shape changed in `GET /api/users`").

### 3. Consolidate

1. Collect findings from all reviewers
2. Deduplicate overlapping findings
3. Categorize:
   - **Blockers** — must fix (Critical/High)
   - **Improvements** — should fix (Medium)
   - **Suggestions** — optional (Low)
4. Update `review_backend_%Y%m%d.md`, present summary to user

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
2. Update `review_backend_%Y%m%d.md`: mark approved, record final status per reviewer
3. Present summary: iterations, findings addressed vs. deferred, outstanding suggestions
4. Ask: "Ready to commit?"

## review_backend_%Y%m%d.md Format

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
- Track iterations in review_backend_%Y%m%d.md
- Run verification after every fix cycle
- Max 3 iterations without user confirmation
- Only blockers are mandatory; never block on suggestions
