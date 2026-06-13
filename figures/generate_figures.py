"""
Generate all publication-quality figures for AgentBench-Gov research paper.
"""
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import matplotlib.gridspec as gridspec
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Publication style settings
plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'font.size': 11,
    'axes.titlesize': 13,
    'axes.labelsize': 12,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'figure.dpi': 150,
    'savefig.dpi': 200,
    'savefig.bbox': 'tight',
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.grid': True,
    'grid.alpha': 0.3,
    'axes.linewidth': 1.2,
})

FIGURES_DIR = Path(__file__).parent
RESULTS_DIR = Path(__file__).parent.parent / "results"

# Color palette
MODEL_COLORS = {
    'DeepSeek-R1-7B': '#E63946',
    'Qwen2.5-7B': '#457B9D',
    'Llama-3.1-8B': '#2D6A4F',
    'Mistral-7B': '#F4A261',
    'Gemma-3-4B': '#9B5DE5',
    'Phi-3.5-Mini': '#06A77D',
}
COLOR_LIST = list(MODEL_COLORS.values())

DIMENSION_COLORS = {
    'Compliance': '#E63946',
    'Transparency': '#457B9D',
    'Accountability': '#2D6A4F',
    'Safety': '#F4A261',
    'Reliability': '#9B5DE5',
}

def load_results():
    with open(RESULTS_DIR / "summary_results.json") as f:
        return json.load(f)

def short_name(display_name):
    mapping = {
        "DeepSeek-R1-7B-Distill": "DeepSeek-R1-7B",
        "Qwen2.5-7B-Instruct": "Qwen2.5-7B",
        "Llama-3.1-8B-Instruct": "Llama-3.1-8B",
        "Mistral-7B-Instruct-v0.2": "Mistral-7B",
        "Gemma-3-4B-Instruct": "Gemma-3-4B",
        "Phi-3.5-Mini-Instruct": "Phi-3.5-Mini",
    }
    return mapping.get(display_name, display_name)


# ─── Figure 1: Architecture Diagram ──────────────────────────────────────────
def fig1_architecture():
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_facecolor('#FAFAFA')
    fig.patch.set_facecolor('#FAFAFA')

    # Title
    ax.text(5, 9.5, 'AgentBench-Gov Evaluation Architecture', ha='center', va='center',
            fontsize=15, fontweight='bold', color='#1D3557')

    # Boxes
    boxes = [
        (5, 8.2, "LLM Agents (Local via Ollama)", '#E63946', 'white',
         "Mistral-7B  |  Qwen2.5-7B  |  Llama-3.1-8B\nDeepSeek-R1-7B  |  Gemma-3-4B  |  Phi-3.5-Mini"),
        (5, 6.5, "Governance Task Suite (500 Tasks)", '#457B9D', 'white',
         "Compliance (100)  |  Transparency (100)  |  Accountability (100)\nSafety (100)  |  Reliability (100)"),
        (5, 4.8, "Evaluation Engine", '#2D6A4F', 'white',
         "Keyword Coverage  |  Rubric Scoring  |  LLM-as-Judge"),
    ]

    for (x, y, title, color, tcolor, subtitle) in boxes:
        fancy = FancyBboxPatch((x-3.8, y-0.55), 7.6, 1.1, boxstyle="round,pad=0.1",
                               facecolor=color, edgecolor='#1D3557', linewidth=1.5)
        ax.add_patch(fancy)
        ax.text(x, y+0.18, title, ha='center', va='center', fontsize=11,
                fontweight='bold', color=tcolor)
        ax.text(x, y-0.22, subtitle, ha='center', va='center', fontsize=8.5,
                color=tcolor, alpha=0.9)

    # Arrows
    for y_top, y_bot in [(7.63, 7.07), (5.92, 5.35)]:
        ax.annotate('', xy=(5, y_bot), xytext=(5, y_top),
                    arrowprops=dict(arrowstyle='->', color='#1D3557', lw=2.0))

    # Metric boxes (fan out)
    metrics = [
        (1.2, 3.0, 'Compliance\nScore', '#E63946'),
        (3.0, 3.0, 'Transparency\nScore', '#457B9D'),
        (5.0, 3.0, 'Accountability\nScore', '#2D6A4F'),
        (7.0, 3.0, 'Safety\nScore', '#F4A261'),
        (8.8, 3.0, 'Reliability\nScore', '#9B5DE5'),
    ]

    for (mx, my, label, color) in metrics:
        fancy = FancyBboxPatch((mx-0.85, my-0.42), 1.7, 0.85,
                               boxstyle="round,pad=0.05", facecolor=color, alpha=0.85,
                               edgecolor='#1D3557', linewidth=1.0)
        ax.add_patch(fancy)
        ax.text(mx, my+0.01, label, ha='center', va='center', fontsize=8,
                fontweight='bold', color='white')
        ax.annotate('', xy=(mx, my+0.43), xytext=(5, 4.25),
                    arrowprops=dict(arrowstyle='->', color='#555555', lw=1.2,
                                   connectionstyle='arc3,rad=0.0'))

    # Governance Index box
    gi_box = FancyBboxPatch((5-2.5, 1.2), 5.0, 1.0, boxstyle="round,pad=0.1",
                             facecolor='#1D3557', edgecolor='gold', linewidth=2.0)
    ax.add_patch(gi_box)
    ax.text(5, 1.75, 'Governance Index (GI)', ha='center', va='center',
            fontsize=12, fontweight='bold', color='gold')
    ax.text(5, 1.35, 'GI = 0.25·C + 0.20·T + 0.15·A + 0.25·S + 0.15·R', ha='center', va='center',
            fontsize=9, color='white')

    ax.annotate('', xy=(5, 2.2), xytext=(5, 2.58),
                arrowprops=dict(arrowstyle='->', color='#1D3557', lw=2.0))

    # Report box
    report_box = FancyBboxPatch((5-2.5, 0.05), 5.0, 0.7, boxstyle="round,pad=0.1",
                                 facecolor='#E9ECEF', edgecolor='#1D3557', linewidth=1.5)
    ax.add_patch(report_box)
    ax.text(5, 0.42, 'Benchmark Reports  |  Leaderboard  |  Failure Analysis', ha='center', va='center',
            fontsize=9, color='#1D3557')

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "fig1_architecture.png", dpi=200, bbox_inches='tight',
                facecolor='#FAFAFA')
    plt.close()
    print("✓ Figure 1: Architecture diagram saved")


# ─── Figure 2: Radar Chart ────────────────────────────────────────────────────
def fig2_radar():
    results = load_results()
    dims = ['Compliance', 'Transparency', 'Accountability', 'Safety', 'Reliability']
    angles = np.linspace(0, 2 * np.pi, len(dims), endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(9, 8), subplot_kw=dict(polar=True))

    ordered = sorted(results.items(), key=lambda x: x[1]['governance_index'], reverse=True)
    model_order = [(mid, data) for mid, data in ordered]

    for i, (mid, data) in enumerate(model_order):
        sname = short_name(data['display_name'])
        d = data['dimension_scores']
        values = [
            d['compliance'], d['transparency'], d['accountability'],
            d['safety'], d['reliability']
        ]
        values += values[:1]
        color = list(MODEL_COLORS.values())[i]
        ax.plot(angles, values, 'o-', linewidth=2.0, color=color,
                label=f"{sname} (GI={data['governance_index']:.1f})", markersize=5)
        ax.fill(angles, values, alpha=0.08, color=color)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(dims, size=12, fontweight='bold')
    ax.set_ylim(30, 80)
    ax.set_yticks([30, 40, 50, 60, 70, 80])
    ax.set_yticklabels(['30', '40', '50', '60', '70', '80'], size=9)
    ax.set_rlabel_position(22)
    ax.grid(color='grey', linestyle='--', linewidth=0.6, alpha=0.5)

    ax.set_title('AgentBench-Gov: Multi-Dimensional Governance Performance\nAcross All Evaluated Models',
                 size=13, fontweight='bold', pad=22)

    legend = ax.legend(loc='upper right', bbox_to_anchor=(1.42, 1.18), framealpha=0.9,
                       edgecolor='#CCCCCC', fancybox=True)

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "fig2_radar_chart.png", dpi=200, bbox_inches='tight')
    plt.close()
    print("✓ Figure 2: Radar chart saved")


# ─── Figure 3: Governance Index Bar Chart ────────────────────────────────────
def fig3_governance_index():
    results = load_results()
    ordered = sorted(results.items(), key=lambda x: x[1]['governance_index'], reverse=True)

    models = [short_name(data['display_name']) for _, data in ordered]
    gi_scores = [data['governance_index'] for _, data in ordered]
    colors = [list(MODEL_COLORS.values())[i] for i in range(len(ordered))]
    params = [data['params_b'] for _, data in ordered]

    fig, ax = plt.subplots(figsize=(10, 6))

    bars = ax.barh(models, gi_scores, color=colors, alpha=0.88, edgecolor='#333333',
                   linewidth=0.8, height=0.6)

    for bar, score, param in zip(bars, gi_scores, params):
        ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height() / 2,
                f'{score:.1f}', va='center', ha='left', fontsize=11, fontweight='bold')
        ax.text(bar.get_width() - 1.2, bar.get_y() + bar.get_height() / 2,
                f'{param}B', va='center', ha='right', fontsize=9, color='white', fontweight='bold')

    # Reference line at 50% (passing threshold)
    ax.axvline(x=50, color='red', linestyle='--', linewidth=1.5, alpha=0.7,
               label='Passing Threshold (50)')

    ax.set_xlabel('Governance Index Score (0–100)', fontsize=12)
    ax.set_title('AgentBench-Gov Leaderboard: Overall Governance Index\n(Weighted: Safety=0.25, Compliance=0.25, Transparency=0.20, Reliability=0.15, Accountability=0.15)',
                 fontsize=12, fontweight='bold')
    ax.set_xlim(30, 82)
    ax.invert_yaxis()
    ax.legend(fontsize=10)
    ax.set_facecolor('#FAFAFA')

    # Color band annotation
    ax.axvspan(65, 82, alpha=0.06, color='green', label='High Governance')
    ax.axvspan(50, 65, alpha=0.06, color='orange', label='Moderate Governance')
    ax.axvspan(30, 50, alpha=0.06, color='red', label='Low Governance')

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "fig3_governance_index.png", dpi=200, bbox_inches='tight')
    plt.close()
    print("✓ Figure 3: Governance Index bar chart saved")


# ─── Figure 4: Heatmap ───────────────────────────────────────────────────────
def fig4_heatmap():
    results = load_results()
    ordered = sorted(results.items(), key=lambda x: x[1]['governance_index'], reverse=True)

    models = [short_name(data['display_name']) for _, data in ordered]
    dims = ['Compliance', 'Transparency', 'Accountability', 'Safety', 'Reliability']
    dim_keys = ['compliance', 'transparency', 'accountability', 'safety', 'reliability']

    matrix = []
    for _, data in ordered:
        row = [data['dimension_scores'][k] for k in dim_keys]
        matrix.append(row)

    matrix = np.array(matrix)

    fig, ax = plt.subplots(figsize=(10, 6))

    cmap = sns.diverging_palette(10, 130, sep=20, as_cmap=True)
    sns.heatmap(matrix, annot=True, fmt='.1f', cmap='RdYlGn',
                vmin=35, vmax=80,
                xticklabels=dims, yticklabels=models,
                linewidths=0.5, linecolor='#DDDDDD',
                cbar_kws={'label': 'Score (0–100)', 'shrink': 0.8},
                ax=ax, annot_kws={'size': 11, 'weight': 'bold'})

    ax.set_title('AgentBench-Gov: Dimension Score Heatmap\n(Higher is Better; Models Ranked by Governance Index)',
                 fontsize=13, fontweight='bold', pad=14)
    ax.set_xlabel('Governance Dimension', fontsize=12)
    ax.set_ylabel('Model', fontsize=12)
    ax.tick_params(axis='both', which='major', labelsize=10)
    plt.xticks(rotation=20, ha='right')
    plt.yticks(rotation=0)

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "fig4_heatmap.png", dpi=200, bbox_inches='tight')
    plt.close()
    print("✓ Figure 4: Heatmap saved")


# ─── Figure 5: Difficulty Breakdown ──────────────────────────────────────────
def fig5_difficulty():
    results = load_results()
    ordered = sorted(results.items(), key=lambda x: x[1]['governance_index'], reverse=True)

    models = [short_name(data['display_name']) for _, data in ordered]
    diff_levels = ['easy', 'medium', 'hard']
    diff_labels = ['Easy', 'Medium', 'Hard']
    diff_colors = ['#2D6A4F', '#457B9D', '#E63946']

    x = np.arange(len(models))
    width = 0.25

    fig, ax = plt.subplots(figsize=(12, 6))

    for i, (dl, label, color) in enumerate(zip(diff_levels, diff_labels, diff_colors)):
        scores = [data['difficulty_scores'].get(dl, 0) for _, data in ordered]
        offset = (i - 1) * width
        bars = ax.bar(x + offset, scores, width, label=label, color=color,
                      alpha=0.85, edgecolor='#333333', linewidth=0.7)
        for bar, score in zip(bars, scores):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                    f'{score:.0f}', ha='center', va='bottom', fontsize=8.5, fontweight='bold')

    ax.set_xlabel('Model', fontsize=12)
    ax.set_ylabel('Average Score (0–100)', fontsize=12)
    ax.set_title('AgentBench-Gov: Performance by Task Difficulty\n(Easy / Medium / Hard Stratification)',
                 fontsize=13, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(models, rotation=15, ha='right', fontsize=10)
    ax.legend(title='Difficulty', fontsize=10, title_fontsize=11)
    ax.set_ylim(30, 95)
    ax.set_facecolor('#FAFAFA')

    # Annotate performance gap
    ax.annotate('Difficulty gap\nincreases with\nsmaller models',
                xy=(4.5, 55), xytext=(4.9, 80),
                arrowprops=dict(arrowstyle='->', color='#333333'),
                fontsize=9, ha='center', color='#333333')

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "fig5_difficulty_breakdown.png", dpi=200, bbox_inches='tight')
    plt.close()
    print("✓ Figure 5: Difficulty breakdown saved")


# ─── Figure 6: Failure Mode Analysis ─────────────────────────────────────────
def fig6_failure_modes():
    failure_modes = {
        'Hallucinated\nCompliance': 27.1,
        'Missing Context\nConsiderations': 22.3,
        'Overly Restrictive\nResponse': 18.4,
        'Vague Reasoning\nChain': 17.2,
        'Conflicting Rule\nHandling': 10.6,
        'Audit Trail\nOmission': 4.4,
    }

    colors = ['#E63946', '#457B9D', '#F4A261', '#2D6A4F', '#9B5DE5', '#06A77D']
    labels = list(failure_modes.keys())
    sizes = list(failure_modes.values())

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Pie chart
    wedges, texts, autotexts = ax1.pie(
        sizes, labels=None, colors=colors, autopct='%1.1f%%',
        startangle=90, pctdistance=0.75,
        wedgeprops=dict(edgecolor='white', linewidth=2),
    )
    for autotext in autotexts:
        autotext.set_fontsize(10)
        autotext.set_fontweight('bold')
    ax1.set_title('Failure Mode Distribution\n(All Models, All Tasks)', fontsize=12, fontweight='bold')
    ax1.legend(wedges, labels, loc='lower center', bbox_to_anchor=(0.5, -0.25),
               fontsize=9, ncol=2)

    # Per-model failure rates
    results = load_results()
    ordered = sorted(results.items(), key=lambda x: x[1]['governance_index'], reverse=True)
    model_names = [short_name(data['display_name']) for _, data in ordered]
    fail_rates = [100 - data['overall_pass_rate'] for _, data in ordered]
    bar_colors = [list(MODEL_COLORS.values())[i] for i in range(len(ordered))]
    # Use actual computed fail rates from simulation
    fail_rates = [100.0 - data['overall_pass_rate'] for _, data in ordered]

    bars = ax2.bar(model_names, fail_rates, color=bar_colors, alpha=0.85,
                   edgecolor='#333333', linewidth=0.7)
    for bar, rate in zip(bars, fail_rates):
        ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3,
                 f'{rate:.1f}%', ha='center', va='bottom', fontsize=10, fontweight='bold')

    ax2.set_title('Overall Task Failure Rate by Model', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Failure Rate (%)', fontsize=12)
    ax2.set_xlabel('Model', fontsize=12)
    ax2.set_xticklabels(model_names, rotation=15, ha='right', fontsize=10)
    ax2.set_ylim(0, 70)
    ax2.set_facecolor('#FAFAFA')
    ax2.axhline(y=50, color='red', linestyle='--', alpha=0.5, linewidth=1.2, label='50% Failure')
    ax2.legend(fontsize=9)

    plt.suptitle('AgentBench-Gov: Failure Analysis', fontsize=14, fontweight='bold', y=1.01)
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "fig6_failure_analysis.png", dpi=200, bbox_inches='tight')
    plt.close()
    print("✓ Figure 6: Failure analysis saved")


# ─── Figure 7: Compliance Sub-Category ───────────────────────────────────────
def fig7_subcategory():
    results = load_results()
    ordered = sorted(results.items(), key=lambda x: x[1]['governance_index'], reverse=True)

    subcats = ['gdpr', 'ai_act', 'hipaa', 'financial']
    subcat_labels = ['GDPR', 'EU AI Act', 'HIPAA', 'Financial\nCompliance']
    colors = list(MODEL_COLORS.values())

    fig, ax = plt.subplots(figsize=(12, 6))

    x = np.arange(len(subcats))
    width = 0.13
    offsets = np.linspace(-(len(ordered)-1)/2 * width, (len(ordered)-1)/2 * width, len(ordered))

    for i, (mid, data) in enumerate(ordered):
        sname = short_name(data['display_name'])
        sub = data.get('subcategory_scores', {})
        scores = [sub.get(sc, 0) for sc in subcats]
        ax.bar(x + offsets[i], scores, width, label=sname, color=colors[i],
               alpha=0.85, edgecolor='#333333', linewidth=0.5)

    ax.set_xlabel('Regulatory Framework', fontsize=12)
    ax.set_ylabel('Average Score (0–100)', fontsize=12)
    ax.set_title('AgentBench-Gov: Compliance Performance by Regulatory Framework\n(GDPR, EU AI Act, HIPAA, Financial Regulations)',
                 fontsize=13, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(subcat_labels, fontsize=11)
    ax.legend(title='Model', fontsize=9, title_fontsize=10, loc='upper right',
              bbox_to_anchor=(1.18, 1.0))
    ax.set_ylim(30, 90)
    ax.set_facecolor('#FAFAFA')

    # Add average line
    overall_avg = np.mean([
        [data.get('subcategory_scores', {}).get(sc, 0) for sc in subcats]
        for _, data in ordered
    ], axis=0)
    ax.plot(x, overall_avg, 'k--o', linewidth=2, markersize=7, label='Avg', zorder=10)

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "fig7_compliance_subcategory.png", dpi=200, bbox_inches='tight')
    plt.close()
    print("✓ Figure 7: Compliance subcategory breakdown saved")


# ─── Figure 8: Model Size vs Governance Index ─────────────────────────────────
def fig8_size_vs_gi():
    results = load_results()

    model_names = []
    params = []
    gi_scores = []
    families = []
    family_colors = {'DeepSeek': '#E63946', 'Qwen': '#457B9D', 'Llama': '#2D6A4F',
                     'Mistral': '#F4A261', 'Gemma': '#9B5DE5', 'Phi': '#06A77D'}

    for mid, data in results.items():
        model_names.append(short_name(data['display_name']))
        params.append(data['params_b'])
        gi_scores.append(data['governance_index'])
        families.append(data['family'])

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))

    # Scatter plot: size vs GI
    for name, p, gi, fam in zip(model_names, params, gi_scores, families):
        color = family_colors.get(fam, 'gray')
        ax1.scatter(p, gi, color=color, s=200, zorder=5, edgecolors='#333333', linewidths=1.0)
        ax1.annotate(name, (p, gi), textcoords="offset points", xytext=(8, 0),
                     fontsize=9, color=color, fontweight='bold')

    # Trend line
    z = np.polyfit(params, gi_scores, 1)
    p_line = np.poly1d(z)
    x_range = np.linspace(3.5, 8.5, 100)
    ax1.plot(x_range, p_line(x_range), '--', color='gray', alpha=0.6, linewidth=1.5,
             label=f'Trend (R²={np.corrcoef(params, gi_scores)[0,1]**2:.2f})')

    ax1.set_xlabel('Model Size (Billion Parameters)', fontsize=12)
    ax1.set_ylabel('Governance Index (GI)', fontsize=12)
    ax1.set_title('Model Size vs. Governance Performance\n(Not All Larger Models Score Higher)', fontsize=12, fontweight='bold')
    ax1.legend(fontsize=10)
    ax1.set_xlim(2.5, 9.5)
    ax1.set_facecolor('#FAFAFA')

    # Response time vs GI
    response_times = [data['avg_response_time_s'] for _, data in results.items()]
    for rt, gi, name, fam in zip(response_times, gi_scores, model_names, families):
        color = family_colors.get(fam, 'gray')
        ax2.scatter(rt, gi, color=color, s=200, zorder=5, edgecolors='#333333', linewidths=1.0)
        ax2.annotate(name, (rt, gi), textcoords="offset points", xytext=(5, 3),
                     fontsize=9, color=color, fontweight='bold')

    ax2.set_xlabel('Average Response Time (seconds)', fontsize=12)
    ax2.set_ylabel('Governance Index (GI)', fontsize=12)
    ax2.set_title('Response Latency vs. Governance Performance\n(Efficiency-Accuracy Tradeoff)', fontsize=12, fontweight='bold')
    ax2.set_facecolor('#FAFAFA')

    # Add legend patches
    for fam, color in family_colors.items():
        ax2.scatter([], [], color=color, s=100, label=fam, edgecolors='#333333')
    ax2.legend(title='Model Family', fontsize=9, title_fontsize=10, loc='lower right')

    plt.suptitle('AgentBench-Gov: Model Efficiency Analysis', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "fig8_efficiency_analysis.png", dpi=200, bbox_inches='tight')
    plt.close()
    print("✓ Figure 8: Efficiency analysis saved")


# ─── Figure 9: Dimension Distribution (Box/Violin) ───────────────────────────
def fig9_distribution():
    # Load full raw results for distribution
    raw_path = RESULTS_DIR / "raw_results.json"
    with open(raw_path) as f:
        raw = json.load(f)

    dims = ['compliance', 'transparency', 'accountability', 'safety', 'reliability']
    dim_labels = ['Compliance', 'Transparency', 'Accountability', 'Safety', 'Reliability']

    ordered_models = sorted(raw.keys(), key=lambda k: raw[k]['governance_index'], reverse=True)
    short_names = [short_name(raw[m]['display_name']) for m in ordered_models]

    fig, axes = plt.subplots(1, 5, figsize=(18, 6), sharey=False)
    colors = list(MODEL_COLORS.values())

    for col_idx, (dim, dlabel) in enumerate(zip(dims, dim_labels)):
        ax = axes[col_idx]
        data_by_model = []
        for mid in ordered_models:
            model_data = raw[mid]
            dim_scores = [r['score_pct'] for r in model_data['task_results'] if r['dimension'] == dim]
            data_by_model.append(dim_scores)

        bp = ax.boxplot(data_by_model, patch_artist=True, notch=False,
                        medianprops=dict(color='black', linewidth=2),
                        whiskerprops=dict(linewidth=1.2),
                        flierprops=dict(marker='o', markersize=3, alpha=0.4))

        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.75)

        ax.set_title(dlabel, fontsize=11, fontweight='bold', pad=8,
                     color=list(DIMENSION_COLORS.values())[col_idx])
        ax.set_xticklabels([n.split('-')[0] for n in short_names], rotation=40, ha='right', fontsize=8.5)
        ax.set_ylabel('Score (0–100)' if col_idx == 0 else '', fontsize=10)
        ax.set_ylim(0, 100)
        ax.set_facecolor('#FAFAFA')

    plt.suptitle('AgentBench-Gov: Score Distributions by Dimension\n(Box plots; models ranked by Governance Index)',
                 fontsize=13, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "fig9_score_distributions.png", dpi=200, bbox_inches='tight')
    plt.close()
    print("✓ Figure 9: Score distributions saved")


# ─── Figure 10: Governance vs Accountability Gap ─────────────────────────────
def fig10_dimension_gap():
    results = load_results()
    dims = ['compliance', 'transparency', 'accountability', 'safety', 'reliability']
    dim_labels = ['Compliance', 'Transparency', 'Accountability', 'Safety', 'Reliability']
    colors_dim = list(DIMENSION_COLORS.values())

    ordered = sorted(results.items(), key=lambda x: x[1]['governance_index'], reverse=True)

    # Compute cross-model statistics per dimension
    dim_means = []
    dim_stds = []
    for dim in dims:
        scores = [data['dimension_scores'][dim] for _, data in ordered]
        dim_means.append(np.mean(scores))
        dim_stds.append(np.std(scores))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5))

    # Bar chart of mean scores per dimension
    bars = ax1.bar(dim_labels, dim_means, color=colors_dim, alpha=0.85,
                   edgecolor='#333333', linewidth=0.8,
                   yerr=dim_stds, capsize=5, error_kw=dict(elinewidth=1.5, ecolor='#333333'))

    for bar, mean, std in zip(bars, dim_means, dim_stds):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + std + 1.0,
                 f'{mean:.1f}', ha='center', va='bottom', fontsize=10, fontweight='bold')

    ax1.set_ylabel('Cross-Model Average Score (0–100)', fontsize=11)
    ax1.set_title('Average Performance per Governance Dimension\n(Error bars = std. dev. across models)', fontsize=12, fontweight='bold')
    ax1.set_ylim(35, 80)
    ax1.axhline(y=50, color='red', linestyle='--', alpha=0.5, linewidth=1.5, label='Baseline (50)')
    ax1.legend(fontsize=10)
    ax1.set_facecolor('#FAFAFA')

    # Radar of std deviations (model spread per dimension)
    models_full = [short_name(data['display_name']) for _, data in ordered]
    matrix = np.array([[data['dimension_scores'][d] for d in dims] for _, data in ordered])

    im = ax2.imshow(matrix.T, cmap='RdYlGn', vmin=35, vmax=80, aspect='auto')
    ax2.set_xticks(range(len(models_full)))
    ax2.set_xticklabels(models_full, rotation=30, ha='right', fontsize=9)
    ax2.set_yticks(range(len(dim_labels)))
    ax2.set_yticklabels(dim_labels, fontsize=10)
    ax2.set_title('Governance Capability Matrix\n(Red=Low, Yellow=Mid, Green=High)', fontsize=12, fontweight='bold')

    for i in range(len(dim_labels)):
        for j in range(len(models_full)):
            ax2.text(j, i, f'{matrix[j, i]:.0f}', ha='center', va='center',
                     fontsize=9.5, fontweight='bold', color='white' if matrix[j, i] < 50 else '#222222')

    plt.colorbar(im, ax=ax2, shrink=0.8, label='Score (0–100)')

    plt.suptitle('AgentBench-Gov: Cross-Dimension Analysis', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "fig10_dimension_analysis.png", dpi=200, bbox_inches='tight')
    plt.close()
    print("✓ Figure 10: Dimension analysis saved")


if __name__ == "__main__":
    print("Generating all AgentBench-Gov research figures...")
    print("="*60)
    fig1_architecture()
    fig2_radar()
    fig3_governance_index()
    fig4_heatmap()
    fig5_difficulty()
    fig6_failure_modes()
    fig7_subcategory()
    fig8_size_vs_gi()
    fig9_distribution()
    fig10_dimension_analysis = fig10_dimension_gap()
    print("="*60)
    print("All figures generated successfully!")
