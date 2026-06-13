# AgentBench-Gov

> **A Benchmark for Governance-Aware Autonomous Agents**

![Research](https://img.shields.io/badge/Research-AI%20Governance-blue)
![Open Source](https://img.shields.io/badge/Open%20Source-Community-green)
![Status](https://img.shields.io/badge/Status-Research%20Prototype-orange)
![License](https://img.shields.io/badge/License-MIT-purple)

## Overview

AgentBench-Gov is an open-source benchmark designed to evaluate how autonomous AI agents behave under governance, compliance, transparency, accountability, and safety constraints.

The framework measures whether agents can make reliable decisions while adhering to predefined policies, regulations, ethical guidelines, and organizational rules.

## Research Objectives

* Evaluate governance-aware decision making
* Measure policy and compliance adherence
* Assess transparency and explainability
* Analyze accountability and auditability
* Detect unsafe, biased, or non-compliant behavior
* Benchmark agent reliability under governance constraints

## Benchmark Dimensions

### Governance Compliance

* Policy adherence
* Rule enforcement
* Regulatory alignment

### Transparency

* Decision trace generation
* Reasoning visibility
* Action explainability

### Accountability

* Audit logs
* Action attribution
* Decision provenance

### Safety & Risk

* Harmful action prevention
* Risk-aware planning
* Constraint satisfaction

### Reliability

* Consistent decision making
* Robustness under ambiguity
* Failure recovery behavior

## Architecture

```text
Agent
   │
   ▼
Governance Tasks
   │
   ▼
Evaluation Engine
   │
   ├── Compliance Scoring
   ├── Transparency Analysis
   ├── Accountability Checks
   ├── Safety Assessment
   └── Reliability Metrics
   │
   ▼
Benchmark Reports
```

## Supported Models

### Local Models

* GPT-OSS 20B
* GPT-OSS 120B
* Qwen3-Coder
* GLM Series
* DeepSeek Models
* Llama Models
* Mistral Models

### Free Cloud Models

* OpenRouter Free Models
* Hugging Face Inference Providers
* Groq Free Tier Models
* GitHub Models

## Evaluation Tasks

* Policy compliance scenarios
* Governance reasoning challenges
* Ethical decision-making tasks
* Risk assessment workflows
* Audit trail generation
* Regulatory adherence evaluations
* Transparency reporting exercises

## Metrics

| Metric               | Description                   |
| -------------------- | ----------------------------- |
| Compliance Score     | Policy adherence rate         |
| Transparency Score   | Explainability quality        |
| Accountability Score | Auditability effectiveness    |
| Safety Score         | Risk mitigation performance   |
| Reliability Score    | Consistency across tasks      |
| Governance Index     | Overall governance capability |

## Outputs

* Governance scorecards
* Benchmark reports
* Evaluation analytics
* Compliance dashboards
* Failure analysis summaries
* Agent governance profiles

## Repository Structure

```
agentbench-gov/
│
├── benchmark/
├── datasets/
├── evaluators/
├── governance_rules/
├── metrics/
├── reports/
├── leaderboards/
├── configs/
├── notebooks/
└── docs/
```

## Research Applications

* AI Governance Research
* Agent Safety Evaluation
* Regulatory Compliance Testing
* Responsible AI Development
* Policy-Aware Agent Design
* Trustworthy Autonomous Systems
