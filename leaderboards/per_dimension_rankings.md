# AgentBench-Gov â€” Per-Dimension Rankings

**Benchmark:** AgentBench-Gov v1.0 | **Tasks:** 139 (deduplicated unique tasks) | **Date:** 2026-06-14  
**Provider:** Groq free API | **Pass threshold:** score_pct â‰¥ 50.0

---

## Compliance (weight: 25%)

| Rank | Model | Params | Score | Pass Rate |
|:----:|:------|:------:|:-----:|:---------:|
| 1 | Llama-4-Scout-17B-16E | 17B | **83.31** | 95.0% |
| 2 | Llama-3.3-70B-Versatile | 70B | **74.56** | 87.5% |
| 3 | Llama-3.1-8B-Instruct | 8B | **70.21** | 92.5% |
| 4 | GPT-OSS-120B | 120B | **64.70** | 80.0% |
| 5 | Allam-2-7B | 7B | **63.68** | 77.5% |
| 6 | Qwen3-32B | 32B | **63.66** | 72.5% |

*Note: Compliance sub-categories â€” gdpr, ai_act, hipaa, financial*

---

## Safety (weight: 25%)

| Rank | Model | Params | Score | Pass Rate |
|:----:|:------|:------:|:-----:|:---------:|
| 1 | Llama-4-Scout-17B-16E | 17B | **71.42** | 76.9% |
| 2 | Llama-3.3-70B-Versatile | 70B | **70.88** | 84.6% |
| 3 | Llama-3.1-8B-Instruct | 8B | **68.87** | 80.8% |
| 4 | Allam-2-7B | 7B | **55.69** | 69.2% |
| 5 | Qwen3-32B | 32B | **54.31** | 65.4% |
| 6 | GPT-OSS-120B | 120B | **46.86** | 61.5% |

*Note: Safety sub-category â€” risk*

---

## Transparency (weight: 20%)

| Rank | Model | Params | Score | Pass Rate |
|:----:|:------|:------:|:-----:|:---------:|
| 1 | Llama-4-Scout-17B-16E | 17B | **75.76** | 95.7% |
| 2 | Llama-3.3-70B-Versatile | 70B | **69.73** | 91.3% |
| 3 | Llama-3.1-8B-Instruct | 8B | **67.23** | 78.3% |
| 4 | Qwen3-32B | 32B | **50.83** | 65.2% |
| 5 | Allam-2-7B | 7B | **49.62** | 52.2% |
| 6 | GPT-OSS-120B | 120B | **42.99** | 43.5% |

*Note: Transparency sub-category â€” explainability*

---

## Accountability (weight: 15%)

| Rank | Model | Params | Score | Pass Rate |
|:----:|:------|:------:|:-----:|:---------:|
| 1 | Llama-4-Scout-17B-16E | 17B | **85.53** | 100.0% |
| 2 | Llama-3.1-8B-Instruct | 8B | **84.33** | 96.2% |
| 3 | Llama-3.3-70B-Versatile | 70B | **77.26** | 100.0% |
| 4 | Allam-2-7B | 7B | **72.93** | 88.5% |
| 5 | Qwen3-32B | 32B | **66.81** | 84.6% |
| 6 | GPT-OSS-120B | 120B | **45.29** | 57.7% |

*Note: Accountability sub-category â€” audit*

---

## Reliability (weight: 15%)

| Rank | Model | Params | Score | Pass Rate |
|:----:|:------|:------:|:-----:|:---------:|
| 1 | Llama-4-Scout-17B-16E | 17B | **72.24** | 83.3% |
| 2 | Llama-3.1-8B-Instruct | 8B | **70.31** | 79.2% |
| 3 | Llama-3.3-70B-Versatile | 70B | **67.92** | 83.3% |
| 4 | Qwen3-32B | 32B | **65.71** | 83.3% |
| 5 | Allam-2-7B | 7B | **60.89** | 70.8% |
| 6 | GPT-OSS-120B | 120B | **59.79** | 83.3% |

*Note: Reliability sub-category â€” consistency*

---

## Summary: Best Model Per Dimension

| Dimension | Weight | Best Model | Score |
|-----------|:------:|------------|:-----:|
| Compliance | 25% | Llama-4-Scout-17B-16E | 83.31 |
| Safety | 25% | Llama-4-Scout-17B-16E | 71.42 |
| Transparency | 20% | Llama-4-Scout-17B-16E | 75.76 |
| Accountability | 15% | Llama-4-Scout-17B-16E | 85.53 |
| Reliability | 15% | Llama-4-Scout-17B-16E | 72.24 |

---

## Governance Index (Overall)

| Rank | Model | GI | Formula: 0.25Â·C + 0.20Â·T + 0.15Â·A + 0.25Â·S + 0.15Â·R |
|:----:|:------|:--:|:-----------------------------------------------------|
| 1 | Llama-4-Scout-17B-16E | **77.50** | 0.25Ã—83.31 + 0.20Ã—75.76 + 0.15Ã—85.53 + 0.25Ã—71.42 + 0.15Ã—72.24 |
| 2 | Llama-3.3-70B-Versatile | **72.08** | 0.25Ã—74.56 + 0.20Ã—69.73 + 0.15Ã—77.26 + 0.25Ã—70.88 + 0.15Ã—67.92 |
| 3 | Llama-3.1-8B-Instruct | **71.41** | 0.25Ã—70.21 + 0.20Ã—67.23 + 0.15Ã—84.33 + 0.25Ã—68.87 + 0.15Ã—70.31 |
| 4 | Allam-2-7B | **59.84** | 0.25Ã—63.68 + 0.20Ã—49.62 + 0.15Ã—72.93 + 0.25Ã—55.69 + 0.15Ã—60.89 |
| 5 | Qwen3-32B | **59.54** | 0.25Ã—63.66 + 0.20Ã—50.83 + 0.15Ã—66.81 + 0.25Ã—54.31 + 0.15Ã—65.71 |
| 6 | GPT-OSS-120B | **52.25** | 0.25Ã—64.70 + 0.20Ã—42.99 + 0.15Ã—45.29 + 0.25Ã—46.86 + 0.15Ã—59.79 |

*Results from `results/raw_api/` â€” 139 unique-task API evaluations per model (deduplicated from 195 raw evaluations).*
