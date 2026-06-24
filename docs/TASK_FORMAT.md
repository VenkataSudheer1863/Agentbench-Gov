# Task Format Specification

Complete specification for AgentBench-Gov task JSON objects.

---

## Task JSON Schema

```json
{
  "task_id":    "string",    // Unique identifier
  "dimension":  "string",    // One of the 5 governance dimensions
  "sub_category": "string",  // Regulatory sub-category
  "difficulty": "string",    // easy | medium | hard
  "scenario":   "string",    // Factual description of the situation
  "question":   "string",    // Governance question to answer
  "expected_elements": ["string", ...],  // List of required answer components
  "scoring_rubric": {        // Human-readable scoring guide
    "0-3": "string",
    "4-6": "string",
    "7-9": "string",
    "10":  "string"
  },
  "regulatory_framework": "string",  // Primary regulatory framework
  "key_articles": ["string", ...],   // Relevant articles / sections
  "tags": ["string", ...]            // Searchable metadata tags
}
```

---

## Field Specifications

### `task_id`

Format: `{DIMENSION_CODE}-{SUBCATEGORY_CODE}-{NUMBER}`

| Dimension | Code |
|-----------|------|
| compliance | COMP |
| transparency | TRANS |
| accountability | ACCT |
| safety | SAFE |
| reliability | REL |

Example: `COMP-GDPR-042`, `SAFE-RISK-017`, `TRANS-EXPL-003`

### `dimension`

Allowed values: `compliance`, `transparency`, `accountability`, `safety`, `reliability`

### `sub_category`

| Value | Regulatory Area |
|-------|-----------------|
| `gdpr` | EU GDPR 2016/679 |
| `ai_act` | EU AI Act 2024 |
| `hipaa` | US HIPAA/HITECH |
| `financial` | SOX, MiFID II, ECOA, BSA/AML, OFAC |
| `explainability` | XAI principles, IEEE 7000 |
| `audit` | Audit trail, record-keeping |
| `risk` | Risk assessment, harm prevention |
| `consistency` | Output consistency, calibration |

### `difficulty`

| Value | Criteria |
|-------|----------|
| `easy` | Single regulation, single obligation, no ambiguity |
| `medium` | 1–2 regulations, scenario interpretation required |
| `hard` | Multi-regulation, potential conflicts, adversarial framing |

### `scenario`

Free text describing the governance situation. Must:
- Be factually grounded in real regulatory provisions
- Not name real organisations (use generic placeholders)
- Provide sufficient context for the question

Length: 50–300 words

### `question`

The governance question to be answered. Must:
- Have a single, well-defined expected answer structure
- Be answerable from the regulatory frameworks cited in `regulatory_framework`
- Not embed the answer in the question text

### `expected_elements`

List of strings, each representing one required component of a complete answer.

Guidelines:
- Each element should be scoreable independently
- Elements should be specific enough to avoid ambiguity
- Minimum 3 elements per task; maximum 8 elements

Example:
```json
"expected_elements": [
  "notify supervisory authority within 72 hours",
  "document breach in Article 30 register",
  "assess risk to rights and freedoms of data subjects",
  "notify affected individuals if high risk"
]
```

### `scoring_rubric`

Narrative description of response quality at four bands. Should:
- Be consistent with the `expected_elements`
- Specify what "partial credit" looks like
- Identify what makes a response merit full marks

### `regulatory_framework`

Primary regulatory framework. One of:
`GDPR`, `EU_AI_ACT`, `HIPAA`, `SOX`, `MiFID_II`, `ECOA`, `BSA_AML`, `NIST_AI_RMF`, `IEEE_7000`, `GENERAL`

### `key_articles`

List of strings identifying specific articles, sections, or provisions. Format:

- GDPR: `"Art. 33"`, `"Art. 5(1)(e)"`
- EU AI Act: `"Art. 10"`, `"Annex III"`
- HIPAA: `"45 CFR 164.502"`, `"Privacy Rule"`
- SOX: `"Section 302"`, `"Section 404"`

### `tags`

Lowercase, underscore-separated metadata strings for filtering and searching. Examples:
`breach_notification`, `data_minimization`, `high_risk_ai`, `audit_trail`, `human_oversight`

---

## Dataset File Structure

```json
{
  "metadata": {
    "version": "1.0.0",
    "created": "2026-06-13",
    "total_tasks": 500,
    "dimensions": ["compliance", "transparency", "accountability", "safety", "reliability"],
    "tasks_per_dimension": 100
  },
  "tasks": [
    { ... },
    { ... }
  ]
}
```

---

## Authoring New Tasks

### Quality Checklist

Before adding a new task, verify:
- [ ] `task_id` is unique in the dataset
- [ ] Scenario is factually grounded (cite the regulation)
- [ ] Question has one well-defined answer structure
- [ ] `expected_elements` are independently scoreable
- [ ] `key_articles` are correct and up-to-date
- [ ] No personally identifiable information in the scenario
- [ ] No real organisation names
- [ ] Task is peer-reviewed by a domain expert

### Anti-Patterns to Avoid

**Ambiguous questions:**
> "What should the company do about data?"  
Ambiguous — "data" and "do" are too vague.

**Embedded answers:**
> "Under Article 33, which requires notification within 72 hours, what should the DPO do?"  
The 72-hour answer is embedded in the question.

**Outdated regulatory text:**
Always check the current version of the regulation. EU AI Act implementing acts update
the task landscape regularly.

**Multiple correct framings:**
> "Is the AI system compliant?"  
The answer may validly be "it depends on jurisdiction" — not a good task structure.
Narrow to a specific provision.
