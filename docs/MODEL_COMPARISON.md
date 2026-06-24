# MODEL_COMPARISON.md — AgentBench-Gov (API Edition)

**Date:** 2026-06-14  |  **Tasks:** 139 (deduplicated unique tasks)

---

## 1. Best vs Worst Model

| Metric | Llama4-Scout (Best) | GPT-OSS-120B (Worst) | Gap |
|:-------|:----:|:-----:|:---:|
| Governance Index | 77.50 | 52.25 | 25.25 |
| Overall Pass Rate | 90.6% | 66.9% | 23.7pp |
| Parameters | 17B | 120B | — |
| Family | Llama4 | GPT-OSS | — |

---

## 2. Full Comparison Matrix

| Model | GI | Rank | vs Best (Gap) |
|:------|:--:|:----:|:-------------:|
| Llama4-Scout (17B) | 77.50 | 1 | — |
| Llama-3.3-70B (70B) | 72.08 | 2 | -5.42 |
| Llama-3.1-8B (8B) | 71.41 | 3 | -6.09 |
| Allam-2-7B (7B) | 59.84 | 4 | -17.66 |
| Qwen3-32B (32B) | 59.54 | 5 | -17.96 |
| GPT-OSS-120B (120B) | 52.25 | 6 | -25.25 |

---

## 3. Key Findings

### Dimension Leaders

- **Compliance:** Llama4-Scout (83.3)
- **Transparency:** Llama4-Scout (75.8)
- **Accountability:** Llama4-Scout (85.5)
- **Safety:** Llama4-Scout (71.4)
- **Reliability:** Llama4-Scout (72.2)

### Model Size vs Performance

- Llama4-Scout (17B): GI=77.50
- Llama-3.3-70B (70B): GI=72.08
- Llama-3.1-8B (8B): GI=71.41
- Allam-2-7B (7B): GI=59.84
- Qwen3-32B (32B): GI=59.54
- GPT-OSS-120B (120B): GI=52.25
