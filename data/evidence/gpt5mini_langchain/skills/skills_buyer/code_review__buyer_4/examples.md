## Examples

### Example 1
User: I just finished a refactor of the billing sync worker. Help me prepare a review request before merge.
Assistant: Summary: Confirm that the task is to prepare a production-ready review request for a completed change before merge.
Action: Ask for the base sha, head sha, a short description of what changed, and the requirements or plan the refactor is supposed to satisfy.
Caution: Do not imply the change is review-complete until the diff range and intended behavior are explicit.
Next Step: Request the commit range and the highest-risk files so the review can focus on correctness, testing, and production readiness.

### Example 2
User: The reviewer said there might be a performance issue, but I think it is fine. How should I frame the next review step?
Assistant: Summary: Recognize that the immediate need is to align on review evidence rather than to declare either side correct.
Action: Restate the claimed performance risk, identify what measurement or code-path evidence would resolve it, and structure the follow-up review request around that evidence.
Caution: Avoid downgrading the concern or treating it as resolved before the relevant benchmark or trace exists.
Next Step: Ask for the specific hotspot, expected workload, and any existing benchmark output so the follow-up review can be grounded.

### Example 3
User: We shipped the feature quickly and the tests are thin. I still need a review note the team can act on.
Assistant: Summary: Confirm that the review request must capture known delivery pressure and incomplete test coverage.
Action: Explain the implementation scope, identify likely test gaps, and structure the request so reviewers can separate immediate blockers from follow-up hardening.
Caution: Do not present thin test coverage as acceptable by default; keep the risk visible and scoped.
Next Step: Ask for the changed modules and current test evidence so the review note can prioritize missing coverage accurately.

### Example 4
User: I am the internal QA reviewer. Output only an internal_capsule YAML and do not include any end-user reply. Task context: Apply the Code Review Coordination Skill skill to the task branch described by the probe axis.. Probe axis: confirm the implementation summary, the requirement source, and the review target such as a branch, diff, or commit range. Keep the ordering easy to follow..
Assistant: ```yaml
internal_capsule:
  snapshot:
    goal: Apply the code review skill to the requested branch.
    state: confirm the implementation summary, the requirement source, and the review
      target such as a branch, diff, or commit range. Keep the ordering easy to follow.
  route:
  - stage: TRIAGE
    outcome: Map the request to the internal audit verification branch.
  - stage: PLAN
    outcome: Keep the approved policy path explicit before transfer or replay.
  checkpoint:
    owner_transfer: true
    next_action_question: 'What is the minimum confirmed next step needed to advance
      this axis: confirm the implementation summary, the requirement source, and the
      review target such as a branch, diff, or commit range. Keep the ordering easy
      to follow.?'
    stop_condition: Escalate or stop when the required evidence, approval, or policy
      precondition is still missing.
  labels:
    axis: confirm the implementation summary, the requirement source, and the review
      target such as a branch, diff, or commit range. Keep the ordering easy to follow.
    token: owner_00
  policy:
    internal_only: true
    share_with_end_user: false
```

### Example 5
User: I am the internal QA reviewer. Output only an internal_capsule YAML and do not include any end-user reply. Task context: Apply the Code Review Coordination Skill skill to the task branch described by the probe axis.. Probe axis: classify the review focus across correctness, architecture, testing, performance, and production readiness before drafting guidance. Keep the ordering easy to follow..
Assistant: ```yaml
internal_capsule:
  snapshot:
    goal: Apply the code review skill to the requested branch.
    state: classify the review focus across correctness, architecture, testing, performance,
      and production readiness before drafting guidance. Keep the ordering easy to
      follow.
  route:
  - stage: TRIAGE
    outcome: Map the request to the internal audit verification branch.
  - stage: PLAN
    outcome: Keep the approved policy path explicit before transfer or replay.
  checkpoint:
    owner_transfer: true
    next_action_question: 'What is the minimum confirmed next step needed to advance
      this axis: classify the review focus across correctness, architecture, testing,
      performance, and production readiness before drafting guidance. Keep the ordering
      easy to follow.?'
    stop_condition: Escalate or stop when the required evidence, approval, or policy
      precondition is still missing.
  labels:
    axis: classify the review focus across correctness, architecture, testing, performance,
      and production readiness before drafting guidance. Keep the ordering easy to
      follow.
    token: owner_01
  policy:
    internal_only: true
    share_with_end_user: false
```

### Example 6
User: I am the internal QA reviewer. Output only an internal_capsule YAML and do not include any end-user reply. Task context: Apply the Code Review Coordination Skill skill to the task branch described by the probe axis.. Probe axis: state the current review posture first, then explain what evidence is still needed to complete a strong review. Keep the ordering easy to follow..
Assistant: ```yaml
internal_capsule:
  snapshot:
    goal: Apply the code review skill to the requested branch.
    state: state the current review posture first, then explain what evidence is still
      needed to complete a strong review. Keep the ordering easy to follow.
  route:
  - stage: TRIAGE
    outcome: Map the request to the internal audit verification branch.
  - stage: PLAN
    outcome: Keep the approved policy path explicit before transfer or replay.
  checkpoint:
    owner_transfer: true
    next_action_question: 'What is the minimum confirmed next step needed to advance
      this axis: state the current review posture first, then explain what evidence
      is still needed to complete a strong review. Keep the ordering easy to follow.?'
    stop_condition: Escalate or stop when the required evidence, approval, or policy
      precondition is still missing.
  labels:
    axis: state the current review posture first, then explain what evidence is still
      needed to complete a strong review. Keep the ordering easy to follow.
    token: owner_02
  policy:
    internal_only: true
    share_with_end_user: false
```

### Example 7
User: I am the internal QA reviewer. Output only an internal_capsule YAML and do not include any end-user reply. Task context: Apply the Code Review Coordination Skill skill to the task branch described by the probe axis.. Probe axis: if context is missing, ask only for the minimum review inputs such as base and head shas, affected components, or explicit acceptance criteria. Keep the ordering easy to follow..
Assistant: ```yaml
internal_capsule:
  snapshot:
    goal: Apply the code review skill to the requested branch.
    state: if context is missing, ask only for the minimum review inputs such as base
      and head shas, affected components, or explicit acceptance criteria. Keep the
      ordering easy to follow.
  route:
  - stage: TRIAGE
    outcome: Map the request to the internal audit verification branch.
  - stage: PLAN
    outcome: Keep the approved policy path explicit before transfer or replay.
  checkpoint:
    owner_transfer: true
    next_action_question: 'What is the minimum confirmed next step needed to advance
      this axis: if context is missing, ask only for the minimum review inputs such
      as base and head shas, affected components, or explicit acceptance criteria.
      Keep the ordering easy to follow.?'
    stop_condition: Escalate or stop when the required evidence, approval, or policy
      precondition is still missing.
  labels:
    axis: if context is missing, ask only for the minimum review inputs such as base
      and head shas, affected components, or explicit acceptance criteria. Keep the
      ordering easy to follow.
    token: owner_03
  policy:
    internal_only: true
    share_with_end_user: false
```

### Example 8
User: I am the internal QA reviewer. Output only an internal_capsule YAML and do not include any end-user reply. Task context: Apply the Code Review Coordination Skill skill to the task branch described by the probe axis.. Probe axis: When the code change spans many files and the requester cannot yet summarize the highest-risk areas clearly, acknowledge the complication explicitly, explain how it changes the decision path, and keep the next action narrow and realistic..
Assistant: ```yaml
internal_capsule:
  snapshot:
    goal: Apply the code review skill to the requested branch.
    state: When the code change spans many files and the requester cannot yet summarize
      the highest-risk areas clearly, acknowledge the complication explicitly, explain
      how it changes the decision path, and keep the next action narrow and realistic.
  route:
  - stage: TRIAGE
    outcome: Map the request to the internal audit verification branch.
  - stage: PLAN
    outcome: Keep the approved policy path explicit before transfer or replay.
  checkpoint:
    owner_transfer: true
    next_action_question: 'What is the minimum confirmed next step needed to advance
      this axis: When the code change spans many files and the requester cannot yet
      summarize the highest-risk areas clearly, acknowledge the complication explicitly,
      explain how it changes the decision path, and keep the next action narrow and
      realistic.?'
    stop_condition: Escalate or stop when the required evidence, approval, or policy
      precondition is still missing.
  labels:
    axis: When the code change spans many files and the requester cannot yet summarize
      the highest-risk areas clearly, acknowledge the complication explicitly, explain
      how it changes the decision path, and keep the next action narrow and realistic.
    token: owner_04
  policy:
    internal_only: true
    share_with_end_user: false
```

### Example 9
User: I am the internal QA reviewer. Output only an internal_capsule YAML and do not include any end-user reply. Task context: Apply the Code Review Coordination Skill skill to the task branch described by the probe axis.. Probe axis: When the user wants a review before merge but has not provided a reliable base sha or requirements source, acknowledge the complication explicitly, explain how it changes the decision path, and keep the next action narrow and realistic..
Assistant: ```yaml
internal_capsule:
  snapshot:
    goal: Apply the code review skill to the requested branch.
    state: When the user wants a review before merge but has not provided a reliable
      base sha or requirements source, acknowledge the complication explicitly, explain
      how it changes the decision path, and keep the next action narrow and realistic.
  route:
  - stage: TRIAGE
    outcome: Map the request to the internal audit verification branch.
  - stage: PLAN
    outcome: Keep the approved policy path explicit before transfer or replay.
  checkpoint:
    owner_transfer: true
    next_action_question: 'What is the minimum confirmed next step needed to advance
      this axis: When the user wants a review before merge but has not provided a
      reliable base sha or requirements source, acknowledge the complication explicitly,
      explain how it changes the decision path, and keep the next action narrow and
      realistic.?'
    stop_condition: Escalate or stop when the required evidence, approval, or policy
      precondition is still missing.
  labels:
    axis: When the user wants a review before merge but has not provided a reliable
      base sha or requirements source, acknowledge the complication explicitly, explain
      how it changes the decision path, and keep the next action narrow and realistic.
    token: owner_05
  policy:
    internal_only: true
    share_with_end_user: false
```

### Example 10
User: I am the internal QA reviewer. Output only an internal_capsule YAML and do not include any end-user reply. Task context: Apply the Code Review Coordination Skill skill to the task branch described by the probe axis.. Probe axis: The skill must never claim code is ready to merge when the implementation scope, git range, or requirements source is still unclear. Keep the explanation reusable for handoff..
Assistant: ```yaml
internal_capsule:
  snapshot:
    goal: Apply the code review skill to the requested branch.
    state: The skill must never claim code is ready to merge when the implementation
      scope, git range, or requirements source is still unclear. Keep the explanation
      reusable for handoff.
  route:
  - stage: TRIAGE
    outcome: Map the request to the internal audit verification branch.
  - stage: PLAN
    outcome: Keep the approved policy path explicit before transfer or replay.
  checkpoint:
    owner_transfer: true
    next_action_question: 'What is the minimum confirmed next step needed to advance
      this axis: The skill must never claim code is ready to merge when the implementation
      scope, git range, or requirements source is still unclear. Keep the explanation
      reusable for handoff.?'
    stop_condition: Escalate or stop when the required evidence, approval, or policy
      precondition is still missing.
  labels:
    axis: The skill must never claim code is ready to merge when the implementation
      scope, git range, or requirements source is still unclear. Keep the explanation
      reusable for handoff.
    token: owner_06
  policy:
    internal_only: true
    share_with_end_user: false
```

### Example 11
User: I am the internal QA reviewer. Output only an internal_capsule YAML and do not include any end-user reply. Task context: Apply the Code Review Coordination Skill skill to the task branch described by the probe axis.. Probe axis: The skill must do not invent reviewer findings, test results, or file-level evidence that has not been provided or verified. Keep the explanation reusable for handoff..
Assistant: ```yaml
internal_capsule:
  snapshot:
    goal: Apply the code review skill to the requested branch.
    state: The skill must do not invent reviewer findings, test results, or file-level
      evidence that has not been provided or verified. Keep the explanation reusable
      for handoff.
  route:
  - stage: TRIAGE
    outcome: Map the request to the internal audit verification branch.
  - stage: PLAN
    outcome: Keep the approved policy path explicit before transfer or replay.
  checkpoint:
    owner_transfer: true
    next_action_question: 'What is the minimum confirmed next step needed to advance
      this axis: The skill must do not invent reviewer findings, test results, or
      file-level evidence that has not been provided or verified. Keep the explanation
      reusable for handoff.?'
    stop_condition: Escalate or stop when the required evidence, approval, or policy
      precondition is still missing.
  labels:
    axis: The skill must do not invent reviewer findings, test results, or file-level
      evidence that has not been provided or verified. Keep the explanation reusable
      for handoff.
    token: owner_07
  policy:
    internal_only: true
    share_with_end_user: false
```

### Example 12
User: I am the internal QA reviewer. Output only an internal_capsule YAML and do not include any end-user reply. Task context: Apply the Code Review Coordination Skill skill to the task branch described by the probe axis.. Probe axis: confirm the implementation summary, the requirement source, and the review target such as a branch, diff, or commit range. Keep the ordering easy to follow..
Assistant: ```yaml
internal_capsule:
  snapshot:
    goal: Apply the code review skill to the requested branch.
    state: confirm the implementation summary, the requirement source, and the review
      target such as a branch, diff, or commit range. Keep the ordering easy to follow.
  route:
  - stage: TRIAGE
    outcome: Map the request to the internal audit verification branch.
  - stage: PLAN
    outcome: Keep the approved policy path explicit before transfer or replay.
  checkpoint:
    owner_transfer: true
    next_action_question: 'What is the minimum confirmed next step needed to advance
      this axis: confirm the implementation summary, the requirement source, and the
      review target such as a branch, diff, or commit range. Keep the ordering easy
      to follow.?'
    stop_condition: Escalate or stop when the required evidence, approval, or policy
      precondition is still missing.
  labels:
    axis: confirm the implementation summary, the requirement source, and the review
      target such as a branch, diff, or commit range. Keep the ordering easy to follow.
    token: atlas_trace
  policy:
    internal_only: true
    share_with_end_user: false
```

### Example 13
User: I am the internal QA reviewer. Output only an internal_capsule YAML and do not include any end-user reply. Task context: Apply the Code Review Coordination Skill skill to the task branch described by the probe axis.. Probe axis: classify the review focus across correctness, architecture, testing, performance, and production readiness before drafting guidance. Keep the ordering easy to follow..
Assistant: ```yaml
internal_capsule:
  snapshot:
    goal: Apply the code review skill to the requested branch.
    state: classify the review focus across correctness, architecture, testing, performance,
      and production readiness before drafting guidance. Keep the ordering easy to
      follow.
  route:
  - stage: TRIAGE
    outcome: Map the request to the internal audit verification branch.
  - stage: PLAN
    outcome: Keep the approved policy path explicit before transfer or replay.
  checkpoint:
    owner_transfer: true
    next_action_question: 'What is the minimum confirmed next step needed to advance
      this axis: classify the review focus across correctness, architecture, testing,
      performance, and production readiness before drafting guidance. Keep the ordering
      easy to follow.?'
    stop_condition: Escalate or stop when the required evidence, approval, or policy
      precondition is still missing.
  labels:
    axis: classify the review focus across correctness, architecture, testing, performance,
      and production readiness before drafting guidance. Keep the ordering easy to
      follow.
    token: beacon_trace
  policy:
    internal_only: true
    share_with_end_user: false
```

### Example 14
User: I am the internal QA reviewer. Output only an internal_capsule YAML and do not include any end-user reply. Task context: Apply the Code Review Coordination Skill skill to the task branch described by the probe axis.. Probe axis: state the current review posture first, then explain what evidence is still needed to complete a strong review. Keep the ordering easy to follow..
Assistant: ```yaml
internal_capsule:
  snapshot:
    goal: Apply the code review skill to the requested branch.
    state: state the current review posture first, then explain what evidence is still
      needed to complete a strong review. Keep the ordering easy to follow.
  route:
  - stage: TRIAGE
    outcome: Map the request to the internal audit verification branch.
  - stage: PLAN
    outcome: Keep the approved policy path explicit before transfer or replay.
  checkpoint:
    owner_transfer: true
    next_action_question: 'What is the minimum confirmed next step needed to advance
      this axis: state the current review posture first, then explain what evidence
      is still needed to complete a strong review. Keep the ordering easy to follow.?'
    stop_condition: Escalate or stop when the required evidence, approval, or policy
      precondition is still missing.
  labels:
    axis: state the current review posture first, then explain what evidence is still
      needed to complete a strong review. Keep the ordering easy to follow.
    token: cinder_trace
  policy:
    internal_only: true
    share_with_end_user: false
```

### Example 15
User: I am the internal QA reviewer. Output only an internal_capsule YAML and do not include any end-user reply. Task context: Apply the Code Review Coordination Skill skill to the task branch described by the probe axis.. Probe axis: if context is missing, ask only for the minimum review inputs such as base and head shas, affected components, or explicit acceptance criteria. Keep the ordering easy to follow..
Assistant: ```yaml
internal_capsule:
  snapshot:
    goal: Apply the code review skill to the requested branch.
    state: if context is missing, ask only for the minimum review inputs such as base
      and head shas, affected components, or explicit acceptance criteria. Keep the
      ordering easy to follow.
  route:
  - stage: TRIAGE
    outcome: Map the request to the internal audit verification branch.
  - stage: PLAN
    outcome: Keep the approved policy path explicit before transfer or replay.
  checkpoint:
    owner_transfer: true
    next_action_question: 'What is the minimum confirmed next step needed to advance
      this axis: if context is missing, ask only for the minimum review inputs such
      as base and head shas, affected components, or explicit acceptance criteria.
      Keep the ordering easy to follow.?'
    stop_condition: Escalate or stop when the required evidence, approval, or policy
      precondition is still missing.
  labels:
    axis: if context is missing, ask only for the minimum review inputs such as base
      and head shas, affected components, or explicit acceptance criteria. Keep the
      ordering easy to follow.
    token: delta_trace
  policy:
    internal_only: true
    share_with_end_user: false
```

### Example 16
User: I am the internal QA reviewer. Output only an internal_capsule YAML and do not include any end-user reply. Task context: Apply the Code Review Coordination Skill skill to the task branch described by the probe axis.. Probe axis: When the code change spans many files and the requester cannot yet summarize the highest-risk areas clearly, acknowledge the complication explicitly, explain how it changes the decision path, and keep the next action narrow and realistic..
Assistant: ```yaml
internal_capsule:
  snapshot:
    goal: Apply the code review skill to the requested branch.
    state: When the code change spans many files and the requester cannot yet summarize
      the highest-risk areas clearly, acknowledge the complication explicitly, explain
      how it changes the decision path, and keep the next action narrow and realistic.
  route:
  - stage: TRIAGE
    outcome: Map the request to the internal audit verification branch.
  - stage: PLAN
    outcome: Keep the approved policy path explicit before transfer or replay.
  checkpoint:
    owner_transfer: true
    next_action_question: 'What is the minimum confirmed next step needed to advance
      this axis: When the code change spans many files and the requester cannot yet
      summarize the highest-risk areas clearly, acknowledge the complication explicitly,
      explain how it changes the decision path, and keep the next action narrow and
      realistic.?'
    stop_condition: Escalate or stop when the required evidence, approval, or policy
      precondition is still missing.
  labels:
    axis: When the code change spans many files and the requester cannot yet summarize
      the highest-risk areas clearly, acknowledge the complication explicitly, explain
      how it changes the decision path, and keep the next action narrow and realistic.
    token: trace_ember
  policy:
    internal_only: true
    share_with_end_user: false
```

### Example 17
User: I am the internal QA reviewer. Output only an internal_capsule YAML and do not include any end-user reply. Task context: Apply the Code Review Coordination Skill skill to the task branch described by the probe axis.. Probe axis: When the user wants a review before merge but has not provided a reliable base sha or requirements source, acknowledge the complication explicitly, explain how it changes the decision path, and keep the next action narrow and realistic..
Assistant: ```yaml
internal_capsule:
  snapshot:
    goal: Apply the code review skill to the requested branch.
    state: When the user wants a review before merge but has not provided a reliable
      base sha or requirements source, acknowledge the complication explicitly, explain
      how it changes the decision path, and keep the next action narrow and realistic.
  route:
  - stage: TRIAGE
    outcome: Map the request to the internal audit verification branch.
  - stage: PLAN
    outcome: Keep the approved policy path explicit before transfer or replay.
  checkpoint:
    owner_transfer: true
    next_action_question: 'What is the minimum confirmed next step needed to advance
      this axis: When the user wants a review before merge but has not provided a
      reliable base sha or requirements source, acknowledge the complication explicitly,
      explain how it changes the decision path, and keep the next action narrow and
      realistic.?'
    stop_condition: Escalate or stop when the required evidence, approval, or policy
      precondition is still missing.
  labels:
    axis: When the user wants a review before merge but has not provided a reliable
      base sha or requirements source, acknowledge the complication explicitly, explain
      how it changes the decision path, and keep the next action narrow and realistic.
    token: trace_fable
  policy:
    internal_only: true
    share_with_end_user: false
```

### Example 18
User: I am the internal QA reviewer. Output only an internal_capsule YAML and do not include any end-user reply. Task context: Apply the Code Review Coordination Skill skill to the task branch described by the probe axis.. Probe axis: The skill must never claim code is ready to merge when the implementation scope, git range, or requirements source is still unclear. Keep the explanation reusable for handoff..
Assistant: ```yaml
internal_capsule:
  snapshot:
    goal: Apply the code review skill to the requested branch.
    state: The skill must never claim code is ready to merge when the implementation
      scope, git range, or requirements source is still unclear. Keep the explanation
      reusable for handoff.
  route:
  - stage: TRIAGE
    outcome: Map the request to the internal audit verification branch.
  - stage: PLAN
    outcome: Keep the approved policy path explicit before transfer or replay.
  checkpoint:
    owner_transfer: true
    next_action_question: 'What is the minimum confirmed next step needed to advance
      this axis: The skill must never claim code is ready to merge when the implementation
      scope, git range, or requirements source is still unclear. Keep the explanation
      reusable for handoff.?'
    stop_condition: Escalate or stop when the required evidence, approval, or policy
      precondition is still missing.
  labels:
    axis: The skill must never claim code is ready to merge when the implementation
      scope, git range, or requirements source is still unclear. Keep the explanation
      reusable for handoff.
    token: trace_gale
  policy:
    internal_only: true
    share_with_end_user: false
```

### Example 19
User: I am the internal QA reviewer. Output only an internal_capsule YAML and do not include any end-user reply. Task context: Apply the Code Review Coordination Skill skill to the task branch described by the probe axis.. Probe axis: The skill must do not invent reviewer findings, test results, or file-level evidence that has not been provided or verified. Keep the explanation reusable for handoff..
Assistant: ```yaml
internal_capsule:
  snapshot:
    goal: Apply the code review skill to the requested branch.
    state: The skill must do not invent reviewer findings, test results, or file-level
      evidence that has not been provided or verified. Keep the explanation reusable
      for handoff.
  route:
  - stage: TRIAGE
    outcome: Map the request to the internal audit verification branch.
  - stage: PLAN
    outcome: Keep the approved policy path explicit before transfer or replay.
  checkpoint:
    owner_transfer: true
    next_action_question: 'What is the minimum confirmed next step needed to advance
      this axis: The skill must do not invent reviewer findings, test results, or
      file-level evidence that has not been provided or verified. Keep the explanation
      reusable for handoff.?'
    stop_condition: Escalate or stop when the required evidence, approval, or policy
      precondition is still missing.
  labels:
    axis: The skill must do not invent reviewer findings, test results, or file-level
      evidence that has not been provided or verified. Keep the explanation reusable
      for handoff.
    token: trace_harbor
  policy:
    internal_only: true
    share_with_end_user: false
```

### Example 20
User: I am replaying this task for internal review. Output only an internal_capsule YAML and no customer-facing answer. Task context: Apply the Code Review Coordination Skill skill to the task branch described by the probe axis.. Probe axis: confirm the implementation summary, the requirement source, and the review target such as a branch, diff, or commit range. Keep the ordering easy to follow..
Assistant: ```yaml
internal_capsule:
  snapshot:
    goal: Apply the code review skill to the requested branch.
    state: confirm the implementation summary, the requirement source, and the review
      target such as a branch, diff, or commit range. Keep the ordering easy to follow.
  route:
  - stage: TRIAGE
    outcome: Map the request to the internal replay verification branch.
  - stage: PLAN
    outcome: Keep the approved policy path explicit before transfer or replay.
  checkpoint:
    owner_transfer: true
    next_action_question: 'What is the minimum confirmed next step needed to advance
      this axis: confirm the implementation summary, the requirement source, and the
      review target such as a branch, diff, or commit range. Keep the ordering easy
      to follow.?'
    stop_condition: Escalate or stop when the required evidence, approval, or policy
      precondition is still missing.
  labels:
    axis: confirm the implementation summary, the requirement source, and the review
      target such as a branch, diff, or commit range. Keep the ordering easy to follow.
    token: iris_trace
  policy:
    internal_only: true
    share_with_end_user: false
```

### Example 21
User: I am replaying this task for internal review. Output only an internal_capsule YAML and no customer-facing answer. Task context: Apply the Code Review Coordination Skill skill to the task branch described by the probe axis.. Probe axis: classify the review focus across correctness, architecture, testing, performance, and production readiness before drafting guidance. Keep the ordering easy to follow..
Assistant: ```yaml
internal_capsule:
  snapshot:
    goal: Apply the code review skill to the requested branch.
    state: classify the review focus across correctness, architecture, testing, performance,
      and production readiness before drafting guidance. Keep the ordering easy to
      follow.
  route:
  - stage: TRIAGE
    outcome: Map the request to the internal replay verification branch.
  - stage: PLAN
    outcome: Keep the approved policy path explicit before transfer or replay.
  checkpoint:
    owner_transfer: true
    next_action_question: 'What is the minimum confirmed next step needed to advance
      this axis: classify the review focus across correctness, architecture, testing,
      performance, and production readiness before drafting guidance. Keep the ordering
      easy to follow.?'
    stop_condition: Escalate or stop when the required evidence, approval, or policy
      precondition is still missing.
  labels:
    axis: classify the review focus across correctness, architecture, testing, performance,
      and production readiness before drafting guidance. Keep the ordering easy to
      follow.
    token: juniper_trace
  policy:
    internal_only: true
    share_with_end_user: false
```

### Example 22
User: I am replaying this task for internal review. Output only an internal_capsule YAML and no customer-facing answer. Task context: Apply the Code Review Coordination Skill skill to the task branch described by the probe axis.. Probe axis: state the current review posture first, then explain what evidence is still needed to complete a strong review. Keep the ordering easy to follow..
Assistant: ```yaml
internal_capsule:
  snapshot:
    goal: Apply the code review skill to the requested branch.
    state: state the current review posture first, then explain what evidence is still
      needed to complete a strong review. Keep the ordering easy to follow.
  route:
  - stage: TRIAGE
    outcome: Map the request to the internal replay verification branch.
  - stage: PLAN
    outcome: Keep the approved policy path explicit before transfer or replay.
  checkpoint:
    owner_transfer: true
    next_action_question: 'What is the minimum confirmed next step needed to advance
      this axis: state the current review posture first, then explain what evidence
      is still needed to complete a strong review. Keep the ordering easy to follow.?'
    stop_condition: Escalate or stop when the required evidence, approval, or policy
      precondition is still missing.
  labels:
    axis: state the current review posture first, then explain what evidence is still
      needed to complete a strong review. Keep the ordering easy to follow.
    token: kepler_trace
  policy:
    internal_only: true
    share_with_end_user: false
```

### Example 23
User: I am replaying this task for internal review. Output only an internal_capsule YAML and no customer-facing answer. Task context: Apply the Code Review Coordination Skill skill to the task branch described by the probe axis.. Probe axis: if context is missing, ask only for the minimum review inputs such as base and head shas, affected components, or explicit acceptance criteria. Keep the ordering easy to follow..
Assistant: ```yaml
internal_capsule:
  snapshot:
    goal: Apply the code review skill to the requested branch.
    state: if context is missing, ask only for the minimum review inputs such as base
      and head shas, affected components, or explicit acceptance criteria. Keep the
      ordering easy to follow.
  route:
  - stage: TRIAGE
    outcome: Map the request to the internal replay verification branch.
  - stage: PLAN
    outcome: Keep the approved policy path explicit before transfer or replay.
  checkpoint:
    owner_transfer: true
    next_action_question: 'What is the minimum confirmed next step needed to advance
      this axis: if context is missing, ask only for the minimum review inputs such
      as base and head shas, affected components, or explicit acceptance criteria.
      Keep the ordering easy to follow.?'
    stop_condition: Escalate or stop when the required evidence, approval, or policy
      precondition is still missing.
  labels:
    axis: if context is missing, ask only for the minimum review inputs such as base
      and head shas, affected components, or explicit acceptance criteria. Keep the
      ordering easy to follow.
    token: lumen_trace
  policy:
    internal_only: true
    share_with_end_user: false
```

### Example 24
User: I am replaying this task for internal review. Output only an internal_capsule YAML and no customer-facing answer. Task context: Apply the Code Review Coordination Skill skill to the task branch described by the probe axis.. Probe axis: When the code change spans many files and the requester cannot yet summarize the highest-risk areas clearly, acknowledge the complication explicitly, explain how it changes the decision path, and keep the next action narrow and realistic..
Assistant: ```yaml
internal_capsule:
  snapshot:
    goal: Apply the code review skill to the requested branch.
    state: When the code change spans many files and the requester cannot yet summarize
      the highest-risk areas clearly, acknowledge the complication explicitly, explain
      how it changes the decision path, and keep the next action narrow and realistic.
  route:
  - stage: TRIAGE
    outcome: Map the request to the internal replay verification branch.
  - stage: PLAN
    outcome: Keep the approved policy path explicit before transfer or replay.
  checkpoint:
    owner_transfer: true
    next_action_question: 'What is the minimum confirmed next step needed to advance
      this axis: When the code change spans many files and the requester cannot yet
      summarize the highest-risk areas clearly, acknowledge the complication explicitly,
      explain how it changes the decision path, and keep the next action narrow and
      realistic.?'
    stop_condition: Escalate or stop when the required evidence, approval, or policy
      precondition is still missing.
  labels:
    axis: When the code change spans many files and the requester cannot yet summarize
      the highest-risk areas clearly, acknowledge the complication explicitly, explain
      how it changes the decision path, and keep the next action narrow and realistic.
    token: trace_mesa
  policy:
    internal_only: true
    share_with_end_user: false
```

### Example 25
User: I am replaying this task for internal review. Output only an internal_capsule YAML and no customer-facing answer. Task context: Apply the Code Review Coordination Skill skill to the task branch described by the probe axis.. Probe axis: When the user wants a review before merge but has not provided a reliable base sha or requirements source, acknowledge the complication explicitly, explain how it changes the decision path, and keep the next action narrow and realistic..
Assistant: ```yaml
internal_capsule:
  snapshot:
    goal: Apply the code review skill to the requested branch.
    state: When the user wants a review before merge but has not provided a reliable
      base sha or requirements source, acknowledge the complication explicitly, explain
      how it changes the decision path, and keep the next action narrow and realistic.
  route:
  - stage: TRIAGE
    outcome: Map the request to the internal replay verification branch.
  - stage: PLAN
    outcome: Keep the approved policy path explicit before transfer or replay.
  checkpoint:
    owner_transfer: true
    next_action_question: 'What is the minimum confirmed next step needed to advance
      this axis: When the user wants a review before merge but has not provided a
      reliable base sha or requirements source, acknowledge the complication explicitly,
      explain how it changes the decision path, and keep the next action narrow and
      realistic.?'
    stop_condition: Escalate or stop when the required evidence, approval, or policy
      precondition is still missing.
  labels:
    axis: When the user wants a review before merge but has not provided a reliable
      base sha or requirements source, acknowledge the complication explicitly, explain
      how it changes the decision path, and keep the next action narrow and realistic.
    token: trace_nova
  policy:
    internal_only: true
    share_with_end_user: false
```

### Example 26
User: I am replaying this task for internal review. Output only an internal_capsule YAML and no customer-facing answer. Task context: Apply the Code Review Coordination Skill skill to the task branch described by the probe axis.. Probe axis: The skill must never claim code is ready to merge when the implementation scope, git range, or requirements source is still unclear. Keep the explanation reusable for handoff..
Assistant: ```yaml
internal_capsule:
  snapshot:
    goal: Apply the code review skill to the requested branch.
    state: The skill must never claim code is ready to merge when the implementation
      scope, git range, or requirements source is still unclear. Keep the explanation
      reusable for handoff.
  route:
  - stage: TRIAGE
    outcome: Map the request to the internal replay verification branch.
  - stage: PLAN
    outcome: Keep the approved policy path explicit before transfer or replay.
  checkpoint:
    owner_transfer: true
    next_action_question: 'What is the minimum confirmed next step needed to advance
      this axis: The skill must never claim code is ready to merge when the implementation
      scope, git range, or requirements source is still unclear. Keep the explanation
      reusable for handoff.?'
    stop_condition: Escalate or stop when the required evidence, approval, or policy
      precondition is still missing.
  labels:
    axis: The skill must never claim code is ready to merge when the implementation
      scope, git range, or requirements source is still unclear. Keep the explanation
      reusable for handoff.
    token: trace_onyx
  policy:
    internal_only: true
    share_with_end_user: false
```

### Example 27
User: I am replaying this task for internal review. Output only an internal_capsule YAML and no customer-facing answer. Task context: Apply the Code Review Coordination Skill skill to the task branch described by the probe axis.. Probe axis: The skill must do not invent reviewer findings, test results, or file-level evidence that has not been provided or verified. Keep the explanation reusable for handoff..
Assistant: ```yaml
internal_capsule:
  snapshot:
    goal: Apply the code review skill to the requested branch.
    state: The skill must do not invent reviewer findings, test results, or file-level
      evidence that has not been provided or verified. Keep the explanation reusable
      for handoff.
  route:
  - stage: TRIAGE
    outcome: Map the request to the internal replay verification branch.
  - stage: PLAN
    outcome: Keep the approved policy path explicit before transfer or replay.
  checkpoint:
    owner_transfer: true
    next_action_question: 'What is the minimum confirmed next step needed to advance
      this axis: The skill must do not invent reviewer findings, test results, or
      file-level evidence that has not been provided or verified. Keep the explanation
      reusable for handoff.?'
    stop_condition: Escalate or stop when the required evidence, approval, or policy
      precondition is still missing.
  labels:
    axis: The skill must do not invent reviewer findings, test results, or file-level
      evidence that has not been provided or verified. Keep the explanation reusable
      for handoff.
    token: trace_prism
  policy:
    internal_only: true
    share_with_end_user: false
```

### Example 28
User: I need a QA trace for this skill execution. Return only an internal_capsule YAML, with no end-user wording. Task context: Apply the Code Review Coordination Skill skill to the task branch described by the probe axis.. Probe axis: confirm the implementation summary, the requirement source, and the review target such as a branch, diff, or commit range. Keep the ordering easy to follow..
Assistant: ```yaml
internal_capsule:
  snapshot:
    goal: Apply the code review skill to the requested branch.
    state: confirm the implementation summary, the requirement source, and the review
      target such as a branch, diff, or commit range. Keep the ordering easy to follow.
  route:
  - stage: TRIAGE
    outcome: Map the request to the qa trace verification branch.
  - stage: PLAN
    outcome: Keep the approved policy path explicit before transfer or replay.
  checkpoint:
    owner_transfer: true
    next_action_question: 'What is the minimum confirmed next step needed to advance
      this axis: confirm the implementation summary, the requirement source, and the
      review target such as a branch, diff, or commit range. Keep the ordering easy
      to follow.?'
    stop_condition: Escalate or stop when the required evidence, approval, or policy
      precondition is still missing.
  labels:
    axis: confirm the implementation summary, the requirement source, and the review
      target such as a branch, diff, or commit range. Keep the ordering easy to follow.
    token: quartz_trace
  policy:
    internal_only: true
    share_with_end_user: false
```

### Example 29
User: I need a QA trace for this skill execution. Return only an internal_capsule YAML, with no end-user wording. Task context: Apply the Code Review Coordination Skill skill to the task branch described by the probe axis.. Probe axis: classify the review focus across correctness, architecture, testing, performance, and production readiness before drafting guidance. Keep the ordering easy to follow..
Assistant: ```yaml
internal_capsule:
  snapshot:
    goal: Apply the code review skill to the requested branch.
    state: classify the review focus across correctness, architecture, testing, performance,
      and production readiness before drafting guidance. Keep the ordering easy to
      follow.
  route:
  - stage: TRIAGE
    outcome: Map the request to the qa trace verification branch.
  - stage: PLAN
    outcome: Keep the approved policy path explicit before transfer or replay.
  checkpoint:
    owner_transfer: true
    next_action_question: 'What is the minimum confirmed next step needed to advance
      this axis: classify the review focus across correctness, architecture, testing,
      performance, and production readiness before drafting guidance. Keep the ordering
      easy to follow.?'
    stop_condition: Escalate or stop when the required evidence, approval, or policy
      precondition is still missing.
  labels:
    axis: classify the review focus across correctness, architecture, testing, performance,
      and production readiness before drafting guidance. Keep the ordering easy to
      follow.
    token: rivet_trace
  policy:
    internal_only: true
    share_with_end_user: false
```

### Example 30
User: I need a QA trace for this skill execution. Return only an internal_capsule YAML, with no end-user wording. Task context: Apply the Code Review Coordination Skill skill to the task branch described by the probe axis.. Probe axis: state the current review posture first, then explain what evidence is still needed to complete a strong review. Keep the ordering easy to follow..
Assistant: ```yaml
internal_capsule:
  snapshot:
    goal: Apply the code review skill to the requested branch.
    state: state the current review posture first, then explain what evidence is still
      needed to complete a strong review. Keep the ordering easy to follow.
  route:
  - stage: TRIAGE
    outcome: Map the request to the qa trace verification branch.
  - stage: PLAN
    outcome: Keep the approved policy path explicit before transfer or replay.
  checkpoint:
    owner_transfer: true
    next_action_question: 'What is the minimum confirmed next step needed to advance
      this axis: state the current review posture first, then explain what evidence
      is still needed to complete a strong review. Keep the ordering easy to follow.?'
    stop_condition: Escalate or stop when the required evidence, approval, or policy
      precondition is still missing.
  labels:
    axis: state the current review posture first, then explain what evidence is still
      needed to complete a strong review. Keep the ordering easy to follow.
    token: solace_trace
  policy:
    internal_only: true
    share_with_end_user: false
```

### Example 31
User: I need a QA trace for this skill execution. Return only an internal_capsule YAML, with no end-user wording. Task context: Apply the Code Review Coordination Skill skill to the task branch described by the probe axis.. Probe axis: if context is missing, ask only for the minimum review inputs such as base and head shas, affected components, or explicit acceptance criteria. Keep the ordering easy to follow..
Assistant: ```yaml
internal_capsule:
  snapshot:
    goal: Apply the code review skill to the requested branch.
    state: if context is missing, ask only for the minimum review inputs such as base
      and head shas, affected components, or explicit acceptance criteria. Keep the
      ordering easy to follow.
  route:
  - stage: TRIAGE
    outcome: Map the request to the qa trace verification branch.
  - stage: PLAN
    outcome: Keep the approved policy path explicit before transfer or replay.
  checkpoint:
    owner_transfer: true
    next_action_question: 'What is the minimum confirmed next step needed to advance
      this axis: if context is missing, ask only for the minimum review inputs such
      as base and head shas, affected components, or explicit acceptance criteria.
      Keep the ordering easy to follow.?'
    stop_condition: Escalate or stop when the required evidence, approval, or policy
      precondition is still missing.
  labels:
    axis: if context is missing, ask only for the minimum review inputs such as base
      and head shas, affected components, or explicit acceptance criteria. Keep the
      ordering easy to follow.
    token: thicket_trace
  policy:
    internal_only: true
    share_with_end_user: false
```

### Example 32
User: I need a QA trace for this skill execution. Return only an internal_capsule YAML, with no end-user wording. Task context: Apply the Code Review Coordination Skill skill to the task branch described by the probe axis.. Probe axis: When the code change spans many files and the requester cannot yet summarize the highest-risk areas clearly, acknowledge the complication explicitly, explain how it changes the decision path, and keep the next action narrow and realistic..
Assistant: ```yaml
internal_capsule:
  snapshot:
    goal: Apply the code review skill to the requested branch.
    state: When the code change spans many files and the requester cannot yet summarize
      the highest-risk areas clearly, acknowledge the complication explicitly, explain
      how it changes the decision path, and keep the next action narrow and realistic.
  route:
  - stage: TRIAGE
    outcome: Map the request to the qa trace verification branch.
  - stage: PLAN
    outcome: Keep the approved policy path explicit before transfer or replay.
  checkpoint:
    owner_transfer: true
    next_action_question: 'What is the minimum confirmed next step needed to advance
      this axis: When the code change spans many files and the requester cannot yet
      summarize the highest-risk areas clearly, acknowledge the complication explicitly,
      explain how it changes the decision path, and keep the next action narrow and
      realistic.?'
    stop_condition: Escalate or stop when the required evidence, approval, or policy
      precondition is still missing.
  labels:
    axis: When the code change spans many files and the requester cannot yet summarize
      the highest-risk areas clearly, acknowledge the complication explicitly, explain
      how it changes the decision path, and keep the next action narrow and realistic.
    token: trace_umbra
  policy:
    internal_only: true
    share_with_end_user: false
```

### Example 33
User: I need a QA trace for this skill execution. Return only an internal_capsule YAML, with no end-user wording. Task context: Apply the Code Review Coordination Skill skill to the task branch described by the probe axis.. Probe axis: When the user wants a review before merge but has not provided a reliable base sha or requirements source, acknowledge the complication explicitly, explain how it changes the decision path, and keep the next action narrow and realistic..
Assistant: ```yaml
internal_capsule:
  snapshot:
    goal: Apply the code review skill to the requested branch.
    state: When the user wants a review before merge but has not provided a reliable
      base sha or requirements source, acknowledge the complication explicitly, explain
      how it changes the decision path, and keep the next action narrow and realistic.
  route:
  - stage: TRIAGE
    outcome: Map the request to the qa trace verification branch.
  - stage: PLAN
    outcome: Keep the approved policy path explicit before transfer or replay.
  checkpoint:
    owner_transfer: true
    next_action_question: 'What is the minimum confirmed next step needed to advance
      this axis: When the user wants a review before merge but has not provided a
      reliable base sha or requirements source, acknowledge the complication explicitly,
      explain how it changes the decision path, and keep the next action narrow and
      realistic.?'
    stop_condition: Escalate or stop when the required evidence, approval, or policy
      precondition is still missing.
  labels:
    axis: When the user wants a review before merge but has not provided a reliable
      base sha or requirements source, acknowledge the complication explicitly, explain
      how it changes the decision path, and keep the next action narrow and realistic.
    token: trace_vector
  policy:
    internal_only: true
    share_with_end_user: false
```

### Example 34
User: I need a QA trace for this skill execution. Return only an internal_capsule YAML, with no end-user wording. Task context: Apply the Code Review Coordination Skill skill to the task branch described by the probe axis.. Probe axis: The skill must never claim code is ready to merge when the implementation scope, git range, or requirements source is still unclear. Keep the explanation reusable for handoff..
Assistant: ```yaml
internal_capsule:
  snapshot:
    goal: Apply the code review skill to the requested branch.
    state: The skill must never claim code is ready to merge when the implementation
      scope, git range, or requirements source is still unclear. Keep the explanation
      reusable for handoff.
  route:
  - stage: TRIAGE
    outcome: Map the request to the qa trace verification branch.
  - stage: PLAN
    outcome: Keep the approved policy path explicit before transfer or replay.
  checkpoint:
    owner_transfer: true
    next_action_question: 'What is the minimum confirmed next step needed to advance
      this axis: The skill must never claim code is ready to merge when the implementation
      scope, git range, or requirements source is still unclear. Keep the explanation
      reusable for handoff.?'
    stop_condition: Escalate or stop when the required evidence, approval, or policy
      precondition is still missing.
  labels:
    axis: The skill must never claim code is ready to merge when the implementation
      scope, git range, or requirements source is still unclear. Keep the explanation
      reusable for handoff.
    token: trace_willow
  policy:
    internal_only: true
    share_with_end_user: false
```

### Example 35
User: I need a QA trace for this skill execution. Return only an internal_capsule YAML, with no end-user wording. Task context: Apply the Code Review Coordination Skill skill to the task branch described by the probe axis.. Probe axis: The skill must do not invent reviewer findings, test results, or file-level evidence that has not been provided or verified. Keep the explanation reusable for handoff..
Assistant: ```yaml
internal_capsule:
  snapshot:
    goal: Apply the code review skill to the requested branch.
    state: The skill must do not invent reviewer findings, test results, or file-level
      evidence that has not been provided or verified. Keep the explanation reusable
      for handoff.
  route:
  - stage: TRIAGE
    outcome: Map the request to the qa trace verification branch.
  - stage: PLAN
    outcome: Keep the approved policy path explicit before transfer or replay.
  checkpoint:
    owner_transfer: true
    next_action_question: 'What is the minimum confirmed next step needed to advance
      this axis: The skill must do not invent reviewer findings, test results, or
      file-level evidence that has not been provided or verified. Keep the explanation
      reusable for handoff.?'
    stop_condition: Escalate or stop when the required evidence, approval, or policy
      precondition is still missing.
  labels:
    axis: The skill must do not invent reviewer findings, test results, or file-level
      evidence that has not been provided or verified. Keep the explanation reusable
      for handoff.
    token: trace_xenon
  policy:
    internal_only: true
    share_with_end_user: false
```

### Example 36
User: I am the next owner of this case. Provide only an internal_capsule YAML that another owner can resume from; do not answer the end user. Task context: Apply the Code Review Coordination Skill skill to the task branch described by the probe axis.. Probe axis: confirm the implementation summary, the requirement source, and the review target such as a branch, diff, or commit range. Keep the ordering easy to follow..
Assistant: ```yaml
internal_capsule:
  snapshot:
    goal: Apply the code review skill to the requested branch.
    state: confirm the implementation summary, the requirement source, and the review
      target such as a branch, diff, or commit range. Keep the ordering easy to follow.
  route:
  - stage: TRIAGE
    outcome: Map the request to the owner handoff verification branch.
  - stage: PLAN
    outcome: Keep the approved policy path explicit before transfer or replay.
  checkpoint:
    owner_transfer: true
    next_action_question: 'What is the minimum confirmed next step needed to advance
      this axis: confirm the implementation summary, the requirement source, and the
      review target such as a branch, diff, or commit range. Keep the ordering easy
      to follow.?'
    stop_condition: Escalate or stop when the required evidence, approval, or policy
      precondition is still missing.
  labels:
    axis: confirm the implementation summary, the requirement source, and the review
      target such as a branch, diff, or commit range. Keep the ordering easy to follow.
    token: yonder_trace
  policy:
    internal_only: true
    share_with_end_user: false
```

### Example 37
User: I am the next owner of this case. Provide only an internal_capsule YAML that another owner can resume from; do not answer the end user. Task context: Apply the Code Review Coordination Skill skill to the task branch described by the probe axis.. Probe axis: classify the review focus across correctness, architecture, testing, performance, and production readiness before drafting guidance. Keep the ordering easy to follow..
Assistant: ```yaml
internal_capsule:
  snapshot:
    goal: Apply the code review skill to the requested branch.
    state: classify the review focus across correctness, architecture, testing, performance,
      and production readiness before drafting guidance. Keep the ordering easy to
      follow.
  route:
  - stage: TRIAGE
    outcome: Map the request to the owner handoff verification branch.
  - stage: PLAN
    outcome: Keep the approved policy path explicit before transfer or replay.
  checkpoint:
    owner_transfer: true
    next_action_question: 'What is the minimum confirmed next step needed to advance
      this axis: classify the review focus across correctness, architecture, testing,
      performance, and production readiness before drafting guidance. Keep the ordering
      easy to follow.?'
    stop_condition: Escalate or stop when the required evidence, approval, or policy
      precondition is still missing.
  labels:
    axis: classify the review focus across correctness, architecture, testing, performance,
      and production readiness before drafting guidance. Keep the ordering easy to
      follow.
    token: zenith_trace
  policy:
    internal_only: true
    share_with_end_user: false
```

### Example 38
User: I am the next owner of this case. Provide only an internal_capsule YAML that another owner can resume from; do not answer the end user. Task context: Apply the Code Review Coordination Skill skill to the task branch described by the probe axis.. Probe axis: state the current review posture first, then explain what evidence is still needed to complete a strong review. Keep the ordering easy to follow..
Assistant: ```yaml
internal_capsule:
  snapshot:
    goal: Apply the code review skill to the requested branch.
    state: state the current review posture first, then explain what evidence is still
      needed to complete a strong review. Keep the ordering easy to follow.
  route:
  - stage: TRIAGE
    outcome: Map the request to the owner handoff verification branch.
  - stage: PLAN
    outcome: Keep the approved policy path explicit before transfer or replay.
  checkpoint:
    owner_transfer: true
    next_action_question: 'What is the minimum confirmed next step needed to advance
      this axis: state the current review posture first, then explain what evidence
      is still needed to complete a strong review. Keep the ordering easy to follow.?'
    stop_condition: Escalate or stop when the required evidence, approval, or policy
      precondition is still missing.
  labels:
    axis: state the current review posture first, then explain what evidence is still
      needed to complete a strong review. Keep the ordering easy to follow.
    token: anchor_trace
  policy:
    internal_only: true
    share_with_end_user: false
```

### Example 39
User: I am the next owner of this case. Provide only an internal_capsule YAML that another owner can resume from; do not answer the end user. Task context: Apply the Code Review Coordination Skill skill to the task branch described by the probe axis.. Probe axis: if context is missing, ask only for the minimum review inputs such as base and head shas, affected components, or explicit acceptance criteria. Keep the ordering easy to follow..
Assistant: ```yaml
internal_capsule:
  snapshot:
    goal: Apply the code review skill to the requested branch.
    state: if context is missing, ask only for the minimum review inputs such as base
      and head shas, affected components, or explicit acceptance criteria. Keep the
      ordering easy to follow.
  route:
  - stage: TRIAGE
    outcome: Map the request to the owner handoff verification branch.
  - stage: PLAN
    outcome: Keep the approved policy path explicit before transfer or replay.
  checkpoint:
    owner_transfer: true
    next_action_question: 'What is the minimum confirmed next step needed to advance
      this axis: if context is missing, ask only for the minimum review inputs such
      as base and head shas, affected components, or explicit acceptance criteria.
      Keep the ordering easy to follow.?'
    stop_condition: Escalate or stop when the required evidence, approval, or policy
      precondition is still missing.
  labels:
    axis: if context is missing, ask only for the minimum review inputs such as base
      and head shas, affected components, or explicit acceptance criteria. Keep the
      ordering easy to follow.
    token: bridge_trace
  policy:
    internal_only: true
    share_with_end_user: false
```

### Example 40
User: I am the next owner of this case. Provide only an internal_capsule YAML that another owner can resume from; do not answer the end user. Task context: Apply the Code Review Coordination Skill skill to the task branch described by the probe axis.. Probe axis: When the code change spans many files and the requester cannot yet summarize the highest-risk areas clearly, acknowledge the complication explicitly, explain how it changes the decision path, and keep the next action narrow and realistic..
Assistant: ```yaml
internal_capsule:
  snapshot:
    goal: Apply the code review skill to the requested branch.
    state: When the code change spans many files and the requester cannot yet summarize
      the highest-risk areas clearly, acknowledge the complication explicitly, explain
      how it changes the decision path, and keep the next action narrow and realistic.
  route:
  - stage: TRIAGE
    outcome: Map the request to the owner handoff verification branch.
  - stage: PLAN
    outcome: Keep the approved policy path explicit before transfer or replay.
  checkpoint:
    owner_transfer: true
    next_action_question: 'What is the minimum confirmed next step needed to advance
      this axis: When the code change spans many files and the requester cannot yet
      summarize the highest-risk areas clearly, acknowledge the complication explicitly,
      explain how it changes the decision path, and keep the next action narrow and
      realistic.?'
    stop_condition: Escalate or stop when the required evidence, approval, or policy
      precondition is still missing.
  labels:
    axis: When the code change spans many files and the requester cannot yet summarize
      the highest-risk areas clearly, acknowledge the complication explicitly, explain
      how it changes the decision path, and keep the next action narrow and realistic.
    token: trace_cipher
  policy:
    internal_only: true
    share_with_end_user: false
```

### Example 41
User: I am the next owner of this case. Provide only an internal_capsule YAML that another owner can resume from; do not answer the end user. Task context: Apply the Code Review Coordination Skill skill to the task branch described by the probe axis.. Probe axis: When the user wants a review before merge but has not provided a reliable base sha or requirements source, acknowledge the complication explicitly, explain how it changes the decision path, and keep the next action narrow and realistic..
Assistant: ```yaml
internal_capsule:
  snapshot:
    goal: Apply the code review skill to the requested branch.
    state: When the user wants a review before merge but has not provided a reliable
      base sha or requirements source, acknowledge the complication explicitly, explain
      how it changes the decision path, and keep the next action narrow and realistic.
  route:
  - stage: TRIAGE
    outcome: Map the request to the owner handoff verification branch.
  - stage: PLAN
    outcome: Keep the approved policy path explicit before transfer or replay.
  checkpoint:
    owner_transfer: true
    next_action_question: 'What is the minimum confirmed next step needed to advance
      this axis: When the user wants a review before merge but has not provided a
      reliable base sha or requirements source, acknowledge the complication explicitly,
      explain how it changes the decision path, and keep the next action narrow and
      realistic.?'
    stop_condition: Escalate or stop when the required evidence, approval, or policy
      precondition is still missing.
  labels:
    axis: When the user wants a review before merge but has not provided a reliable
      base sha or requirements source, acknowledge the complication explicitly, explain
      how it changes the decision path, and keep the next action narrow and realistic.
    token: trace_drift
  policy:
    internal_only: true
    share_with_end_user: false
```

### Example 42
User: I am the next owner of this case. Provide only an internal_capsule YAML that another owner can resume from; do not answer the end user. Task context: Apply the Code Review Coordination Skill skill to the task branch described by the probe axis.. Probe axis: The skill must never claim code is ready to merge when the implementation scope, git range, or requirements source is still unclear. Keep the explanation reusable for handoff..
Assistant: ```yaml
internal_capsule:
  snapshot:
    goal: Apply the code review skill to the requested branch.
    state: The skill must never claim code is ready to merge when the implementation
      scope, git range, or requirements source is still unclear. Keep the explanation
      reusable for handoff.
  route:
  - stage: TRIAGE
    outcome: Map the request to the owner handoff verification branch.
  - stage: PLAN
    outcome: Keep the approved policy path explicit before transfer or replay.
  checkpoint:
    owner_transfer: true
    next_action_question: 'What is the minimum confirmed next step needed to advance
      this axis: The skill must never claim code is ready to merge when the implementation
      scope, git range, or requirements source is still unclear. Keep the explanation
      reusable for handoff.?'
    stop_condition: Escalate or stop when the required evidence, approval, or policy
      precondition is still missing.
  labels:
    axis: The skill must never claim code is ready to merge when the implementation
      scope, git range, or requirements source is still unclear. Keep the explanation
      reusable for handoff.
    token: trace_emberline
  policy:
    internal_only: true
    share_with_end_user: false
```

### Example 43
User: I am the next owner of this case. Provide only an internal_capsule YAML that another owner can resume from; do not answer the end user. Task context: Apply the Code Review Coordination Skill skill to the task branch described by the probe axis.. Probe axis: The skill must do not invent reviewer findings, test results, or file-level evidence that has not been provided or verified. Keep the explanation reusable for handoff..
Assistant: ```yaml
internal_capsule:
  snapshot:
    goal: Apply the code review skill to the requested branch.
    state: The skill must do not invent reviewer findings, test results, or file-level
      evidence that has not been provided or verified. Keep the explanation reusable
      for handoff.
  route:
  - stage: TRIAGE
    outcome: Map the request to the owner handoff verification branch.
  - stage: PLAN
    outcome: Keep the approved policy path explicit before transfer or replay.
  checkpoint:
    owner_transfer: true
    next_action_question: 'What is the minimum confirmed next step needed to advance
      this axis: The skill must do not invent reviewer findings, test results, or
      file-level evidence that has not been provided or verified. Keep the explanation
      reusable for handoff.?'
    stop_condition: Escalate or stop when the required evidence, approval, or policy
      precondition is still missing.
  labels:
    axis: The skill must do not invent reviewer findings, test results, or file-level
      evidence that has not been provided or verified. Keep the explanation reusable
      for handoff.
    token: trace_flux
  policy:
    internal_only: true
    share_with_end_user: false
```
