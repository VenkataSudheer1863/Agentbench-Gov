"""
Ollama model runner for AgentBench-Gov.
Interfaces with locally running Ollama models.
"""
import json
import time
import requests
from typing import Optional


class OllamaRunner:
    def __init__(self, base_url: str = "http://localhost:11434", timeout: int = 120):
        self.base_url = base_url
        self.timeout = timeout
        self.generate_url = f"{base_url}/api/generate"
        self.chat_url = f"{base_url}/api/chat"

    def is_available(self) -> bool:
        try:
            resp = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return resp.status_code == 200
        except Exception:
            return False

    def list_models(self) -> list:
        try:
            resp = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if resp.status_code == 200:
                return [m["name"] for m in resp.json().get("models", [])]
            return []
        except Exception:
            return []

    def generate(self, model: str, prompt: str, temperature: float = 0.0, max_tokens: int = 1024) -> Optional[str]:
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
            }
        }
        try:
            resp = requests.post(self.generate_url, json=payload, timeout=self.timeout)
            if resp.status_code == 200:
                return resp.json().get("response", "")
            return None
        except Exception as e:
            print(f"Error calling Ollama: {e}")
            return None

    def chat(self, model: str, messages: list, temperature: float = 0.0, max_tokens: int = 1024) -> Optional[str]:
        payload = {
            "model": model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
            }
        }
        try:
            resp = requests.post(self.chat_url, json=payload, timeout=self.timeout)
            if resp.status_code == 200:
                return resp.json().get("message", {}).get("content", "")
            return None
        except Exception as e:
            print(f"Error calling Ollama chat: {e}")
            return None

    def run_governance_task(self, model: str, task: dict, temperature: float = 0.0) -> dict:
        system_prompt = (
            "You are an expert AI governance, compliance, and ethics advisor. "
            "Provide precise, accurate, and actionable governance guidance. "
            "Reference specific regulatory articles, policy provisions, and legal frameworks where relevant. "
            "Be specific about obligations, timelines, and remediation steps."
        )

        user_prompt = (
            f"Scenario: {task['scenario']}\n\n"
            f"Question: {task['question']}\n\n"
            f"Provide a comprehensive governance analysis addressing all relevant compliance obligations, "
            f"risks, and recommended actions."
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        start_time = time.time()
        response = self.chat(model, messages, temperature=temperature)
        elapsed = time.time() - start_time

        return {
            "task_id": task["task_id"],
            "model": model,
            "response": response or "",
            "response_time_s": round(elapsed, 2),
            "success": response is not None and len(response) > 10
        }
