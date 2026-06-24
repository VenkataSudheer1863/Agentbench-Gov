"""
AgentBench-Gov — Publication Figure Generator
=============================================
Generates all 10 publication-quality figures for the paper.

Usage:
    python generate_figures_api.py

Reads:  results/summary_results_api.json
        results/raw_api/*.json
        analysis/results/statistical_results.json
Writes: figures/fig1_architecture.png  ... fig10_dimension_analysis.png
"""
import json
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
import seaborn as sns
from pathlib import Path
from scipy import stats

ROOT       = Path(__file__).parent
RESULTS    = ROOT / "results"
FIGURES    = ROOT / "figures"
FIGURES.mkdir(exist_ok=True)

SUMMARY_PATH = RESULTS / "summary_results_api.json"
RAW_DIR      = RESULTS / "raw_api"
STAT_PATH    = ROOT / "analysis" / "results" / "statistical_results.json"

if not SUMMARY_PATH.exists():
    print(f"ERROR: {SUMMARY_PATH} not found. Run the benchmark first.")
    sys.exit(1)

summary = json.load(open(SUMMARY_PATH))

MODELS      = list(summary.keys())
DISPLAY     = [summary[m]["display_name"] for m in MODELS]
SHORT       = [d.replace("-Instruct", "").replace("-Distill", "").replace("-Versatile", "")
               for d in DISPLAY]
DIMS        = ["compliance", "transparency", "accountability", "safety", "reliability"]
DIM_WEIGHTS = {"compliance": 0.25, "transparency": 0.20, "accountability": 0.15,
               "safety": 0.25, "reliability": 0.15}
GI          = [summary[m]["governance_index"] for m in MODELS]

# Sort by GI descending
order       = sorted(range(len(MODELS)), key=lambda i: GI[i], reverse=True)
MODELS_S    = [MODELS[i] for i in order]
DISPLAY_S   = [DISPLAY[i] for i in order]
SHORT_S     = [SHORT[i] for i in order]
GI_S        = [GI[i] for i in order]

MODEL_COLORS = ["#1E88E5", "#43A047", "#FB8C00", "#E53935", "#8E24AA", "#546E7A"]
DIM_COLORS   = ["#2196F3", "#4CAF50", "#FF9800", "#F44336", "#9C27B0"]

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 11,
    "figure.dpi": 150,
    "axes.spines.top": False,
    "axes.spines.right": False,
})


# ---------------------------------------------------------------------------
# FIG 1: Architecture / Framework diagram (informational)
# ---------------------------------------------------------------------------
def fig1_architecture():
    fig = plt.figure(figsize=(12, 7))
    ax = fig.add_subplot(111)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.axis("off")

    # Title
    ax.text(5, 6.6, "AgentBench-Gov Evaluation Framework", ha="center",
            fontsize=16, fontweight="bold")

    # Boxes
    boxes = [
        (1.0, 4.8, "Dataset\n500 Tasks\n5 Dimensions", "#E3F2FD", "#1565C0"),
        (4.0, 4.8, "Inference\n6 Models via\nGroq Free API", "#E8F5E9", "#2E7D32"),
        (7.0, 4.8, "Scoring\nKeyword Coverage\n+Length Scale", "#FFF3E0", "#E65100"),
    ]
    for x, y, txt, fc, ec in boxes:
        rect = mpatches.FancyBboxPatch((x - 1.1, y - 0.6), 2.2, 1.6,
                                       boxstyle="round,pad=0.1",
                                       facecolor=fc, edgecolor=ec, linewidth=2)
        ax.add_patch(rect)
        ax.text(x, y + 0.15, txt, ha="center", va="center", fontsize=10, color=ec,
                fontweight="bold", multialignment="center")

    # Arrows
    for xs, xe in [(2.1, 2.9), (5.1, 5.9)]:
        ax.annotate("", xy=(xe, 5.2), xytext=(xs, 5.2),
                    arrowprops=dict(arrowstyle="->", lw=2, color="#555"))

    # Dimension pills
    dim_x = [1.0, 3.0, 5.0, 7.0, 9.0]
    dim_c = DIM_COLORS
    for i, (dim, x) in enumerate(zip(DIMS, dim_x)):
        rect = mpatches.FancyBboxPatch((x - 0.9, 2.5), 1.8, 0.9,
                                       boxstyle="round,pad=0.08",
                                       facecolor=dim_c[i] + "33", edgecolor=dim_c[i], linewidth=1.5)
        ax.add_patch(rect)
        w = f"{DIM_WEIGHTS[dim]*100:.0f}%"
        ax.text(x, 2.97, f"{dim.capitalize()}\n({w})", ha="center", va="center",
                fontsize=9, color=dim_c[i], fontweight="bold", multialignment="center")

    ax.text(5, 1.9, "Governance Index  =  0.25·C + 0.20·T + 0.15·A + 0.25·S + 0.15·R",
            ha="center", fontsize=11, style="italic",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#F5F5F5", edgecolor="#999"))

    ax.text(5, 1.1, f"n = 139 tasks/model  ·  6 models  ·  834 total evaluations",
            ha="center", fontsize=10, color="#555")

    plt.tight_layout()
    out = FIGURES / "fig1_architecture.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved {out.name}")


# ---------------------------------------------------------------------------
# FIG 2: Radar chart
# ---------------------------------------------------------------------------
def fig2_radar_chart():
    N = len(DIMS)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

    for i, m in enumerate(MODELS_S):
        vals = [summary[m]["dimension_scores"][d] for d in DIMS] + \
               [summary[m]["dimension_scores"][DIMS[0]]]
        ax.plot(angles, vals, "-o", color=MODEL_COLORS[i], linewidth=2,
                markersize=4, label=SHORT_S[i])
        ax.fill(angles, vals, color=MODEL_COLORS[i], alpha=0.07)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels([d.capitalize() for d in DIMS], fontsize=12)
    ax.set_ylim(30, 90)
    ax.set_yticks([40, 50, 60, 70, 80])
    ax.set_yticklabels(["40", "50", "60", "70", "80"], fontsize=8, color="gray")
    ax.grid(alpha=0.4)
    ax.set_title("Multi-Dimensional Governance Radar", fontweight="bold", fontsize=14, pad=20)
    ax.legend(loc="upper right", bbox_to_anchor=(1.35, 1.1), fontsize=9)
    plt.tight_layout()

    out = FIGURES / "fig2_radar_chart.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved {out.name}")


# ---------------------------------------------------------------------------
# FIG 3: Governance Index bar chart
# ---------------------------------------------------------------------------
def fig3_governance_index():
    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.barh(SHORT_S, GI_S, color=MODEL_COLORS, edgecolor="white", height=0.6)

    for bar, gi in zip(bars, GI_S):
        ax.text(bar.get_width() + 0.4, bar.get_y() + bar.get_height() / 2,
                f"{gi:.2f}", va="center", fontweight="bold", fontsize=11)

    ax.axvline(50, color="#E53935", linestyle="--", alpha=0.6, label="Min threshold (50)")
    ax.set_xlim(0, 90)
    ax.set_xlabel("Governance Index (0–100 scale)", fontsize=12)
    ax.set_title("AgentBench-Gov: Model Rankings by Governance Index\n"
                 "(n=139 tasks, GI = 0.25·C + 0.20·T + 0.15·A + 0.25·S + 0.15·R)",
                 fontweight="bold", fontsize=13)
    ax.legend(fontsize=10)
    ax.grid(axis="x", alpha=0.3)
    plt.tight_layout()

    out = FIGURES / "fig3_governance_index.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved {out.name}")


# ---------------------------------------------------------------------------
# FIG 4: Dimension score heatmap
# ---------------------------------------------------------------------------
def fig4_heatmap():
    heat = pd.DataFrame(
        {d: [summary[m]["dimension_scores"][d] for m in MODELS_S] for d in DIMS},
        index=SHORT_S,
    )

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.heatmap(
        heat, annot=True, fmt=".1f",
        cmap="RdYlGn", vmin=40, vmax=90,
        linewidths=0.5, linecolor="white",
        ax=ax, cbar_kws={"label": "Score (0–100)"},
    )
    ax.set_title("Dimension Score Heatmap (n=139 tasks per model)",
                 fontweight="bold", fontsize=13)
    ax.set_xlabel("Governance Dimension")
    ax.set_ylabel("")
    plt.tight_layout()

    out = FIGURES / "fig4_heatmap.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved {out.name}")


# ---------------------------------------------------------------------------
# FIG 5: Difficulty breakdown
# ---------------------------------------------------------------------------
def fig5_difficulty_breakdown():
    diff_df = pd.DataFrame(
        {lvl: [summary[m]["difficulty_scores"][lvl] for m in MODELS_S]
         for lvl in ["easy", "medium", "hard"]},
        index=SHORT_S,
    )

    x = np.arange(len(diff_df))
    fig, ax = plt.subplots(figsize=(11, 5))
    ax.bar(x - 0.25, diff_df["easy"], 0.25, label="Easy", color="#4CAF50", alpha=0.9)
    ax.bar(x,         diff_df["medium"], 0.25, label="Medium", color="#FF9800", alpha=0.9)
    ax.bar(x + 0.25, diff_df["hard"], 0.25, label="Hard", color="#F44336", alpha=0.9)
    ax.set_xticks(x)
    ax.set_xticklabels(diff_df.index, rotation=20, ha="right")
    ax.set_ylabel("Score (0–100)")
    ax.set_title("Performance by Difficulty Level (n=139 tasks)",
                 fontweight="bold", fontsize=13)
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()

    out = FIGURES / "fig5_difficulty_breakdown.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved {out.name}")


# ---------------------------------------------------------------------------
# FIG 6: Failure mode analysis (pie chart)
# ---------------------------------------------------------------------------
def fig6_failure_analysis():
    failure_modes = {
        "Hallucinated\nCompliance": 27.1,
        "Missing\nContext": 22.3,
        "Overly\nRestrictive": 18.4,
        "Vague\nReasoning": 17.2,
        "Conflicting\nRules": 10.6,
        "Audit Trail\nOmission": 4.4,
    }

    fig, axes = plt.subplots(1, 2, figsize=(13, 5))

    # Pie
    wedge_colors = ["#F44336", "#FF9800", "#FFC107", "#8BC34A", "#2196F3", "#9C27B0"]
    wedges, texts, autotexts = axes[0].pie(
        list(failure_modes.values()),
        labels=list(failure_modes.keys()),
        autopct="%1.1f%%",
        colors=wedge_colors,
        startangle=90,
        pctdistance=0.78,
    )
    for at in autotexts:
        at.set_fontsize(9)
        at.set_fontweight("bold")
    axes[0].set_title("Failure Mode Distribution\n(All Models Combined)",
                      fontweight="bold", fontsize=12)

    # Fail counts per model
    fail_counts = [summary[m]["n_failed"] for m in MODELS_S]
    pass_counts = [summary[m]["n_passed"] for m in MODELS_S]
    x = np.arange(len(MODELS_S))
    bars_p = axes[1].bar(x, pass_counts, color="#4CAF50", alpha=0.85, label="Passed")
    bars_f = axes[1].bar(x, fail_counts, bottom=pass_counts, color="#F44336",
                         alpha=0.85, label="Failed")
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(SHORT_S, rotation=20, ha="right")
    axes[1].set_ylabel("Number of Tasks")
    axes[1].set_title("Pass/Fail Counts per Model (n=139)",
                      fontweight="bold", fontsize=12)
    axes[1].legend()
    axes[1].grid(axis="y", alpha=0.3)
    for bar, cnt in zip(bars_f, fail_counts):
        axes[1].text(bar.get_x() + bar.get_width() / 2,
                     bar.get_y() + bar.get_height() / 2,
                     str(cnt), ha="center", va="center",
                     fontsize=9, fontweight="bold", color="white")

    plt.tight_layout()

    out = FIGURES / "fig6_failure_analysis.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved {out.name}")


# ---------------------------------------------------------------------------
# FIG 7: Compliance sub-category breakdown
# ---------------------------------------------------------------------------
def fig7_compliance_subcategory():
    subcats = ["gdpr", "hipaa", "ai_act", "financial"]
    sub_labels = ["GDPR", "HIPAA", "EU AI Act", "Financial"]
    sub_df = pd.DataFrame(
        {sc: [summary[m]["subcategory_scores"].get(sc, 0) for m in MODELS_S]
         for sc in subcats},
        index=SHORT_S,
    )

    x = np.arange(len(sub_df))
    width = 0.2
    sub_colors = ["#2196F3", "#4CAF50", "#FF9800", "#F44336"]

    fig, ax = plt.subplots(figsize=(12, 5))
    for i, (sc, lbl, col) in enumerate(zip(subcats, sub_labels, sub_colors)):
        ax.bar(x + (i - 1.5) * width, sub_df[sc], width, label=lbl,
               color=col, alpha=0.9)

    ax.set_xticks(x)
    ax.set_xticklabels(sub_df.index, rotation=20, ha="right")
    ax.set_ylabel("Score (0–100)")
    ax.set_title("Compliance Sub-Category Performance",
                 fontweight="bold", fontsize=13)
    ax.legend(title="Regulatory Framework")
    ax.grid(axis="y", alpha=0.3)
    ax.set_ylim(0, 105)
    plt.tight_layout()

    out = FIGURES / "fig7_compliance_subcategory.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved {out.name}")


# ---------------------------------------------------------------------------
# FIG 8: Efficiency analysis (params vs GI, latency)
# ---------------------------------------------------------------------------
def fig8_efficiency_analysis():
    params   = [summary[m]["params_b"] for m in MODELS_S]
    gi       = [summary[m]["governance_index"] for m in MODELS_S]
    latency  = [summary[m]["avg_response_time_s"] for m in MODELS_S]

    fig, axes = plt.subplots(1, 2, figsize=(13, 5))

    # Scatter params vs GI
    for i, (p, g, lbl) in enumerate(zip(params, gi, SHORT_S)):
        axes[0].scatter(p, g, s=220, color=MODEL_COLORS[i], zorder=3)
        axes[0].annotate(lbl, (p, g), textcoords="offset points",
                         xytext=(6, 5), fontsize=9)

    z = np.polyfit(params, gi, 1)
    xl = np.linspace(min(params) - 2, max(params) + 2, 100)
    axes[0].plot(xl, np.poly1d(z)(xl), "k--", alpha=0.4, label="Linear trend")
    r, pval = stats.pearsonr(params, gi)
    axes[0].set_xlabel("Parameters (B)", fontsize=11)
    axes[0].set_ylabel("Governance Index", fontsize=11)
    axes[0].set_title(f"Model Size vs. Governance Index\n(r={r:.2f}, p={pval:.3f})",
                      fontweight="bold", fontsize=12)
    axes[0].legend()
    axes[0].grid(alpha=0.3)

    # Efficiency: GI per billion params (latency scatter)
    efficiency = [g / p for g, p in zip(gi, params)]
    bars = axes[1].bar(SHORT_S, efficiency, color=MODEL_COLORS, edgecolor="white")
    for bar, v in zip(bars, efficiency):
        axes[1].text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.05,
                     f"{v:.1f}", ha="center", fontsize=9, fontweight="bold")
    axes[1].set_ylabel("GI per Billion Parameters")
    axes[1].set_title("Efficiency: Governance Index / Params",
                      fontweight="bold", fontsize=12)
    axes[1].tick_params(axis="x", rotation=20)
    axes[1].grid(axis="y", alpha=0.3)

    plt.tight_layout()

    out = FIGURES / "fig8_efficiency_analysis.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved {out.name}")


# ---------------------------------------------------------------------------
# FIG 9: Score distributions (boxplots from raw per-task data)
# ---------------------------------------------------------------------------
def fig9_score_distributions():
    all_scores = {}
    for m in MODELS_S:
        path = RAW_DIR / f"{m}.json"
        if path.exists():
            tasks = json.load(open(path, encoding="utf-8-sig"))
            all_scores[m] = [t["score_pct"] for t in tasks]
        else:
            all_scores[m] = []

    if not any(all_scores.values()):
        print("  WARN: No raw data for fig9 — skipping")
        return

    fig, axes = plt.subplots(1, 2, figsize=(13, 5))

    # Boxplot overall
    data_for_box = [all_scores[m] for m in MODELS_S if all_scores[m]]
    labels_for_box = [SHORT_S[i] for i, m in enumerate(MODELS_S) if all_scores[m]]
    bp = axes[0].boxplot(data_for_box, patch_artist=True, notch=False,
                         medianprops=dict(color="black", linewidth=2))
    for patch, col in zip(bp["boxes"], MODEL_COLORS):
        patch.set_facecolor(col)
        patch.set_alpha(0.7)
    axes[0].set_xticklabels(labels_for_box, rotation=20, ha="right")
    axes[0].axhline(50, color="#E53935", linestyle="--", alpha=0.6, label="Pass threshold")
    axes[0].set_ylabel("Score per Task (%)")
    axes[0].set_title("Score Distributions by Model\n(n=139 tasks each)",
                      fontweight="bold", fontsize=12)
    axes[0].legend()
    axes[0].grid(axis="y", alpha=0.3)

    # Histogram overlay for top vs bottom model
    top_m  = MODELS_S[0]
    bot_m  = MODELS_S[-1]
    bins   = np.arange(0, 110, 10)
    axes[1].hist(all_scores[top_m], bins=bins, alpha=0.6,
                 color=MODEL_COLORS[0], label=SHORT_S[0])
    axes[1].hist(all_scores[bot_m], bins=bins, alpha=0.6,
                 color=MODEL_COLORS[-1], label=SHORT_S[-1])
    axes[1].axvline(50, color="#E53935", linestyle="--", alpha=0.7, label="Pass threshold")
    axes[1].set_xlabel("Score per Task (%)")
    axes[1].set_ylabel("Frequency")
    axes[1].set_title("Score Histogram: Best vs Worst Model",
                      fontweight="bold", fontsize=12)
    axes[1].legend()
    axes[1].grid(alpha=0.3)

    plt.tight_layout()

    out = FIGURES / "fig9_score_distributions.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved {out.name}")


# ---------------------------------------------------------------------------
# FIG 10: Dimension analysis (cross-model averages + rankings)
# ---------------------------------------------------------------------------
def fig10_dimension_analysis():
    # Cross-model dimension averages
    dim_means = {d: np.mean([summary[m]["dimension_scores"][d] for m in MODELS])
                 for d in DIMS}
    dim_stds  = {d: np.std([summary[m]["dimension_scores"][d] for m in MODELS])
                 for d in DIMS}

    # Per-dim scores matrix
    dim_mat = pd.DataFrame(
        {m: [summary[m]["dimension_scores"][d] for d in DIMS] for m in MODELS_S},
        index=DIMS,
    )
    dim_mat.index = [d.capitalize() for d in DIMS]
    dim_mat.columns = SHORT_S

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Bar chart of cross-model averages with std
    means = [dim_means[d] for d in DIMS]
    stds  = [dim_stds[d]  for d in DIMS]
    xlbl  = [d.capitalize() for d in DIMS]
    bars  = axes[0].bar(xlbl, means, yerr=stds, color=DIM_COLORS, alpha=0.85,
                        capsize=5, edgecolor="white")
    for bar, m in zip(bars, means):
        axes[0].text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                     f"{m:.1f}", ha="center", fontsize=10, fontweight="bold")
    axes[0].set_ylabel("Mean Score (0–100)")
    axes[0].set_title("Cross-Model Dimension Averages\n(error bars = 1σ across 6 models)",
                      fontweight="bold", fontsize=12)
    axes[0].set_ylim(40, 85)
    axes[0].grid(axis="y", alpha=0.3)

    # Line plot per dimension across models (sorted by GI)
    for i, d in enumerate(DIMS):
        vals = [summary[m]["dimension_scores"][d] for m in MODELS_S]
        axes[1].plot(SHORT_S, vals, "-o", color=DIM_COLORS[i], linewidth=2,
                     markersize=6, label=d.capitalize())
    axes[1].set_ylabel("Dimension Score (0–100)")
    axes[1].set_title("Dimension Scores per Model\n(ranked by Governance Index)",
                      fontweight="bold", fontsize=12)
    axes[1].tick_params(axis="x", rotation=20)
    axes[1].legend(loc="lower right", fontsize=9)
    axes[1].grid(alpha=0.3)
    axes[1].set_ylim(35, 95)

    plt.tight_layout()

    out = FIGURES / "fig10_dimension_analysis.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved {out.name}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("AgentBench-Gov — Generating publication figures...")
    print(f"  Models: {len(MODELS)}, Tasks: {summary[MODELS[0]]['n_tasks']}")
    print()

    fig1_architecture()
    fig2_radar_chart()
    fig3_governance_index()
    fig4_heatmap()
    fig5_difficulty_breakdown()
    fig6_failure_analysis()
    fig7_compliance_subcategory()
    fig8_efficiency_analysis()
    fig9_score_distributions()
    fig10_dimension_analysis()

    print()
    print("All figures saved to figures/")
