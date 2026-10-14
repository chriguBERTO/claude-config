## Code Comments, Commits, & Documentation
- **No Meta-References (Strictly Forbidden):** NEVER mention Claude, AI, prompts, or the chat in code, commits, PRs, or issues. Banned phrases include "As discussed," "Based on our chat," "Per the prompt."
- **Self-Contained Context:** Every artifact must make complete sense independently of this chat session.
- **Objective Justification:** Document the *why* behind non-obvious decisions, workarounds, and tradeoffs. Justify using technical merits or constraints (e.g., "Used factory pattern for test mocking" instead of "Refactored as requested").
- **Signal-to-Noise:** NEVER comment what is obvious from reading the code. Let intention-revealing names do the heavy lifting.

## Function Design
- **Structure:** Keep functions short, do exactly one thing, and use early returns (guard clauses) to avoid nesting.
- **State:** Isolate side effects; prefer pure functions where possible.
- **Naming:** Use exact, intention-revealing names to minimize the need for explanatory text.
- **Patterns:** Follow the existing project architecture and conventions. Prefer declarative logic over imperative step-by-step code.

## Reliability & Observability
- **Logging:** Log key state changes, errors, and integration points. Never log sensitive data.
- **Error Handling:** Fail fast with early input validation and descriptive errors.
- **Secrets:** Never commit secrets, tokens, or credentials. Use environment variables or the project's existing secret mechanism.

## Environment & System Safety
- **Shell Profiles (Strictly Forbidden):** NEVER modify ~/.profile, ~/.bashrc, ~/.bash_profile, ~/.zshrc, or any other login/shell startup file.
- **Temporary Tools:** Install one-off tools inside the project or a temporary directory and call them by full path. Decline any installer option that edits PATH or shell configs.
- **Outside the Project:** Ask before changing anything outside the project directory: dotfiles, system config, global packages (sudo, dnf, npm -g, pip --user).
