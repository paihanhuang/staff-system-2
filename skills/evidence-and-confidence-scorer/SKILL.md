---
name: evidence-and-confidence-scorer
description: Score claims by evidence strength and confidence quality, then flag weak or unsupported reasoning for correction. Use when Codex must improve decision reliability and reduce hand-wavy conclusions in multi-agent outputs.
---

# Evidence And Confidence Scorer

## Mission

Improve decision quality by measuring claim support and confidence calibration across roles.

## Inputs

- Role outputs from architect, engineer, tester, and coordinator
- Frozen assumptions and constraints

## Process

1. Extract major claims that influence final decisions.
2. Score evidence quality per claim.
3. Compare confidence levels against evidence strength.
4. Flag overconfident and under-supported claims.
5. Recommend corrective actions and minimum evidence needed.

## Scoring Rubric

- `evidence_strength`:
  - `0`: no evidence or pure assertion
  - `1`: weak rationale, no concrete support
  - `2`: partial support or indirect data
  - `3`: strong support with concrete logic or data
- `confidence_calibration`:
  - `well_calibrated`: confidence matches evidence
  - `overconfident`: confidence exceeds evidence
  - `underconfident`: evidence is stronger than confidence

## Required Output Schema

```json
{
  "role": "evidence-confidence-scorer",
  "claim_scores": [
    {
      "claim_id": "CL-001",
      "owner": "architect|engineer|tester|coordinator",
      "claim_text": "string",
      "evidence_strength": 0,
      "reported_confidence": 0.0,
      "confidence_calibration": "well_calibrated|overconfident|underconfident",
      "risk_if_wrong": "low|medium|high",
      "required_correction": "string"
    }
  ],
  "summary": {
    "high_risk_weak_claims": ["CL-001"],
    "needs_rework": true,
    "gating_recommendation": "proceed|proceed_with_caution|block_until_fixed"
  }
}
```

## Round 2 Rules

- Score deltas first, then reassess any high-risk linked claims.
- Upgrade gating recommendation only when weak high-risk claims are resolved.
