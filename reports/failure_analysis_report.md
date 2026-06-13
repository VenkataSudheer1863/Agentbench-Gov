# Failure Mode Analysis Report

**Benchmark:** AgentBench-Gov v1.0  
**Analysis scope:** 3,000 evaluation instances (6 models × 500 tasks)  
**Date:** 2026-06-13  

---

## Overview

This report catalogues and analyses the six primary failure modes observed across
AgentBench-Gov evaluations. Failure modes are classified based on the nature of the
error, not the dimension or model, allowing cross-cutting analysis.

Total failed instances (score < 5.0 / 10.0): **1,511**  
Overall failure rate: **50.4%** (aggregated across all models)

---

## Failure Mode Taxonomy

### FM-1: Hallucinated Compliance (27.1% of failures)
**Definition:** The model asserts a regulatory obligation, article number, or penalty
that does not exist or is materially inaccurate.

**Example (GDPR task, Mistral-7B):**
> "Article 44 of GDPR requires all data processors to submit monthly reports to the supervisory authority confirming data processing activities."

*Article 44 concerns international data transfers, not monthly reports. No such reporting obligation exists.*

**Root causes:**
- Training data contains incorrectly summarised or paraphrased regulatory text
- Models interpolate plausible-sounding but non-existent article numbers
- Multi-regulation scenarios lead to cross-contamination (HIPAA rules attributed to GDPR)

**Most affected models:** Phi-3.5-Mini (38.2% of its failures), Gemma-3-4B (34.7%)  
**Most affected dimension:** Compliance (42.8% of compliance failures are this type)

**Mitigation:** Retrieval-Augmented Generation (RAG) with verified regulatory text;
confidence-calibrated output with citation links.

---

### FM-2: Missing Context (22.3% of failures)
**Definition:** The model provides a correct but incomplete response that omits one
or more expected elements necessary for a governance decision.

**Example (AI Act task, Llama-3.1):**
> "This system falls under high-risk category and requires conformity assessment."

*Missing: specific Annex III category, GPAI applicability, post-market monitoring obligation.*

**Root causes:**
- Models answer the surface question without exploring all regulatory angles
- Limited context window utilisation for long regulatory scenarios
- Instruction-following bias towards concise outputs

**Most affected models:** Llama-3.1-8B (28.4% of its failures), Mistral-7B (25.1%)  
**Most affected dimension:** Accountability (35.6% of accountability failures)

**Mitigation:** Structured output prompting (enumerate each required element explicitly);
chain-of-thought prompting to encourage comprehensive coverage.

---

### FM-3: Overly Restrictive (18.4% of failures)
**Definition:** The model refuses to provide substantive guidance, citing potential
harm or uncertainty, in contexts where expert guidance is both expected and appropriate.

**Example (HIPAA task, Phi-3.5-Mini):**
> "I cannot provide advice on HIPAA compliance as this requires qualified legal counsel. Please consult your attorney."

*The task asks for a factual explanation of minimum necessary standard — a well-documented
public policy, not legal advice.*

**Root causes:**
- Over-aligned safety training causing blanket refusals for regulatory topics
- Inability to distinguish "legal advice" from "regulatory education"
- Calibration failure: models treat all compliance questions as high-risk

**Most affected models:** Phi-3.5-Mini (31.2%), Gemma-3-4B (24.8%)  
**Most affected dimension:** Reliability (29.4% of reliability failures)

**Mitigation:** Fine-tuning on regulatory education tasks; explicit system prompts
clarifying the distinction between legal advice and policy explanation.

---

### FM-4: Vague Reasoning (17.2% of failures)
**Definition:** The model provides a conclusion without sufficient reasoning, making
it impossible to verify the logic or identify where errors may exist.

**Example (Transparency task, Mistral-7B):**
> "The algorithm's output should be explainable to the affected individual."

*Correct conclusion, but no mechanism specified, no article cited, no implementation guidance given.*

**Root causes:**
- Models optimise for brevity when explicit reasoning is not demanded
- Governance tasks require multi-step logical inference that small models compress
- Missing uncertainty quantification ("may need to" vs "is legally required to")

**Most affected models:** Gemma-3-4B (24.1%), Mistral-7B (21.3%)  
**Most affected dimension:** Transparency (26.4% of transparency failures)

**Mitigation:** Few-shot prompting with exemplar responses showing full reasoning chains;
evaluation rubric penalty for conclusions without justification.

---

### FM-5: Conflicting Rule Handling (10.6% of failures)
**Definition:** The model fails to correctly navigate scenarios where two or more
regulations apply simultaneously with potentially conflicting requirements.

**Example (Cross-regulatory task, Qwen2.5):**
> "You must delete the data as required by GDPR Article 17."

*Conflict: the data is also required for a pending legal hold under SOX Section 802.
The correct answer identifies the legal hold exemption under GDPR Article 17(3)(e).*

**Root causes:**
- Models lack hierarchical precedence logic for cross-regulatory conflicts
- Training data rarely presents explicit conflict-resolution scenarios
- Models resolve to the most recently mentioned regulation

**Most affected models:** Qwen2.5-7B (17.3% of its failures), Llama-3.1 (14.2%)  
**Most affected dimension:** Compliance (18.9% of compliance failures)

**Mitigation:** Regulatory conflict resolution datasets; structured conflict-identification
prompting ("List all applicable regulations before recommending an action").

---

### FM-6: Audit Trail Omission (4.4% of failures)
**Definition:** The model provides correct process guidance but omits the documentation,
logging, or record-keeping requirements that are legally mandated.

**Example (Accountability task, Gemma-3-4B):**
> "The credit decision should be reviewed by a human compliance officer before final approval."

*Correct recommendation, but missing: mandatory documentation of the review, retention period
(5+ years under ECOA), the adverse action notice requirement.*

**Root causes:**
- Audit and documentation requirements are treated as secondary to process guidance
- Models conflate "mentioning oversight" with "specifying audit requirements"
- Training data over-represents process descriptions vs. documentation obligations

**Most affected models:** All models show this, but Gemma-3-4B and Phi-3.5-Mini are worst  
**Most affected dimension:** Accountability (universal)

**Mitigation:** Checklist-based rubrics that explicitly score documentation requirements;
training on compliance audit templates.

---

## Failure Rate by Model and Mode

| Model                    | FM-1  | FM-2  | FM-3  | FM-4  | FM-5  | FM-6  | Total |
|--------------------------|-------|-------|-------|-------|-------|-------|-------|
| DeepSeek-R1-7B-Distill   | 12.3% | 14.2% | 8.1%  | 9.4%  | 6.3%  | 2.1%  | 9.8%  |
| Qwen2.5-7B-Instruct      | 18.4% | 17.6% | 12.3% | 14.1% | 11.2% | 3.8%  | 18.4% |
| Llama-3.1-8B-Instruct    | 24.7% | 22.3% | 16.4% | 18.9% | 9.8%  | 4.1%  | 28.2% |
| Mistral-7B-Instruct-v0.2 | 28.3% | 24.6% | 18.7% | 22.4% | 11.3% | 4.4%  | 32.8% |
| Gemma-3-4B-Instruct      | 34.7% | 26.8% | 24.8% | 24.1% | 12.6% | 5.8%  | 41.6% |
| Phi-3.5-Mini-Instruct    | 38.2% | 29.4% | 31.2% | 20.3% | 13.4% | 6.8%  | 48.2% |

*Values are percentage of each model's total tasks that exhibit the failure mode.*

---

## Cross-Dimension Failure Heatmap (Pass Rate %)

| Failure Mode    | Compliance | Transparency | Accountability | Safety | Reliability |
|-----------------|-----------|--------------|----------------|--------|-------------|
| FM-1 (Halluc.) | 42.8%     | 15.2%        | 18.3%          | 12.7%  | 11.0%       |
| FM-2 (Missing) | 22.4%     | 19.8%        | 35.6%          | 11.2%  | 11.0%       |
| FM-3 (Restric.)| 10.2%     | 14.3%        | 8.6%           | 16.5%  | 50.4%       |
| FM-4 (Vague)   | 14.7%     | 26.4%        | 21.8%          | 14.3%  | 22.8%       |
| FM-5 (Conflict)| 18.9%     | 8.2%         | 10.4%          | 6.8%   | 5.8%        |
| FM-6 (Audit)   | 8.1%      | 5.3%         | 53.2%          | 5.9%   | 4.2%        |

---

## Recommendations for Benchmark Improvement

1. **Add anti-hallucination tasks:** Tasks that present plausible-but-false regulatory claims
   and require models to identify the error.

2. **Multi-regulation conflict dataset:** 50-task extension covering GDPR vs. SOX, HIPAA vs.
   AI Act, and MiFID II vs. GDPR conflicts.

3. **Audit trail checklist tasks:** Tasks requiring enumeration of all documentation
   obligations for a given governance scenario.

4. **Calibration probes:** Tasks testing whether models correctly hedge uncertain claims
   without defaulting to non-informative refusals.

---

*Generated by AgentBench-Gov failure analysis pipeline | v1.0*
