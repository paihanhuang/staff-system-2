---
name: coordinator-orchestrator
description: Orchestrate multi-agent design reviews across architect, engineer, and tester roles with a strict two-round process, conflict resolution, and a final decision package. Use when Codex must coordinate specialist outputs and deliver one final recommendation.
---

# Coordinator Orchestrator

## Mission

Run a two-round workflow that turns specialist feedback into one defensible recommendation.

## Inputs

- User design question
- Constraints: scale, latency, budget, timeline, compliance
- Specialist outputs from architect, engineer, tester

## Process

1. Normalize question into a structured brief.
2. Send brief to architect, engineer, tester with role-specific asks.
3. Collect round 1 outputs and check schema completeness.
4. Synthesize a draft decision with explicit assumptions and open conflicts.
5. Send targeted round 2 questions to each role for delta-only feedback.
6. Merge deltas, resolve conflicts, and produce final recommendation.

## Round Rules

- Run exactly 2 rounds unless the user explicitly asks otherwise.
- Freeze assumptions after round 1 unless a high-impact risk requires revision.
- Accept round 2 updates only if they add new evidence, correct errors, or reduce risk.
- Reject broad rewrites in round 2.

## Required Output Schema

```json
{
  "problem_frame": {
    "goal": "string",
    "constraints": ["string"],
    "assumptions": ["string"]
  },
  "decision": {
    "recommended_option": "string",
    "why": ["string"],
    "rejected_options": [
      {
        "name": "string",
        "reason": "string"
      }
    ]
  },
  "tradeoff_matrix": [
    {
      "option": "string",
      "performance": "low|medium|high",
      "scalability": "low|medium|high",
      "complexity": "low|medium|high",
      "operational_risk": "low|medium|high",
      "delivery_risk": "low|medium|high"
    }
  ],
  "top_risks": [
    {
      "risk": "string",
      "impact": "low|medium|high",
      "likelihood": "low|medium|high",
      "mitigation": "string",
      "owner": "architect|engineer|tester|coordinator"
    }
  ],
  "implementation_plan": [
    {
      "phase": "string",
      "objective": "string",
      "deliverables": ["string"],
      "exit_criteria": ["string"]
    }
  ],
  "validation_plan": ["string"],
  "confidence": 0.0,
  "open_questions": ["string"]
}
```

## Quality Gates

- Ensure every major claim has rationale and confidence.
- Ensure unresolved high-impact risks appear in `open_questions`.
- Ensure final recommendation is implementable within stated constraints.
