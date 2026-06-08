from __future__ import annotations

import json
import re
import urllib.error
import urllib.request
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from agentjudge.models import JudgeResult, TestCase


BASE_SYSTEM_PROMPT = (
    "You are an AI Judge evaluating model answers. "
    "Compare the 'AI Answer' to the 'Reference' in the context of the 'Question'. "
    "Provide a score from 1 to 10, where 10 means fully accurate/correct, and 1 means completely wrong. "
    "Evaluate factual correctness, completeness, instruction following, and format. "
    "Do not add Markdown, preambles, or additional text outside the requested format. "
)


@dataclass(frozen=True)
class ProviderConfig:
    provider: str
    api_key: str = ""
    model: str = ""
    base_url: str = ""
    output_format: str = "json"
    timeout_seconds: int = 60


class ApiError(RuntimeError):
    pass


class AiProvider(ABC):
    def __init__(self, config: ProviderConfig) -> None:
        self.config = config

    @abstractmethod
    def judge(self, test_case: TestCase) -> JudgeResult:
        raise NotImplementedError

    def _build_user_prompt(self, test_case: TestCase) -> str:
        return (
            f"Question:\n{test_case.question}\n\n"
            f"Reference:\n{test_case.reference}\n\n"
            f"AI Answer:\n{test_case.ai_answer}\n\n"
            f"Required judge response format: {self.config.output_format.upper()}."
        )

    def _system_prompt(self) -> str:
        if self.config.output_format == "txt":
            return (
                BASE_SYSTEM_PROMPT
                + "Return only two TXT lines in format:\n"
                + "score: 7\n"
                + "reason: short explanation in English"
            )
        return (
            BASE_SYSTEM_PROMPT
            + "Return only JSON in format: "
            + '{"score": 7, "reason": "short explanation in English"}'
        )

    def _post_json(self, url: str, payload: dict[str, Any], headers: dict[str, str]) -> dict[str, Any]:
        headers = {
            "Accept": "application/json",
            "User-Agent": "AgentJudge/0.1 (+https://local.cli)",
            **headers,
        }
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        request = urllib.request.Request(url=url, data=data, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(request, timeout=self.config.timeout_seconds) as response:
                body = response.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise ApiError(f"API HTTP {exc.code}: {detail}") from exc
        except urllib.error.URLError as exc:
            raise ApiError(f"API connection error: {exc.reason}") from exc
        except TimeoutError as exc:
            raise ApiError(f"API request timed out after {self.config.timeout_seconds} seconds. Try increasing --timeout.") from exc

        try:
            return json.loads(body)
        except json.JSONDecodeError as exc:
            raise ApiError(f"API returned non-JSON response: {body[:500]}") from exc

    def _parse_judge_result(self, raw: str) -> JudgeResult:
        text = raw.strip()
        if text.startswith("```"):
            text = re.sub(r"^```(?:json|txt)?\s*|\s*```$", "", text, flags=re.IGNORECASE | re.DOTALL).strip()

        try:
            data = json.loads(text)
            score = float(data["score"])
            reason = str(data.get("reason", "")).strip()
        except (json.JSONDecodeError, KeyError, TypeError, ValueError):
            score_match = re.search(r"(?:score|бал)\D*(10|[1-9])", text, flags=re.IGNORECASE)
            if not score_match:
                raise ApiError(f"Judge response is not valid JSON/TXT with score: {raw}")
            score = float(score_match.group(1))
            reason = text

        if not 1 <= score <= 10:
            raise ApiError(f"Judge score out of range 1..10: {score}")
        return JudgeResult(score=score, reason=reason, raw_response=raw)


class OpenAiCompatibleProvider(AiProvider):
    DEFAULTS = {
        "openai": ("https://api.openai.com/v1", "gpt-4o-mini"),
        "groq": ("https://api.groq.com/openai/v1", "llama-3.3-70b-versatile"),
        "ollama": ("http://localhost:11434/v1", "llama3.1"),
    }

    def judge(self, test_case: TestCase) -> JudgeResult:
        base_url, default_model = self.DEFAULTS[self.config.provider]
        base_url = (self.config.base_url or base_url).rstrip("/")
        model = self.config.model or default_model
        payload: dict[str, Any] = {
            "model": model,
            "messages": [
                {"role": "system", "content": self._system_prompt()},
                {"role": "user", "content": self._build_user_prompt(test_case)},
            ],
            "temperature": 0,
        }
        if self.config.output_format == "json":
            payload["response_format"] = {"type": "json_object"}

        headers = {"Content-Type": "application/json"}
        if self.config.api_key:
            headers["Authorization"] = f"Bearer {self.config.api_key}"

        response = self._post_json(f"{base_url}/chat/completions", payload, headers)
        content = response["choices"][0]["message"]["content"]
        return self._parse_judge_result(content)


class AnthropicProvider(AiProvider):
    def judge(self, test_case: TestCase) -> JudgeResult:
        if not self.config.api_key:
            raise ApiError("Anthropic requires an API key.")

        base_url = (self.config.base_url or "https://api.anthropic.com").rstrip("/")
        model = self.config.model or "claude-3-5-sonnet-20241022"
        payload = {
            "model": model,
            "max_tokens": 500,
            "temperature": 0,
            "system": self._system_prompt(),
            "messages": [{"role": "user", "content": self._build_user_prompt(test_case)}],
        }
        headers = {
            "Content-Type": "application/json",
            "x-api-key": self.config.api_key,
            "anthropic-version": "2023-06-01",
        }
        response = self._post_json(f"{base_url}/v1/messages", payload, headers)
        content_blocks = response.get("content", [])
        text = "".join(block.get("text", "") for block in content_blocks if block.get("type") == "text")
        return self._parse_judge_result(text)


class GeminiProvider(AiProvider):
    def judge(self, test_case: TestCase) -> JudgeResult:
        if not self.config.api_key:
            raise ApiError("Gemini requires an API key.")

        base_url = (self.config.base_url or "https://generativelanguage.googleapis.com/v1beta").rstrip("/")
        model = self.config.model or "gemini-1.5-flash"
        url = f"{base_url}/models/{model}:generateContent?key={self.config.api_key}"
        payload = {
            "systemInstruction": {"parts": [{"text": self._system_prompt()}]},
            "contents": [{"role": "user", "parts": [{"text": self._build_user_prompt(test_case)}]}],
            "generationConfig": {
                "temperature": 0,
                "responseMimeType": "application/json" if self.config.output_format == "json" else "text/plain",
            },
        }
        response = self._post_json(url, payload, {"Content-Type": "application/json"})
        text = response["candidates"][0]["content"]["parts"][0]["text"]
        return self._parse_judge_result(text)


class ProviderFactory:
    @staticmethod
    def create(config: ProviderConfig) -> AiProvider:
        provider = config.provider.lower()
        normalized = ProviderConfig(
            provider=provider,
            api_key=config.api_key,
            model=config.model,
            base_url=config.base_url,
            output_format=config.output_format.lower(),
            timeout_seconds=config.timeout_seconds,
        )
        if provider in {"openai", "groq", "ollama"}:
            return OpenAiCompatibleProvider(normalized)
        if provider == "anthropic":
            return AnthropicProvider(normalized)
        if provider == "gemini":
            return GeminiProvider(normalized)
        raise ValueError("Unsupported provider. Use openai, groq, ollama, anthropic, or gemini.")
