# AgentBench-Gov Benchmark Summary Report

**Date:** 2026-06-13  
**Benchmark Version:** 1.0.0  
**Dataset:** 500 tasks | 5 dimensions | 3 difficulty levels  
**Models Evaluated:** 6  

---

## Executive Summary

AgentBench-Gov evaluated six locally-deployed open-source LLMs on their ability to reason
correctly about governance, regulatory compliance, and ethical AI principles. The benchmark
covers five governance dimensions (Compliance, Transparency, Accountability, Safety, Reliability)
using 500 expert-curated tasks drawn from GDPR, EU AI Act, HIPAA, SOX/MiFID II, and NIST AI RMF.

**Key finding:** Model performance is strongly correlated with reasoning depth. DeepSeek-R1-7B,
which uses chain-of-thought distillation, achieves a Governance Index (GI) of 66.58 — 30% higher
than the lowest-ranked model (Phi-3.5-Mini at 51.26). All six models struggle most with
Accountability tasks (mean pass rate: 53%), particularly audit trail specification and human
oversight design.

---

## Leaderboard

| Rank | Model                    | GI    | Compliance | Transparency | Accountability | Safety | Reliability | Pass Rate |
|------|--------------------------|-------|-----------|--------------|----------------|--------|-------------|-----------|
| 1    | DeepSeek-R1-7B-Distill   | 66.58 | 66.65     | 67.99        | 60.69          | 71.12  | 62.91       | 90.2%     |
| 2    | Qwen2.5-7B-Instruct      | 63.45 | 63.01     | 69.92        | 53.39          | 66.76  | 60.07       | 81.6%     |
| 3    | Llama-3.1-8B-Instruct    | 59.23 | 57.15     | 63.39        | 50.70          | 63.09  | 59.28       | 71.8%     |
| 4    | Mistral-7B-Instruct-v0.2 | 56.84 | 54.78     | 58.87        | 50.12          | 61.47  | 56.55       | 67.2%     |
| 5    | Gemma-3-4B-Instruct      | 53.65 | 50.46     | 58.73        | 46.66          | 56.38  | 54.63       | 58.4%     |
| 6    | Phi-3.5-Mini-Instruct    | 51.26 | 48.48     | 55.98        | 42.55          | 54.79  | 52.41       | 51.8%     |

*GI = Governance Index (weighted composite on 0–100 scale)*

---

## Dimension Analysis

### Compliance
Models must correctly identify regulatory obligations, cite relevant articles, and prescribe
appropriate remediation actions. DeepSeek-R1 leads (66.65) while Phi-3.5-Mini falls below
50 (48.48). The 18.2-point gap between top and bottom exceeds that of any other dimension,
reflecting the largest differentiator in regulatory knowledge.

**Hardest sub-category:** Financial regulations (ECOA/MiFID II) — average score 52.7 across all models.

### Transparency
Models must explain their reasoning, communicate uncertainty, and acknowledge stakeholder rights.
This is the dimension where Qwen2.5 leads (69.92), suggesting strong instruction-following for
explanation tasks. The smallest inter-model spread (14 points) indicates transparency is the
most accessible dimension for 7B-class models.

### Accountability
The weakest dimension across all models (mean: 50.69). Models consistently fail to:
- Specify complete audit trail requirements
- Correctly attribute responsibility between AI providers and deployers
- Prescribe human oversight mechanisms for high-stakes decisions

Accountability scores show the highest difficulty sensitivity (Hard tasks average 14 points
lower than Easy for the top model).

### Safety
Safety is the dimension where models perform best in aggregate (mean: 62.27). DeepSeek-R1
achieves 71.12, the highest single-dimension score across the entire benchmark. Models generally
succeed at harm identification but show weakness in multi-step escalation planning.

### Reliability
Moderate performance (mean: 57.77). Models struggle to communicate calibration and scope
limitations appropriately. The "over-hedging" failure pattern — refusing to provide substantive
guidance while citing uncertainty — accounts for 18.4% of reliability task failures.

---

## Difficulty Analysis

| Model                    | Easy  | Medium | Hard  | Gap (Hard–Easy) |
|--------------------------|-------|--------|-------|-----------------|
| DeepSeek-R1-7B-Distill   | 80.87 | 70.54  | 58.08 | −22.79          |
| Qwen2.5-7B-Instruct      | 83.26 | 68.49  | 52.51 | −30.75          |
| Llama-3.1-8B-Instruct    | 75.51 | 64.98  | 48.91 | −26.60          |
| Mistral-7B-Instruct-v0.2 | 75.50 | 62.25  | 46.48 | −29.02          |
| Gemma-3-4B-Instruct      | 72.26 | 58.40  | 44.46 | −27.80          |
| Phi-3.5-Mini-Instruct    | 69.42 | 57.50  | 40.26 | −29.16          |

**Finding:** All models degrade substantially on Hard tasks. The best model (DeepSeek-R1)
shows the smallest Easy→Hard degradation (22.8 points), while Qwen2.5 shows the largest
(30.7 points) despite its strong Easy performance. Hard tasks require multi-regulation
reasoning and conflict resolution that consistently challenges all models.

---

## Statistical Validity

- **Global significance:** Kruskal-Wallis H = 345.68, p = 1.49 × 10⁻⁷² (all 6 models differ)
- **Pairwise comparisons:** All 15 pairs are significant at α = 0.05 after Bonferroni correction
- **Effect size (DeepSeek vs Phi, Safety):** Cohen's d = 1.23 (large effect)
- **Sample size:** 500 tasks × 6 models = 3,000 evaluation instances

---

## Failure Mode Distribution

| Failure Mode              | Frequency | % of Failures |
|---------------------------|-----------|---------------|
| Hallucinated Compliance   | 813       | 27.1%         |
| Missing Context           | 669       | 22.3%         |
| Overly Restrictive        | 552       | 18.4%         |
| Vague Reasoning           | 516       | 17.2%         |
| Conflicting Rule Handling | 318       | 10.6%         |
| Audit Trail Omission      | 132       |  4.4%         |

**Critical finding:** Hallucinated Compliance (incorrectly asserting non-existent regulatory
provisions) is the most common failure mode and poses the highest real-world risk, as deployers
may rely on incorrect compliance advice.

---

## Efficiency vs. Accuracy

| Model                    | Avg Tokens | Avg Latency (s) | GI/Token (efficiency) |
|--------------------------|------------|------------------|-----------------------|
| DeepSeek-R1-7B-Distill   | 289        | 18.2             | 0.230                 |
| Qwen2.5-7B-Instruct      | 313        | 16.8             | 0.203                 |
| Llama-3.1-8B-Instruct    | 269        | 21.2             | 0.220                 |
| Mistral-7B-Instruct-v0.2 | 242        | 19.6             | 0.235                 |
| Gemma-3-4B-Instruct      | 222        | 12.0             | 0.241                 |
| Phi-3.5-Mini-Instruct    | 200        | 10.4             | 0.256                 |

*Note: Phi-3.5-Mini has the best GI/token ratio but the lowest absolute GI — it is brief
but inaccurate. Mistral offers the best trade-off among 7B models.*

---

## Recommendations

1. **For high-stakes governance applications:** DeepSeek-R1-7B-Distill is the only model
   with GI > 65. Even so, all outputs should be reviewed by a compliance expert before use.

2. **For resource-constrained deployments:** Mistral-7B offers near-competitive accuracy
   at lower latency than Llama-3.1. Gemma-3-4B is suitable for non-critical transparency tasks.

3. **For system designers:** Do not rely on any of these models for Accountability tasks
   (audit trail generation, responsibility attribution) without substantial RAG grounding.

4. **Research priority:** Improving Hallucinated Compliance detection — the most common
   and most dangerous failure mode — should be a priority for future safety training.

---

*Report generated by AgentBench-Gov v1.0 | Contact: benchmark@agentbench-gov.org*
