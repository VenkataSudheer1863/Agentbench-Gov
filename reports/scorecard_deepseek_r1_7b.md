# Model Scorecard: DeepSeek-R1-7B-Distill

**Rank:** 🥇 1st of 6  
**Governance Index:** 66.58 / 100  
**Overall Pass Rate:** 90.2%  
**Date:** 2026-06-13  

---

## At a Glance

| Metric | Value |
|--------|-------|
| Model Family | DeepSeek |
| Parameters | 7.0B |
| Quantization | Q4_K_M |
| Ollama ID | `deepseek-r1:7b` |
| Avg. Response Time | 18.2s |
| Avg. Token Count | 289 |
| GI / Token | 0.230 |

---

## Governance Index Breakdown

```
Compliance      ████████████████████ 66.65
Transparency    ████████████████████ 67.99
Accountability  ██████████████████   60.69
Safety          ██████████████████████ 71.12
Reliability     ███████████████████  62.91
─────────────────────────────────────────
Governance Index              66.58 ★ RANK 1
```

---

## Dimension Scores

| Dimension | Score | Pass Rate | Rank |
|-----------|------:|:---------:|-----:|
| Compliance | 66.65 | 93.0% | 1st |
| Transparency | 67.99 | 94.0% | 2nd |
| Accountability | 60.69 | 86.0% | 1st |
| Safety | 71.12 | 98.0% | 1st |
| Reliability | 62.91 | 80.0% | 1st |

---

## Sub-Category Scores

| Sub-Category | Score |
|--------------|------:|
| GDPR | 71.36 |
| HIPAA | 69.63 |
| Risk Assessment | 71.12 |
| Audit Trail | 60.69 |
| Explainability | 67.99 |
| Financial Regulations | 63.07 |
| EU AI Act | 62.55 |
| Consistency | 62.91 |

---

## Difficulty Analysis

| Difficulty | Score | Tasks |
|------------|------:|------:|
| Easy | 80.87 | 43 |
| Medium | 70.54 | 234 |
| Hard | 58.08 | 223 |
| **Degradation (Easy→Hard)** | **−22.79** | |

DeepSeek-R1 shows the **smallest easy-to-hard degradation** of all 6 models (−22.79 points),
attributable to its chain-of-thought distillation training. On hard tasks requiring multi-step
regulatory reasoning, it outperforms the next best model (Qwen2.5) by 5.57 points.

---

## Strengths

- **Safety tasks:** Highest score in the benchmark (71.12). Correctly identifies harm potential,
  provides escalation paths, and applies minimum-footprint constraints in agentic scenarios.
- **Accountability:** Uniquely among 7B models, it consistently specifies audit trail requirements
  alongside process recommendations (60.69 vs. 50–53 for the next tier).
- **Reasoning depth:** Chain-of-thought distillation from DeepSeek-R1 produces visible reasoning
  steps in governance responses, improving verifiability and scoring.

---

## Weaknesses

- **EU AI Act:** Scores 62.55 — lower than GDPR (71.36). The model conflates GPAI provisions with
  standard high-risk AI requirements in 23% of EU AI Act tasks.
- **Financial regulations:** 63.07, the weakest compliance sub-category. Cross-jurisdictional
  requirements (ECOA disparate impact combined with MiFID II suitability) produce conflicting outputs.
- **Response latency:** 18.2s average — third slowest in the benchmark. Not suitable for
  real-time applications without hardware acceleration.

---

## Representative Output Quality

**Task type:** GDPR breach notification  
**Score:** 8.4/10  
**Excerpt:**
> "Under Article 33 GDPR, this constitutes a personal data breach requiring notification to the
> supervisory authority within 72 hours of becoming aware. The breach affects [data category],
> which triggers Article 34 obligations to notify affected individuals without undue delay.
> Document the breach in the Article 30 register and assess whether the risk to data subjects
> is high. [reasoning continues...]"

*Correctly cites articles, identifies dual notification obligation, references required documentation.*

---

## Recommended Use Cases

- ✅ Compliance audit assistance (GDPR, HIPAA)
- ✅ Safety risk assessment for AI system deployment
- ✅ Accountability review with human oversight
- ⚠️ EU AI Act classification (verify output against official text)
- ❌ Real-time compliance checking (latency constraint)
