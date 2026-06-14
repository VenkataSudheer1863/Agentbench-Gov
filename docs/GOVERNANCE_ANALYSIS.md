# GOVERNANCE_ANALYSIS.md — AgentBench-Gov (API Edition)

**Date:** 2026-06-14

---

## 1. Dimension-Level Analysis

### Cross-Model Dimension Averages

| Dimension | Cross-Model Mean | Status |
|:----------|:----------------:|:------:|
| Compliance | 70.02 |  |
| Transparency | 62.37 | Weakest |
| Accountability | 72.00 | Strongest |
| Safety | 66.31 |  |
| Reliability | 69.97 |  |

**Key observation:** Transparency is the weakest dimension (mean=62.37), while Accountability is the strongest (mean=72.00).

---

## 2. Model-Level Governance Profiles

### Llama4-Scout (GI=80.62)

- **Strongest dimension:** Compliance (83.3)
- **Weakest dimension:** Reliability (77.2)
- **Overall pass rate:** 93.3%
- **Model family:** Llama4 | **Parameters:** 17B | **Provider:** groq

### Llama-3.1-8B (GI=77.38)

- **Strongest dimension:** Accountability (86.9)
- **Weakest dimension:** Compliance (70.2)
- **Overall pass rate:** 90.3%
- **Model family:** Llama | **Parameters:** 8B | **Provider:** groq

### Llama-3.3-70B (GI=73.65)

- **Strongest dimension:** Accountability (74.8)
- **Weakest dimension:** Transparency (72.5)
- **Overall pass rate:** 91.8%
- **Model family:** Llama | **Parameters:** 70B | **Provider:** groq

### Qwen3-32B (GI=63.24)

- **Strongest dimension:** Reliability (69.9)
- **Weakest dimension:** Transparency (58.4)
- **Overall pass rate:** 79.5%
- **Model family:** Qwen | **Parameters:** 32B | **Provider:** groq

### Allam-2-7B (GI=60.96)

- **Strongest dimension:** Accountability (73.7)
- **Weakest dimension:** Transparency (50.2)
- **Overall pass rate:** 76.4%
- **Model family:** Allam | **Parameters:** 7B | **Provider:** groq

### GPT-OSS-120B (GI=51.26)

- **Strongest dimension:** Compliance (64.7)
- **Weakest dimension:** Transparency (37.2)
- **Overall pass rate:** 63.6%
- **Model family:** GPT-OSS | **Parameters:** 120B | **Provider:** groq

---

## 3. Regulatory Framework Analysis

Sub-category scores reveal model performance across different regulatory domains:

| Sub-Category | Llama4-Scout | Llama-3.1-8B | Llama-3.3-70B | Qwen3-32B | Allam-2-7B | GPT-OSS-120B |
|:-------------|:---:|:---:|:---:|:---:|:---:|:---:|
| AI_ACT | 75.9 | 64.6 | 71.2 | 59.7 | 55.3 | 55.5 |
| AUDIT | 82.6 | 86.9 | 74.8 | 67.7 | 73.7 | 46.3 |
| CONSISTENCY | 77.2 | 77.7 | 73.6 | 69.9 | 62.4 | 59.0 |
| EXPLAINABILITY | 80.0 | 76.0 | 72.5 | 58.4 | 50.2 | 37.2 |
| FINANCIAL | 83.3 | 71.1 | 73.1 | 69.6 | 66.8 | 61.9 |
| GDPR | 88.7 | 75.5 | 77.5 | 64.5 | 65.7 | 71.6 |
| HIPAA | 90.0 | 72.7 | 79.1 | 61.1 | 70.9 | 76.6 |
| RISK | 79.3 | 79.8 | 73.0 | 60.0 | 58.4 | 47.4 |