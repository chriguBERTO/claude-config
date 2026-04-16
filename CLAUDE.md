## Comments
- Add code comments when comments add useful situational information about non-obvious decisions, constraints, workarounds, gotchas, tradeoffs.
- NEVER comment what’s obvious by reading the code.

## Function Design
- **Structure**: Functions are short, do exactly one thing, and use early returns (guard clauses) to avoid nesting.
- **State**: Isolate side effects; prefer pure functions where possible.

## Reliability & Observability
- **Logging**: Include strategic logs for key state changes, errors, and integration points; avoid logging sensitive data.
- **Error Handling**: Fail fast with early input validation and descriptive errors.
- **Naming**: Use intention-revealing names to minimize the need for explanatory text.
- **Patterns**: Prefer declarative logic and match existing project architecture.
