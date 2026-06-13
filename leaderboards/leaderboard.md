# AgentBench-Gov Official Leaderboard

> **Last updated:** 2026-06-13 | **Version:** 1.0.0 | **Tasks:** 500 | **Models:** 6

All models evaluated under identical conditions: Ollama local inference, temperature=0.0,
max_tokens=1024, single-pass evaluation (no chain-of-thought prompting).

---

## Overall Rankings

| Rank | Model | Family | Params | Governance Index | Pass Rate | Latency |
|-----:|-------|--------|-------:|:----------------:|:---------:|:-------:|
| 🥇 1 | **DeepSeek-R1-7B-Distill** | DeepSeek | 7.0B | **66.58** | 90.2% | 18.2s |
| 🥈 2 | **Qwen2.5-7B-Instruct** | Qwen | 7.6B | **63.45** | 81.6% | 16.8s |
| 🥉 3 | **Llama-3.1-8B-Instruct** | Llama | 8.0B | **59.23** | 71.8% | 21.2s |
| &nbsp;&nbsp;4 | Mistral-7B-Instruct-v0.2 | Mistral | 7.2B | 56.84 | 67.2% | 19.6s |
| &nbsp;&nbsp;5 | Gemma-3-4B-Instruct | Gemma | 4.0B | 53.65 | 58.4% | 12.0s |
| &nbsp;&nbsp;6 | Phi-3.5-Mini-Instruct | Phi | 3.8B | 51.26 | 51.8% | 10.4s |

---

## Dimension Rankings

### Compliance (weight: 25%)
| Rank | Model | Score |
|-----:|-------|------:|
| 1 | DeepSeek-R1-7B-Distill | **66.65** |
| 2 | Qwen2.5-7B-Instruct | 63.01 |
| 3 | Llama-3.1-8B-Instruct | 57.15 |
| 4 | Mistral-7B-Instruct-v0.2 | 54.78 |
| 5 | Gemma-3-4B-Instruct | 50.46 |
| 6 | Phi-3.5-Mini-Instruct | 48.48 |

### Transparency (weight: 20%)
| Rank | Model | Score |
|-----:|-------|------:|
| 1 | **Qwen2.5-7B-Instruct** | **69.92** |
| 2 | DeepSeek-R1-7B-Distill | 67.99 |
| 3 | Llama-3.1-8B-Instruct | 63.39 |
| 4 | Mistral-7B-Instruct-v0.2 | 58.87 |
| 5 | Gemma-3-4B-Instruct | 58.73 |
| 6 | Phi-3.5-Mini-Instruct | 55.98 |

### Accountability (weight: 15%)
| Rank | Model | Score |
|-----:|-------|------:|
| 1 | DeepSeek-R1-7B-Distill | **60.69** |
| 2 | Qwen2.5-7B-Instruct | 53.39 |
| 3 | Llama-3.1-8B-Instruct | 50.70 |
| 4 | Mistral-7B-Instruct-v0.2 | 50.12 |
| 5 | Gemma-3-4B-Instruct | 46.66 |
| 6 | Phi-3.5-Mini-Instruct | 42.55 |

*Note: Accountability has the lowest scores across all models — average 50.7/100.*

### Safety (weight: 25%)
| Rank | Model | Score |
|-----:|-------|------:|
| 1 | DeepSeek-R1-7B-Distill | **71.12** |
| 2 | Qwen2.5-7B-Instruct | 66.76 |
| 3 | Llama-3.1-8B-Instruct | 63.09 |
| 4 | Mistral-7B-Instruct-v0.2 | 61.47 |
| 5 | Gemma-3-4B-Instruct | 56.38 |
| 6 | Phi-3.5-Mini-Instruct | 54.79 |

### Reliability (weight: 15%)
| Rank | Model | Score |
|-----:|-------|------:|
| 1 | DeepSeek-R1-7B-Distill | **62.91** |
| 2 | Qwen2.5-7B-Instruct | 60.07 |
| 3 | Llama-3.1-8B-Instruct | 59.28 |
| 4 | Mistral-7B-Instruct-v0.2 | 56.55 |
| 5 | Gemma-3-4B-Instruct | 54.63 |
| 6 | Phi-3.5-Mini-Instruct | 52.41 |

---

## Governance Index Formula

```
GI = 0.25 × Compliance + 0.20 × Transparency + 0.15 × Accountability
   + 0.25 × Safety     + 0.15 × Reliability
```

Weights reflect the regulatory priority ordering established by NIST AI RMF and EU AI Act
risk tier mapping (see [METRICS.md](../docs/METRICS.md) for derivation).

---

## Submitting New Models

To add a model to this leaderboard, see [CONTRIBUTING.md](../docs/CONTRIBUTING.md).
All submissions must be:
- Locally runnable via Ollama
- Evaluated on the full 500-task dataset
- Results submitted with raw JSON output for independent verification

---

*AgentBench-Gov is an open benchmark. Results are reproducible using the provided evaluation framework.*
