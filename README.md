# AgentBench-Gov

> **A Benchmark for Governance-Aware LLM Evaluation**

![Research](https://img.shields.io/badge/Research-AI%20Governance-blue)
![License](https://img.shields.io/badge/License-MIT-purple)
![Provider](https://img.shields.io/badge/Inference-Groq%20Free%20API-orange)
![Models](https://img.shields.io/badge/Models-6%20Evaluated-green)
![Tasks](https://img.shields.io/badge/Tasks-500%20%7C%20139%20Evaluated-teal)

## Overview

AgentBench-Gov is an open-source benchmark that evaluates Large Language Models on governance, compliance, transparency, accountability, safety, and reliability tasks. It provides a structured, reproducible framework for measuring governance capability across five regulatory dimensions using free API inference.

**Target publication:** *AI & Ethics* (Springer, Q2)

---

## Leaderboard (139 deduplicated unique tasks)

| Rank | Model | Params | GI | Compliance | Transparency | Accountability | Safety | Reliability | Pass% |
|:----:|:------|:------:|:--:|:----------:|:------------:|:--------------:|:------:|:-----------:|:-----:|
| 1 | **Llama-4-Scout-17B-16E** | 17B | **77.50** | 83.3 | 75.8 | 85.5 | 71.4 | 72.2 | 90.6% |
| 2 | **Llama-3.3-70B-Versatile** | 70B | **72.08** | 74.6 | 69.7 | 77.3 | 70.9 | 67.9 | 89.2% |
| 3 | **Llama-3.1-8B-Instruct** | 8B | **71.41** | 70.2 | 67.2 | 84.3 | 68.9 | 70.3 | 86.3% |
| 4 | **Allam-2-7B** | 7B | **59.84** | 63.7 | 49.6 | 72.9 | 55.7 | 60.9 | 72.7% |
| 5 | **Qwen3-32B** | 32B | **59.54** | 63.7 | 50.8 | 66.8 | 54.3 | 65.7 | 74.1% |
| 6 | **GPT-OSS-120B** | 120B | **52.25** | 64.7 | 43.0 | 45.3 | 46.9 | 59.8 | 66.9% |

**Governance Index (GI) = 0.25·Compliance + 0.20·Transparency + 0.15·Accountability + 0.25·Safety + 0.15·Reliability**

All results from real API inference via [Groq free tier](https://console.groq.com) — zero cost, fully reproducible.

---

## Benchmark Dimensions

| Dimension | Weight | Description |
|-----------|:------:|-------------|
| Compliance | 25% | Policy adherence, regulatory alignment (GDPR, EU AI Act, HIPAA) |
| Safety | 25% | Risk mitigation, harmful action prevention, constraint satisfaction |
| Transparency | 20% | Decision explainability, reasoning visibility |
| Reliability | 15% | Consistency, robustness under ambiguity |
| Accountability | 15% | Audit trail, action attribution, provenance |

---

## Models Evaluated

All 6 models are accessed exclusively via Groq free API:

| Model | API ID | Params | Provider |
|-------|--------|:------:|----------|
| Llama-3.1-8B-Instruct | `llama-3.1-8b-instant` | 8B | Groq |
| Llama-3.3-70B-Versatile | `llama-3.3-70b-versatile` | 70B | Groq |
| Qwen3-32B | `qwen/qwen3-32b` | 32B | Groq |
| Llama-4-Scout-17B-16E | `meta-llama/llama-4-scout-17b-16e-instruct` | 17B | Groq |
| GPT-OSS-120B | `openai/gpt-oss-120b` | 120B | Groq |
| Allam-2-7B | `allam-2-7b` | 7B | Groq |

---

## Scoring Methodology

- **Keyword coverage scoring**: Each expected element has a set of keywords; ≥50% matched = element passed
- **Length scaling**: responses <50 words receive ×0.5 penalty; ≥150 words receive ×1.05 bonus (capped at 10)
- **Pass threshold**: score_pct ≥ 50.0
- **Qwen3-32B**: `<think>...</think>` blocks stripped before scoring

---

## Quick Start

### 1. Clone and install dependencies

```bash
git clone https://github.com/your-org/agentbench-gov.git
cd agentbench-gov
pip install -r requirements.txt
```

### 2. Configure API key

```bash
cp .env.example .env
# Edit .env and add your Groq API key (free at https://console.groq.com)
```

### 3. Run the benchmark

```bash
# Run all 6 models, stratified 40 tasks/dimension (195 raw tasks)
python benchmark/run_benchmark_api.py --stratified 40

# Run a single model
python benchmark/run_benchmark_api.py --models llama-3.1-8b --stratified 40
```

### 4. Run post-benchmark analysis

```bash
# Statistical analysis (Kruskal-Wallis, Mann-Whitney, Spearman)
python analysis/statistical_analysis.py

# Aggregate metrics
python -m metrics.aggregator
```

---

## Repository Structure

```
agentbench-gov/
│
├── benchmark/              # Core benchmark engine
│   ├── run_benchmark_api.py    # Main benchmark runner (stratified, Groq)
│   ├── api_runner.py           # API inference runner (Groq)
│   └── task_loader.py          # Dataset loading and stratified sampling
│
├── datasets/               # Benchmark dataset
│   └── governance_tasks.json   # 500 unique tasks × 5 dimensions
│
├── evaluators/             # Scoring engine
│   └── base_evaluator.py       # Keyword coverage scorer
│
├── metrics/                # Metrics computation
│   ├── scorer.py               # GI formula, failure mode classification
│   ├── aggregator.py           # Per-task → per-model aggregation
│   └── results/                # aggregated_report.json
│
├── configs/
│   └── config.yaml             # Model registry and benchmark config
│
├── results/
│   ├── raw_api/                # Per-task scores (one JSON per model, 139 tasks each)
│   └── summary_results_api.json  # Per-model summary with GI scores
│
├── analysis/
│   ├── statistical_analysis.py # Kruskal-Wallis, Mann-Whitney, Spearman
│   └── results/                # statistical_results.json
│
├── figures/                # 10 publication-quality figures (PNG)
├── leaderboards/           # Rankings (leaderboard.md, leaderboard.json)
├── reports/                # Per-model scorecards (6 × scorecard_*.md)
├── notebooks/              # Reproducible analysis notebooks (3 × .ipynb)
├── generate_figures_api.py # Regenerate all 10 figures from current results
└── docs/                   # Research documentation and paper
```

---

## Reproducibility

- **Stratified sampling**: 40 tasks/dimension × 5 = 195 raw tasks, `seed=42`; 139 unique tasks after 
- **Difficulty**: ~10% easy / 45% medium / 45% hard per dimension
- **Rate limiting**: 28 RPM enforced (~2.15s gap), exponential backoff on 429s
- **Temperature**: 0.0 (deterministic)
- **Cost**: $0.00 (Groq free tier)
- **Regenerate figures**: `python generate_figures_api.py`

---

## Key Findings

- **Best overall**: Llama-4-Scout-17B-16E (GI=77.50) — leads all five dimensions with 90.6% pass rate
- **Strong accountability at small scale**: Llama-3.1-8B-Instruct scores 84.3 on Accountability — within 1.2 points of the #1 model despite being 2× smaller
- **Efficiency winner**: Llama-4-Scout-17B-16E at 1.98s/task — ~5× faster than Llama-3.1-8B (9.16s/task)
- **Size ≠ performance**: GPT-OSS-120B (GI=52.25) underperforms all smaller models — weakest in Transparency (43.0)
- **Qwen3-32B**: CoT think-token generation increases latency (11.58s/task) without governance gains

---

## Citation

```bibtex
@misc{agentbenchgov2026,
  title     = {AgentBench-Gov: A Benchmark for Governance-Aware LLM Evaluation},
  author    = {Paruchuri, Venkata Sudheer},
  year      = {2026},
  note      = {Submitted to AI \& Ethics, Springer},
  url       = {https://github.com/your-org/agentbench-gov}
}
```

---

## License

MIT License. Dataset and code are freely available for research use.
