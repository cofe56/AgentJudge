from __future__ import annotations

from agentjudge.models import EvaluationRecord, TestCase
from agentjudge.providers import AiProvider


class Evaluator:
    def __init__(self, provider: AiProvider) -> None:
        self._provider = provider

    def evaluate(self, cases: list[TestCase]) -> list[EvaluationRecord]:
        records: list[EvaluationRecord] = []
        for index, test_case in enumerate(cases, start=1):
            print(f"[{index}/{len(cases)}] Оцінювання питання...")
            result = self._provider.judge(test_case)
            print(f"  Бал: {result.score}/10")
            records.append(EvaluationRecord.from_case(test_case, result))
        return records

