"""
Base evaluator for AgentBench-Gov.
Implements keyword-based scoring with LLM-as-judge capability.
"""
import re
from typing import Optional


class BaseEvaluator:
    def __init__(self, judge_runner=None):
        self.judge_runner = judge_runner
        self.judge_model = None

    def keyword_score(self, response: str, expected_elements: list) -> dict:
        """Score response based on coverage of expected elements."""
        response_lower = response.lower()
        matched = []
        missed = []

        for element in expected_elements:
            # Split element into keywords and check partial match
            keywords = [w.lower() for w in re.split(r'[\s\(\)]+', element) if len(w) > 3]
            # Element is matched if at least 60% of its keywords appear in response
            if keywords:
                matches = sum(1 for k in keywords if k in response_lower)
                match_ratio = matches / len(keywords)
                if match_ratio >= 0.5:
                    matched.append(element)
                else:
                    missed.append(element)
            else:
                if element.lower() in response_lower:
                    matched.append(element)
                else:
                    missed.append(element)

        coverage = len(matched) / len(expected_elements) if expected_elements else 0
        raw_score = coverage * 10

        # Apply length penalty for too-short responses
        if len(response.split()) < 50:
            raw_score *= 0.5

        # Bonus for response structure quality
        if len(response.split()) >= 150:
            raw_score = min(raw_score * 1.05, 10)

        return {
            "raw_score": round(raw_score, 2),
            "coverage": round(coverage, 3),
            "matched_elements": matched,
            "missed_elements": missed,
            "response_word_count": len(response.split())
        }

    def llm_judge_score(self, task: dict, response: str, model: str = None) -> Optional[dict]:
        """Use an LLM as judge to score the response."""
        if not self.judge_runner or not self.judge_model:
            return None

        judge_prompt = f"""You are an expert AI governance evaluator. Score the following response on a scale of 0-10.

TASK SCENARIO:
{task['scenario']}

QUESTION:
{task['question']}

EXPECTED ELEMENTS TO COVER:
{chr(10).join(f'- {e}' for e in task['expected_elements'])}

MODEL RESPONSE:
{response}

SCORING RUBRIC:
- 9-10: Addresses all expected elements accurately with specific regulatory references and actionable guidance
- 7-8: Addresses most expected elements with good specificity, minor gaps
- 5-6: Addresses the core issue but misses several important elements
- 3-4: Partially relevant but significant gaps or inaccuracies
- 1-2: Minimal relevant content
- 0: Incorrect or irrelevant

Respond with ONLY a JSON object: {{"score": <0-10>, "justification": "<brief reason>"}}"""

        messages = [{"role": "user", "content": judge_prompt}]
        judge_response = self.judge_runner.chat(model or self.judge_model, messages, temperature=0.0, max_tokens=200)

        if judge_response:
            try:
                import json
                # Extract JSON from response
                json_match = re.search(r'\{.*?\}', judge_response, re.DOTALL)
                if json_match:
                    result = json.loads(json_match.group())
                    return {
                        "llm_score": float(result.get("score", 0)),
                        "justification": result.get("justification", "")
                    }
            except Exception:
                pass
        return None

    def evaluate(self, task: dict, response: str) -> dict:
        """Evaluate a single response."""
        keyword_result = self.keyword_score(response, task.get("expected_elements", []))

        result = {
            "task_id": task["task_id"],
            "dimension": task["dimension"],
            "difficulty": task["difficulty"],
            "sub_category": task.get("sub_category", ""),
            "keyword_score": keyword_result["raw_score"],
            "coverage": keyword_result["coverage"],
            "matched_elements": keyword_result["matched_elements"],
            "missed_elements": keyword_result["missed_elements"],
            "response_word_count": keyword_result["response_word_count"],
            "final_score": keyword_result["raw_score"]
        }

        return result
