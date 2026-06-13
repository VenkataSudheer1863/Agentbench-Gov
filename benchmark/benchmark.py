"""
AgentBench-Gov Benchmark Orchestrator
Coordinates task loading, model inference, evaluation, and result persistence.
"""
import json
import time
import traceback
from pathlib import Path
from typing import Optional

from benchmark.task_loader  import TaskLoader
from benchmark.ollama_runner import OllamaRunner
from evaluators.base_evaluator import BaseEvaluator
from metrics.scorer import governance_index, GOVERNANCE_INDEX_WEIGHTS
from metrics.aggregator import ResultAggregator


RESULTS_DIR = Path(__file__).parent.parent / "results"


class BenchmarkRunner:
    """
    High-level orchestrator for AgentBench-Gov evaluations.

    Usage
    -----
    runner = BenchmarkRunner()
    results = runner.run(model="mistral:7b", limit=100)
    runner.save(results, "my_run.json")
    """

    def __init__(
        self,
        ollama_url:    str = "http://localhost:11434",
        results_dir:   Optional[Path] = None,
        temperature:   float = 0.0,
        max_tokens:    int   = 1024,
        verbose:       bool  = True,
    ):
        self.loader      = TaskLoader()
        self.ollama      = OllamaRunner(base_url=ollama_url)
        self.evaluator   = BaseEvaluator()
        self.aggregator  = ResultAggregator(results_dir or RESULTS_DIR)
        self.temperature = temperature
        self.max_tokens  = max_tokens
        self.verbose     = verbose

    # ------------------------------------------------------------------
    # Pre-flight checks
    # ------------------------------------------------------------------

    def check_prerequisites(self) -> dict:
        """Verify Ollama availability and dataset integrity."""
        status = {
            "ollama_running":    self.ollama.is_available(),
            "available_models":  self.ollama.list_models() if self.ollama.is_available() else [],
            "dataset_loaded":    False,
            "n_tasks":           0,
        }
        try:
            self.loader._ensure_loaded()
            status["dataset_loaded"] = True
            status["n_tasks"]        = len(self.loader)
        except Exception as e:
            status["dataset_error"] = str(e)

        return status

    # ------------------------------------------------------------------
    # Single-model evaluation run
    # ------------------------------------------------------------------

    def run(
        self,
        model:        str,
        dimension:    Optional[str] = None,
        difficulty:   Optional[str] = None,
        limit:        Optional[int] = None,
        shuffle:      bool = False,
    ) -> dict:
        """
        Evaluate a single model on the benchmark.

        Parameters
        ----------
        model      : Ollama model identifier (e.g. 'mistral:7b')
        dimension  : restrict to one dimension (optional)
        difficulty : restrict to one difficulty level (optional)
        limit      : max tasks to evaluate (optional)
        shuffle    : shuffle task order before limiting

        Returns
        -------
        dict with model metadata, task_results list, and summary statistics
        """
        tasks = self.loader.load(
            dimension=dimension, difficulty=difficulty,
            limit=limit, shuffle=shuffle
        )

        if not tasks:
            raise ValueError("No tasks matched the specified filters.")

        self._log(f"Evaluating [{model}] on {len(tasks)} tasks …")
        start = time.time()

        task_results = []
        for i, task in enumerate(tasks, 1):
            result = self._evaluate_one(model, task, idx=i, total=len(tasks))
            task_results.append(result)

        elapsed = time.time() - start
        summary = self._summarise(task_results)
        summary["model"]          = model
        summary["elapsed_s"]      = round(elapsed, 1)
        summary["tasks_per_sec"]  = round(len(tasks) / elapsed, 2) if elapsed > 0 else 0

        self._log(f"Done. GI={summary['governance_index']}  "
                  f"pass={summary['overall_pass_rate']}%  "
                  f"elapsed={summary['elapsed_s']}s")

        return {
            "model":        model,
            "run_config":   {
                "dimension": dimension, "difficulty": difficulty,
                "limit": limit, "temperature": self.temperature,
            },
            "task_results": task_results,
            "summary":      summary,
        }

    # ------------------------------------------------------------------
    # Multi-model sweep
    # ------------------------------------------------------------------

    def run_all(self, models: list[str], **kwargs) -> dict:
        """Run benchmark across multiple models and return combined results."""
        all_results = {}
        for model in models:
            try:
                all_results[model] = self.run(model, **kwargs)
            except Exception as e:
                self._log(f"ERROR evaluating {model}: {e}")
                traceback.print_exc()
        return all_results

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def save(self, results: dict, filename: str = "eval_output.json"):
        """Write results dict to the results directory."""
        RESULTS_DIR.mkdir(parents=True, exist_ok=True)
        out = RESULTS_DIR / filename
        with open(out, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)
        self._log(f"Results saved → {out}")
        return out

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _evaluate_one(self, model: str, task: dict, idx: int, total: int) -> dict:
        """Run and score a single task."""
        output = self.ollama.run_governance_task(model, task, temperature=self.temperature)
        response = output.get("response", "")

        if output["success"] and response:
            eval_result = self.evaluator.evaluate(task, response)
        else:
            eval_result = {
                "task_id":       task["task_id"],
                "dimension":     task["dimension"],
                "difficulty":    task.get("difficulty", "medium"),
                "sub_category":  task.get("sub_category", ""),
                "keyword_score": 0.0,
                "coverage":      0.0,
                "matched_elements": [],
                "missed_elements":  task.get("expected_elements", []),
                "response_word_count": 0,
                "final_score":   0.0,
            }

        score_10  = eval_result["final_score"]
        score_pct = score_10 * 10.0
        passed    = score_pct >= 50.0

        if self.verbose:
            status = "PASS" if passed else "FAIL"
            print(f"  [{idx:4d}/{total}] {task['task_id']:22s}"
                  f" [{task.get('difficulty','?'):6s}]"
                  f" score={score_pct:5.1f}  [{status}]"
                  f" ({output.get('response_time_s',0):.1f}s)")

        return {
            "task_id":           task["task_id"],
            "dimension":         task["dimension"],
            "sub_category":      task.get("sub_category", ""),
            "difficulty":        task.get("difficulty", "medium"),
            "score_pct":         round(score_pct, 2),
            "score_10":          round(score_10, 2),
            "passed":            passed,
            "coverage":          eval_result.get("coverage", 0.0),
            "matched_elements":  eval_result.get("matched_elements", []),
            "missed_elements":   eval_result.get("missed_elements", []),
            "response_time_s":   output.get("response_time_s", 0),
            "response_words":    eval_result.get("response_word_count", 0),
        }

    def _summarise(self, task_results: list[dict]) -> dict:
        """Build a summary dict from a list of task results."""
        from collections import defaultdict
        import statistics as stat

        dim_scores:  dict[str, list] = defaultdict(list)
        diff_scores: dict[str, list] = defaultdict(list)
        all_scores:  list[float] = []

        for r in task_results:
            s = r["score_pct"]
            dim_scores[r["dimension"]].append(s)
            diff_scores[r["difficulty"]].append(s)
            all_scores.append(s)

        dim_means  = {d: round(stat.mean(v), 2) for d, v in dim_scores.items()}
        diff_means = {d: round(stat.mean(v), 2) for d, v in diff_scores.items()}
        gi         = governance_index(dim_means)

        return {
            "governance_index":  gi,
            "dimension_scores":  dim_means,
            "difficulty_scores": diff_means,
            "overall_pass_rate": round(sum(1 for r in task_results if r["passed"])
                                       / len(task_results) * 100, 1),
            "overall_mean_pct":  round(stat.mean(all_scores), 2),
            "overall_std_pct":   round(stat.stdev(all_scores) if len(all_scores) > 1 else 0, 2),
        }

    def _log(self, msg: str):
        if self.verbose:
            print(f"[BenchmarkRunner] {msg}")
