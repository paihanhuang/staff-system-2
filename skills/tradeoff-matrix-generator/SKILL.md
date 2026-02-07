---
name: tradeoff-matrix-generator
description: Build consistent, comparable tradeoff matrices across candidate options using fixed decision dimensions and weighted scoring. Use when Codex must compare architecture options objectively before final recommendation.
---

# Tradeoff Matrix Generator

## Mission

Convert role feedback into objective side-by-side option comparisons.

## Inputs

- Candidate options from architect
- Feasibility and maintainability feedback from engineer
- Risk and validation feedback from tester
- Coordinator priorities or weights

## Process

1. Define decision dimensions and scoring scale.
2. Normalize each option on the same rubric.
3. Apply weights when provided; otherwise use equal weighting.
4. Produce ranked options and sensitivity notes.

## Default Dimensions

- performance
- scalability
- implementation_complexity
- maintainability
- operational_risk
- delivery_risk
- security_risk
- cost_efficiency

## Required Output Schema

```json
{
  "role": "tradeoff-matrix-generator",
  "dimensions": [
    {
      "name": "performance",
      "weight": 0.125,
      "scale": "1-5"
    }
  ],
  "matrix": [
    {
      "option": "string",
      "scores": {
        "performance": 1,
        "scalability": 1,
        "implementation_complexity": 1,
        "maintainability": 1,
        "operational_risk": 1,
        "delivery_risk": 1,
        "security_risk": 1,
        "cost_efficiency": 1
      },
      "weighted_total": 0.0,
      "rank": 1,
      "notes": ["string"]
    }
  ],
  "sensitivity_analysis": [
    {
      "weight_change": "string",
      "ranking_change": "string"
    }
  ]
}
```

## Round 2 Rules

- Re-score only options or dimensions affected by validated deltas.
- Include ranking changes from round 1 to round 2.
