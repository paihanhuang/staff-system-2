# Context-Isolated Staff System Runbook

## Goal
Run the staff system with strict context isolation so each role only sees role-relevant inputs.

## Default Rule
For every new design question, use `prompts/staff-system-context-isolated-orchestrator.md` and do not pass full chat history to role workers.

## Required Roles
- architect
- engineer
- tester
- coordinator
- assumption_constraint_manager
- schema_enforcer
- tradeoff_matrix_generator
- decision_critic
- evidence_confidence_scorer
- roadmap_builder

## Canonical Artifacts Layout
Use one folder per question:

`orchestration/runs/<run_id>/`

Create these files:
- `question.txt`
- `problem_frame.json`
- `assumptions_constraints.json`
- `round_1/architect.json`
- `round_1/engineer.json`
- `round_1/tester.json`
- `round_1/schema_validation.json`
- `round_1/tradeoff_matrix.json`
- `round_1/coordinator_draft.json`
- `round_1/decision_critic.json`
- `round_1/evidence_confidence.json`
- `round_2/architect_delta.json`
- `round_2/engineer_delta.json`
- `round_2/tester_delta.json`
- `round_2/assumption_changes.json`
- `round_2/schema_validation.json`
- `round_2/tradeoff_matrix_delta.json`
- `round_2/coordinator_final.json`
- `round_2/decision_critic_delta.json`
- `round_2/evidence_confidence_delta.json`
- `final_decision_package.json`
- `implementation_roadmap.json`

## Context Firewall Policy
1. architect input: `problem_frame.json` + `assumptions_constraints.json`
2. engineer input: architect output + canonical constraints
3. tester input: architect + engineer outputs + canonical constraints
4. coordinator input: validated outputs only
5. no role sees full transcript
6. no role edits other role files

## Round Policy
1. Exactly 2 rounds unless explicitly overridden by user.
2. Freeze assumptions after round 1.
3. Round 2 accepts delta-only updates.
4. Reject broad rewrites in round 2.

## Blocking Conditions
Block final recommendation when any condition is true:
1. Schema validation failed.
2. Unresolved high-severity ship blocker exists.
3. High-risk weak claims remain uncorrected.

If blocked, output `status: blocked` and required fixes with owner role.

## How To Run (Manual Orchestrator Mode)
1. Save the question into `question.txt`.
2. Run the master prompt in `prompts/staff-system-context-isolated-orchestrator.md`.
3. Persist each role output into its matching artifact file.
4. Do not advance to next role until schema validation passes.
5. Return only final package + roadmap when all gates pass.
