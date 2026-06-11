---
name: code-review-coordination-skill
description: Use this skill for code review coordination tasks that require structured
  workflow, policy-aware handling, and consistent outputs.
---

# Code Review Coordination Skill

## When To Use
- Identify what was implemented, what requirements or plan the change is supposed to satisfy, and which code range should be reviewed. Keep the explanation reusable for handoff.
- Turn raw implementation context into a precise review request that highlights correctness, architecture, testing, and production-readiness concerns. Keep the explanation reusable for handoff.
- Help the user separate critical blockers from important but deferrable quality issues. Keep the explanation reusable for handoff.
- Reduce review ambiguity by making missing context, missing diffs, or missing test evidence explicit early. Keep the explanation reusable for handoff.

## When Not To Use
- Requests outside the scope of code review coordination.
- Tasks that belong to another specialized skill family or workflow.
- Requests that should remain customer-facing without the structured output contract defined here.

## Core Workflow
1. Confirm the implementation summary, the requirement source, and the review target such as a branch, diff, or commit range. Keep the ordering easy to follow.
2. Classify the review focus across correctness, architecture, testing, performance, and production readiness before drafting guidance. Keep the ordering easy to follow.
3. State the current review posture first, then explain what evidence is still needed to complete a strong review. Keep the ordering easy to follow.
4. If context is missing, ask only for the minimum review inputs such as base and head shas, affected components, or explicit acceptance criteria. Keep the ordering easy to follow.
5. When review findings are available, separate strengths, critical issues, important issues, and minor recommendations clearly. Keep the ordering easy to follow.

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
