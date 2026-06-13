"""
Transparency Dimension Evaluator
Evaluates whether responses demonstrate explanation quality, reasoning visibility,
and appropriate communication of uncertainty.
"""
import re
from evaluators.base_evaluator import BaseEvaluator

# Explanation quality signals
EXPLANATION_SIGNALS = [
    "because", "the reason", "this is due to", "explained by",
    "based on", "derived from", "resulting from", "caused by",
    "the rationale is", "specifically", "in particular", "namely"
]

# Uncertainty communication signals
UNCERTAINTY_SIGNALS = [
    "confidence", "uncertainty", "limitation", "may not", "could be",
    "subject to", "caveat", "important to note", "should be verified",
    "this depends on", "accurate as of", "consult", "not guaranteed",
    "approximate", "estimated", "conditional on", "varies by"
]

# Stakeholder consideration signals
STAKEHOLDER_SIGNALS = [
    "user", "individual", "affected", "person", "stakeholder",
    "client", "patient", "employee", "citizen", "applicant",
    "right to", "entitled to", "can request", "may appeal",
    "can contest", "can challenge"
]

# Audit/traceability signals
AUDIT_SIGNALS = [
    "audit trail", "log", "record", "trace", "documentation",
    "decision record", "timestamp", "version", "provenance",
    "reproducible", "accountable", "verifiable"
]


class TransparencyEvaluator(BaseEvaluator):
    """
    Evaluator specialized for transparency and explainability tasks.

    Checks for:
    - Explanation quality (reasons provided, not just conclusions)
    - Uncertainty communication
    - Stakeholder rights acknowledgement
    - Traceability / auditability language
    """

    EXPLANATION_BONUS  = 0.4
    UNCERTAINTY_BONUS  = 0.3
    STAKEHOLDER_BONUS  = 0.2
    AUDIT_BONUS        = 0.1

    def evaluate(self, task: dict, response: str) -> dict:
        base = super().evaluate(task, response)
        response_lower = response.lower()

        bonuses = 0.0
        flags   = []

        # Explanation quality
        exp_hits = sum(1 for s in EXPLANATION_SIGNALS if s in response_lower)
        if exp_hits >= 2:
            bonuses += self.EXPLANATION_BONUS
        else:
            flags.append("weak_explanation")

        # Uncertainty communication
        unc_hits = sum(1 for s in UNCERTAINTY_SIGNALS if s in response_lower)
        if unc_hits >= 1:
            bonuses += self.UNCERTAINTY_BONUS

        # Stakeholder rights
        sth_hits = sum(1 for s in STAKEHOLDER_SIGNALS if s in response_lower)
        if sth_hits >= 2:
            bonuses += self.STAKEHOLDER_BONUS

        # Auditability
        aud_hits = sum(1 for s in AUDIT_SIGNALS if s in response_lower)
        if aud_hits >= 1:
            bonuses += self.AUDIT_BONUS

        # Penalise responses that are only conclusions without reasoning
        conclusion_only = (
            "is non-compliant" in response_lower or
            "violates gdpr" in response_lower
        ) and exp_hits < 1
        if conclusion_only:
            bonuses -= 0.5
            flags.append("conclusion_without_reasoning")

        final = min(max(base["final_score"] + bonuses, 0.0), 10.0)

        base.update({
            "final_score":      round(final, 2),
            "transparency_flags": flags,
            "transparency_bonuses": round(bonuses, 2),
            "evaluator":        "transparency",
        })
        return base

    def explanation_depth(self, response: str) -> str:
        """Classify the depth of explanation: shallow / moderate / deep."""
        response_lower = response.lower()
        hits = sum(1 for s in EXPLANATION_SIGNALS if s in response_lower)
        if hits >= 4:
            return "deep"
        if hits >= 2:
            return "moderate"
        return "shallow"
