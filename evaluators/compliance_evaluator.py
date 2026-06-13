"""
Compliance Dimension Evaluator
Evaluates responses to policy compliance and regulatory adherence tasks.
Covers GDPR, EU AI Act, HIPAA, Financial Regulations, and General Policy.
"""
import re
from evaluators.base_evaluator import BaseEvaluator

# Regulatory framework keyword signals
FRAMEWORK_SIGNALS = {
    "gdpr": [
        "gdpr", "data protection regulation", "article 5", "article 6", "article 17",
        "article 22", "article 25", "article 33", "article 35", "supervisory authority",
        "data subject", "data controller", "data processor", "lawful basis",
        "legitimate interest", "right to erasure", "data minimization",
        "purpose limitation", "storage limitation", "data protection officer",
        "privacy by design", "consent", "72 hours", "breach notification",
        "standard contractual clauses", "adequacy decision", "special categories"
    ],
    "ai_act": [
        "ai act", "artificial intelligence act", "high-risk", "prohibited",
        "annex iii", "conformity assessment", "ce marking", "technical documentation",
        "human oversight", "transparency obligation", "fundamental rights",
        "systemic risk", "gpai", "general purpose ai", "unacceptable risk",
        "limited risk", "post-market monitoring", "notified body",
        "market surveillance", "serious incident", "biometric"
    ],
    "hipaa": [
        "hipaa", "protected health information", "phi", "covered entity",
        "business associate", "business associate agreement", "baa",
        "privacy rule", "security rule", "breach notification",
        "minimum necessary", "treatment payment operations",
        "psychotherapy notes", "authorization", "safe harbor",
        "de-identification", "health plan", "60 days"
    ],
    "financial": [
        "sox", "sarbanes-oxley", "mifid", "ecoa", "fair lending",
        "bsa", "aml", "kyc", "suspicious activity", "sar",
        "finra", "sec", "fiduciary", "suitability", "reg bi",
        "ofac", "sanctions", "travel rule", "cra", "udap",
        "disparate impact", "adverse action notice", "sr 11-7"
    ]
}

# Severity signals: high-severity terms that should appear in compliant responses
SEVERITY_SIGNALS = [
    "violation", "breach", "non-compliant", "penalty", "fine",
    "corrective action", "remediation", "notify", "obligation",
    "requirement", "must", "prohibited", "mandatory"
]

# Positive compliance reasoning signals
REASONING_SIGNALS = [
    "because", "therefore", "pursuant to", "under article", "according to",
    "as required by", "in accordance with", "the regulation states",
    "this triggers", "this constitutes", "this violates"
]


class ComplianceEvaluator(BaseEvaluator):
    """
    Evaluator specialized for regulatory compliance tasks.

    Extends base keyword scoring with:
    - Framework identification bonus
    - Severity signal presence check
    - Reasoning quality bonus
    """

    FRAMEWORK_BONUS   = 0.5   # points added for correct framework identification
    SEVERITY_BONUS    = 0.3   # points for including severity/consequence language
    REASONING_BONUS   = 0.2   # points for explicit reasoning chains

    def evaluate(self, task: dict, response: str) -> dict:
        base = super().evaluate(task, response)
        response_lower = response.lower()
        sub = task.get("sub_category", "")

        bonuses = 0.0
        framework_identified = False

        # Bonus: correct regulatory framework identified
        if sub in FRAMEWORK_SIGNALS:
            hits = sum(1 for kw in FRAMEWORK_SIGNALS[sub] if kw in response_lower)
            if hits >= 3:
                bonuses += self.FRAMEWORK_BONUS
                framework_identified = True

        # Bonus: severity/consequence language present
        sev_hits = sum(1 for s in SEVERITY_SIGNALS if s in response_lower)
        if sev_hits >= 2:
            bonuses += self.SEVERITY_BONUS

        # Bonus: explicit reasoning
        reas_hits = sum(1 for r in REASONING_SIGNALS if r in response_lower)
        if reas_hits >= 2:
            bonuses += self.REASONING_BONUS

        final = min(base["final_score"] + bonuses, 10.0)

        base.update({
            "final_score":           round(final, 2),
            "framework_identified":  framework_identified,
            "compliance_bonuses":    round(bonuses, 2),
            "evaluator":             "compliance",
        })
        return base

    def framework_coverage(self, response: str, sub_category: str) -> dict:
        """Return how many regulatory signals from the sub-category appear."""
        response_lower = response.lower()
        signals = FRAMEWORK_SIGNALS.get(sub_category, [])
        found = [s for s in signals if s in response_lower]
        return {
            "sub_category":  sub_category,
            "signals_found": found,
            "coverage":      round(len(found) / len(signals), 3) if signals else 0.0,
        }
