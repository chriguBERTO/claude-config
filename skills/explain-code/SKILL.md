---
name: explain-code
description: Use this skill whenever the user asks to explain code, a class, function, module, or pattern — including queries like "Explain class X in @path/filename", "How does this function work?", "Walk me through this module", or "What design pattern is this?". Trigger even for partial references like "explain the auth logic" or "what's happening here". Always use this skill when explaining code, not just when explicitly asked.
---

# Code Explanation Skill

## Understanding the Request

The user may reference code in several ways:
- **Inline code** pasted directly in the chat
- **File references** like `@path/filename`
- **Named targets** like "class User", "function process_payment", "the auth module"
- **Combined**: "Explain class User in @path/filename"

When a file reference (`@path/filename`) is present, read the file first and locate the named target within it. If only a name is given (no `@`), search the codebase or ask for clarification if ambiguous.

## Explanation Structure

### 1. High-Level Overview
- What is this code's purpose and responsibility?
- What are the main entry points through which the code is reached?
- Where does it fit in the broader system? (e.g., "This is the ORM model layer", "This handles authentication middleware")
- What problem does it solve?

### 2. Design Patterns & Architecture Choices
- Identify patterns used (e.g., Repository, Singleton, Observer, Factory)
- Explain *why* this pattern was likely chosen
- Discuss trade-offs: advantages and disadvantages in this context
- Note any deviations from standard patterns and why

### 3. Step-by-Step Walkthrough
- Walk through the code in logical (not necessarily line-by-line) order
- Highlight non-obvious logic, edge cases, and important conditionals
- Explain any performance-relevant decisions
- Flag security considerations if relevant (e.g., input validation, auth checks, SQL injection risks)

### 4. Best Practices Assessment (if useful)
- What's done well?
- What could be improved or modernized?

## Style Guidelines

- **Conversational tone** — write like you're pair-programming with a colleague
- **Use analogies** for abstract concepts, especially multiple analogies for complex ideas
- **Scale depth to complexity** — a 5-line helper needs less explanation than a 200-line class
- **Code callouts** — reference specific lines or snippets to anchor explanations
- **Ask if unclear** — if the target is ambiguous (e.g., multiple classes named `User`), ask before explaining
