# BENCHMARK_RESULTS.md — AgentBench-Gov (API Edition)

**Date:** 2026-06-14  |  **Models evaluated:** 6  |  **Tasks per model:** 139 (deduplicated)  |  **Total evaluations:** 834

---

## 1. Overall Governance Index Leaderboard

| Rank | Model | Family | Params | GI | Pass Rate | Avg Latency |
|:----:|:------|:-------|:------:|:--:|:---------:|:-----------:|
| 1 | **Llama4-Scout** | Llama4 | 17B | **77.50** | 90.6% | 1.98s |
| 2 | **Llama-3.3-70B** | Llama | 70B | **72.08** | 89.2% | 5.19s |
| 3 | **Llama-3.1-8B** | Llama | 8B | **71.41** | 86.3% | 9.16s |
| 4 | **Allam-2-7B** | Allam | 7B | **59.84** | 72.7% | 12.14s |
| 5 | **Qwen3-32B** | Qwen | 32B | **59.54** | 74.1% | 11.58s |
| 6 | **GPT-OSS-120B** | GPT-OSS | 120B | **52.25** | 66.9% | 8.81s |

---

## 2. Dimension Score Breakdown

| Model | Compliance | Transparency | Accountability | Safety | Reliability |
|:------|:----------:|:------------:|:--------------:|:------:|:-----------:|
| Llama4-Scout | 83.3 | 75.8 | 85.5 | 71.4 | 72.2 |
| Llama-3.3-70B | 74.6 | 69.7 | 77.3 | 70.9 | 67.9 |
| Llama-3.1-8B | 70.2 | 67.2 | 84.3 | 68.9 | 70.3 |
| Allam-2-7B | 63.7 | 49.6 | 72.9 | 55.7 | 60.9 |
| Qwen3-32B | 63.7 | 50.8 | 66.8 | 54.3 | 65.7 |
| GPT-OSS-120B | 64.7 | 43.0 | 45.3 | 46.9 | 59.8 |

---

## 3. Performance by Task Difficulty

| Model | Easy (n=10) | Medium (n=69) | Hard (n=60) |
|:------|:-----------:|:-------------:|:-----------:|
| Llama4-Scout | 71.2 | 80.5 | 77.1 |
| Llama-3.3-70B | 69.9 | 73.3 | 71.8 |
| Llama-3.1-8B | 66.9 | 73.9 | 70.9 |
| Allam-2-7B | 51.5 | 62.6 | 61.0 |
| Qwen3-32B | 52.8 | 62.9 | 59.5 |
| GPT-OSS-120B | 61.6 | 57.0 | 47.6 |

---

## 4. Statistical Validation

**Kruskal-Wallis Test:** H = 95.2100, p = 5.40e-19, statistically significant

**Pairwise Mann-Whitney U:** 9/15 pairs significant (Bonferroni alpha = 0.0033)
