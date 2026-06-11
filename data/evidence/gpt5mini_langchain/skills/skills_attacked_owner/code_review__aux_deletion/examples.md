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
