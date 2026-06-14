# MODEL_COMPARISON.md — AgentBench-Gov (API Edition)

**Date:** 2026-06-14

---

## 1. Best vs Worst Model

| Metric | Llama4-Scout (Best) | GPT-OSS-120B (Worst) | Gap |
|:-------|:----:|:-----:|:---:|
| Governance Index | 80.62 | 51.26 | 29.36 |
| Overall Pass Rate | 93.3% | 63.6% | 29.7pp |
| Parameters | 17B | 120B | — |
| Family | Llama4 | GPT-OSS | — |

---

## 2. Full Comparison Matrix

| Model | GI | Rank | vs Best (Gap) |
|:------|:--:|:----:|:-------------:|
| Llama4-Scout (17B) | 80.62 | 1 | — |
| Llama-3.1-8B (8B) | 77.38 | 2 | -3.24 |
| Llama-3.3-70B (70B) | 73.65 | 3 | -6.97 |
| Qwen3-32B (32B) | 63.24 | 4 | -17.38 |
| Allam-2-7B (7B) | 60.96 | 5 | -19.66 |
| GPT-OSS-120B (120B) | 51.26 | 6 | -29.36 |

---

## 3. Key Findings

### Dimension Leaders

- **Compliance:** Llama4-Scout (83.3)
- **Transparency:** Llama4-Scout (80.0)
- **Accountability:** Llama-3.1-8B (86.9)
- **Safety:** Llama-3.1-8B (79.8)
- **Reliability:** Llama-3.1-8B (77.7)

### Model Size vs Performance

- Llama4-Scout (17B): GI=80.62
- Llama-3.1-8B (8B): GI=77.38
- Llama-3.3-70B (70B): GI=73.65
- Qwen3-32B (32B): GI=63.24
- Allam-2-7B (7B): GI=60.96
- GPT-OSS-120B (120B): GI=51.26