# AgentBench-Gov Leaderboard

**Benchmark:** AgentBench-Gov v1.0  |  **Tasks:** 195 (stratified, 39 per dimension)  |  **Date:** 2026-06-14

## Overall Rankings

| Rank | Model | GI | Comp. | Trans. | Acct. | Safety | Reli. | Pass% |
|:----:|:------|:--:|:-----:|:------:|:-----:|:------:|:-----:|:-----:|
| 1 | **Llama4-Scout** (17B) | **80.6** | 83.3 | 80.0 | 82.6 | 79.3 | 77.2 | 93.3% |
| 2 | **Llama-3.1-8B** (8B) | **77.4** | 70.2 | 76.0 | 86.9 | 79.8 | 77.7 | 90.3% |
| 3 | **Llama-3.3-70B** (70B) | **73.7** | 74.6 | 72.5 | 74.8 | 73.0 | 73.6 | 91.8% |
| 4 | **Qwen3-32B** (32B) | **63.2** | 63.7 | 58.4 | 67.7 | 60.0 | 69.9 | 79.5% |
| 5 | **Allam-2-7B** (7B) | **61.0** | 63.7 | 50.2 | 73.7 | 58.4 | 62.4 | 76.4% |
| 6 | **GPT-OSS-120B** (120B) | **51.3** | 64.7 | 37.2 | 46.3 | 47.4 | 59.0 | 63.6% |

---

## Methodology

- **Evaluation provider:** Groq free API (llama-3.1-8b, llama-3.3-70b, qwen3-32b, llama-4-scout, gpt-oss-120b, allam-2-7b)
- **Scoring:** Keyword coverage (≥50% keyword match per expected element)
- **GI formula:** 0.25·C + 0.20·T + 0.15·A + 0.25·S + 0.15·R
- **Pass threshold:** ≥50% score

## Dimension Rankings

### Compliance

| Rank | Model | Compliance Score |
|:----:|:------|:-----------:|
| 1 | Llama4-Scout | 83.3 |
| 2 | Llama-3.3-70B | 74.6 |
| 3 | Llama-3.1-8B | 70.2 |
| 4 | GPT-OSS-120B | 64.7 |
| 5 | Allam-2-7B | 63.7 |
| 6 | Qwen3-32B | 63.7 |

### Transparency

| Rank | Model | Transparency Score |
|:----:|:------|:-----------:|
| 1 | Llama4-Scout | 80.0 |
| 2 | Llama-3.1-8B | 76.0 |
| 3 | Llama-3.3-70B | 72.5 |
| 4 | Qwen3-32B | 58.4 |
| 5 | Allam-2-7B | 50.2 |
| 6 | GPT-OSS-120B | 37.2 |

### Accountability

| Rank | Model | Accountability Score |
|:----:|:------|:-----------:|
| 1 | Llama-3.1-8B | 86.9 |
| 2 | Llama4-Scout | 82.6 |
| 3 | Llama-3.3-70B | 74.8 |
| 4 | Allam-2-7B | 73.7 |
| 5 | Qwen3-32B | 67.7 |
| 6 | GPT-OSS-120B | 46.3 |

### Safety

| Rank | Model | Safety Score |
|:----:|:------|:-----------:|
| 1 | Llama-3.1-8B | 79.8 |
| 2 | Llama4-Scout | 79.3 |
| 3 | Llama-3.3-70B | 73.0 |
| 4 | Qwen3-32B | 60.0 |
| 5 | Allam-2-7B | 58.4 |
| 6 | GPT-OSS-120B | 47.4 |

### Reliability

| Rank | Model | Reliability Score |
|:----:|:------|:-----------:|
| 1 | Llama-3.1-8B | 77.7 |
| 2 | Llama4-Scout | 77.2 |
| 3 | Llama-3.3-70B | 73.6 |
| 4 | Qwen3-32B | 69.9 |
| 5 | Allam-2-7B | 62.4 |
| 6 | GPT-OSS-120B | 59.0 |
