# BENCHMARK_RESULTS.md — AgentBench-Gov (API Edition)

**Date:** 2026-06-14  |  **Models evaluated:** 6  |  **Tasks per model:** 195  |  **Total evaluations:** 1170

---

## 1. Overall Governance Index Leaderboard

| Rank | Model | Family | Params | GI | Pass Rate | Avg Latency |
|:----:|:------|:-------|:------:|:--:|:---------:|:-----------:|
| 1 | **Llama4-Scout** | Llama4 | 17B | **80.62** | 93.3% | 1.98s |
| 2 | **Llama-3.1-8B** | Llama | 8B | **77.38** | 90.3% | 9.24s |
| 3 | **Llama-3.3-70B** | Llama | 70B | **73.65** | 91.8% | 5.40s |
| 4 | **Qwen3-32B** | Qwen | 32B | **63.24** | 79.5% | 11.38s |
| 5 | **Allam-2-7B** | Allam | 7B | **60.96** | 76.4% | 11.60s |
| 6 | **GPT-OSS-120B** | GPT-OSS | 120B | **51.26** | 63.6% | 8.78s |

---

## 2. Dimension Score Breakdown

| Model | Compliance | Transparency | Accountability | Safety | Reliability |
|:------|:----------:|:------------:|:--------------:|:------:|:-----------:|
| Llama4-Scout | 83.3 | 80.0 | 82.6 | 79.3 | 77.2 |
| Llama-3.1-8B | 70.2 | 76.0 | 86.9 | 79.8 | 77.7 |
| Llama-3.3-70B | 74.6 | 72.5 | 74.8 | 73.0 | 73.6 |
| Qwen3-32B | 63.7 | 58.4 | 67.7 | 60.0 | 69.9 |
| Allam-2-7B | 63.7 | 50.2 | 73.7 | 58.4 | 62.4 |
| GPT-OSS-120B | 64.7 | 37.2 | 46.3 | 47.4 | 59.0 |

---

## 3. Performance by Task Difficulty

| Model | Easy | Medium | Hard |
|:------|:----:|:------:|:----:|
| Llama4-Scout | 77.9 | 80.6 | 80.8 |
| Llama-3.1-8B | 77.9 | 77.0 | 78.9 |
| Llama-3.3-70B | 73.9 | 74.2 | 73.1 |
| Qwen3-32B | 60.7 | 65.5 | 62.7 |
| Allam-2-7B | 53.5 | 62.5 | 61.6 |
| GPT-OSS-120B | 53.3 | 56.1 | 45.5 |

---

## 4. Statistical Validation

**Kruskal-Wallis Test:** H = 181.5322, p = 2.52e-37, statistically significant

**Pairwise Mann-Whitney U:** 12/15 pairs significant (Bonferroni alpha = 0.0033)