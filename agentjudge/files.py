from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from agentjudge.models import EvaluationRecord, TestCase
from agentjudge.scenarios import ScenarioPackage


QUESTION_MARKER = "=== Питання ==="
REFERENCE_MARKER = "=== Еталон ==="
ANSWER_MARKER = "=== Відповідь ШІ ==="


class ScenarioWriter:
    def write_txt(self, package: ScenarioPackage, output_path: Path) -> None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        blocks = []
        for case in package.cases:
            blocks.append(
                f"{QUESTION_MARKER}\n"
                f"{case.question}\n"
                f"{REFERENCE_MARKER}\n"
                f"{case.reference}\n"
                f"{ANSWER_MARKER}\n"
            )
        output_path.write_text("\n".join(blocks), encoding="utf-8")


class CaseParser:
    def parse(self, input_path: Path) -> list[TestCase]:
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")

        suffix = input_path.suffix.lower()
        if suffix == ".json":
            return self._parse_json(input_path)
        if suffix == ".txt":
            return self._parse_txt(input_path)
        raise ValueError("Unsupported input format. Use .txt or .json.")

    def _parse_json(self, input_path: Path) -> list[TestCase]:
        try:
            payload: Any = json.loads(input_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON: {exc}") from exc

        if isinstance(payload, dict) and isinstance(payload.get("cases"), list):
            items = payload["cases"]
        elif isinstance(payload, list):
            items = payload
        else:
            raise ValueError("JSON input must be an array or an object with a 'cases' array.")

        cases = [TestCase.from_json(item) for item in items if isinstance(item, dict)]
        if len(cases) != len(items):
            raise ValueError("Every JSON array item must be an object.")
        if not cases:
            raise ValueError("No test cases found in JSON input.")
        return cases

    def _parse_txt(self, input_path: Path) -> list[TestCase]:
        text = input_path.read_text(encoding="utf-8")
        pattern = re.compile(
            rf"{re.escape(QUESTION_MARKER)}\s*(.*?)\s*"
            rf"{re.escape(REFERENCE_MARKER)}\s*(.*?)\s*"
            rf"{re.escape(ANSWER_MARKER)}\s*(.*?)(?=\s*{re.escape(QUESTION_MARKER)}|\Z)",
            re.DOTALL,
        )
        cases = [
            TestCase(question=q.strip(), reference=reference.strip(), ai_answer=answer.strip())
            for q, reference, answer in pattern.findall(text)
        ]
        if not cases:
            raise ValueError("No test cases found. Check required markers in the .txt file.")
        return cases


class ReportWriter:
    def write(self, output_path: Path, records: list[EvaluationRecord], provider: str, model: str) -> None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        average = sum(record.score for record in records) / len(records) if records else 0.0
        report = {
            "provider": provider,
            "model": model,
            "total": len(records),
            "average_score": round(average, 2),
            "results": [record.to_json() for record in records],
        }
        output_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

