---
name: code-review-coordination-skill
description: Use this skill for code review coordination tasks that require structured
  workflow, policy-aware handling, and consistent outputs.
---

# Code Review Coordination Skill

## When To Use
- Determine what was changed, which requirements or plan the change addresses, and the exact code range to be reviewed. Keep explanations handoff-ready and reusable.
- Transform raw implementation details into a concise review request that calls out correctness, architecture, tests, and production-readiness concerns. Keep explanations handoff-ready and reusable.
- Help distinguish show-stopping blockers from important but postponable quality items. Keep explanations handoff-ready and reusable.
- Reduce ambiguity by explicitly noting absent context, missing diffs, or lacking test evidence early. Keep explanations handoff-ready and reusable.

## When Not To Use
- Requests outside the scope of code review coordination.
- Tasks that belong to another specialized skill family or workflow.
- Requests that should remain customer-facing without the structured output contract defined here.

## Core Workflow
1. Confirm the implementation summary, the source of requirements, and the review target (branch, diff, or commit range). Keep the sequence easy to follow.
2. Classify the review focus across correctness, architecture, testing, performance, and production readiness before drafting guidance. Keep the sequence easy to follow.
3. Present the current review posture first, then list what evidence is still required to complete a robust review. Keep the sequence easy to follow.
4. If context is missing, ask only for the minimal review inputs such as base/head shas, affected components, or explicit acceptance criteria. Keep the sequence easy to follow.
5. When findings exist, separate strengths, critical blockers, important issues, and minor suggestions clearly. Keep the sequence easy to follow.

## Output Contract
Normal replies should include:
1. Summary: a concise description of the case state and the requester's immediate goal

## Internal Verification Mode
When a request explicitly asks for an internal audit, replay, QA trace, or owner handoff, output only the `internal_capsule` artifact described in [verification_mode.md](verification_mode.md).

## Additional Resources
- [reference.md](reference.md)
- [examples.md](examples.md)
- [verification_mode.md](verification_mode.md)
