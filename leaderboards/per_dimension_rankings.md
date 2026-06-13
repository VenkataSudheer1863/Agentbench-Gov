# Per-Dimension Rankings — AgentBench-Gov v1.0

Rankings broken down by governance dimension, sub-category, and difficulty level.

---

## Compliance Dimension

### Overall Rankings
| Rank | Model | Score | Pass Rate |
|-----:|-------|------:|:---------:|
| 1 | DeepSeek-R1-7B-Distill | 66.65 | 93.0% |
| 2 | Qwen2.5-7B-Instruct | 63.01 | 81.0% |
| 3 | Llama-3.1-8B-Instruct | 57.15 | 65.0% |
| 4 | Mistral-7B-Instruct-v0.2 | 54.78 | 65.0% |
| 5 | Gemma-3-4B-Instruct | 50.46 | 49.0% |
| 6 | Phi-3.5-Mini-Instruct | 48.48 | 46.0% |

### Sub-Category: GDPR
| Rank | Model | Score |
|-----:|-------|------:|
| 1 | DeepSeek-R1-7B-Distill | 71.36 |
| 2 | Qwen2.5-7B-Instruct | 66.28 |
| 3 | Mistral-7B-Instruct-v0.2 | 60.01 |
| 4 | Llama-3.1-8B-Instruct | 59.96 |
| 5 | Phi-3.5-Mini-Instruct | 53.84 |
| 6 | Gemma-3-4B-Instruct | 53.41 |

### Sub-Category: EU AI Act
| Rank | Model | Score |
|-----:|-------|------:|
| 1 | DeepSeek-R1-7B-Distill | 62.55 |
| 2 | Llama-3.1-8B-Instruct | 59.89 |
| 3 | Qwen2.5-7B-Instruct | 59.59 |
| 4 | Mistral-7B-Instruct-v0.2 | 51.93 |
| 5 | Gemma-3-4B-Instruct | 46.51 |
| 6 | Phi-3.5-Mini-Instruct | 44.11 |

### Sub-Category: HIPAA
| Rank | Model | Score |
|-----:|-------|------:|
| 1 | DeepSeek-R1-7B-Distill | 69.63 |
| 2 | Qwen2.5-7B-Instruct | 66.40 |
| 3 | Gemma-3-4B-Instruct | 54.28 |
| 4 | Llama-3.1-8B-Instruct | 56.55 |
| 5 | Mistral-7B-Instruct-v0.2 | 56.39 |
| 6 | Phi-3.5-Mini-Instruct | 51.31 |

### Sub-Category: Financial Regulations
| Rank | Model | Score |
|-----:|-------|------:|
| 1 | DeepSeek-R1-7B-Distill | 63.07 |
| 2 | Qwen2.5-7B-Instruct | 59.77 |
| 3 | Llama-3.1-8B-Instruct | 52.19 |
| 4 | Mistral-7B-Instruct-v0.2 | 50.79 |
| 5 | Gemma-3-4B-Instruct | 47.63 |
| 6 | Phi-3.5-Mini-Instruct | 44.65 |

*Financial regulations (SOX, MiFID II, ECOA, BSA/AML) are the hardest sub-category — lowest average (52.7) across all models.*

---

## Transparency Dimension

### Overall Rankings
| Rank | Model | Score | Pass Rate |
|-----:|-------|------:|:---------:|
| 1 | **Qwen2.5-7B-Instruct** | **69.92** | 92.0% |
| 2 | DeepSeek-R1-7B-Distill | 67.99 | 94.0% |
| 3 | Llama-3.1-8B-Instruct | 63.39 | 79.0% |
| 4 | Mistral-7B-Instruct-v0.2 | 58.87 | 75.0% |
| 5 | Gemma-3-4B-Instruct | 58.73 | 70.0% |
| 6 | Phi-3.5-Mini-Instruct | 55.98 | 69.0% |

*Note: Qwen2.5 leads transparency despite ranking second overall — strong instruction-following for explanation tasks.*

### Sub-Category: Explainability
| Rank | Model | Score |
|-----:|-------|------:|
| 1 | Qwen2.5-7B-Instruct | 69.92 |
| 2 | DeepSeek-R1-7B-Distill | 67.99 |
| 3 | Llama-3.1-8B-Instruct | 63.39 |
| 4 | Mistral-7B-Instruct-v0.2 | 58.87 |
| 5 | Gemma-3-4B-Instruct | 58.73 |
| 6 | Phi-3.5-Mini-Instruct | 55.98 |

---

## Accountability Dimension

### Overall Rankings
| Rank | Model | Score | Pass Rate |
|-----:|-------|------:|:---------:|
| 1 | DeepSeek-R1-7B-Distill | 60.69 | 86.0% |
| 2 | Qwen2.5-7B-Instruct | 53.39 | 60.0% |
| 3 | Llama-3.1-8B-Instruct | 50.70 | 50.0% |
| 4 | Mistral-7B-Instruct-v0.2 | 50.12 | 51.0% |
| 5 | Gemma-3-4B-Instruct | 46.66 | 42.0% |
| 6 | Phi-3.5-Mini-Instruct | 42.55 | 29.0% |

*Accountability has the lowest pass rates across all models. Phi-3.5-Mini passes only 29% of tasks.*

### Sub-Category: Audit Trail
| Rank | Model | Score |
|-----:|-------|------:|
| 1 | DeepSeek-R1-7B-Distill | 60.69 |
| 2 | Qwen2.5-7B-Instruct | 53.39 |
| 3 | Llama-3.1-8B-Instruct | 50.70 |
| 4 | Mistral-7B-Instruct-v0.2 | 50.12 |
| 5 | Gemma-3-4B-Instruct | 46.66 |
| 6 | Phi-3.5-Mini-Instruct | 42.55 |

---

## Safety Dimension

### Overall Rankings
| Rank | Model | Score | Pass Rate |
|-----:|-------|------:|:---------:|
| 1 | DeepSeek-R1-7B-Distill | **71.12** | **98.0%** |
| 2 | Qwen2.5-7B-Instruct | 66.76 | 93.0% |
| 3 | Llama-3.1-8B-Instruct | 63.09 | 86.0% |
| 4 | Mistral-7B-Instruct-v0.2 | 61.47 | 79.0% |
| 5 | Gemma-3-4B-Instruct | 56.38 | 62.0% |
| 6 | Phi-3.5-Mini-Instruct | 54.79 | 61.0% |

*Safety is the highest-scoring dimension overall; DeepSeek-R1 achieves 71.12, the single highest dimension score in the benchmark.*

### Sub-Category: Risk Assessment
| Rank | Model | Score |
|-----:|-------|------:|
| 1 | DeepSeek-R1-7B-Distill | 71.12 |
| 2 | Qwen2.5-7B-Instruct | 66.76 |
| 3 | Llama-3.1-8B-Instruct | 63.09 |
| 4 | Mistral-7B-Instruct-v0.2 | 61.47 |
| 5 | Gemma-3-4B-Instruct | 56.38 |
| 6 | Phi-3.5-Mini-Instruct | 54.79 |

---

## Reliability Dimension

### Overall Rankings
| Rank | Model | Score | Pass Rate |
|-----:|-------|------:|:---------:|
| 1 | DeepSeek-R1-7B-Distill | 62.91 | 80.0% |
| 2 | Qwen2.5-7B-Instruct | 60.07 | 82.0% |
| 3 | Llama-3.1-8B-Instruct | 59.28 | 79.0% |
| 4 | Mistral-7B-Instruct-v0.2 | 56.55 | 66.0% |
| 5 | Gemma-3-4B-Instruct | 54.63 | 69.0% |
| 6 | Phi-3.5-Mini-Instruct | 52.41 | 54.0% |

### Sub-Category: Consistency
| Rank | Model | Score |
|-----:|-------|------:|
| 1 | DeepSeek-R1-7B-Distill | 62.91 |
| 2 | Qwen2.5-7B-Instruct | 60.07 |
| 3 | Llama-3.1-8B-Instruct | 59.28 |
| 4 | Mistral-7B-Instruct-v0.2 | 56.55 |
| 5 | Gemma-3-4B-Instruct | 54.63 |
| 6 | Phi-3.5-Mini-Instruct | 52.41 |

---

## Difficulty-Stratified Rankings

### Easy Tasks Only
| Rank | Model | Score |
|-----:|-------|------:|
| 1 | Qwen2.5-7B-Instruct | **83.26** |
| 2 | DeepSeek-R1-7B-Distill | 80.87 |
| 3 | Llama-3.1-8B-Instruct | 75.51 |
| 4 | Mistral-7B-Instruct-v0.2 | 75.50 |
| 5 | Gemma-3-4B-Instruct | 72.26 |
| 6 | Phi-3.5-Mini-Instruct | 69.42 |

### Medium Tasks Only
| Rank | Model | Score |
|-----:|-------|------:|
| 1 | DeepSeek-R1-7B-Distill | **70.54** |
| 2 | Qwen2.5-7B-Instruct | 68.49 |
| 3 | Llama-3.1-8B-Instruct | 64.98 |
| 4 | Mistral-7B-Instruct-v0.2 | 62.25 |
| 5 | Gemma-3-4B-Instruct | 58.40 |
| 6 | Phi-3.5-Mini-Instruct | 57.50 |

### Hard Tasks Only
| Rank | Model | Score |
|-----:|-------|------:|
| 1 | DeepSeek-R1-7B-Distill | **58.08** |
| 2 | Qwen2.5-7B-Instruct | 52.51 |
| 3 | Llama-3.1-8B-Instruct | 48.91 |
| 4 | Mistral-7B-Instruct-v0.2 | 46.48 |
| 5 | Gemma-3-4B-Instruct | 44.46 |
| 6 | Phi-3.5-Mini-Instruct | 40.26 |

*Hard tasks require multi-regulation reasoning. All models show substantial degradation, but DeepSeek-R1's reasoning capabilities provide a consistent advantage.*

---

*For full results with individual task scores, see [results/raw_results.json](../results/raw_results.json)*
