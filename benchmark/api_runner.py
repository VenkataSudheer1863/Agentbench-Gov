"""
API inference runner for AgentBench-Gov — Groq free tier.

Routes all inference to Groq free API only. All 6 evaluated models are
available on Groq at zero cost:

    llama-3.1-8b-instant
    llama-3.3-70b-versatile
    qwen/qwen3-32b
    meta-llama/llama-4-scout-17b-16e-instruct
    openai/gpt-oss-120b
    allam-2-7b

Required environment variable:
    GROQ_API_KEY  — get free at https://console.groq.com
"""
import os
import time
import logging
from typing import Optional

from openai import OpenAI

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Provider registry — Groq only
# ---------------------------------------------------------------------------

PROVIDER_CONFIG = {
    "groq": {
        "base_url": "https://api.groq.com/openai/v1",
        "api_key_env": "GROQ_API_KEY",
        "extra_headers": {},
    },
}

# Model key → (provider, canonical API ID)
MODEL_MAP = {
    "llama-3.1-8b":     ("groq", "llama-3.1-8b-instant"),
    "llama-3.3-70b":    ("groq", "llama-3.3-70b-versatile"),
    "qwen3-32b":        ("groq", "qwen/qwen3-32b"),
    "llama-4-scout-17b":("groq", "meta-llama/llama-4-scout-17b-16e-instruct"),
    "gpt-oss-120b":     ("groq", "openai/gpt-oss-120b"),
    "allam-2-7b":       ("groq", "allam-2-7b"),
}

# Default fallback when model key is unrecognized
DEFAULT_MODEL = ("groq", "llama-3.1-8b-instant")


def _resolve_model(model_id: str) -> tuple[str, str]:
    """Return (provider, resolved_api_id) for a model key or API ID."""
    # Exact key lookup
    if model_id in MODEL_MAP:
        return MODEL_MAP[model_id]
    # Substring match against API IDs
    for key, (provider, api_id) in MODEL_MAP.items():
        if model_id in api_id or api_id in model_id:
            return provider, api_id
    return DEFAULT_MODEL


def _get_client(provider: str, timeout: int = 120) -> OpenAI:
    cfg = PROVIDER_CONFIG[provider]
    api_key = os.environ.get(cfg["api_key_env"], "")
    return OpenAI(api_key=api_key, base_url=cfg["base_url"], timeout=timeout)


# ---------------------------------------------------------------------------
# APIRunner — Groq inference runner
# ---------------------------------------------------------------------------

class APIRunner:
    """
    Groq API inference runner for AgentBench-Gov.

    Routes all 6 benchmark models to Groq free tier.

    Usage
    -----
    runner = APIRunner()
    response = runner.generate("llama-4-scout-17b", "Explain GDPR Article 17.")
    """

    def __init__(
        self,
        base_url: str = "",       # ignored — kept for interface compatibility
        timeout: int = 120,
        max_retries: int = 4,
        temperature: float = 0.0,
        max_tokens: int = 1024,
    ):
        self.timeout = timeout
        self.max_retries = max_retries
        self.temperature = temperature
        self.max_tokens = max_tokens
        self._clients: dict[str, OpenAI] = {}

    def _client_for(self, model_id: str, provider: Optional[str] = None) -> tuple[OpenAI, str, str]:
        """Return (client, provider_name, resolved_api_id) for the given model."""
        if provider and provider in PROVIDER_CONFIG:
            resolved_provider = provider
            resolved_model = model_id
        else:
            resolved_provider, resolved_model = _resolve_model(model_id)
            if provider and provider not in PROVIDER_CONFIG:
                logger.warning(
                    f"[APIRunner] Unknown provider '{provider}'. "
                    f"Using '{resolved_provider}' instead."
                )
        if resolved_provider not in self._clients:
            self._clients[resolved_provider] = _get_client(resolved_provider, self.timeout)
        return self._clients[resolved_provider], resolved_provider, resolved_model

    def is_available(self) -> bool:
        """Return True if the Groq API key is configured."""
        return bool(os.environ.get("GROQ_API_KEY", ""))

    def list_models(self) -> list:
        """Return all supported model API IDs."""
        return [api_id for _, (_, api_id) in MODEL_MAP.items()]

    def generate(
        self,
        model: str,
        prompt: str,
        temperature: float = 0.0,
        max_tokens: int = 1024,
        provider: Optional[str] = None,
    ) -> Optional[str]:
        """Generate a response for a plain text prompt."""
        messages = [{"role": "user", "content": prompt}]
        return self._chat(model, messages, temperature, max_tokens, provider)

    def chat(
        self,
        model: str,
        messages: list,
        temperature: float = 0.0,
        max_tokens: int = 1024,
        provider: Optional[str] = None,
    ) -> Optional[str]:
        """Send a chat message list and return the assistant reply."""
        return self._chat(model, messages, temperature, max_tokens, provider)

    def _chat(
        self,
        model: str,
        messages: list,
        temperature: float,
        max_tokens: int,
        provider: Optional[str],
    ) -> Optional[str]:
        client, resolved_provider, resolved_model = self._client_for(model, provider)
        last_error: Optional[Exception] = None
        for attempt in range(self.max_retries):
            try:
                response = client.chat.completions.create(
                    model=resolved_model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
                return response.choices[0].message.content or ""
            except Exception as exc:
                msg = str(exc)
                wait = 2 ** attempt
                if "429" in msg or "rate limit" in msg.lower() or "quota" in msg.lower():
                    logger.info(
                        f"[APIRunner] Rate limit on {resolved_provider}/{resolved_model}. "
                        f"Retrying in {wait}s…"
                    )
                else:
                    logger.warning(
                        f"[APIRunner] Error from {resolved_provider}/{resolved_model}: {exc}"
                    )
                last_error = exc
                if attempt < self.max_retries - 1:
                    time.sleep(wait)
        logger.error(
            f"[APIRunner] All retries failed for {resolved_model}. Last error: {last_error}"
        )
        return None

    def run_governance_task(
        self,
        model: str,
        task: dict,
        temperature: float = 0.0,
        provider: Optional[str] = None,
    ) -> dict:
        """
        Run a governance benchmark task and return a structured result dict.

        Parameters
        ----------
        model       : Model key or API ID (e.g. 'llama-4-scout-17b').
        task        : Task dict with 'scenario', 'question', 'task_id' keys.
        temperature : Sampling temperature (default 0.0 for determinism).
        provider    : Provider override (default: auto-resolved to 'groq').

        Returns
        -------
        dict with task_id, model, response, response_time_s, success,
             provider_used, model_used.
        """
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
            {"role": "user", "content": user_prompt},
        ]

        _, resolved_provider, resolved_model = self._client_for(model, provider)
        start_time = time.time()
        response = self.chat(model, messages, temperature=temperature, provider=provider)
        elapsed = time.time() - start_time

        return {
            "task_id": task["task_id"],
            "model": model,
            "provider_used": resolved_provider,
            "model_used": resolved_model,
            "response": response or "",
            "response_time_s": round(elapsed, 2),
            "success": response is not None and len(response) > 10,
        }

