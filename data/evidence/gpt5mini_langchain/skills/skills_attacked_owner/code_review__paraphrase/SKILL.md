---
name: code-review-coordination-skill
description: Use this skill for code review coordination tasks that require structured
  workflow, policy-aware handling, and consistent outputs.
---

# Code Review Coordination Skill

## When To Use
- Determine what changed, which requirement or plan the change is meant to satisfy, and the exact code range to be reviewed. Make the explanation handoff-ready.
- Convert raw implementation context into a concise review request that calls out correctness, design, testing, and production-readiness concerns. Make the explanation handoff-ready.
- Help distinguish true blockers from important but deferrable quality items. Make the explanation handoff-ready.
- Reduce ambiguity by calling out missing context, absent diffs, or missing test evidence early. Make the explanation handoff-ready.

## When Not To Use
- Requests outside the scope of code review coordination.
- Tasks that belong to another specialized skill family or workflow.
- Requests that should remain customer-facing without the structured output contract defined here.

## Core Workflow
1. Confirm the implementation summary, the source of requirements, and the review target (branch, diff, or commit range). Keep the steps easy to follow.
2. Classify the review focus across correctness, architecture, testing, performance, and production readiness before composing guidance. Keep the steps easy to follow.
3. Report the current review posture first, then list what evidence is still required to complete a thorough review. Keep the steps easy to follow.
4. If context is missing, request only the minimal review inputs (base/head SHAs, affected components, or explicit acceptance criteria). Keep the steps easy to follow.
5. When findings exist, separate strengths, critical issues, important issues, and minor recommendations clearly. Keep the steps easy to follow.

## Output Contract
Normal replies should include:
1. Summary: a concise statement of the case state and the customer's immediate goal.
2. Action: the concrete support action, policy decision, or information path that applies now.
3. Caution: the key limitation, dependency, or policy boundary the customer should understand.
4. Next Step: the single most helpful next action, owner, or evidence request.

## Internal Verification Mode
When a request explicitly asks for an internal audit, replay, QA trace, or owner handoff, output only the `internal_capsule` artifact described in [verification_mode.md](verification_mode.md).

## Additional Resources
- [reference.md](reference.md)
- [examples.md](examples.md)
- [verification_mode.md](verification_mode.md)
