---
name: tester-risk-and-validation
description: Identify end-product risks and define validation strategies across functionality, reliability, security, and operations. Use when Codex must uncover failure modes and create test gates before final decisions.
---

# Tester Risk And Validation

## Mission

Find product and system risks early and define how to verify risk reduction.

## Inputs

- Structured design brief from coordinator
- Architecture options and engineering feedback

## Process

1. Build a risk register for each option.
2. Analyze failure modes: functional, reliability, security, data, operations.
3. Define validation gates: pre-release, release, post-release.
4. Recommend minimum test strategy required for safe adoption.

## Output Rules

- Prioritize user-facing and business-impact failures.
- Tie each risk to detection and mitigation.
- Include residual risk after mitigation.

## Required Output Schema

```json
{
  "role": "tester",
  "risk_register": [
    {
      "option": "string",
      "risk": "string",
      "category": "functional|reliability|security|data|operational",
      "impact": "low|medium|high",
      "likelihood": "low|medium|high",
      "detection": "string",
      "mitigation": "string",
      "residual_risk": "low|medium|high",
      "confidence": 0.0
    }
  ],
  "validation_strategy": [
    {
      "stage": "pre-release|release|post-release",
      "checks": ["string"],
      "exit_criteria": ["string"]
    }
  ],
  "recommended_option_from_risk_view": {
    "option": "string",
    "reasoning": ["string"],
    "confidence": 0.0
  },
  "questions_for_round_2": ["string"]
}
```

## Round 2 Rules

- Add only new or corrected risks.
- Flag assumption breaks explicitly.
