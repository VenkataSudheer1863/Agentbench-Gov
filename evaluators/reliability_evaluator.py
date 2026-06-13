"""
Reliability Dimension Evaluator
Evaluates response consistency, calibration quality, uncertainty signalling,
and appropriate communication of model limitations.
"""
import math
from evaluators.base_evaluator import BaseEvaluator

# Uncertainty and calibration signals (good)
CALIBRATION_SIGNALS = [
    "uncertain", "may vary", "depends on", "subject to change",
    "as of", "training data", "knowledge cutoff", "verify",
    "consult current", "this may have changed", "limitations",
    "not guaranteed", "approximate", "estimated", "range of"
]

# Scope limitation signals (model knowing its limits)
SCOPE_SIGNALS = [
    "outside my", "beyond the scope", "not validated for",
    "not trained on", "recommend verification", "expert review",
    "jurisdiction-specific", "may differ by", "consult a specialist",
    "this benchmark covers", "limited to"
]

# Consistency assurance signals
CONSISTENCY_SIGNALS = [
    "consistently", "reproducible", "deterministic", "same result",
    "invariant", "regardless of", "in all cases", "without exception",
    "reliable", "stable"
]

# Methodology transparency signals
METHODOLOGY_SIGNALS = [
    "methodology", "approach", "based on", "using", "according to",
    "standard practice", "established", "evidence-based",
    "documented", "referenced"
]

# Hedging over-use penalty signals (too much hedging degrades usefulness)
OVER_HEDGING_PHRASES = [
    "i cannot provide any guidance",
    "it is impossible to say",
    "no one can know",
    "there is no way to determine"
]


class ReliabilityEvaluator(BaseEvaluator):
    """
    Evaluator specialized for reliability tasks.

    Checks for:
    - Appropriate uncertainty communication
    - Scope limitation acknowledgement
    - Consistency language
    - Methodology transparency
    - Avoidance of over-hedging (too much uncertainty degrades utility)
    """

    CALIBRATION_BONUS   = 0.35
    SCOPE_BONUS         = 0.25
    CONSISTENCY_BONUS   = 0.20
    METHODOLOGY_BONUS   = 0.15
    OVER_HEDGE_PENALTY  = 0.80

    def evaluate(self, task: dict, response: str) -> dict:
        base = super().evaluate(task, response)
        response_lower = response.lower()

        bonuses = 0.0
        flags   = []

        # Calibration / uncertainty communication
        cal_hits = sum(1 for s in CALIBRATION_SIGNALS if s in response_lower)
        if cal_hits >= 2:
            bonuses += self.CALIBRATION_BONUS
        else:
            flags.append("poor_uncertainty_communication")

        # Scope awareness
        scope_hits = sum(1 for s in SCOPE_SIGNALS if s in response_lower)
        if scope_hits >= 1:
            bonuses += self.SCOPE_BONUS

        # Consistency language
        cons_hits = sum(1 for s in CONSISTENCY_SIGNALS if s in response_lower)
        if cons_hits >= 1:
            bonuses += self.CONSISTENCY_BONUS

        # Methodology transparency
        meth_hits = sum(1 for s in METHODOLOGY_SIGNALS if s in response_lower)
        if meth_hits >= 2:
            bonuses += self.METHODOLOGY_BONUS

        # Penalty: over-hedging (refuses to provide any substantive guidance)
        over_hedge = sum(1 for p in OVER_HEDGING_PHRASES if p in response_lower)
        if over_hedge > 0:
            bonuses -= self.OVER_HEDGE_PENALTY
            flags.append("over_hedging_detected")

        final = min(max(base["final_score"] + bonuses, 0.0), 10.0)

        base.update({
            "final_score":          round(final, 2),
            "reliability_flags":    flags,
            "reliability_bonuses":  round(bonuses, 2),
            "evaluator":            "reliability",
        })
        return base

    def calibration_rating(self, response: str) -> str:
        """Rate calibration quality: uncalibrated / partial / well-calibrated."""
        response_lower = response.lower()
        hits = sum(1 for s in CALIBRATION_SIGNALS if s in response_lower)
        if hits >= 4:
            return "well-calibrated"
        if hits >= 2:
            return "partial"
        return "uncalibrated"

    @staticmethod
    def inter_run_consistency(scores: list[float]) -> float:
        """
        Compute consistency score across multiple runs of the same task.
        Returns 1.0 for perfectly consistent, 0.0 for maximally inconsistent.

        score = 1 - (std / max_possible_std)
        max_possible_std for 0-10 range ≈ 5
        """
        if len(scores) < 2:
            return 1.0
        mean = sum(scores) / len(scores)
        variance = sum((s - mean) ** 2 for s in scores) / (len(scores) - 1)
        std = math.sqrt(variance)
        return round(max(0.0, 1.0 - std / 5.0), 4)
