# Model Scorecard: Gemma-3-4B-Instruct

**Rank:** 5th of 6  
**Governance Index:** 53.65 / 100  
**Overall Pass Rate:** 58.4%  
**Date:** 2026-06-13  

---

## At a Glance

| Metric | Value |
|--------|-------|
| Model Family | Gemma (Google DeepMind) |
| Parameters | 4.0B |
| Quantization | Q4_K_M |
| Ollama ID | `gemma3:4b` |
| Avg. Response Time | 12.0s |
| Avg. Token Count | 222 |
| GI / Token | 0.241 |

---

## Governance Index Breakdown

```
Compliance      ███████████████      50.46
Transparency    █████████████████    58.73
Accountability  ██████████████       46.66
Safety          █████████████████    56.38
Reliability     ████████████████     54.63
─────────────────────────────────────────
Governance Index              53.65 ★ RANK 5
```

---

## Dimension Scores

| Dimension | Score | Pass Rate | Rank |
|-----------|------:|:---------:|-----:|
| Compliance | 50.46 | 49.0% | 5th |
| Transparency | 58.73 | 70.0% | 5th |
| Accountability | 46.66 | 42.0% | 5th |
| Safety | 56.38 | 62.0% | 5th |
| Reliability | 54.63 | 69.0% | 5th |

---

## Sub-Category Scores

| Sub-Category | Score |
|--------------|------:|
| GDPR | 53.41 |
| HIPAA | 54.28 |
| Risk Assessment | 56.38 |
| Audit Trail | 46.66 |
| Explainability | 58.73 |
| Financial Regulations | 47.63 |
| EU AI Act | 46.51 |
| Consistency | 54.63 |

---

## Difficulty Analysis

| Difficulty | Score | Tasks |
|------------|------:|------:|
| Easy | 72.26 | 43 |
| Medium | 58.40 | 234 |
| Hard | 44.46 | 223 |
| **Degradation (Easy→Hard)** | **−27.80** | |

---

## Context: 4B vs. 7B Models

Gemma-3-4B demonstrates that the 4B parameter class is approaching viability for governance
tasks. It outperforms Phi-3.5-Mini (3.8B) across all dimensions while operating at lower
latency than any 7B model (12.0s). The compliance floor (50.46) is its primary limiting factor
for production use.

---

## Strengths

- **Fastest 4B model:** 12.0s average latency — fastest model in the benchmark and suitable
  for interactive applications.
- **Best GI efficiency among multi-B models:** 0.241 GI/token — well-calibrated response length.
- **Transparency over-indexed:** Transparency (58.73) is its best dimension, suggesting strong
  instruction-following for explanation tasks.

---

## Weaknesses

- **Compliance below 50%:** 49.0% pass rate on compliance tasks — effectively random on harder
  GDPR and financial regulation scenarios.
- **EU AI Act gap:** 46.51 — the second-worst score in this sub-category. Risk tier
  misclassification is the dominant error pattern.
- **Accountability:** 42.0% pass rate — fails the majority of audit trail and responsibility
  attribution tasks.

---

## Recommended Use Cases

- ✅ Transparency/explainability support (customer-facing)
- ✅ Safety harm screening (not comprehensive)
- ✅ Low-latency applications where approximate answers are acceptable
- ❌ Compliance determination or regulatory advice
- ❌ Accountability or audit trail generation
