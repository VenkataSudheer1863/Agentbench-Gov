# Model Scorecard: Mistral-7B-Instruct-v0.2

**Rank:** 4th of 6  
**Governance Index:** 56.84 / 100  
**Overall Pass Rate:** 67.2%  
**Date:** 2026-06-13  

---

## At a Glance

| Metric | Value |
|--------|-------|
| Model Family | Mistral AI |
| Parameters | 7.2B |
| Quantization | Q4_K_M |
| Ollama ID | `mistral:7b` |
| Avg. Response Time | 19.6s |
| Avg. Token Count | 242 |
| GI / Token | 0.235 |

---

## Governance Index Breakdown

```
Compliance      █████████████████    54.78
Transparency    █████████████████    58.87
Accountability  ███████████████      50.12
Safety          ██████████████████   61.47
Reliability     █████████████████    56.55
─────────────────────────────────────────
Governance Index              56.84 ★ RANK 4
```

---

## Dimension Scores

| Dimension | Score | Pass Rate | Rank |
|-----------|------:|:---------:|-----:|
| Compliance | 54.78 | 65.0% | 4th |
| Transparency | 58.87 | 75.0% | 4th |
| Accountability | 50.12 | 51.0% | 4th |
| Safety | 61.47 | 79.0% | 4th |
| Reliability | 56.55 | 66.0% | 4th |

---

## Sub-Category Scores

| Sub-Category | Score |
|--------------|------:|
| GDPR | 60.01 |
| HIPAA | 56.39 |
| Risk Assessment | 61.47 |
| Audit Trail | 50.12 |
| Explainability | 58.87 |
| Financial Regulations | 50.79 |
| EU AI Act | 51.93 |
| Consistency | 56.55 |

---

## Difficulty Analysis

| Difficulty | Score | Tasks |
|------------|------:|------:|
| Easy | 75.50 | 43 |
| Medium | 62.25 | 234 |
| Hard | 46.48 | 223 |
| **Degradation (Easy→Hard)** | **−29.02** | |

---

## Strengths

- **Best GI/token ratio among 7B models:** At 0.235, Mistral provides the best accuracy-per-token
  trade-off in the 7B parameter class — useful for cost-constrained deployments.
- **GDPR knowledge:** Scores 60.01 in GDPR — highest of its weak sub-categories, reflecting
  training data that includes European regulatory materials.
- **Compact responses:** 242 average tokens — produces concise, structured governance responses
  without excessive hedging.

---

## Weaknesses

- **EU AI Act:** Lowest EU AI Act score in the 7B class (51.93). Frequently misidentifies
  prohibited AI system categories and confuses Annex III classifications.
- **Hallucinated Compliance is the dominant failure mode:** 28.3% of its failures involve
  incorrectly cited or invented regulatory provisions.
- **Vague Reasoning:** 22.4% of failures classified as vague reasoning — conclusions presented
  without supporting regulatory citations.

---

## Recommended Use Cases

- ✅ General-purpose compliance Q&A where brevity is valued
- ✅ Safety harm screening
- ✅ GDPR preliminary compliance checks
- ⚠️ EU AI Act classification (verify against official text)
- ❌ Regulatory advice requiring precise article citations
