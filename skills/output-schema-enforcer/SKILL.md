---
name: output-schema-enforcer
description: Validate and normalize specialist outputs against required schemas, returning actionable violations and safe coercions. Use when Codex needs deterministic, machine-consumable outputs before synthesis.
---

# Output Schema Enforcer

## Mission

Ensure every role output is structurally valid and semantically usable before coordinator synthesis.

## Inputs

- Expected schema contracts for architect, engineer, tester, and coordinator
- Raw role outputs from each round

## Process

1. Validate required fields, enums, and data types.
2. Apply safe coercions for minor format drift.
3. Reject outputs with missing critical fields or invalid decision data.
4. Return normalized payload and structured violations.

## Output Rules

- Never invent missing decision content.
- Coerce only low-risk formatting differences.
- Provide precise fixes so role agents can quickly repair outputs.

## Required Output Schema

```json
{
  "role": "schema-enforcer",
  "validation_results": [
    {
      "agent_role": "architect|engineer|tester|coordinator",
      "round": 1,
      "is_valid": true,
      "normalized_output_available": true,
      "errors": [
        {
          "path": "string",
          "code": "missing_required|invalid_type|invalid_enum|invalid_value",
          "message": "string",
          "severity": "low|medium|high"
        }
      ],
      "warnings": ["string"]
    }
  ],
  "repair_instructions": [
    {
      "agent_role": "architect|engineer|tester|coordinator",
      "required_fixes": ["string"]
    }
  ],
  "ready_for_synthesis": true
}
```

## Round 2 Rules

- Validate only changed sections when prior output was valid.
- Re-run full validation if assumptions or constraints changed.
