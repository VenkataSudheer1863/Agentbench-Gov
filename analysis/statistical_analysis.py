"""
Statistical analysis for AgentBench-Gov paper.
Computes significance tests, correlations, and summary statistics.
"""
import json
import numpy as np
import pandas as pd
from pathlib import Path
from scipy import stats
from itertools import combinations

RESULTS_DIR = Path(__file__).parent.parent / "results"
ANALYSIS_DIR = Path(__file__).parent


def load_all_scores():
    with open(RESULTS_DIR / "raw_results.json") as f:
        raw = json.load(f)
    return raw


def pairwise_significance(raw_results):
    """Compute pairwise Mann-Whitney U tests between models."""
    models = list(raw_results.keys())
    results = {}

    for m1, m2 in combinations(models, 2):
        scores1 = [r["score_pct"] for r in raw_results[m1]["task_results"]]
        scores2 = [r["score_pct"] for r in raw_results[m2]["task_results"]]
        stat, p = stats.mannwhitneyu(scores1, scores2, alternative='two-sided')
        results[f"{m1}_vs_{m2}"] = {
            "statistic": round(float(stat), 1),
            "p_value": float(p),
            "significant": bool(p < 0.05),
            "effect_size_r": round(float(stat / (len(scores1) * len(scores2) / 2) - 1), 3)
        }

    return results


def dimension_correlations(raw_results):
    """Compute Spearman correlations between governance dimensions."""
    dims = ["compliance", "transparency", "accountability", "safety", "reliability"]
    model_list = list(raw_results.keys())

    dim_scores_per_model = {}
    for mid in model_list:
        tasks = raw_results[mid]["task_results"]
        dim_scores_per_model[mid] = {
            d: [r["score_pct"] for r in tasks if r["dimension"] == d]
            for d in dims
        }

    # Compute per-task correlation matrix (pooled across models)
    data = {d: [] for d in dims}
    # For correlation, use model-level averages
    for mid in model_list:
        for d in dims:
            data[d].append(np.mean(dim_scores_per_model[mid][d]))

    corr_matrix = {}
    for d1 in dims:
        corr_matrix[d1] = {}
        for d2 in dims:
            if d1 == d2:
                corr_matrix[d1][d2] = 1.0
            else:
                r, p = stats.spearmanr(data[d1], data[d2])
                corr_matrix[d1][d2] = round(float(r), 3)

    return corr_matrix


def summary_statistics(raw_results):
    """Compute comprehensive summary statistics."""
    summary = {}
    dims = ["compliance", "transparency", "accountability", "safety", "reliability"]

    for mid, model_data in raw_results.items():
        tasks = model_data["task_results"]
        all_scores = [r["score_pct"] for r in tasks]

        dim_stats = {}
        for d in dims:
            dim_scores = [r["score_pct"] for r in tasks if r["dimension"] == d]
            dim_stats[d] = {
                "mean": round(float(np.mean(dim_scores)), 2),
                "std": round(float(np.std(dim_scores)), 2),
                "median": round(float(np.median(dim_scores)), 2),
                "q25": round(float(np.percentile(dim_scores, 25)), 2),
                "q75": round(float(np.percentile(dim_scores, 75)), 2),
                "min": round(float(np.min(dim_scores)), 2),
                "max": round(float(np.max(dim_scores)), 2),
                "n": len(dim_scores)
            }

        diff_stats = {}
        for diff in ["easy", "medium", "hard"]:
            diff_scores = [r["score_pct"] for r in tasks if r["difficulty"] == diff]
            if diff_scores:
                diff_stats[diff] = {
                    "mean": round(float(np.mean(diff_scores)), 2),
                    "std": round(float(np.std(diff_scores)), 2),
                    "n": len(diff_scores)
                }

        summary[mid] = {
            "display_name": model_data["display_name"],
            "overall_mean": round(float(np.mean(all_scores)), 2),
            "overall_std": round(float(np.std(all_scores)), 2),
            "overall_median": round(float(np.median(all_scores)), 2),
            "governance_index": model_data["governance_index"],
            "dimension_stats": dim_stats,
            "difficulty_stats": diff_stats,
            "n_tasks": len(tasks)
        }

    return summary


def effect_sizes_by_dimension(raw_results):
    """Compute Cohen's d effect sizes between best and worst model per dimension."""
    dims = ["compliance", "transparency", "accountability", "safety", "reliability"]
    results = {}

    for d in dims:
        model_scores = {}
        for mid, model_data in raw_results.items():
            scores = [r["score_pct"] for r in model_data["task_results"] if r["dimension"] == d]
            model_scores[mid] = scores

        sorted_models = sorted(model_scores.keys(),
                               key=lambda m: np.mean(model_scores[m]), reverse=True)
        best = sorted_models[0]
        worst = sorted_models[-1]

        best_scores = model_scores[best]
        worst_scores = model_scores[worst]

        # Cohen's d
        mean_diff = np.mean(best_scores) - np.mean(worst_scores)
        pooled_std = np.sqrt((np.std(best_scores)**2 + np.std(worst_scores)**2) / 2)
        cohens_d = float(mean_diff / pooled_std) if pooled_std > 0 else 0

        # Mann-Whitney U
        stat, p = stats.mannwhitneyu(best_scores, worst_scores, alternative='greater')

        results[d] = {
            "best_model": best,
            "worst_model": worst,
            "best_mean": round(float(np.mean(best_scores)), 2),
            "worst_mean": round(float(np.mean(worst_scores)), 2),
            "gap": round(float(np.mean(best_scores) - np.mean(worst_scores)), 2),
            "cohens_d": round(cohens_d, 3),
            "mw_p_value": float(p),
            "significant": bool(p < 0.05)
        }

    return results


def reliability_analysis(raw_results):
    """Analyze score variance as proxy for reliability/consistency."""
    dims = ["compliance", "transparency", "accountability", "safety", "reliability"]
    results = {}

    for mid, model_data in raw_results.items():
        tasks = model_data["task_results"]
        all_scores = [r["score_pct"] for r in tasks]
        cv = float(np.std(all_scores) / np.mean(all_scores)) if np.mean(all_scores) > 0 else 0

        dim_cv = {}
        for d in dims:
            dim_scores = [r["score_pct"] for r in tasks if r["dimension"] == d]
            cv_d = float(np.std(dim_scores) / np.mean(dim_scores)) if np.mean(dim_scores) > 0 else 0
            dim_cv[d] = round(cv_d, 4)

        results[mid] = {
            "display_name": model_data["display_name"],
            "overall_cv": round(cv, 4),
            "dimension_cv": dim_cv,
            "consistency_rank": 0  # filled below
        }

    # Rank by consistency (lower CV = more consistent)
    ranked = sorted(results.keys(), key=lambda m: results[m]["overall_cv"])
    for rank, mid in enumerate(ranked, 1):
        results[mid]["consistency_rank"] = rank

    return results


def main():
    raw_results = load_all_scores()
    print("Running statistical analysis...")

    # 1. Summary statistics
    print("\n1. Computing summary statistics...")
    summary = summary_statistics(raw_results)

    # 2. Pairwise significance tests
    print("2. Running pairwise significance tests...")
    pairwise = pairwise_significance(raw_results)
    n_significant = sum(1 for v in pairwise.values() if v["significant"])
    print(f"   {n_significant}/{len(pairwise)} pairwise comparisons are statistically significant (p<0.05)")

    # 3. Dimension correlations
    print("3. Computing dimension correlations...")
    corr = dimension_correlations(raw_results)

    # 4. Effect sizes
    print("4. Computing effect sizes by dimension...")
    effects = effect_sizes_by_dimension(raw_results)

    # 5. Reliability analysis
    print("5. Analyzing model consistency...")
    reliability = reliability_analysis(raw_results)

    # Compile all results
    analysis_output = {
        "summary_statistics": summary,
        "pairwise_significance": pairwise,
        "dimension_correlations": corr,
        "effect_sizes_by_dimension": effects,
        "reliability_analysis": reliability
    }

    out_path = ANALYSIS_DIR / "statistical_results.json"
    with open(out_path, "w") as f:
        json.dump(analysis_output, f, indent=2)
    print(f"\nStatistical results saved to {out_path}")

    # Print key findings
    print("\n" + "="*70)
    print("KEY STATISTICAL FINDINGS")
    print("="*70)

    print("\nDimension Performance Gaps (best vs worst model):")
    for d, e in effects.items():
        sig = "*" if e["significant"] else ""
        print(f"  {d:20s}: gap={e['gap']:.1f}pts, Cohen's d={e['cohens_d']:.2f}{sig}")

    print("\nDimension Correlations (Spearman, model-level):")
    dims = list(corr.keys())
    print(f"  {'':15s}", end="")
    for d in dims:
        print(f"{d[:5]:8s}", end="")
    print()
    for d1 in dims:
        print(f"  {d1[:15]:15s}", end="")
        for d2 in dims:
            print(f"{corr[d1][d2]:8.2f}", end="")
        print()

    print("\nModel Consistency (Coefficient of Variation, lower=more consistent):")
    for mid, r in sorted(reliability.items(), key=lambda x: x[1]['overall_cv']):
        print(f"  Rank {r['consistency_rank']}: {r['display_name']:35s} CV={r['overall_cv']:.3f}")

    print("\nKruskal-Wallis Test Across All Models:")
    all_scores_by_model = [
        [r["score_pct"] for r in raw_results[mid]["task_results"]]
        for mid in raw_results
    ]
    stat, p = stats.kruskal(*all_scores_by_model)
    print(f"  H-statistic: {stat:.2f}, p-value: {p:.2e}")
    print(f"  Models differ significantly: {p < 0.05}")

    return analysis_output


if __name__ == "__main__":
    main()
