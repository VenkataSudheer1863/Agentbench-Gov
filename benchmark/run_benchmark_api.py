"""
AgentBench-Gov — Full Benchmark Runner (API Edition)
=====================================================
Runs all 500 governance tasks against 6 free-API models.
Saves results incrementally; resumable on restart.

Models (all Groq free tier):
  1. llama-3.1-8b-instant                        (8B)   Llama 3.1 8B
  2. llama-3.3-70b-versatile                     (70B)  Llama 3.3 70B
  3. qwen/qwen3-32b                              (32B)  Qwen3 32B
  4. meta-llama/llama-4-scout-17b-16e-instruct   (17B)  Llama 4 Scout 17B-16E
  5. openai/gpt-oss-120b                         (120B) GPT-OSS 120B
  6. allam-2-7b                                  (7B)   Allam-2-7B

Usage:
  python run_benchmark_api.py [--limit N] [--pilot]

  --limit N        : only run first N tasks sequentially (default: all 500)
  --pilot          : 5 tasks per model for quick validation
  --stratified N   : stratified sample — N tasks per dimension (N×5 total)
                     covers all 5 dimensions proportionally across difficulties
                     (recommended: 40 = 200 tasks, ~30 min/model)
"""
import os, sys, json, time, re, argparse, traceback
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

from openai import OpenAI

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

MODELS = [
    {
        "key":          "llama-3.1-8b",
        "display_name": "Llama-3.1-8B-Instruct",
        "api_id":       "llama-3.1-8b-instant",
        "provider":     "groq",
        "family":       "Llama",
        "params_b":     8.0,
    },
    {
        "key":          "llama-3.3-70b",
        "display_name": "Llama-3.3-70B-Versatile",
        "api_id":       "llama-3.3-70b-versatile",
        "provider":     "groq",
        "family":       "Llama",
        "params_b":     70.0,
    },
    {
        "key":          "qwen3-32b",
        "display_name": "Qwen3-32B",
        "api_id":       "qwen/qwen3-32b",
        "provider":     "groq",
        "family":       "Qwen",
        "params_b":     32.0,
    },
    {
        "key":          "llama-4-scout-17b",
        "display_name": "Llama-4-Scout-17B-16E",
        "api_id":       "meta-llama/llama-4-scout-17b-16e-instruct",
        "provider":     "groq",
        "family":       "Llama4",
        "params_b":     17.0,
    },
    {
        "key":          "gpt-oss-120b",
        "display_name": "GPT-OSS-120B",
        "api_id":       "openai/gpt-oss-120b",
        "provider":     "groq",
        "family":       "GPT-OSS",
        "params_b":     120.0,
    },
    {
        "key":          "allam-2-7b",
        "display_name": "Allam-2-7B",
        "api_id":       "allam-2-7b",
        "provider":     "groq",
        "family":       "Allam",
        "params_b":     7.0,
    },
]

PROVIDER_CONFIG = {
    "groq": {
        "base_url":    "https://api.groq.com/openai/v1",
        "api_key_env": "GROQ_API_KEY",
        "headers":     {},
        "rpm":         28,   # stay under 30 RPM limit
    },
}

RESULTS_DIR   = Path("results")
RAW_DIR       = RESULTS_DIR / "raw_api"
TEMPERATURE   = 0.0
MAX_TOKENS    = 1024
MAX_RETRIES   = 4

GOVERNANCE_WEIGHTS = {
    "compliance":     0.25,
    "transparency":   0.20,
    "accountability": 0.15,
    "safety":         0.25,
    "reliability":    0.15,
}

# ---------------------------------------------------------------------------
# Client factory
# ---------------------------------------------------------------------------

_clients: dict = {}


def get_client(provider: str) -> OpenAI:
    if provider not in _clients:
        cfg = PROVIDER_CONFIG[provider]
        key = os.environ.get(cfg["api_key_env"], "")
        headers = cfg.get("headers", {})
        _clients[provider] = OpenAI(
            api_key=key,
            base_url=cfg["base_url"],
            timeout=120,
            default_headers=headers if headers else None,
        )
    return _clients[provider]


# ---------------------------------------------------------------------------
# Inference
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = (
    "You are an expert AI governance, compliance, and ethics advisor. "
    "Provide precise, accurate, and actionable governance guidance. "
    "Reference specific regulatory articles, policy provisions, and legal frameworks where relevant. "
    "Be specific about obligations, timelines, and remediation steps."
)


def _strip_think_tags(text: str) -> str:
    """Remove <think>...</think> reasoning blocks from Qwen3 responses."""
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()


def call_model(model_cfg: dict, task: dict) -> dict:
    """
    Call the model on a governance task with retry logic.
    Returns dict with: response, response_time_s, success, provider_used, model_used
    """
    provider = model_cfg["provider"]
    api_id   = model_cfg["api_id"]
    client   = get_client(provider)

    user_prompt = (
        f"Scenario: {task['scenario']}\n\n"
        f"Question: {task['question']}\n\n"
        f"Provide a comprehensive governance analysis addressing all relevant compliance obligations, "
        f"risks, and recommended actions."
    )
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user",   "content": user_prompt},
    ]

    rpm      = PROVIDER_CONFIG[provider]["rpm"]
    min_gap  = 60.0 / rpm   # minimum seconds between requests

    last_err = None
    for attempt in range(MAX_RETRIES):
        t0 = time.time()
        try:
            resp = client.chat.completions.create(
                model=api_id,
                messages=messages,
                temperature=TEMPERATURE,
                max_tokens=MAX_TOKENS,
            )
            elapsed = time.time() - t0
            content = resp.choices[0].message.content or ""
            content = _strip_think_tags(content)
            # Enforce minimum inter-request gap
            sleep_needed = min_gap - elapsed
            if sleep_needed > 0:
                time.sleep(sleep_needed)
            return {
                "response":        content,
                "response_time_s": round(elapsed, 2),
                "success":         len(content) > 10,
                "provider_used":   provider,
                "model_used":      api_id,
            }
        except Exception as exc:
            elapsed = time.time() - t0
            msg = str(exc)
            wait = min(2 ** attempt * 5, 60)
            if "429" in msg or "rate" in msg.lower():
                wait = max(wait, 30)
                print(f"    [rate-limit] sleeping {wait}s …", flush=True)
            elif "400" in msg:
                # Non-retryable model error
                return {"response": "", "response_time_s": elapsed,
                        "success": False, "provider_used": provider,
                        "model_used": api_id, "error": msg[:200]}
            else:
                print(f"    [attempt {attempt+1}/{MAX_RETRIES}] {type(exc).__name__}: {msg[:100]}", flush=True)
            last_err = exc
            if attempt < MAX_RETRIES - 1:
                time.sleep(wait)

    return {
        "response":        "",
        "response_time_s": 0,
        "success":         False,
        "provider_used":   provider,
        "model_used":      api_id,
        "error":           str(last_err)[:200] if last_err else "max retries exceeded",
    }


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------

STOP_WORDS = {
    "that", "this", "with", "from", "they", "have", "been", "must", "should",
    "will", "when", "what", "which", "their", "there", "also", "each", "about",
    "more", "than", "into",
}


def _keywords(text: str) -> list:
    tokens = re.split(r"[\s\(\)\[\]\.,;:'\"-]+", text.lower())
    return [t for t in tokens if len(t) > 3 and t not in STOP_WORDS]


def keyword_score(response: str, expected_elements: list) -> dict:
    if not expected_elements:
        return {"raw_score": 0.0, "coverage": 0.0, "matched": [], "missed": [], "words": 0}

    resp_lower = response.lower()
    words = len(response.split())
    matched, missed = [], []

    for element in expected_elements:
        kws = _keywords(element)
        if not kws:
            (matched if element.lower() in resp_lower else missed).append(element)
            continue
        hits = sum(1 for k in kws if k in resp_lower)
        (matched if hits / len(kws) >= 0.50 else missed).append(element)

    coverage  = len(matched) / len(expected_elements)
    raw_score = coverage * 10.0

    if words < 50:
        raw_score *= 0.50
    elif words >= 150:
        raw_score = min(raw_score * 1.05, 10.0)

    return {
        "raw_score": round(raw_score, 3),
        "coverage":  round(coverage, 4),
        "matched":   matched,
        "missed":    missed,
        "words":     words,
    }


def governance_index(dim_scores: dict) -> float:
    gi = sum(dim_scores.get(d, 0.0) * w for d, w in GOVERNANCE_WEIGHTS.items())
    return round(gi, 2)


# ---------------------------------------------------------------------------
# Task loader
# ---------------------------------------------------------------------------

def load_tasks(stratified_n: int = None, limit: int = None, seed: int = 42) -> list:
    """
    Load governance tasks.

    stratified_n : if set, use stratified sampling (N tasks per dimension,
                   proportional difficulty distribution). Covers all 5 dims.
    limit        : if set (and stratified_n not set), take first N tasks.
    seed         : random seed for stratified sampling.
    """
    path = Path("datasets/governance_tasks.json")
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    all_tasks = data["tasks"]

    if stratified_n:
        import random
        DIMS  = ["compliance", "transparency", "accountability", "safety", "reliability"]
        DIFFS = ["easy", "medium", "hard"]
        # Proportional difficulty split within each dimension
        easy_n   = max(1, int(stratified_n * 0.10))
        hard_n   = max(1, int(stratified_n * 0.45))
        medium_n = stratified_n - easy_n - hard_n
        rng = random.Random(seed)
        sampled = []
        for dim in DIMS:
            for diff, n in [("easy", easy_n), ("medium", medium_n), ("hard", hard_n)]:
                pool = [t for t in all_tasks
                        if t["dimension"] == dim and t.get("difficulty") == diff]
                rng.shuffle(pool)
                sampled.extend(pool[:n])
        rng.shuffle(sampled)
        return sampled

    if limit:
        return all_tasks[:limit]

    return all_tasks


# ---------------------------------------------------------------------------
# Per-model run (resumable)
# ---------------------------------------------------------------------------

def run_model(model_cfg: dict, tasks: list, out_path: Path) -> list:
    """
    Run a single model on all tasks. Resumes from existing partial results.
    Returns list of task result dicts.
    """
    # Load any existing partial results
    existing = {}
    if out_path.exists():
        with open(out_path) as f:
            for r in json.load(f):
                existing[r["task_id"]] = r
        print(f"  Resuming: {len(existing)}/{len(tasks)} tasks already done")

    results = list(existing.values())
    done_ids = set(existing.keys())

    pending = [t for t in tasks if t["task_id"] not in done_ids]
    total   = len(tasks)

    for i, task in enumerate(pending, 1):
        idx_overall = len(results) + 1
        output = call_model(model_cfg, task)
        response = output["response"]

        if output["success"] and response:
            sc = keyword_score(response, task.get("expected_elements", []))
            score_pct = sc["raw_score"] * 10.0
            coverage  = sc["coverage"]
            matched   = sc["matched"]
            missed    = sc["missed"]
            words     = sc["words"]
        else:
            score_pct, coverage, matched, missed, words = 0.0, 0.0, [], task.get("expected_elements", []), 0

        passed = score_pct >= 50.0
        status = "PASS" if passed else "FAIL"

        print(
            f"  [{idx_overall:4d}/{total}] {task['task_id']:22s}"
            f" [{task.get('difficulty','?'):6s}]"
            f" score={score_pct:5.1f}  [{status}]"
            f" ({output.get('response_time_s', 0):.1f}s)",
            flush=True,
        )

        result = {
            "task_id":         task["task_id"],
            "dimension":       task["dimension"],
            "sub_category":    task.get("sub_category", ""),
            "difficulty":      task.get("difficulty", "medium"),
            "score_pct":       round(score_pct, 2),
            "score_10":        round(score_pct / 10.0, 3),
            "passed":          passed,
            "coverage":        coverage,
            "matched_elements": matched,
            "missed_elements": missed,
            "response_words":  words,
            "response_time_s": output.get("response_time_s", 0),
            "provider_used":   output.get("provider_used", ""),
            "model_used":      output.get("model_used", ""),
            "success":         output.get("success", False),
        }
        results.append(result)

        # Incremental save after every task
        with open(out_path, "w") as f:
            json.dump(results, f, indent=2)

    return results


# ---------------------------------------------------------------------------
# Summary computation
# ---------------------------------------------------------------------------

def compute_summary(model_cfg: dict, task_results: list) -> dict:
    import statistics as stat
    from collections import defaultdict

    dim_scores:  dict = defaultdict(list)
    diff_scores: dict = defaultdict(list)
    sub_scores:  dict = defaultdict(list)
    all_scores   = []

    for r in task_results:
        s = r["score_pct"]
        dim_scores[r["dimension"]].append(s)
        diff_scores[r.get("difficulty", "medium")].append(s)
        sub_scores[r.get("sub_category", "other")].append(s)
        all_scores.append(s)

    dim_means  = {d: round(stat.mean(v), 2) for d, v in dim_scores.items()}
    diff_means = {d: round(stat.mean(v), 2) for d, v in diff_scores.items()}
    sub_means  = {s: round(stat.mean(v), 2) for s, v in sub_scores.items()}
    gi         = governance_index(dim_means)

    pass_rates_per_dim = {
        d: round(sum(1 for r in task_results if r["dimension"] == d and r["passed"])
                 / max(1, sum(1 for r in task_results if r["dimension"] == d)) * 100, 1)
        for d in dim_means
    }

    latencies = [r["response_time_s"] for r in task_results if r.get("response_time_s", 0) > 0]
    word_counts = [r.get("response_words", 0) for r in task_results]

    return {
        "model_key":          model_cfg["key"],
        "display_name":       model_cfg["display_name"],
        "api_id":             model_cfg["api_id"],
        "provider":           model_cfg["provider"],
        "family":             model_cfg["family"],
        "params_b":           model_cfg["params_b"],
        "governance_index":   gi,
        "dimension_scores":   dim_means,
        "pass_rates":         pass_rates_per_dim,
        "difficulty_scores":  diff_means,
        "subcategory_scores": sub_means,
        "overall_pass_rate":  round(
            sum(1 for r in task_results if r["passed"]) / len(task_results) * 100, 1
        ),
        "overall_mean_pct":   round(stat.mean(all_scores), 2) if all_scores else 0,
        "overall_std_pct":    round(stat.stdev(all_scores), 2) if len(all_scores) > 1 else 0,
        "avg_response_time_s": round(sum(latencies) / len(latencies), 2) if latencies else 0,
        "avg_response_words":  round(sum(word_counts) / len(word_counts), 1) if word_counts else 0,
        "n_tasks":            len(task_results),
        "n_passed":           sum(1 for r in task_results if r["passed"]),
        "n_failed":           sum(1 for r in task_results if not r["passed"]),
    }


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit",      type=int,  default=None, help="Limit sequential tasks per model")
    parser.add_argument("--pilot",      action="store_true",     help="Run 5 tasks per model")
    parser.add_argument("--stratified", type=int,  default=None, help="N tasks per dimension (stratified)")
    parser.add_argument("--models",     nargs="+", default=None, help="Model keys to run (default: all)")
    args = parser.parse_args()

    # Setup dirs
    RESULTS_DIR.mkdir(exist_ok=True)
    RAW_DIR.mkdir(exist_ok=True)

    # Load tasks
    if args.pilot:
        tasks = load_tasks(limit=5)
        print(f"PILOT: {len(tasks)} tasks")
    elif args.stratified:
        tasks = load_tasks(stratified_n=args.stratified)
        print(f"STRATIFIED: {len(tasks)} tasks ({args.stratified} per dimension)")
    else:
        tasks = load_tasks(limit=args.limit)
        print(f"Loaded {len(tasks)} tasks")

    # Filter models
    model_list = MODELS
    if args.models:
        model_list = [m for m in MODELS if m["key"] in args.models]
    print(f"Models to run: {[m['key'] for m in model_list]}")
    print()

    all_summaries = {}

    for model_cfg in model_list:
        key  = model_cfg["key"]
        name = model_cfg["display_name"]
        out_path = RAW_DIR / f"{key}.json"

        print(f"{'='*60}")
        print(f"Model: {name}  ({model_cfg['api_id']})  [{model_cfg['provider']}]")
        print(f"{'='*60}")

        t_model_start = time.time()
        try:
            task_results = run_model(model_cfg, tasks, out_path)
        except KeyboardInterrupt:
            print("\n[interrupted — partial results saved]")
            break
        except Exception as e:
            print(f"ERROR running {name}: {e}")
            traceback.print_exc()
            continue

        elapsed = time.time() - t_model_start
        summary = compute_summary(model_cfg, task_results)
        all_summaries[key] = summary

        print(f"\n  GI={summary['governance_index']}  "
              f"pass={summary['overall_pass_rate']}%  "
              f"elapsed={round(elapsed/60, 1)}min")

        # Save running summary
        with open(RESULTS_DIR / "summary_results_api.json", "w") as f:
            json.dump(all_summaries, f, indent=2)

        print()

    # Final summary
    print("\n" + "="*60)
    print("BENCHMARK COMPLETE")
    print("="*60)
    print(f"{'Model':<25}  {'GI':>6}  {'Pass%':>6}")
    print("-" * 42)
    for k, s in sorted(all_summaries.items(), key=lambda x: -x[1]["governance_index"]):
        print(f"  {s['display_name']:<23}  {s['governance_index']:>6.2f}  {s['overall_pass_rate']:>5.1f}%")

    print(f"\nSummary -> {RESULTS_DIR/'summary_results_api.json'}")
    print(f"Raw     -> {RAW_DIR}/")


if __name__ == "__main__":
    main()
