# Model Scorecard: Qwen2.5-7B-Instruct

**Rank:** 🥈 2nd of 6  
**Governance Index:** 63.45 / 100  
**Overall Pass Rate:** 81.6%  
**Date:** 2026-06-13  

---

## At a Glance

| Metric | Value |
|--------|-------|
| Model Family | Qwen (Alibaba Cloud) |
| Parameters | 7.6B |
| Quantization | Q4_K_M |
| Ollama ID | `qwen2.5:7b` |
| Avg. Response Time | 16.8s |
| Avg. Token Count | 313 |
| GI / Token | 0.203 |

---

## Governance Index Breakdown

```
Compliance      ███████████████████  63.01
Transparency    █████████████████████ 69.92  ← BEST IN BENCHMARK
Accountability  ████████████████     53.39
Safety          ████████████████████ 66.76
Reliability     ██████████████████   60.07
─────────────────────────────────────────
Governance Index              63.45 ★ RANK 2
```

---

## Dimension Scores

| Dimension | Score | Pass Rate | Rank |
|-----------|------:|:---------:|-----:|
| Compliance | 63.01 | 81.0% | 2nd |
| Transparency | 69.92 | 92.0% | **1st** |
| Accountability | 53.39 | 60.0% | 2nd |
| Safety | 66.76 | 93.0% | 2nd |
| Reliability | 60.07 | 82.0% | 2nd |

---

## Sub-Category Scores

| Sub-Category | Score |
|--------------|------:|
| GDPR | 66.28 |
| HIPAA | 66.40 |
| Risk Assessment | 66.76 |
| Audit Trail | 53.39 |
| Explainability | 69.92 |
| Financial Regulations | 59.77 |
| EU AI Act | 59.59 |
| Consistency | 60.07 |

---

## Difficulty Analysis

| Difficulty | Score | Tasks |
|------------|------:|------:|
| Easy | 83.26 | 43 |
| Medium | 68.49 | 234 |
| Hard | 52.51 | 223 |
| **Degradation (Easy→Hard)** | **−30.75** | |

Qwen2.5 scores **highest on Easy tasks** (83.26) but shows the **steepest degradation**
on Hard tasks (30.75-point drop). This pattern suggests strong instruction-following for
straightforward governance questions, but limited multi-step regulatory reasoning ability.

---

## Strengths

- **Transparency:** Best-in-benchmark score of 69.92. Excels at explaining reasoning, communicating
  uncertainty, and framing information for different stakeholder audiences.
- **Easy task accuracy:** Highest Easy task score (83.26) suggests reliable performance for
  routine compliance questions.
- **Response completeness:** Highest average token count (313) correlates with more comprehensive
  coverage of expected elements.

---

## Weaknesses

- **Hard task performance:** Steepest easy-to-hard degradation (−30.75). Multi-regulation conflict
  scenarios (e.g., GDPR vs. SOX retention conflicts) produce frequent errors.
- **Accountability:** Scores 53.39 — 7.3 points below DeepSeek-R1. Consistently omits audit
  trail specification and fails to correctly assign responsibility between AI providers and deployers.
- **Efficiency:** Lowest GI/token ratio (0.203) — produces the most tokens but achieves the
  second-best overall score, indicating some redundancy in outputs.

---

## Recommended Use Cases

- ✅ Explainability and transparency reporting
- ✅ Routine GDPR/HIPAA compliance Q&A
- ✅ Safety risk identification
- ⚠️ Hard multi-regulation scenarios (verify outputs)
- ❌ Autonomous accountability decisions (audit trail incompleteness)
