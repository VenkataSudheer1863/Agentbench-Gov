"""
AgentBench-Gov Result Aggregator
Aggregates per-task scores into dimension, model-level, and cross-model summaries.
"""
import json
import statistics
from collections import defaultdict
from pathlib import Path
from typing import Optional

from metrics.scorer import governance_index, GOVERNANCE_INDEX_WEIGHTS, DIMENSIONS


class ResultAggregator:
    """Aggregates raw per-task evaluation results into summary tables."""

    def __init__(self, results_dir: Optional[Path] = None):
        self.results_dir = results_dir or Path(__file__).parent.parent / "results"

    # ------------------------------------------------------------------
    # Load / save helpers
    # ------------------------------------------------------------------

    def load_raw(self, filename: str = "raw_results.json") -> dict:
        path = self.results_dir / filename
        with open(path, encoding="utf-8") as f:
            return json.load(f)

    def load_summary(self, filename: str = "summary_results.json") -> dict:
        path = self.results_dir / filename
        with open(path, encoding="utf-8") as f:
            return json.load(f)

    # ------------------------------------------------------------------
    # Per-model aggregation
    # ------------------------------------------------------------------

    def aggregate_model(self, task_results: list[dict]) -> dict:
        """
        Aggregate all task results for a single model.

        Parameters
        ----------
        task_results : list of dicts, each with at minimum:
            task_id, dimension, difficulty, sub_category, score_pct (0-100)

        Returns
        -------
        dict with governance_index, dimension_scores, difficulty_scores,
             subcategory_scores, overall_pass_rate, descriptive statistics
        """
        dim_scores:  dict[str, list[float]] = defaultdict(list)
        diff_scores: dict[str, list[float]] = defaultdict(list)
        sub_scores:  dict[str, list[float]] = defaultdict(list)
        all_scores: list[float] = []

        for r in task_results:
            s = r.get("score_pct", r.get("score", 0) * 10)
            dim_scores[r["dimension"]].append(s)
            diff_scores[r.get("difficulty", "medium")].append(s)
            sub_scores[r.get("sub_category", "general")].append(s)
            all_scores.append(s)

        dim_means  = {d: round(statistics.mean(v), 2) for d, v in dim_scores.items()}
        diff_means = {d: round(statistics.mean(v), 2) for d, v in diff_scores.items()}
        sub_means  = {s: round(statistics.mean(v), 2) for s, v in sub_scores.items()}

        gi = governance_index(dim_means)
        pass_rate = round(
            sum(1 for s in all_scores if s >= 50) / len(all_scores) * 100, 1
        ) if all_scores else 0.0

        overall_mean = statistics.mean(all_scores) if all_scores else 0.0
        overall_std  = statistics.stdev(all_scores) if len(all_scores) > 1 else 0.0

        return {
            "governance_index":    gi,
            "dimension_scores":    dim_means,
            "difficulty_scores":   diff_means,
            "subcategory_scores":  sub_means,
            "overall_pass_rate":   pass_rate,
            "overall_mean_pct":    round(overall_mean, 2),
            "overall_std_pct":     round(overall_std, 2),
            "overall_cv":          round(overall_std / overall_mean, 4) if overall_mean > 0 else 0.0,
            "n_tasks":             len(all_scores),
            "n_passed":            sum(1 for s in all_scores if s >= 50),
        }

    # ------------------------------------------------------------------
    # Cross-model aggregation
    # ------------------------------------------------------------------

    def cross_model_summary(self, raw_results: dict) -> dict:
        """
        Compute cross-model statistics: dimension-level means/stds,
        best/worst model per dimension, Governance Index ranking.
        """
        dim_data: dict[str, dict[str, list[float]]] = {d: {} for d in DIMENSIONS}

        for model_id, model_data in raw_results.items():
            task_results = model_data.get("task_results", [])
            for d in DIMENSIONS:
                scores = [r.get("score_pct", 0) for r in task_results
                          if r.get("dimension") == d]
                if scores:
                    dim_data[d][model_id] = scores

        cross = {}
        for d in DIMENSIONS:
            model_means = {m: statistics.mean(s) for m, s in dim_data[d].items()}
            if not model_means:
                continue
            all_flat = [s for lst in dim_data[d].values() for s in lst]
            cross[d] = {
                "cross_model_mean":  round(statistics.mean(all_flat), 2),
                "cross_model_std":   round(statistics.stdev(all_flat) if len(all_flat) > 1 else 0.0, 2),
                "best_model":        max(model_means, key=model_means.get),
                "worst_model":       min(model_means, key=model_means.get),
                "best_score":        round(max(model_means.values()), 2),
                "worst_score":       round(min(model_means.values()), 2),
                "gap":               round(max(model_means.values()) - min(model_means.values()), 2),
            }

        gi_scores = {
            m: raw_results[m].get("governance_index", 0.0)
            for m in raw_results
        }
        ranking = sorted(gi_scores.items(), key=lambda x: x[1], reverse=True)

        return {
            "dimension_cross_model": cross,
            "governance_index_ranking": [
                {"rank": i + 1, "model": m, "gi": gi}
                for i, (m, gi) in enumerate(ranking)
            ],
            "n_models": len(raw_results),
            "gi_range": {
                "max": round(max(gi_scores.values()), 2),
                "min": round(min(gi_scores.values()), 2),
                "spread": round(max(gi_scores.values()) - min(gi_scores.values()), 2),
            }
        }

    # ------------------------------------------------------------------
    # Failure mode aggregation
    # ------------------------------------------------------------------

    def failure_mode_summary(self, raw_results: dict) -> dict:
        """Aggregate failure modes across all models and produce distributions."""
        global_counts: dict[str, int] = defaultdict(int)
        per_model: dict[str, dict[str, int]] = {}

        for model_id, model_data in raw_results.items():
            model_counts: dict[str, int] = defaultdict(int)
            for r in model_data.get("task_results", []):
                fm = r.get("failure_mode")
                if fm:
                    global_counts[fm] += 1
                    model_counts[fm] += 1
            per_model[model_id] = dict(model_counts)

        total_failures = sum(global_counts.values())
        global_pct = {
            k: round(v / total_failures * 100, 1) if total_failures > 0 else 0
            for k, v in global_counts.items()
        }

        return {
            "global_counts":      dict(global_counts),
            "global_percentages": global_pct,
            "per_model":          per_model,
            "total_failures":     total_failures,
        }

    # ------------------------------------------------------------------
    # Difficulty analysis
    # ------------------------------------------------------------------

    def difficulty_analysis(self, raw_results: dict) -> dict:
        """Compute per-difficulty performance statistics per model and cross-model."""
        difficulties = ["easy", "medium", "hard"]
        result = {}

        for diff in difficulties:
            model_means = {}
            for model_id, model_data in raw_results.items():
                scores = [r.get("score_pct", 0) for r in model_data.get("task_results", [])
                          if r.get("difficulty") == diff]
                if scores:
                    model_means[model_id] = round(statistics.mean(scores), 2)

            all_scores = list(model_means.values())
            result[diff] = {
                "per_model":        model_means,
                "cross_model_mean": round(statistics.mean(all_scores), 2) if all_scores else 0.0,
                "cross_model_std":  round(statistics.stdev(all_scores), 2) if len(all_scores) > 1 else 0.0,
            }

        # Compute degradation ratios (easy→hard)
        degradation = {}
        for model_id in raw_results:
            easy = result["easy"]["per_model"].get(model_id, 0)
            hard = result["hard"]["per_model"].get(model_id, 0)
            if easy > 0:
                degradation[model_id] = round((easy - hard) / easy * 100, 1)

        result["degradation_pct_easy_to_hard"] = degradation
        return result

    # ------------------------------------------------------------------
    # Generate full aggregated report dict
    # ------------------------------------------------------------------

    def full_aggregate(self) -> dict:
        """Load raw results and compute the complete aggregated report."""
        raw = self.load_raw()
        cross = self.cross_model_summary(raw)
        failures = self.failure_mode_summary(raw)
        difficulty = self.difficulty_analysis(raw)

        return {
            "cross_model_summary":    cross,
            "failure_mode_analysis":  failures,
            "difficulty_analysis":    difficulty,
            "n_total_tasks_evaluated": sum(
                len(m.get("task_results", [])) for m in raw.values()
            ),
        }


if __name__ == "__main__":
    agg = ResultAggregator()
    report = agg.full_aggregate()
    out = Path(__file__).parent.parent / "results" / "aggregated_report.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    print(f"Aggregated report saved to {out}")
    print("\nGI Ranking:")
    for entry in report["cross_model_summary"]["governance_index_ranking"]:
        print(f"  {entry['rank']}. {entry['model']:<25} GI={entry['gi']:.1f}")
