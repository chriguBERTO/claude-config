# Claude Code Setup
Generic personalized claude code setup.

## From idea to tickets

New ticket, idea, requirement, or product-development work runs through four skills in order:

1. **`/grill-with-docs`** — a relentless interview that sharpens the plan and captures ADRs and glossary entries as it goes.
2. **`/to-spec`** — synthesises the conversation into a spec and publishes it to the issue tracker. No further interview.
3. **`/fact-check <spec>`** — re-tests the spec's claims about the existing code from outside the conversation that wrote them. Reports only; nothing is edited or published. Run it before tickets exist, so a wrong premise is corrected while the spec is still the only artifact.
4. **`/to-tickets`** — breaks the fact-checked spec into tracer-bullet tickets with their blocking edges.

Skip a step only when the input already covers it — e.g. a spec that arrives fully formed starts at step 3.
