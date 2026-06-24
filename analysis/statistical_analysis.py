"""
AgentBench-Gov — Statistical Analysis (API Results Edition)
============================================================
Runs comprehensive statistical tests on benchmark results.

Usage:
    python analysis/statistical_analysis.py

Reads: results/raw_api/{model_key}.json
Writes: analysis/results/statistical_results.json
"""
import json
import sys
import itertools
from pathlib import Path
from collections import defaultdict

import numpy as np
from scipy import stats

RESULTS_DIR  = Path("results")
RAW_DIR      = RESULTS_DIR / "raw_api"
ANALYSIS_DIR = Path("analysis") / "results"
ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)

DIMENSIONS = ["compliance", "transparency", "accountability", "safety", "reliability"]
GOVERNANCE_WEIGHTS = {
    "compliance":     0.25,
    "transparency":   0.20,
    "accountability": 0.15,
    "safety":         0.25,
    "reliability":    0.15,
}


def load_all_raw() -> dict:
    """Load per-task results for all models."""
    model_data = {}
    for path in sorted(RAW_DIR.glob("*.json")):
        mk = path.stem
        with open(path, encoding="utf-8-sig") as f:
            model_data[mk] = json.load(f)
    return model_data


def extract_scores(task_list: list, dim: str = None) -> list:
    """Extract score_pct values, optionally filtered to one dimension."""
    if dim:
        return [r["score_pct"] for r in task_list if r.get("dimension") == dim]
    return [r["score_pct"] for r in task_list]


def run_kruskal_wallis(model_data: dict) -> dict:
    """Kruskal-Wallis H test across all models."""
    groups = [extract_scores(tasks) for tasks in model_data.values()]
    h, p = stats.kruskal(*groups)
    return {
        "H_statistic": round(h, 4),
        "p_value":      float(p),
        "significant":  bool(p < 0.05),
        "interpretation": (
            f"H={h:.2f}, p={p:.2e} — Models differ significantly"
            if p < 0.05 else
            f"H={h:.2f}, p={p:.4f} — No significant difference"
        ),
    }


def run_pairwise_mannwhitney(model_data: dict, alpha: float = 0.05) -> dict:
    """Pairwise Mann-Whitney U with Bonferroni correction."""
    keys  = list(model_data.keys())
    n_pairs = len(keys) * (len(keys) - 1) // 2
    alpha_bonf = alpha / n_pairs if n_pairs > 0 else alpha
    pairs = {}
    for m1, m2 in itertools.combinations(keys, 2):
        s1 = extract_scores(model_data[m1])
        s2 = extract_scores(model_data[m2])
        u, p = stats.mannwhitneyu(s1, s2, alternative="two-sided")
        significant = bool(p < alpha_bonf)
        # Effect size r = Z / sqrt(N)
        n = len(s1) + len(s2)
        z = stats.norm.ppf(1 - p / 2) if p > 0 else 0
        r = abs(z) / np.sqrt(n)
        pairs[f"{m1} vs {m2}"] = {
            "U":           round(float(u), 2),
            "p_value":     float(p),
            "p_bonferroni": float(p * n_pairs),
            "significant": significant,
            "effect_r":    round(float(r), 4),
        }
    return {"alpha_bonferroni": alpha_bonf, "n_pairs": n_pairs, "pairs": pairs}


def run_spearman(model_data: dict) -> dict:
    """Spearman correlations between dimension scores per model."""
    correlations = {}
    for mk, tasks in model_data.items():
        dim_scores = {}
        for dim in DIMENSIONS:
            s = extract_scores(tasks, dim)
            dim_scores[dim] = s if s else [0]

        dim_corr = {}
        for d1, d2 in itertools.combinations(DIMENSIONS, 2):
            n = min(len(dim_scores[d1]), len(dim_scores[d2]))
            if n < 3:
                continue
            rho, p = stats.spearmanr(dim_scores[d1][:n], dim_scores[d2][:n])
            dim_corr[f"{d1} vs {d2}"] = {
                "rho": round(float(rho), 4), "p": float(p)
            }
        correlations[mk] = dim_corr
    return correlations


def summary_statistics(model_data: dict) -> dict:
    """Per-model per-dimension descriptive statistics."""
    stats_out = {}
    for mk, tasks in model_data.items():
        model_stats = {"overall": {}, "by_dimension": {}, "by_difficulty": {}}
        all_scores = extract_scores(tasks)
        if all_scores:
            model_stats["overall"] = {
                "n":     len(all_scores),
                "mean":  round(float(np.mean(all_scores)), 2),
                "std":   round(float(np.std(all_scores)),  2),
                "min":   round(float(np.min(all_scores)),  2),
                "max":   round(float(np.max(all_scores)),  2),
                "q25":   round(float(np.percentile(all_scores, 25)), 2),
                "q75":   round(float(np.percentile(all_scores, 75)), 2),
                "pass_rate": round(sum(1 for s in all_scores if s >= 50) / len(all_scores), 4),
            }
        for dim in DIMENSIONS:
            s = extract_scores(tasks, dim)
            if s:
                model_stats["by_dimension"][dim] = {
                    "n":    len(s),
                    "mean": round(float(np.mean(s)), 2),
                    "std":  round(float(np.std(s)),  2),
                    "pass_rate": round(sum(1 for x in s if x >= 50) / len(s), 4),
                }
        for diff in ["easy", "medium", "hard"]:
            s = [r["score_pct"] for r in tasks if r.get("difficulty") == diff]
            if s:
                model_stats["by_difficulty"][diff] = {
                    "n":    len(s),
                    "mean": round(float(np.mean(s)), 2),
                    "std":  round(float(np.std(s)),  2),
                }
        stats_out[mk] = model_stats
    return stats_out


def governance_index(dim_means: dict) -> float:
    return round(sum(dim_means.get(d, 0) * w for d, w in GOVERNANCE_WEIGHTS.items()), 2)


def main():
    summary_path = RESULTS_DIR / "summary_results_api.json"
    if not summary_path.exists():
        print("ERROR: summary_results_api.json not found. Run benchmark first.")
        sys.exit(1)

    print("Loading raw results…")
    model_data = load_all_raw()
    if not model_data:
        print("ERROR: No raw result files found in results/raw_api/")
        sys.exit(1)

    for mk, tasks in model_data.items():
        print(f"  {mk}: {len(tasks)} tasks")

    print("\nRunning statistical tests…")

    kw = run_kruskal_wallis(model_data)
    print(f"  Kruskal-Wallis: {kw['interpretation']}")

    pw = run_pairwise_mannwhitney(model_data)
    n_sig = sum(1 for v in pw["pairs"].values() if v["significant"])
    print(f"  Pairwise Mann-Whitney: {n_sig}/{pw['n_pairs']} pairs significant (Bonferroni alpha={pw['alpha_bonferroni']:.4f})")

    sp = run_spearman(model_data)
    print(f"  Spearman correlations: computed for {len(sp)} models")

    desc = summary_statistics(model_data)
    print(f"  Descriptive statistics: computed for {len(desc)} models")

    # Compile output
    output = {
        "kruskal_wallis":      kw,
        "pairwise_mann_whitney": pw,
        "spearman_correlations": sp,
        "descriptive_statistics": desc,
    }

    out_path = ANALYSIS_DIR / "statistical_results.json"
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)

    print(f"\nStatistical results saved -> {out_path}")

    # Print leaderboard summary
    with open(summary_path, encoding="utf-8-sig") as f:
        summary = json.load(f)

    ordered = sorted(summary.items(), key=lambda x: x[1]["governance_index"], reverse=True)
    print("\nFINAL LEADERBOARD:")
    print(f"{'Rank':<5} {'Model':<28} {'GI':>6}  {'Pass%':>6}  {'Params':>8}")
    print("-" * 58)
    for rank, (mk, data) in enumerate(ordered, 1):
        print(f"  {rank}    {data['display_name']:<26}  {data['governance_index']:>6.2f}  "
              f"{data['overall_pass_rate']:>5.1f}%  {data['params_b']:>5.0f}B")


if __name__ == "__main__":
    main()
