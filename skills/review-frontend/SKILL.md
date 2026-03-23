---
name: review
description: Orchestrates multi-agent code review. Architect, designer, contradist, security, and performance-engineer review code from different perspectives. Code-simplifier cleans up fixes. Iterates until all reviewers approve. USE WHEN review code, code review, review changes, review PR, review before merge, check code quality.
---

# Review Workflow

Orchestrate a structured multi-agent code review. Five specialist agents review code from different perspectives, findings are consolidated, the frontend-engineer addresses them, and the cycle repeats until all reviewers approve.

## Reviewers

| Agent                    | Review Focus                                                           | Tools Used                         |
| ------------------------ | ---------------------------------------------------------------------- | ---------------------------------- |
| **architect**            | Architecture, code structure, package boundaries, dependency direction | Code analysis                      |
| **designer**             | Usability, UI correctness, design system compliance                    | Figma MCP + Playwright screenshots |
| **contradist**           | Over-engineering, unnecessary complexity, scope creep                  | Code analysis                      |
| **security**             | OWASP vulnerabilities, threat vectors, input handling                  | Code analysis                      |
| **performance-engineer** | Performance bottlenecks, bundle impact, Web Vitals                     | Code analysis                      |
| **platform-engineer**    | Windows compatibility of Node scripts (paths, file handling, OS APIs)  | Code analysis                      |

## Prerequisites

- Code to review exists on the current branch
- Branch follows naming convention: `<type>/<team>/<ticketId or date>-<description>`
- A plan exists in `.ai/plans/<team>/<ticket or date>_<description>/` (recommended but not required)
- The application is running for visual review (designer step — can be skipped if not applicable)

## Steps

### Step 1: Setup [required]

Establish the review context.

- **Agent:** self
- **Actions:**
  1. Run `git branch --show-current` and parse `<type>/<team>/<ticket>-<description>`
  2. If branch does not match convention, ask the user to create a proper branch first and STOP
  3. If ticket is `NOISSUE`, use current date (`YYYY-MM-DD`) as ticket ID
  4. Derive review directory: `.ai/plans/<team>/<ticket or date>_<description>/`
  5. Collect changed files: `git diff --name-only main...HEAD` (or appropriate base branch)
  6. Identify affected packages from the changed files
  7. Read the plan files if they exist (plan.md, architecture.md, ux.md)
  8. Read the `__specs__/` ground truth files for affected packages
  9. Ask the user which reviewers to include (default: all applicable). Some reviews may not apply (e.g., designer review only makes sense for UI changes, platform-engineer review only makes sense when Node scripts or build tooling in `tools/` are changed)
  10. Create `review.md` in the plan directory with iteration tracking (format below)
- **Output:** Review context established, changed files listed, reviewers selected

### Step 2: Lore Check [required]

Check tribal knowledge (lore) for affected packages to surface relevant decisions, constraints, and gotchas.

- **Agent:** self
- **Actions:**
  1. Run `yarn lore:affected` to get lore entries for packages affected by the current branch
  2. Read and understand the output — each entry has a `kind` (decision, constraint, gotcha, tradeoff, workaround, context), `title`, `body`, and `package`
  3. Evaluate whether the current changes respect the lore:
     - **Decisions:** Are the changes consistent with documented decisions?
     - **Constraints:** Do the changes violate any documented constraints?
     - **Gotchas:** Are there known pitfalls the changes might trigger?
     - **Workarounds:** Are there existing workarounds the changes should be aware of?
  4. If lore entries suggest changes are needed (e.g., a constraint is violated, a decision is ignored, or a gotcha applies), implement the necessary fixes using the frontend-engineer agent
  5. Record relevant lore findings in `review.md` under the review context section
- **Output:** Lore-informed context established, any necessary fixes applied

### Step 3: Parallel Review [required]

Run all selected reviewers in parallel. Each reviewer focuses on their specialty.

**In Agent Teams mode:** all selected reviewers run as simultaneous teammates, each with their own review task. Fix tasks are assigned per-package to different implementation teammates for parallel remediation. Reviewers start re-reviewing as soon as fixes relevant to their findings complete — do not wait for all fixes.

- **Agents:** architect, designer, contradist, security, performance-engineer, platform-engineer (as selected)
- **Actions:**
  1. Spawn all selected reviewers in parallel, each with:
     - The list of changed files
     - The affected packages and their `__specs__/` ground truth
     - The plan files (if they exist)
     - Reviewer-specific instructions (see below)
  2. Wait for all reviewers to complete

#### Architect Review Input

Provide the architect with:

- Changed files list
- Package `__specs__/architecture.md` for each affected package
- Plan `architecture.md` if it exists
- Instructions: "Review these changes for architectural correctness. Check: component structure follows the spec, package boundaries are respected, dependency direction is correct, Relay patterns are followed, no circular dependencies introduced, code organization matches conventions."

#### Designer Review Input

Provide the designer with:

- Changed files list (filtered to UI components and pages)
- Package `__specs__/ux.md` for each affected package
- Plan `ux.md` if it exists
- Instructions: "Review these changes for usability and UI correctness. Use the Figma MCP to compare the implementation against the design. Use Playwright browser automation to take screenshots of the implemented UI. Compare the screenshots against the Figma designs. Check: design system components used correctly, spacing follows 8dp grid, responsive behavior works, accessibility requirements met, all 4 themes supported, visual output matches Figma."

#### Contradist Review Input

Provide the contradist with:

- Changed files list
- Plan files (plan.md, architecture.md)
- Instructions: "Review these changes for over-engineering and unnecessary complexity. Check: are there simpler alternatives? Is there scope creep beyond the plan? Are new abstractions justified? Could existing components handle this? Is the package placement correct?"

#### Security Review Input

Provide the security agent with:

- Changed files list
- Package `__specs__/architecture.md` for data flow context
- Instructions: "Review these changes for security vulnerabilities. Check: input handling, XSS vectors, authentication/authorization correctness, data exposure, error message information leakage, unsafe patterns (eval, dangerouslySetInnerHTML, open redirects)."

#### Performance Engineer Review Input

Provide the performance-engineer with:

- Changed files list
- Package `__specs__/architecture.md` for component tree context
- Instructions: "Review these changes for performance impact. Check: rendering efficiency, data fetching patterns, bundle size impact, Core Web Vitals impact (LCP, INP, CLS), memory management, missing lazy loading or memoization, main thread blocking (>50ms)."

#### Platform Engineer Review Input

Provide the platform-engineer with:

- Changed files list (filtered to Node scripts, CLI tools, build tooling, and `tools/` packages)
- Instructions: "Review these changes for Windows compatibility. This review applies ONLY to Node.js scripts and build tooling — skip browser-only frontend code. Check:
  - **Path separators:** Use `path.join()` / `path.resolve()` / `path.posix` / `path.sep` instead of hardcoded `/` or `\\` in file paths. String concatenation with `/` for filesystem paths is a bug on Windows.
  - **Path normalization:** Use `path.normalize()` or consistent handling when comparing paths. Windows paths may have mixed separators and drive letters (e.g., `C:\\` vs `c:/`).
  - **Drive letters:** Paths on Windows start with a drive letter (`C:\\`). Code that assumes paths start with `/` will break. Watch for regex patterns like `/^\//` or `startsWith('/')`.
  - **File URI schemes:** `file:///path` vs `file:///C:/path` — `url.pathToFileURL()` and `url.fileURLToPath()` handle this correctly.
  - **Glob patterns:** Many glob libraries require forward slashes even on Windows. Use `.split(path.sep).join('/')` or `path.posix.join()` when constructing glob patterns.
  - **File handle limits:** Windows has lower default limits for open file descriptors. Never open many files concurrently without batching — process at most ~100 files per batch using chunked `Promise.all` or a concurrency limiter like `p-limit`. Unbounded `Promise.all(files.map(f => fs.readFile(f)))` will cause `EMFILE` errors on Windows.
  - **Line endings:** If reading/writing text files, be aware of `\\r\\n` vs `\\n`. Use `.replaceAll('\\r\\n', '\\n')` when comparing text content or use `os.EOL`.
  - **File name restrictions:** Windows disallows `<>:\"|?*` in filenames and has reserved names (`CON`, `PRN`, `NUL`, `COM1`, etc.).
  - **Case sensitivity:** Windows filesystems are case-insensitive. Don't rely on case differences to distinguish files.
  - **Long paths:** Windows has a 260-character path limit by default. Deeply nested `node_modules` or generated paths can exceed this.
  - **Temp directories:** Use `os.tmpdir()` instead of hardcoding `/tmp`.
  - **`fs.watch` / `fs.watchFile`:** Behavior differs across platforms. Document or test platform-specific behavior."

- **Output:** Individual review findings from each agent

### Step 4: Consolidate [required]

Merge all review findings into a single actionable document.

- **Agent:** self
- **Actions:**
  1. Collect findings from all reviewers
  2. Deduplicate: if multiple reviewers flagged the same issue, merge into one finding
  3. Categorize findings:
     - **Blockers** — Must fix before merge (Critical/High severity from any reviewer)
     - **Improvements** — Should fix, code will be better (Medium severity)
     - **Suggestions** — Nice to have, optional (Low severity or style preferences)
  4. Update `review.md` with the consolidated findings for this iteration
  5. Present the consolidated review to the user:
     - Total findings by category (blockers / improvements / suggestions)
     - Summary per reviewer
     - List of all blockers with file paths
- **Output:** Updated `review.md` with consolidated findings

### Step 5: User Decision [required]

Let the user decide what to address.

- **Agent:** self
- **Actions:**
  1. Present the review summary to the user
  2. Ask: "Which findings should we address? Options:"
     - **All blockers** (recommended minimum)
     - **Blockers + improvements**
     - **Everything**
     - **Custom selection** (user picks specific findings)
     - **None — approve as-is** (user overrides reviewers)
  3. If user selects "approve as-is", go to Step 9
  4. Record the user's selection in `review.md`
- **Output:** List of findings to address

### Step 6: Fix [conditional]

Send selected findings to the frontend-engineer for remediation.

- **Agent:** frontend-engineer
- **Actions:**
  1. Provide frontend-engineer with:
     - The selected findings to address (with file paths, line numbers, and remediation guidance)
     - The original plan files for context
     - The package `__specs__/` ground truth
  2. Frontend-engineer fixes issues one package at a time
  3. After fixes, run the **Verify Skill** (`@.ai/skills/verify.md`)
  4. **Failure strategy:** Fix and retry — frontend-engineer fixes until passing (max 3 attempts, then ask user)
  5. Present a summary of changes made to the user
- **Input:** Selected findings from Step 5
- **Output:** Code fixes applied and verified

### Step 7: Simplify [conditional]

Clean up the fixed code before re-review.

- **Agent:** code-simplifier
- **Actions:**
  1. Run code-simplifier on the files modified in Step 5
  2. Simplifier reduces complexity, removes redundancy, and improves readability without changing behavior
  3. Run the **Verify Skill** (`@.ai/skills/verify.md`) to ensure nothing broke
  4. **Failure strategy:** Revert — the simplifier reverts changes that caused failures
  5. Present a summary of simplifications made
- **Input:** Fixed files from Step 6
- **Output:** Simplified code, ready for re-review
- **Skip if:** No fixes were applied in Step 6

### Step 8: Re-Review [conditional]

Run reviewers again on the fixed code. Only re-run reviewers whose findings were addressed.

- **Agent:** self
- **Actions:**
  1. Identify which reviewers had findings that were addressed
  2. Re-run only those reviewers (same process as Step 3, but scoped to the fixes)
  3. Consolidate new findings (same process as Step 4)
  4. If new blockers found, return to Step 5
  5. If no new blockers, proceed to Step 9
  6. Track iteration count in `review.md` — if more than 3 iterations, ask the user whether to continue or accept current state
- **Output:** Updated `review.md` with new iteration results

### Step 9: Approve [required]

Finalize the review.

- **Agent:** self
- **Actions:**
  1. Run the **Verify Skill** (`@.ai/skills/verify.md`) as a final check
  2. Update `review.md`: mark review as `approved` with final status per reviewer
  3. Present final summary:
     - Total iterations
     - Findings addressed vs. deferred
     - Final status per reviewer (approved / approved-with-notes / overridden)
     - Outstanding suggestions (for future consideration)
  4. Ask user: "Review complete. Ready to commit?"
- **Output:** Finalized `review.md`, user approval

## review.md Format

```markdown
# Review: <feature name>

## Status: in_progress | approved

## Context

- **Branch:** <branch name>
- **Reviewers:** <list of active reviewers>
- **Changed Files:** <count>
- **Affected Packages:** <list>

## teration 1

### Findings

#### Blockers

- [ ] [<reviewer>] <finding title> — `<file>:<line>` — <description>
- [ ] [<reviewer>] <finding title> — `<file>:<line>` — <description>

#### Improvements

- [ ] [<reviewer>] <finding title> — `<file>:<line>` — <description>

#### Suggestions

- [ ] [<reviewer>] <finding title> — `<file>:<line>` — <description>

### User Decision

<what the user chose to address>

### Fixes Applied

- [x] <finding> — <how it was fixed>
- [x] <finding> — <how it was fixed>

## Iteration 2

...

## Final Status

| Reviewer             | Status              | Notes                |
| -------------------- | ------------------- | -------------------- |
| architect            | approved            |                      |
| designer             | approved-with-notes | <minor visual notes> |
| contradist           | approved            |                      |
| security             | approved            |                      |
| performance-engineer | approved            |                      |
| platform-engineer    | approved            |                      |

## Deferred

- <suggestion deferred for future work>
```

## Rules

- ALWAYS run Step 1 (setup) to establish context before any review
- ALWAYS run reviewers in parallel — never sequentially
- ALWAYS present consolidated findings to the user before fixing
- ALWAYS let the user decide which findings to address
- ALWAYS re-run affected reviewers after fixes — don't assume fixes are correct
- ALWAYS track iterations in review.md
- ALWAYS run verification (lint, typecheck, test) after fixes
- NEVER skip the user decision step — the user owns the final call
- NEVER let the review loop more than 3 iterations without user confirmation to continue
- NEVER block on suggestions or low-severity findings — only blockers are mandatory
- If a reviewer has no findings, record "no issues found" for that reviewer
- If the designer review requires a running application and one is not available, skip the visual comparison and note it in review.md
