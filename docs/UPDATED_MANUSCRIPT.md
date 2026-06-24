# AgentBench-Gov: A Comprehensive Benchmark for Evaluating Governance-Aware Capabilities in Large Language Models via Free Inference APIs

**Venkata Sudheer Paruchuri**
Independent Researcher
paruchurivenkatasudheer@gmail.com

**Dr. J.J. Jayakanth** *(Expert Advisor)*
Methodology Reviewer and Benchmark Validation Oversight

---

> **Target:** *AI & Ethics* (Springer, Q2)
> **Track:** Original Research
> **Keywords:** AI Governance, LLM Evaluation, Benchmark, Regulatory Compliance, Responsible AI, Free Inference APIs

---

## Abstract

The deployment of autonomous AI agents in regulated domains demands rigorous evaluation of their governance, compliance, transparency, accountability, safety, and reliability capabilities. Existing benchmarks primarily assess task completion and knowledge recall, leaving governance capability largely unmeasured. We present **AgentBench-Gov**, an open-source benchmark comprising 500 governance-specific evaluation tasks across five dimensions—Compliance, Transparency, Accountability, Safety, and Reliability—grounded in real-world regulatory frameworks including GDPR, EU AI Act, HIPAA, and financial regulations (SOX, MiFID II). We evaluate six LLMs via free inference APIs (Groq)—Llama4-Scout, Llama-3.1-8B, Llama-3.3-70B, Qwen3-32B, Allam-2-7B, and GPT-OSS-120B—using a novel weighted **Governance Index (GI)** metric. Our stratified evaluation across all five governance dimensions reveals: (1) significant inter-model variance in governance capabilities (GI range: 52.3–77.5); (2) Transparency as the consistently weakest dimension across all models (cross-model mean: 59.4); (3) Llama4-Scout achieves the highest governance performance (GI = 77.5, 90.6% pass rate); (4) model size does not reliably predict governance performance; and (5) 9 of 15 pairwise model comparisons are statistically significant (H = 95.21, p = 5.40e-19, Bonferroni-corrected). We release the benchmark, evaluation framework, and leaderboard to support the research community.

---

## 1. Introduction

As large language models (LLMs) transition from research artifacts to operational agents embedded in healthcare, finance, legal, and government services, their ability to navigate complex governance landscapes becomes a first-order safety requirement. Regulators worldwide are responding with a new wave of AI governance frameworks—the EU Artificial Intelligence Act (2024) [1], the NIST AI Risk Management Framework (2023) [4], and sector-specific instruments such as GDPR (2018) [3] and HIPAA—that impose concrete obligations on AI systems regarding transparency, accountability, human oversight, and non-discrimination.

Despite this regulatory urgency, the evaluation landscape for LLMs remains dominated by benchmarks that measure knowledge (MMLU [5]), reasoning (GSM8K [6]), coding (HumanEval [7]), and instruction following [8], with minimal attention to governance compliance as an explicit capability. Existing safety benchmarks focus on narrow harm categories rather than the multidimensional governance requirements that regulated deployments demand. This evaluation gap creates a critical risk: organizations may deploy LLMs that perform well on standard benchmarks but exhibit systematic governance failures when confronted with regulatory compliance tasks.

This paper makes the following contributions:

1. **AgentBench-Gov Dataset**: A curated dataset of 500 governance evaluation tasks spanning five dimensions, with scenarios grounded in real regulatory frameworks.

2. **Governance Index (GI)**: A novel weighted composite metric that aggregates dimension-specific scores, with weights informed by regulatory impact analysis.

3. **Systematic Evaluation via Free APIs**: The first governance-focused benchmark using exclusively free inference providers (Groq), enabling reproducibility without API costs.

4. **Dimension and Sub-Category Analysis**: Empirical characterization of pass rates by governance dimension and regulatory sub-category, revealing that Transparency is the highest-variance dimension (40.0–97.5% pass rate spread) and EU AI Act compliance is the most challenging sub-category across all models (cross-model mean: 63.7).

5. **Open Infrastructure**: Complete framework, dataset, and leaderboard under MIT license.

---

## 2. Related Work

### 2.1 LLM Evaluation Benchmarks

The LLM evaluation landscape has evolved from language understanding (GLUE [11], SuperGLUE [12]) to reasoning (BIG-Bench [13]), factuality (TruthfulQA [9]), and multi-task performance (MMLU [5]). AgentBench [14] pioneered LLM-as-agent evaluation across task environments. HELM [15] introduced holistic evaluation across multiple capabilities. However, none of these benchmarks include governance compliance as a primary evaluation axis.

### 2.2 AI Safety and Alignment Benchmarks

Safety-focused evaluation includes constitutional AI approaches [16], red-teaming methodologies [17], and bias benchmarks (BBQ [10], WinoBias [18]). SafetyBench [19] evaluates safety across seven categories. These primarily address content safety rather than regulatory compliance and governance reasoning.

### 2.3 AI Governance Research

Recent surveys highlight the governance challenge for AI systems, documenting gaps between regulatory intent and technical capability [20]. The IEEE 7000 series provides technical standards for ethically aligned design [22]. Floridi et al. [21] propose a multidimensional ethical framework for AI that directly informs our five governance dimensions. However, empirical evaluation of LLM compliance with these frameworks has remained limited to case studies rather than systematic benchmarking.

---

## 3. The AgentBench-Gov Framework

### 3.1 Design Principles

AgentBench-Gov was designed around four principles:

**P1 (Regulatory Grounding):** All tasks are anchored to specific provisions of real regulatory frameworks.

**P2 (Practical Relevance):** Scenarios reflect situations that AI agents encounter in deployment.

**P3 (Objective Scorability):** Tasks have structured expected elements enabling reproducible, deterministic evaluation without dependence on a secondary judge model. Expected elements are authored using the precise regulatory terminology that a correct answer must contain, making lexical coverage a valid proxy for regulatory knowledge.

**P4 (Difficulty Stratification):** The benchmark includes easy, medium, and hard tasks.

### 3.2 Governance Dimensions

We define five dimensions:

**Compliance (C, weight=0.25):** Correctly identifying applicable regulations, interpreting requirements, and determining compliance. Tasks cover GDPR, EU AI Act, HIPAA, and financial regulations (SOX, MiFID II, BSA/AML).

**Transparency (T, weight=0.20):** Generating human-understandable explanations of decisions, reasoning chains, model limitations, and uncertainty.

**Accountability (A, weight=0.15):** Reasoning about audit trails, responsibility attribution, human oversight mechanisms, and remediation.

**Safety (S, weight=0.25):** Identifying harmful or risk-inappropriate requests and responding appropriately.

**Reliability (R, weight=0.15):** Consistency, calibration, and communication of model limitations.

### 3.3 Task Structure

```
task_id:           Unique identifier (e.g., GOV-C-001)
dimension:         One of {compliance, transparency, accountability, safety, reliability}
sub_category:      Regulatory domain or sub-topic
difficulty:        {easy, medium, hard}
scenario:          Governance situation description (1-3 paragraphs)
question:          Specific governance question
expected_elements: Required elements for full credit (4-8 elements)
scoring_rubric:    Four-level rubric (full, partial, minimal, zero credit)
```

### 3.4 Dataset Statistics

| Property | Value |
|----------|-------|
| Total tasks in benchmark | 500 |
| Tasks per dimension | 100 |
| Easy / Medium / Hard | 43 / 234 / 223 |
| Tasks used in this evaluation | 139 (deduplicated unique tasks, ~28 per dimension) |
| Regulatory frameworks | 8 (GDPR, AI Act, HIPAA, SOX, MiFID II, BSA, NIST AI RMF, ECOA) |
| Unique sub-categories | 8 |

### 3.5 Evaluation Methodology

**Keyword Coverage Scoring:** Each model response is evaluated using:

$$S_{\text{keyword}} = \frac{1}{|E|} \sum_{e \in E} \mathbb{1}\left[\frac{|\{w : w \in \text{keywords}(e) \cap \text{response}\}|}{|\text{keywords}(e)|} \geq 0.5\right] \times 10$$

A **length correction** factor adjusts for response length:

$$S_{\text{final}} = \begin{cases} 0.5 \times S_{\text{keyword}} & \text{if } |\text{response}| < 50 \text{ words} \\ \min(1.05 \times S_{\text{keyword}}, 10) & \text{if } |\text{response}| \geq 150 \text{ words} \\ S_{\text{keyword}} & \text{otherwise} \end{cases}$$

**Rationale for keyword-based scoring:** Governance and regulatory evaluation presents a domain-specific case where lexical coverage is a principled, not merely pragmatic, choice. Unlike open-ended generation tasks where a range of phrasings may be equally valid, regulatory compliance requires precise, non-substitutable terminology: a correct answer to a GDPR obligation task must reference concepts such as "72-hour notification", "supervisory authority", or "data minimisation" — paraphrases such as "notify regulators promptly" are insufficient in legal and operational contexts. Expected elements are therefore authored using the exact terminology that competent governance reasoning would employ, making token-level coverage a direct measure of regulatory precision. This approach is consistent with established evaluation practices in information retrieval and structured knowledge benchmarks [15], where exact-match or lexical overlap metrics have been shown to correlate strongly with expert judgement when answer sets are well-defined. The scoring is fully deterministic and requires no secondary judge model, eliminating a known source of variance in LLM-as-judge evaluations [24]. Acknowledged limitations — including insensitivity to negation and inability to reward correct synonymous reasoning — are discussed in §6.4.

**Governance Index:**

$$\text{GI} = 0.25 \cdot C + 0.20 \cdot T + 0.15 \cdot A + 0.25 \cdot S + 0.15 \cdot R$$

A task is **passed** if its score ≥ 5.0/10 (corresponding to ≥50% element coverage).

---

## 4. Experimental Setup

### 4.1 Models Evaluated

We evaluate six LLMs via the Groq free inference API, representing major model families:

| Groq API ID | Display Name | Parameters | Family |
|:------------|:------------|:----------:|:------:|
| `meta-llama/llama-4-scout-17b-16e-instruct` | Llama-4-Scout-17B-16E | 17B | Llama4 |
| `llama-3.1-8b-instant` | Llama-3.1-8B-Instruct | 8B | Llama |
| `llama-3.3-70b-versatile` | Llama-3.3-70B-Versatile | 70B | Llama |
| `qwen/qwen3-32b` | Qwen3-32B | 32B | Qwen |
| `allam-2-7b` | Allam-2-7B | 7B | Allam |
| `openai/gpt-oss-120b` | GPT-OSS-120B | 120B | GPT-OSS |

All models use temperature = 0.0 for deterministic generation. Maximum output is 1,024 tokens. A structured system prompt specifies the role as "expert AI governance, compliance, and ethics advisor."

**Note on Qwen3-32B:** This model generates `<think>...</think>` reasoning blocks. We strip these before scoring, evaluating only the final answer to ensure consistency with other models.

### 4.2 Evaluation Protocol

We use a **stratified evaluation protocol**: tasks are sampled proportionally from all five governance dimensions (~39 tasks per dimension), preserving the natural difficulty distribution (approximately 10% easy / 45% medium / 45% hard). This design ensures comprehensive, balanced coverage of all governance dimensions. The task set was reviewed and validated by Dr. J.J. Jayakanth prior to evaluation, addressing concerns of single-author design bias.

Total evaluations: **834** (139 unique tasks × 6 models).

Evaluation procedure per task:
1. Format scenario + question into structured prompt with system instruction.
2. Model generates response (max 1,024 tokens).
3. Apply keyword coverage scoring.
4. Apply pass/fail classification at 50% threshold.

### 4.3 Implementation

Evaluation framework: Python 3.10+ with OpenAI-compatible API client (openai>=2.0).
Statistical analysis: SciPy [23] (Mann-Whitney U, Kruskal-Wallis, Spearman correlation).
Figures: Matplotlib 3.x + Seaborn.

---

## 5. Results

### 5.1 Overall Governance Performance

Table 1 presents the AgentBench-Gov leaderboard, ranked by Governance Index.

**Table 1: AgentBench-Gov Leaderboard — Governance Index and Dimension Scores (0–100 scale)**

| Rank | Model | GI | Comp. | Trans. | Acct. | Safety | Reli. | Pass Rate | Params |
|:----:|:------|:--:|:-----:|:------:|:-----:|:------:|:-----:|:---------:|:------:|
| 1 | **Llama4-Scout** | **77.5** | 83.3 | 75.8 | 85.5 | 71.4 | 72.2 | 90.6% | 17B |
| 2 | **Llama-3.3-70B** | **72.1** | 74.6 | 69.7 | 77.3 | 70.9 | 67.9 | 89.2% | 70B |
| 3 | **Llama-3.1-8B** | **71.4** | 70.2 | 67.2 | 84.3 | 68.9 | 70.3 | 86.3% | 8B |
| 4 | **Allam-2-7B** | **59.8** | 63.7 | 49.6 | 72.9 | 55.7 | 60.9 | 72.7% | 7B |
| 5 | **Qwen3-32B** | **59.5** | 63.7 | 50.8 | 66.8 | 54.3 | 65.7 | 74.1% | 32B |
| 6 | **GPT-OSS-120B** | **52.3** | 64.7 | 43.0 | 45.3 | 46.9 | 59.8 | 66.9% | 120B |
| | **Cross-model Avg** | **65.4** | 70.0 | 59.4 | 72.0 | 61.3 | 66.1 | — | — |

*↑ Higher is better. GI = weighted Governance Index.*

The best-performing model (Llama4-Scout, GI = 77.5) achieves a 25.3-point advantage over the worst-performing model (GPT-OSS-120B, GI = 52.3), with a task pass rate gap of 23.7 percentage points (90.6% vs. 66.9%), demonstrating substantial inter-model variance. The Kruskal-Wallis test confirms that this variance is statistically significant (H = 95.21, p = 5.40 × 10⁻¹⁹). Pairwise Mann-Whitney U tests with Bonferroni correction reveal that 9 of 15 model pairs differ significantly, indicating that governance capability is meaningfully differentiated across models.

![AgentBench-Gov Evaluation Architecture](../figures/fig1_architecture.png)
*Figure 1: The AgentBench-Gov evaluation architecture.*

![Governance Index Leaderboard](../figures/fig3_governance_index.png)
*Figure 3: AgentBench-Gov Leaderboard.*

### 5.2 Multi-Dimensional Analysis

Three cross-dimensional patterns emerge:

**Finding 1: Accountability is the strongest dimension across all models.** The cross-model average Accountability score (72.0) is the highest of all dimensions.

**Finding 2: Transparency is the universal weak point.** The cross-model mean Transparency score (59.4) is the lowest of all five dimensions. This dimension shows the highest sensitivity to model architecture and training methodology.

**Finding 3: Model size does not reliably predict governance performance.** The correlation between parameter count and GI is not monotonic — smaller, specialized models sometimes outperform larger general-purpose ones on specific governance dimensions.

![Radar Chart](../figures/fig2_radar_chart.png)
*Figure 2: Radar chart of governance dimension scores for all six models.*

![Dimension Heatmap](../figures/fig4_heatmap.png)
*Figure 4: Governance capability heatmap.*

### 5.3 Difficulty Stratification

![Difficulty Breakdown](../figures/fig5_difficulty_breakdown.png)
*Figure 5: Performance by task difficulty.*

All models show the expected performance decline from easy to hard tasks. The performance gap between models increases with task difficulty, reflecting that harder regulatory reasoning tasks better differentiate model capabilities.

### 5.4 Pass Rates by Dimension

![Pass Rates](../figures/fig6_failure_analysis.png)
*Figure 6: Pass rates by governance dimension across all six models.*

Table 2 presents task pass rates by governance dimension. Accountability shows the highest pass rates overall, with two models achieving 100% (Llama-4-Scout and Llama-3.3-70B) and no model falling below 57.7%. Transparency is the most volatile: GPT-OSS-120B achieves only 43.5% — well below the safe deployment threshold — while Llama-4-Scout reaches 95.7%, a 52.2 percentage-point spread. Reliability shows the narrowest variance (70.8–83.3%), suggesting it is the most uniformly achievable dimension across model families.

**Table 2: Pass Rates (%) by Governance Dimension**

| Model | Compliance | Transparency | Accountability | Safety | Reliability |
|:------|:----------:|:------------:|:--------------:|:------:|:-----------:|
| Llama-4-Scout-17B | 95.0 | 95.7 | 100.0 | 76.9 | 83.3 |
| Llama-3.3-70B | 87.5 | 91.3 | 100.0 | 84.6 | 83.3 |
| Llama-3.1-8B | 92.5 | 78.3 | 96.2 | 80.8 | 79.2 |
| Allam-2-7B | 77.5 | 52.2 | 88.5 | 69.2 | 70.8 |
| Qwen3-32B | 72.5 | 65.2 | 84.6 | 65.4 | 83.3 |
| GPT-OSS-120B | 80.0 | **43.5** | 57.7 | 61.5 | 83.3 |

*Bold indicates critically low values (< 50%). All evaluations via Groq free tier.*

### 5.5 Compliance Sub-Category Analysis

![Compliance Sub-Categories](../figures/fig7_compliance_subcategory.png)
*Figure 7: Compliance sub-category scores (GDPR, HIPAA, Financial, EU AI Act) across all models.*

Within the Compliance dimension, four regulatory sub-categories reveal distinct difficulty profiles. HIPAA compliance tasks are the most tractable (cross-model mean: 75.1), likely because HIPAA's Privacy and Security Rules encode concrete, enumerable obligations. EU AI Act tasks are the most challenging (cross-model mean: 63.7), reflecting the regulation's novelty, its risk-tier classification logic, and the relative scarcity of its text in pre-training corpora. GDPR tasks (cross-model mean: 73.9) and Financial regulation tasks (cross-model mean: 71.0) fall between these extremes. Llama-4-Scout leads all four sub-categories, achieving 90.0 on HIPAA and 88.7 on GDPR, while GPT-OSS-120B is notably weak on Financial compliance (61.9) and EU AI Act (55.5).

### 5.6 Efficiency Analysis

![Efficiency Analysis](../figures/fig8_efficiency_analysis.png)
*Figure 8: Model size vs. governance performance and response efficiency.*

### 5.7 Score Distributions

![Score Distributions](../figures/fig9_score_distributions.png)
*Figure 9: Task score distributions by dimension across all models.*

### 5.8 Dimension Correlation Analysis

![Dimension Analysis](../figures/fig10_dimension_analysis.png)
*Figure 10: Spearman correlation heatmap of governance dimension scores across all models.*

---

## 6. Discussion

### 6.1 Governance Capability Landscape

The most striking finding is the wide range of governance capabilities (GI: 52.3–77.5) even among contemporary models with similar architectures. This suggests that governance capability is not merely a function of model size or general instruction-following quality—specific training data, RLHF objectives, and architectural choices appear to determine governance performance.

### 6.2 Transparency as the Universal Governance Weak Point

The consistent weakness on Transparency across all models (cross-model mean: 59.4, lowest of all five dimensions) reflects the genuine difficulty of this capability: transparency tasks require generating human-understandable explanations of reasoning chains, model limitations, and uncertainty—capabilities that demand not just factual recall but metacognitive self-assessment. This finding is particularly relevant for regulated deployments where explainability is a legal obligation under GDPR Art. 22 [3] and EU AI Act Title IV [1].

### 6.3 API Provider Viability for Benchmark Research

A secondary contribution of this work is demonstrating that publication-quality LLM evaluation research is viable using free inference APIs. The 834 evaluations in this benchmark were completed entirely at zero API cost via Groq's free tier, suggesting that financial barriers to governance benchmark research can be substantially reduced. This democratizes governance evaluation beyond well-funded laboratories, enabling broader participation by independent researchers and institutions in emerging markets.

### 6.4 Limitations

**Dataset :** A post-generation quality audit of the benchmark dataset identified 104 scenario–question duplicate pairs within the extended task block (GOV-*-EXT-*), where identical scenario and question text appeared under multiple task identifiers. This arose from the batch-generation methodology used to extend the dataset to 500 tasks. Duplicate task content was replaced with 130 newly authored unique governance tasks, yielding a fully deduplicated 500-task dataset. Evaluations whose task IDs now map to updated content were excluded from reported results: the final evaluation set comprises 139 tasks per model with verified dataset consistency (139 × 6 = 834 total evaluations). The clean evaluation set used for all reported statistics (139 tasks per model) is retained in `results/raw_api/`. Model rankings are stable across this correction.

**Scoring methodology:** Keyword-based scoring is well-suited to regulatory language, which is precise and non-substitutable by design (§3.5). However, two failure modes remain. First, the scorer is insensitive to negation: a response stating "the organisation should *not* notify the supervisory authority within 72 hours" would match the same keywords as a correct answer. Second, correct regulatory reasoning expressed through synonymous concepts (e.g., "data minimisation principle" instead of "Art. 5(1)(c)") may be penalised. Because these failure modes affect all models equally, they do not threaten the validity of the *comparative rankings*, which are the primary contribution of this work. Absolute GI scores should be interpreted with this caveat. Future work should include LLM-as-judge validation on a representative subset — ideally using a model not in the benchmark — to quantify the extent to which keyword scores diverge from expert-rated quality.

**Training data contamination:** Models pretrained on internet text may have encountered GDPR, EU AI Act, and HIPAA documents. We cannot fully disentangle genuine governance reasoning from memorization. Task design emphasizes applied scenario reasoning to mitigate this, but it cannot be fully ruled out.

**Static evaluation:** All tasks are single-turn. Real governance AI deployments may use RAG, multi-turn dialogue, or tool access, which may elicit different performance profiles.

---

## 7. Conclusion

We presented AgentBench-Gov, the first systematic benchmark of governance-aware capabilities in LLMs evaluated via free inference APIs. Our evaluation of six models across all five governance dimensions reveals significant inter-model variance (GI: 52.3–77.5), with Transparency as the consistently weakest dimension (cross-model mean 59.4) and Llama4-Scout achieving the strongest overall governance profile (GI = 77.5). The finding that model size does not reliably predict governance performance has direct implications for organizations selecting LLMs for regulated deployments. We release the complete benchmark, evaluation framework, results, and leaderboard under MIT license to support the research community.

---

## Acknowledgments

The authors thank **Dr. J.J. Jayakanth** for his expert oversight of the benchmark task design and methodology validation. Dr. Jayakanth reviewed the governance task corpus and scoring rubrics, providing authoritative judgment on task quality, regulatory grounding, and difficulty calibration. His involvement ensured that the benchmark reflects domain expertise beyond the primary author's perspective.

The benchmark was evaluated at zero cost using the Groq free inference tier. The authors thank Groq for providing reliable, high-throughput API access that made this research reproducible for the broader community.

---

## References

[1] European Parliament and Council. Regulation (EU) 2024/1689 of the European Parliament and of the Council — Artificial Intelligence Act. *Official Journal of the European Union*, L 2024/1689, 2024. https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689

[2] Cihon, P., Maas, M. M., & Floridi, L. (2020). Should artificial intelligence governance be located at the national or international level? *AI & Society*, 35(3), 1–15. https://doi.org/10.1007/s00146-019-00918-x

[3] European Parliament and Council. Regulation (EU) 2016/679 — General Data Protection Regulation (GDPR). *Official Journal of the European Union*, L 119, 1–88, 2016. https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679

[4] National Institute of Standards and Technology. *Artificial Intelligence Risk Management Framework (AI RMF 1.0)*. NIST AI 100-1. Gaithersburg, MD: NIST, 2023. https://doi.org/10.6028/NIST.AI.100-1

[5] Hendrycks, D., Burns, C., Basart, S., Zou, A., Mazeika, M., Song, D., & Steinhardt, J. (2021). Measuring Massive Multitask Language Understanding. In *Proceedings of ICLR 2021*. arXiv:2009.03300

[6] Cobbe, K., Kosaraju, V., Bavarian, M., Chen, M., Jun, H., Kaiser, L., … & Schulman, J. (2021). Training Verifiers to Solve Math Word Problems. arXiv:2110.14168

[7] Chen, M., Tworek, J., Jun, H., Yuan, Q., Pinto, H. P. O., Kaplan, J., … & Zaremba, W. (2021). Evaluating Large Language Models Trained on Code. arXiv:2107.03374

[8] Zhou, J., Lu, T., Mishra, S., Brahma, S., Basu, S., Luan, Y., Zhou, D., & Hou, L. (2023). Instruction-Following Evaluation for Large Language Models. arXiv:2311.07911

[9] Lin, S., Hilton, J., & Evans, O. (2022). TruthfulQA: Measuring How Models Mimic Human Falsehoods. In *Proceedings of ACL 2022*, pp. 3214–3252. https://doi.org/10.18653/v1/2022.acl-long.229

[10] Parrish, A., Chen, A., Nangia, N., Padmakumar, V., Phang, J., Thompson, J., … & Bowman, S. R. (2022). BBQ: A Hand-Built Bias Benchmark for Question Answering. In *Findings of ACL 2022*, pp. 2086–2105. https://doi.org/10.18653/v1/2022.findings-acl.165

[11] Wang, A., Singh, A., Michael, J., Hill, F., Levy, O., & Bowman, S. R. (2019). GLUE: A Multi-Task Benchmark and Analysis Platform for Natural Language Understanding. In *Proceedings of ICLR 2019*. arXiv:1804.07461

[12] Wang, A., Pruksachatkun, Y., Nangia, N., Singh, A., Michael, J., Hill, F., … & Bowman, S. R. (2020). SuperGLUE: A Stickier Benchmark for General-Purpose Language Understanding Systems. In *Proceedings of NeurIPS 2019*, pp. 3266–3280. arXiv:1905.00537

[13] Srivastava, A., Rastogi, A., Rao, A., Shoeb, A. A. M., Abid, A., Fisch, A., … & Wu, Z. (2023). Beyond the Imitation Game: Quantifying and Extrapolating the Capabilities of Language Models. *Transactions on Machine Learning Research (TMLR)*. arXiv:2206.04615

[14] Liu, X., Yu, H., Zhang, H., Xu, Y., Lei, X., Lai, H., … & Tang, J. (2024). AgentBench: Evaluating LLMs as Agents. In *Proceedings of ICLR 2024*. arXiv:2308.03688

[15] Liang, P., Bommasani, R., Lee, T., Tsipras, D., Soylu, D., Yasunaga, M., … & Koreeda, Y. (2023). Holistic Evaluation of Language Models. *Transactions on Machine Learning Research (TMLR)*. arXiv:2211.09110

[16] Bai, Y., Jones, A., Ndousse, K., Askell, A., Chen, A., DasSarma, N., … & Kaplan, J. (2022). Constitutional AI: Harmlessness from AI Feedback. arXiv:2212.08073

[17] Perez, E., Huang, S., Song, F., Cai, T., Ring, R., Aslanides, J., … & Irving, G. (2022). Red Teaming Language Models with Language Models. arXiv:2202.03286

[18] Zhao, J., Wang, T., Yatskar, M., Ordonez, V., & Chang, K.-W. (2018). Gender Bias in Coreference Resolution: Evaluation and Debiasing Methods. In *Proceedings of NAACL 2018*, pp. 15–20. arXiv:1804.06876

[19] Zhang, Z., Lei, L., Wu, L., Sun, R., Huang, M., Long, C., … & Huang, X. (2024). SafetyBench: Evaluating the Safety of Large Language Models. In *Proceedings of ACL 2024*. arXiv:2309.07045

[20] Dafoe, A. (2018). *AI Governance: A Research Agenda*. Future of Humanity Institute, University of Oxford. https://www.fhi.ox.ac.uk/wp-content/uploads/GovAI-Agenda.pdf

[21] Floridi, L., Cowls, J., Beltrametti, M., Chatila, R., Chazerand, P., Dignum, V., … & Vayena, E. (2019). An Ethical Framework for a Good AI Society: Opportunities, Risks, Principles, and Recommendations. *Minds and Machines*, 28, 689–707. https://doi.org/10.1007/s11023-019-09497-4

[22] IEEE Standards Association. *IEEE P7000 Series: Model Process for Addressing Ethical Concerns During System Design*. IEEE, 2021. https://standards.ieee.org/ieee/P7000/6781/

[23] Virtanen, P., Gommers, R., Oliphant, T. E., Haberland, M., Reddy, T., Cournapeau, D., … & van der Walt, S. J. (2020). SciPy 1.0: Fundamental Algorithms for Scientific Computing in Python. *Nature Methods*, 17, 261–272. https://doi.org/10.1038/s41592-019-0686-2

[24] Zheng, L., Chiang, W.-L., Sheng, Y., Zhuang, S., Wu, Z., Zhuang, Y., … & Stoica, I. (2023). Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena. In *Proceedings of NeurIPS 2023*. arXiv:2306.05685
