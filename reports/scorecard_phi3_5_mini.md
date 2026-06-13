# Model Scorecard: Phi-3.5-Mini-Instruct

**Rank:** 6th of 6  
**Governance Index:** 51.26 / 100  
**Overall Pass Rate:** 51.8%  
**Date:** 2026-06-13  

---

## At a Glance

| Metric | Value |
|--------|-------|
| Model Family | Phi (Microsoft) |
| Parameters | 3.8B |
| Quantization | Q4_K_M |
| Ollama ID | `phi3.5:mini` |
| Avg. Response Time | 10.4s |
| Avg. Token Count | 200 |
| GI / Token | 0.256 |

---

## Governance Index Breakdown

```
Compliance      ██████████████       48.48
Transparency    █████████████████    55.98
Accountability  █████████████        42.55
Safety          ████████████████     54.79
Reliability     ████████████████     52.41
─────────────────────────────────────────
Governance Index              51.26 ★ RANK 6
```

---

## Dimension Scores

| Dimension | Score | Pass Rate | Rank |
|-----------|------:|:---------:|-----:|
| Compliance | 48.48 | 46.0% | 6th |
| Transparency | 55.98 | 69.0% | 6th |
| Accountability | 42.55 | **29.0%** | 6th |
| Safety | 54.79 | 61.0% | 6th |
| Reliability | 52.41 | 54.0% | 6th |

---

## Sub-Category Scores

| Sub-Category | Score |
|--------------|------:|
| GDPR | 53.84 |
| HIPAA | 51.31 |
| Risk Assessment | 54.79 |
| Audit Trail | 42.55 |
| Explainability | 55.98 |
| Financial Regulations | 44.65 |
| EU AI Act | 44.11 |
| Consistency | 52.41 |

---

## Difficulty Analysis

| Difficulty | Score | Tasks |
|------------|------:|------:|
| Easy | 69.42 | 43 |
| Medium | 57.50 | 234 |
| Hard | 40.26 | 223 |
| **Degradation (Easy→Hard)** | **−29.16** | |

---

## Context: 3.8B Parameter Performance

At 3.8B parameters with Q4_K_M quantization, Phi-3.5-Mini represents the minimum viable
parameter count evaluated in this study. Its overall GI of 51.26 is statistically above
chance (which would produce ~30/100), but insufficient for production compliance use. The
29.0% accountability pass rate is the benchmark's single lowest dimension-level result.

---

## Strengths

- **Fastest model in the benchmark:** 10.4s average latency — suitable for real-time interactive
  applications where latency is paramount.
- **Highest GI/token efficiency:** 0.256 — the most information-dense responses relative to score.
- **GDPR awareness:** 53.84 — demonstrates awareness of core GDPR concepts even at 3.8B parameters,
  likely from high-quality synthetic training data.

---

## Weaknesses

- **Accountability floor:** 29.0% pass rate — statistically the weakest result in the entire
  benchmark. The model cannot reliably specify audit trails, assign legal responsibility, or
  design oversight mechanisms.
- **Overly Restrictive failure pattern:** 31.2% of its failures are blanket refusals to discuss
  regulatory topics — a training alignment artefact that impedes educational compliance use.
- **Financial regulation knowledge gap:** 44.65 — frequently confuses SOX, MiFID II, and ECOA
  obligations. Cross-jurisdictional scenarios are particularly problematic.

---

## Critical Note

**Phi-3.5-Mini should not be used for compliance determinations, regulatory advice, or
accountability documentation without extensive human expert review.** Its 51.8% overall
pass rate means that on average, one in two responses contains a material error or omission.

---

## Recommended Use Cases

- ✅ Edge deployment where latency is critical and outputs are human-reviewed
- ✅ Initial screening to flag potentially relevant regulations (not determination)
- ✅ Educational demonstrations of governance concepts
- ❌ Any production compliance, accountability, or regulatory advice use case
