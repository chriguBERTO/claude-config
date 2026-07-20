## Code Comments, Commits, & Documentation
- **No Meta-References (Strictly Forbidden):** NEVER mention Claude, AI, prompts, or the chat in code, commits, PRs, or issues. 
- **Banned Phrases:** "As discussed," "Based on our chat," "Per the prompt," etc.
- **Self-Contained Context:** Every artifact must make complete sense independently of this chat session.
- **Objective Justification:** Document the *why* behind non-obvious decisions, workarounds, and tradeoffs. Justify using technical merits or constraints (e.g., "Used factory pattern for test mocking" instead of "Refactored as requested").
- **Signal-to-Noise:** NEVER comment what is obvious from reading the code. Let intention-revealing names do the heavy lifting.

## Function Design
- **Structure:** Keep functions short, do exactly one thing, and use early returns (guard clauses) to avoid nesting.
- **State:** Isolate side effects; prefer pure functions where possible.

## Reliability & Observability
- **Logging:** Log key state changes, errors, and integration points. Never log sensitive data.
- **Error Handling:** Fail fast with early input validation and descriptive errors.
- **Naming:** Use exact, intention-revealing names to minimize the need for explanatory text.
- **Patterns:** Prefer declarative logic and adhere to the existing project architecture.
