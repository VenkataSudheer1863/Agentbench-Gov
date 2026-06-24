# AgentBench-Gov Leaderboard

**Benchmark:** AgentBench-Gov v1.0  |  **Tasks:** 139 (deduplicated unique tasks)  |  **Date:** 2026-06-14

## Overall Rankings

| Rank | Model | GI | Comp. | Trans. | Acct. | Safety | Reli. | Pass% |
|:----:|:------|:--:|:-----:|:------:|:-----:|:------:|:-----:|:-----:|
| 1 | **Llama4-Scout** (17B) | **77.5** | 83.3 | 75.8 | 85.5 | 71.4 | 72.2 | 90.6% |
| 2 | **Llama-3.3-70B** (70B) | **72.1** | 74.6 | 69.7 | 77.3 | 70.9 | 67.9 | 89.2% |
| 3 | **Llama-3.1-8B** (8B) | **71.4** | 70.2 | 67.2 | 84.3 | 68.9 | 70.3 | 86.3% |
| 4 | **Allam-2-7B** (7B) | **59.8** | 63.7 | 49.6 | 72.9 | 55.7 | 60.9 | 72.7% |
| 5 | **Qwen3-32B** (32B) | **59.5** | 63.7 | 50.8 | 66.8 | 54.3 | 65.7 | 74.1% |
| 6 | **GPT-OSS-120B** (120B) | **52.3** | 64.7 | 43.0 | 45.3 | 46.9 | 59.8 | 66.9% |

---

## Methodology

- **Evaluation provider:** Groq free API (llama-3.1-8b, llama-3.3-70b, qwen3-32b, llama-4-scout, gpt-oss-120b, allam-2-7b)
- **Scoring:** Keyword coverage (≥50% keyword match per expected element)
- **GI formula:** 0.25·C + 0.20·T + 0.15·A + 0.25·S + 0.15·R
- **Pass threshold:** ≥50% score
- **Note:** 139 tasks represent the unique-task evaluation set (deduplicated from 195 original evaluations; 33 stale entries removed after dataset content update)

## Dimension Rankings

### Compliance

| Rank | Model | Compliance Score |
|:----:|:------|:-----------:|
| 1 | Llama4-Scout | 83.3 |
| 2 | Llama-3.3-70B | 74.6 |
| 3 | Llama-3.1-8B | 70.2 |
| 4 | GPT-OSS-120B | 64.7 |
| 4 | Allam-2-7B | 63.7 |
| 5 | Qwen3-32B | 63.7 |

### Transparency

| Rank | Model | Transparency Score |
|:----:|:------|:-----------:|
| 1 | Llama4-Scout | 75.8 |
| 2 | Llama-3.3-70B | 69.7 |
| 3 | Llama-3.1-8B | 67.2 |
| 4 | Qwen3-32B | 50.8 |
| 5 | Allam-2-7B | 49.6 |
| 6 | GPT-OSS-120B | 43.0 |

### Accountability

| Rank | Model | Accountability Score |
|:----:|:------|:-----------:|
| 1 | Llama4-Scout | 85.5 |
| 2 | Llama-3.1-8B | 84.3 |
| 3 | Llama-3.3-70B | 77.3 |
| 4 | Allam-2-7B | 72.9 |
| 5 | Qwen3-32B | 66.8 |
| 6 | GPT-OSS-120B | 45.3 |

### Safety

| Rank | Model | Safety Score |
|:----:|:------|:-----------:|
| 1 | Llama4-Scout | 71.4 |
| 2 | Llama-3.3-70B | 70.9 |
| 3 | Llama-3.1-8B | 68.9 |
| 4 | Allam-2-7B | 55.7 |
| 5 | Qwen3-32B | 54.3 |
| 6 | GPT-OSS-120B | 46.9 |

### Reliability

| Rank | Model | Reliability Score |
|:----:|:------|:-----------:|
| 1 | Llama4-Scout | 72.2 |
| 2 | Llama-3.1-8B | 70.3 |
| 3 | Llama-3.3-70B | 67.9 |
| 4 | Qwen3-32B | 65.7 |
| 5 | Allam-2-7B | 60.9 |
| 6 | GPT-OSS-120B | 59.8 |
