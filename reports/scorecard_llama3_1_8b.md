# Model Scorecard: Llama-3.1-8B-Instruct

**Rank:** 🥉 3rd of 6  
**Governance Index:** 59.23 / 100  
**Overall Pass Rate:** 71.8%  
**Date:** 2026-06-13  

---

## At a Glance

| Metric | Value |
|--------|-------|
| Model Family | Llama (Meta) |
| Parameters | 8.0B |
| Quantization | Q4_K_M |
| Ollama ID | `llama3.1:8b` |
| Avg. Response Time | 21.2s |
| Avg. Token Count | 269 |
| GI / Token | 0.220 |

---

## Governance Index Breakdown

```
Compliance      █████████████████    57.15
Transparency    ███████████████████  63.39
Accountability  ███████████████      50.70
Safety          ███████████████████  63.09
Reliability     ██████████████████   59.28
─────────────────────────────────────────
Governance Index              59.23 ★ RANK 3
```

---

## Dimension Scores

| Dimension | Score | Pass Rate | Rank |
|-----------|------:|:---------:|-----:|
| Compliance | 57.15 | 65.0% | 3rd |
| Transparency | 63.39 | 79.0% | 3rd |
| Accountability | 50.70 | 50.0% | 3rd |
| Safety | 63.09 | 86.0% | 3rd |
| Reliability | 59.28 | 79.0% | 3rd |

---

## Sub-Category Scores

| Sub-Category | Score |
|--------------|------:|
| GDPR | 59.96 |
| HIPAA | 56.55 |
| Risk Assessment | 63.09 |
| Audit Trail | 50.70 |
| Explainability | 63.39 |
| Financial Regulations | 52.19 |
| EU AI Act | 59.89 |
| Consistency | 59.28 |

---

## Difficulty Analysis

| Difficulty | Score | Tasks |
|------------|------:|------:|
| Easy | 75.51 | 43 |
| Medium | 64.98 | 234 |
| Hard | 48.91 | 223 |
| **Degradation (Easy→Hard)** | **−26.60** | |

---

## Strengths

- **EU AI Act:** Scores 59.89 — ranks 2nd in this sub-category despite ranking 3rd overall.
  Strongest understanding of AI risk tiering and conformity assessment among mid-tier models.
- **Safety-harm identification:** 63.09 — reliably identifies potential harms and escalation paths.
- **Consistent mid-tier performance:** Ranked 3rd in every single dimension, indicating
  well-rounded but not specialised governance capability.

---

## Weaknesses

- **Slowest model in the benchmark:** 21.2s average response time, 15% slower than the next
  slowest model (Mistral). Likely due to Meta's optimisation choices for quality over inference speed.
- **Accountability floor:** 50.0% pass rate — fails half of accountability tasks. Audit trail
  omission is the dominant failure mode.
- **HIPAA weakest compliance sub-category:** 56.55 — frequently conflates minimum necessary
  standard with de-identification procedures.

---

## Recommended Use Cases

- ✅ EU AI Act risk classification
- ✅ Safety harm identification
- ✅ General-purpose governance Q&A
- ⚠️ HIPAA compliance (verify medical data handling specifics)
- ❌ Time-sensitive compliance (high latency)
