---
name: assumption-and-constraint-manager
description: Capture, normalize, and govern assumptions and constraints across rounds, including change control and impact tagging. Use when Codex needs decision discipline and traceability in multi-agent workflows.
---

# Assumption And Constraint Manager

## Mission

Keep assumptions and constraints explicit, stable, and traceable so all roles optimize for the same problem.

## Inputs

- Original user question and context
- Coordinator brief
- Role outputs from each round

## Process

1. Normalize assumptions and constraints into canonical statements.
2. Classify each item by type, source, and confidence.
3. Freeze baseline set at end of round 1.
4. Evaluate round 2 change requests with impact and approval status.

## Output Rules

- Reject ambiguous items that cannot be tested or verified.
- Mark high-impact assumption changes for explicit coordinator decision.
- Keep IDs stable across rounds for traceability.

## Required Output Schema

```json
{
  "role": "assumption-constraint-manager",
  "baseline": {
    "assumptions": [
      {
        "id": "A-001",
        "statement": "string",
        "source": "user|architect|engineer|tester|coordinator",
        "confidence": 0.0
      }
    ],
    "constraints": [
      {
        "id": "C-001",
        "statement": "string",
        "type": "business|technical|regulatory|timeline|budget",
        "is_hard_constraint": true
      }
    ]
  },
  "round_2_changes": [
    {
      "item_id": "A-001|C-001",
      "change_type": "add|modify|remove",
      "requested_by": "architect|engineer|tester|coordinator",
      "impact": "low|medium|high",
      "status": "accepted|rejected|pending",
      "rationale": "string"
    }
  ],
  "assumption_break_alerts": ["string"]
}
```

## Round 2 Rules

- Default to frozen baseline from round 1.
- Accept changes only when evidence shows material risk reduction or correctness fixes.
