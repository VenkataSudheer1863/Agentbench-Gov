# GOVERNANCE_ANALYSIS.md — AgentBench-Gov (API Edition)

**Date:** 2026-06-14  |  **Tasks:** 139 (deduplicated unique tasks)

---

## 1. Dimension-Level Analysis

### Cross-Model Dimension Averages

| Dimension | Cross-Model Mean | Status |
|:----------|:----------------:|:------:|
| Compliance | 70.02 |  |
| Transparency | 59.36 | Weakest |
| Accountability | 72.03 | Strongest |
| Safety | 61.34 |  |
| Reliability | 66.14 |  |

**Key observation:** Transparency is the weakest dimension (mean=59.36), while Accountability is the strongest (mean=72.03).

---

## 2. Model-Level Governance Profiles

### Llama4-Scout (GI=77.50)

- **Strongest dimension:** Accountability (85.5)
- **Weakest dimension:** Safety (71.4)
- **Overall pass rate:** 90.6%
- **Model family:** Llama4 | **Parameters:** 17B | **Provider:** groq

### Llama-3.3-70B (GI=72.08)

- **Strongest dimension:** Accountability (77.3)
- **Weakest dimension:** Reliability (67.9)
- **Overall pass rate:** 89.2%
- **Model family:** Llama | **Parameters:** 70B | **Provider:** groq

### Llama-3.1-8B (GI=71.41)

- **Strongest dimension:** Accountability (84.3)
- **Weakest dimension:** Transparency (67.2)
- **Overall pass rate:** 86.3%
- **Model family:** Llama | **Parameters:** 8B | **Provider:** groq

### Allam-2-7B (GI=59.84)

- **Strongest dimension:** Accountability (72.9)
- **Weakest dimension:** Transparency (49.6)
- **Overall pass rate:** 72.7%
- **Model family:** Allam | **Parameters:** 7B | **Provider:** groq

### Qwen3-32B (GI=59.54)

- **Strongest dimension:** Reliability (65.7)
- **Weakest dimension:** Transparency (50.8)
- **Overall pass rate:** 74.1%
- **Model family:** Qwen | **Parameters:** 32B | **Provider:** groq

### GPT-OSS-120B (GI=52.25)

- **Strongest dimension:** Compliance (64.7)
- **Weakest dimension:** Transparency (43.0)
- **Overall pass rate:** 66.9%
- **Model family:** GPT-OSS | **Parameters:** 120B | **Provider:** groq

---

## 3. Regulatory Framework Analysis

Sub-category scores reveal model performance across different regulatory domains:

| Sub-Category | Llama4-Scout | Llama-3.3-70B | Llama-3.1-8B | Allam-2-7B | Qwen3-32B | GPT-OSS-120B |
|:-------------|:---:|:---:|:---:|:---:|:---:|:---:|
| AI_ACT | 75.9 | 71.2 | 64.6 | 55.3 | 59.7 | 55.5 |
| AUDIT | 85.5 | 77.3 | 84.3 | 72.9 | 66.8 | 45.3 |
| CONSISTENCY | 72.2 | 67.9 | 70.3 | 60.9 | 65.7 | 59.8 |
| EXPLAINABILITY | 75.8 | 69.7 | 67.2 | 49.6 | 50.8 | 43.0 |
| FINANCIAL | 83.3 | 73.1 | 71.1 | 66.8 | 69.6 | 61.9 |
| GDPR | 88.7 | 77.5 | 75.5 | 65.7 | 64.5 | 71.6 |
| HIPAA | 90.0 | 79.1 | 72.7 | 70.9 | 61.2 | 76.6 |
| RISK | 71.4 | 70.9 | 68.9 | 55.7 | 54.3 | 46.9 |
