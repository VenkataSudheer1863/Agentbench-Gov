# Evaluation Guide

Step-by-step instructions for running AgentBench-Gov evaluations on new models.

---

## Prerequisites

### 1. Install Ollama

Download and install Ollama from [ollama.ai](https://ollama.ai):

```bash
# Linux / macOS
curl -fsSL https://ollama.ai/install.sh | sh

# Windows: use the installer from ollama.ai
```

Verify installation:

```bash
ollama --version
# ollama version 0.4.x
```

### 2. Pull your model

```bash
ollama pull deepseek-r1:7b
ollama pull qwen2.5:7b
ollama pull llama3.1:8b
ollama pull mistral:7b
ollama pull gemma3:4b
ollama pull phi3.5:mini
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

Required packages: numpy, pandas, matplotlib, seaborn, scipy, scikit-learn, requests, PyYAML, tqdm, tabulate.

### 4. Verify Ollama is running

```bash
curl http://localhost:11434/api/tags
```

You should see a JSON response listing available models.

---

## Quick Start

Run the benchmark for a single model:

```bash
python run_benchmark.py --model deepseek-r1:7b --tasks 500 --output results/my_eval.json
```

Run all 6 default models:

```bash
python benchmark/benchmark.py --all
```

---

## Full Evaluation Pipeline

### Step 1: Dataset Preparation

The dataset should already exist at `datasets/governance_tasks.json`. If not, generate it:

```bash
cd datasets
python generate_extended.py
```

Verify the dataset:

```bash
python -c "
import json
with open('datasets/governance_tasks.json') as f:
    data = json.load(f)
print(f'Total tasks: {len(data[\"tasks\"])}')
print(f'Dimensions: {list(set(t[\"dimension\"] for t in data[\"tasks\"]))}')
"
```

### Step 2: Configure Models

Edit `configs/config.yaml` to add or modify model configurations:

```yaml
models:
  your-model-id:
    display_name: "Your Model Name"
    ollama_id: "your-model:tag"
    params_b: 7.0
    family: "YourFamily"
    quantization: "Q4_K_M"
    enabled: true
```

### Step 3: Run Evaluation

```bash
python run_benchmark.py \
  --model your-model:tag \
  --tasks 500 \
  --temperature 0.0 \
  --output results/your_model_results.json
```

Options:
- `--model` — Ollama model ID (required)
- `--tasks` — number of tasks to evaluate (default: 500)
- `--dimension` — restrict to one dimension: compliance|transparency|accountability|safety|reliability
- `--difficulty` — restrict to difficulty: easy|medium|hard
- `--temperature` — sampling temperature (default: 0.0)
- `--output` — output file path (default: results/raw_results.json)

### Step 4: Aggregate Results

```bash
python -c "
from metrics.aggregator import ResultAggregator
agg = ResultAggregator()
results = agg.full_aggregate()
print(results)
"
```

### Step 5: Statistical Analysis

```bash
python analysis/statistical_analysis.py
```

This produces `analysis/statistical_results.json` with pairwise significance tests,
effect sizes, and reliability metrics.

### Step 6: Generate Figures

```bash
python figures/generate_figures.py
```

All 10 publication-quality figures are saved to `figures/`.

---

## Evaluating a Custom Model

If your model is not in Ollama, you can implement a custom runner:

```python
from evaluators.base_evaluator import BaseEvaluator
import json

evaluator = BaseEvaluator()

with open("datasets/governance_tasks.json") as f:
    tasks = json.load(f)["tasks"]

results = []
for task in tasks[:10]:  # test on 10 tasks
    # Get response from your model
    response = your_model_generate(task["scenario"] + "\n\n" + task["question"])
    
    # Score the response
    score = evaluator.evaluate(task, response)
    results.append(score)

print(f"Mean score: {sum(r['final_score'] for r in results) / len(results):.2f}")
```

---

## Scoring Explanation

Each task is scored using keyword coverage:

1. **Extract expected elements** from `task["expected_elements"]`
2. **Tokenise** each element and the model response
3. **Match:** element is covered if ≥50% of its keywords appear in the response
4. **Base score:** `(covered elements / total elements) × 10`
5. **Length adjustment:** −50% penalty for responses < 50 words; +5% bonus for responses ≥ 150 words

Dimension-specific evaluators (`evaluators/compliance_evaluator.py` etc.) add additional
bonuses for framework identification, reasoning quality, and safety signal presence.

---

## Interpreting Results

| Governance Index | Interpretation |
|:---:|---|
| 70–100 | Strong governance capability — suitable for assisted compliance use |
| 60–70 | Moderate — usable with human expert review |
| 50–60 | Weak — significant gaps, not suitable for production compliance |
| < 50 | Insufficient — should not be used for governance tasks |

---

## Reproducing Published Results

To reproduce the benchmark results from the AgentBench-Gov paper:

```bash
python results/generate_results.py
```

This uses the fixed-seed simulation with `MODEL_PROFILES` calibrated to the paper's results.
Note: actual Ollama inference results may differ due to quantization and hardware variation.

---

## Troubleshooting

**Ollama connection refused:**
```bash
ollama serve &  # start in background
```

**Model not found:**
```bash
ollama pull <model-name>:<tag>
```

**UnicodeEncodeError on Windows:**
```powershell
$env:PYTHONIOENCODING = "utf-8"
```

**Out of memory during evaluation:**
- Use a smaller quantization (Q3_K_M or Q2_K)
- Reduce `max_tokens` in `configs/config.yaml`
- Close other GPU-intensive applications
