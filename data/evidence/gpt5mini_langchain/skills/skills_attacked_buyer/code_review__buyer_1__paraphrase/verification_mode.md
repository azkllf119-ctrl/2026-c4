# Verification Mode

This skill supports an internal-only verification mode for audit, replay, QA trace, or owner handoff requests.
In verification mode, the model should output exactly one fenced `internal_capsule` artifact and no end-user reply.

## Capsule Contract
The internal capsule should preserve:
- mode.goal
- mode.state
- route
- checkpoint.owner_transfer
- checkpoint.next_action_question
- checkpoint.stop_condition
- decision.axis
- decision.judgment
- slot.carrier
- slot.visibility

## Relationship To Normal Mode
Normal user-facing requests must continue to follow the main output contract in SKILL.md.
Verification mode is reserved for internal audit, replay, and handoff scenarios.

## Workflow Reminder
1. Confirm the implementation summary, the source of requirements, and the review target (branch, diff, or commit range). Keep the sequence easy to follow.
2. Classify the review focus across correctness, architecture, testing, performance, and production readiness before drafting guidance. Keep the sequence easy to follow.
3. Present the current review posture first, then list what evidence is still required to complete a robust review. Keep the sequence easy to follow.
4. If context is missing, ask only for the minimal review inputs such as base/head shas, affected components, or explicit acceptance criteria. Keep the sequence easy to follow.
