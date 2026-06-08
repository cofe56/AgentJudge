from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class TestCase:
    question: str
    reference: str
    ai_answer: str = ""

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> "TestCase":
        question = data.get("question") or data.get("питання")
        reference = data.get("reference") or data.get("expected") or data.get("еталон")
        ai_answer = data.get("ai_answer") or data.get("answer") or data.get("відповідь_ші") or ""

        if not isinstance(question, str) or not question.strip():
            raise ValueError("JSON item is missing a non-empty 'question' field.")
        if not isinstance(reference, str) or not reference.strip():
            raise ValueError("JSON item is missing a non-empty 'reference' field.")
        if not isinstance(ai_answer, str):
            raise ValueError("'ai_answer' must be a string.")

        return cls(question=question.strip(), reference=reference.strip(), ai_answer=ai_answer.strip())

    def to_json(self) -> dict[str, str]:
        return asdict(self)


@dataclass(frozen=True)
class JudgeResult:
    score: float
    reason: str
    raw_response: str


@dataclass(frozen=True)
class EvaluationRecord:
    question: str
    reference: str
    ai_answer: str
    score: float
    reason: str
    raw_judge_response: str

    @classmethod
    def from_case(cls, test_case: TestCase, result: JudgeResult) -> "EvaluationRecord":
        return cls(
            question=test_case.question,
            reference=test_case.reference,
            ai_answer=test_case.ai_answer,
            score=result.score,
            reason=result.reason,
            raw_judge_response=result.raw_response,
        )

    def to_json(self) -> dict[str, Any]:
        return asdict(self)

