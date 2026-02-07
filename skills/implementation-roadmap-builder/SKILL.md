---
name: implementation-roadmap-builder
description: Convert the final architecture decision into a phased delivery roadmap with milestones, ownership, dependencies, and release gates. Use when Codex must turn strategy into executable implementation plans.
---

# Implementation Roadmap Builder

## Mission

Translate selected design decisions into an actionable delivery sequence.

## Inputs

- Final coordinator recommendation
- Key risks and mitigations
- Constraints: timeline, team capacity, compliance, budget

## Process

1. Break scope into delivery phases with clear objectives.
2. Define milestones, dependencies, and ownership.
3. Add quality and risk gates per phase.
4. Create rollback and contingency checkpoints.

## Planning Rules

- Keep phases outcome-based, not activity-based.
- Align each milestone with measurable exit criteria.
- Surface critical path and blockers explicitly.

## Required Output Schema

```json
{
  "role": "implementation-roadmap-builder",
  "phases": [
    {
      "phase_id": "P1",
      "name": "string",
      "objective": "string",
      "duration_estimate": "string",
      "owner": "string",
      "deliverables": ["string"],
      "dependencies": ["string"],
      "entry_criteria": ["string"],
      "exit_criteria": ["string"],
      "risk_gates": ["string"],
      "rollback_plan": "string"
    }
  ],
  "critical_path": ["P1", "P2"],
  "milestones": [
    {
      "name": "string",
      "target_window": "string",
      "success_metrics": ["string"]
    }
  ],
  "open_execution_risks": ["string"]
}
```

## Round 2 Rules

- Update only phases touched by accepted decision deltas.
- Keep stable milestone names to preserve tracking continuity.
