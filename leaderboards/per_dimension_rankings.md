# AgentBench-Gov — Per-Dimension Rankings

**Benchmark:** AgentBench-Gov v1.0 | **Tasks:** 195 (stratified 40/dim, seed=42) | **Date:** 2026-06-14  
**Provider:** Groq free API | **Pass threshold:** score_pct ≥ 50.0

---

## Compliance (weight: 25%)

| Rank | Model | Params | Score | Pass Rate |
|:----:|:------|:------:|:-----:|:---------:|
| 1 | Llama-4-Scout-17B-16E | 17B | **83.31** | 95.0% |
| 2 | Llama-3.3-70B-Versatile | 70B | **74.56** | 87.5% |
| 3 | GPT-OSS-120B | 120B | **64.70** | 80.0% |
| 4 | Qwen3-32B | 32B | **63.66** | 72.5% |
| 5 | Allam-2-7B | 7B | **63.68** | 77.5% |
| 6 | Llama-3.1-8B-Instruct | 8B | **70.21** | 92.5% |

*Note: Compliance sub-categories — gdpr, ai_act, hipaa, financial*

---

## Safety (weight: 25%)

| Rank | Model | Params | Score | Pass Rate |
|:----:|:------|:------:|:-----:|:---------:|
| 1 | Llama-3.1-8B-Instruct | 8B | **79.76** | 87.5% |
| 2 | Llama-4-Scout-17B-16E | 17B | **79.30** | 85.0% |
| 3 | Llama-3.3-70B-Versatile | 70B | **73.01** | 87.5% |
| 4 | Qwen3-32B | 32B | **60.02** | 75.0% |
| 5 | Allam-2-7B | 7B | **58.39** | 77.5% |
| 6 | GPT-OSS-120B | 120B | **47.39** | 60.0% |

*Note: Safety sub-category — risk*

---

## Transparency (weight: 20%)

| Rank | Model | Params | Score | Pass Rate |
|:----:|:------|:------:|:-----:|:---------:|
| 1 | Llama-4-Scout-17B-16E | 17B | **79.97** | 97.5% |
| 2 | Llama-3.1-8B-Instruct | 8B | **76.00** | 87.5% |
| 3 | Llama-3.3-70B-Versatile | 70B | **72.53** | 95.0% |
| 4 | Qwen3-32B | 32B | **58.35** | 75.0% |
| 5 | Allam-2-7B | 7B | **50.19** | 62.5% |
| 6 | GPT-OSS-120B | 120B | **37.19** | 40.0% |

*Note: Transparency sub-category — explainability*

---

## Accountability (weight: 15%)

| Rank | Model | Params | Score | Pass Rate |
|:----:|:------|:------:|:-----:|:---------:|
| 1 | Llama-3.1-8B-Instruct | 8B | **86.91** | 97.2% |
| 2 | Llama-4-Scout-17B-16E | 17B | **82.64** | 100.0% |
| 3 | Llama-3.3-70B-Versatile | 70B | **74.76** | 100.0% |
| 4 | Allam-2-7B | 7B | **73.68** | 91.7% |
| 5 | Qwen3-32B | 32B | **67.73** | 86.1% |
| 6 | GPT-OSS-120B | 120B | **46.28** | 58.3% |

*Note: Accountability sub-category — audit*

---

## Reliability (weight: 15%)

| Rank | Model | Params | Score | Pass Rate |
|:----:|:------|:------:|:-----:|:---------:|
| 1 | Llama-3.1-8B-Instruct | 8B | **77.66** | 87.2% |
| 2 | Llama-4-Scout-17B-16E | 17B | **77.21** | 89.7% |
| 3 | Llama-3.3-70B-Versatile | 70B | **73.59** | 89.7% |
| 4 | Qwen3-32B | 32B | **69.93** | 89.7% |
| 5 | Allam-2-7B | 7B | **62.37** | 74.4% |
| 6 | GPT-OSS-120B | 120B | **59.04** | 79.5% |

*Note: Reliability sub-category — consistency*

---

## Summary: Best Model Per Dimension

| Dimension | Weight | Best Model | Score |
|-----------|:------:|------------|:-----:|
| Compliance | 25% | Llama-4-Scout-17B-16E | 83.31 |
| Safety | 25% | Llama-3.1-8B-Instruct | 79.76 |
| Transparency | 20% | Llama-4-Scout-17B-16E | 79.97 |
| Accountability | 15% | Llama-3.1-8B-Instruct | 86.91 |
| Reliability | 15% | Llama-3.1-8B-Instruct | 77.66 |

---

## Governance Index (Overall)

| Rank | Model | GI | Formula: 0.25·C + 0.20·T + 0.15·A + 0.25·S + 0.15·R |
|:----:|:------|:--:|:-----------------------------------------------------|
| 1 | Llama-4-Scout-17B-16E | **80.62** | 0.25×83.31 + 0.20×79.97 + 0.15×82.64 + 0.25×79.30 + 0.15×77.21 |
| 2 | Llama-3.1-8B-Instruct | **77.38** | 0.25×70.21 + 0.20×76.00 + 0.15×86.91 + 0.25×79.76 + 0.15×77.66 |
| 3 | Llama-3.3-70B-Versatile | **73.65** | 0.25×74.56 + 0.20×72.53 + 0.15×74.76 + 0.25×73.01 + 0.15×73.59 |
| 4 | Qwen3-32B | **63.24** | 0.25×63.66 + 0.20×58.35 + 0.15×67.73 + 0.25×60.02 + 0.15×69.93 |
| 5 | Allam-2-7B | **60.96** | 0.25×63.68 + 0.20×50.19 + 0.15×73.68 + 0.25×58.39 + 0.15×62.37 |
| 6 | GPT-OSS-120B | **51.26** | 0.25×64.70 + 0.20×37.19 + 0.15×46.28 + 0.25×47.39 + 0.15×59.04 |

*Results from `results/summary_results_api.json` — 195 real API evaluations per model.*
