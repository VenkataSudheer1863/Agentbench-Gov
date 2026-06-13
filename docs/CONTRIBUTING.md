# Contributing to AgentBench-Gov

Thank you for your interest in contributing. This document covers how to submit
new models, tasks, and bug reports.

---

## Code of Conduct

All contributions must adhere to responsible AI research practices:
- Do not submit tasks that encourage harmful or illegal behaviour
- Ensure regulatory content is accurate and properly sourced
- Do not submit benchmark evaluations that misrepresent model capabilities

---

## Ways to Contribute

### 1. Submit a New Model Evaluation

To add your model to the leaderboard:

**Requirements:**
- Model must be locally runnable via Ollama
- Evaluate on all 500 tasks
- Submit raw results JSON for independent verification
- Provide hardware and software configuration

**Steps:**

1. Fork the repository
2. Run the full evaluation:
   ```bash
   python run_benchmark.py \
     --model your-model:tag \
     --tasks 500 \
     --temperature 0.0 \
     --output results/your_model_eval.json
   ```
3. Add model config to `configs/config.yaml`
4. Update `results/summary_results.json` and `results/leaderboard.csv`
5. Submit a pull request with:
   - `configs/config.yaml` update
   - `results/your_model_results.json`
   - Updated `leaderboards/leaderboard.json` and `leaderboards/leaderboard.md`
   - Hardware specification in PR description

**Required PR metadata:**
```yaml
model: "Model Name v1.0"
ollama_id: "model:tag"
hardware: "NVIDIA RTX 4090 24GB"
os: "Ubuntu 22.04"
ollama_version: "0.4.x"
temperature: 0.0
max_tokens: 1024
```

---

### 2. Contribute New Tasks

Task contributions expand benchmark coverage. Priority areas:
- Cross-regulation conflict scenarios (GDPR vs. SOX, HIPAA vs. AI Act)
- Emerging AI governance frameworks (NIST AI 100-1, ISO/IEC 42001)
- Financial regulation depth (ECOA adverse action, MiFID II suitability)
- Agentic AI governance (tool-use constraints, multi-agent accountability)

**Task authoring requirements:**

1. Follow the schema in [TASK_FORMAT.md](TASK_FORMAT.md)
2. All regulatory citations must be verifiable against official texts
3. Submit for domain expert review before opening PR
4. Minimum 10 tasks per PR; maximum 50

**Task PR checklist:**
- [ ] All tasks pass JSON schema validation
- [ ] No duplicate task IDs
- [ ] Difficulty levels correctly assessed
- [ ] No real organisation or person names
- [ ] Regulatory text is current (check EU AI Act updates)
- [ ] Domain expert review completed

**Validate your tasks:**
```bash
python -c "
import json, jsonschema

with open('schemas/task_schema.json') as f:
    schema = json.load(f)

with open('datasets/my_new_tasks.json') as f:
    tasks = json.load(f)

for task in tasks:
    jsonschema.validate(task, schema)
print('All tasks valid')
"
```

---

### 3. Report a Bug

Use GitHub Issues with the `bug` label. Include:
- Python version and OS
- Full error traceback
- Minimal reproduction script
- Expected vs. actual behaviour

---

### 4. Improve Evaluation Methodology

Research contributions to the scoring methodology are welcome. Areas of interest:
- LLM-as-judge evaluation (supplementing keyword coverage)
- Multi-turn evaluation protocols
- Cross-lingual governance task adaptation
- Adversarial task generation for hallucination detection

Open a GitHub Discussion before implementing major methodology changes.

---

## Development Setup

```bash
git clone https://github.com/your-org/agentbench-gov
cd agentbench-gov
pip install -r requirements.txt
pip install -r requirements-dev.txt  # pytest, black, mypy
```

Run tests:
```bash
pytest tests/ -v
```

Format code:
```bash
black .
```

---

## Pull Request Guidelines

1. Keep PRs focused — one concern per PR
2. Update tests for any changed scoring logic
3. Update documentation if changing task format or metrics
4. All CI checks must pass before review

---

## Governance and Attribution

- All dataset contributions are released under CC-BY-4.0
- Code contributions are released under MIT License
- Contributors are credited in `CONTRIBUTORS.md`

By submitting a contribution, you confirm that:
- You have the right to submit the contribution
- The contribution is accurate to the best of your knowledge
- Regulatory content is grounded in publicly available official text

---

*For questions: open a GitHub Discussion or contact the maintainers.*
