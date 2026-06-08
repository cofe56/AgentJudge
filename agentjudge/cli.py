from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from agentjudge.evaluator import Evaluator
from agentjudge.files import CaseParser, ReportWriter, ScenarioWriter
from agentjudge.providers import ApiError, ProviderConfig, ProviderFactory
from agentjudge.scenarios import ScenarioCatalog


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="AgentJudge",
        description="CLI tool for LLM-as-a-Judge evaluation of AI answers.",
    )
    subparsers = parser.add_subparsers(dest="mode", required=True)

    scenarios = subparsers.add_parser("scenarios", help="List built-in scenario packages.")

    generate = subparsers.add_parser("generate", help="Generate a .txt scenario file.")
    generate.add_argument("--package", "-p", required=True, help="Package key or title.")
    generate.add_argument("--output", "-o", required=True, help="Output .txt path.")

    evaluate = subparsers.add_parser("evaluate", help="Evaluate filled .txt or .json test file.")
    evaluate.add_argument("--input", "-i", required=True, help="Filled .txt or .json file.")
    evaluate.add_argument("--provider", "-p", required=True, choices=["openai", "groq", "ollama", "anthropic", "gemini"])
    evaluate.add_argument("--api-key", default="", help="API key. Optional for local Ollama.")
    evaluate.add_argument("--model", default="", help="Provider model name.")
    evaluate.add_argument("--base-url", default="", help="Override provider base URL.")
    evaluate.add_argument("--format", choices=["json", "txt"], default="json", help="Required judge response format.")
    evaluate.add_argument("--report", default="report.json", help="Output report path.")
    evaluate.add_argument("--timeout", type=int, default=60, help="API timeout in seconds.")

    return parser


def list_scenarios() -> int:
    catalog = ScenarioCatalog()
    print("Доступні пакети:")
    for package in catalog.all():
        print(f"- {package.key}: {package.title} ({len(package.cases)} питань)")
    return 0


def generate_scenario(package_name: str, output: str) -> int:
    catalog = ScenarioCatalog()
    package = catalog.get(package_name)
    output_path = Path(output)
    ScenarioWriter().write_txt(package, output_path)
    print(f"Згенеровано пакет '{package.title}': {output_path}")
    return 0


def evaluate_file(args: argparse.Namespace) -> int:
    cases = CaseParser().parse(Path(args.input))
    api_key = args.api_key or os.getenv(f"{args.provider.upper()}_API_KEY", "")
    provider = ProviderFactory.create(
        ProviderConfig(
            provider=args.provider,
            api_key=api_key,
            model=args.model,
            base_url=args.base_url,
            output_format=args.format,
            timeout_seconds=args.timeout,
        )
    )
    records = Evaluator(provider).evaluate(cases)
    average = sum(record.score for record in records) / len(records) if records else 0.0
    report_path = Path(args.report)
    ReportWriter().write(report_path, records, args.provider, args.model)
    print(f"Середній бал: {average:.2f}/10")
    print(f"Звіт збережено: {report_path}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.mode == "scenarios":
            return list_scenarios()
        if args.mode == "generate":
            return generate_scenario(args.package, args.output)
        if args.mode == "evaluate":
            return evaluate_file(args)
    except (FileNotFoundError, KeyError, ValueError, ApiError) as exc:
        print(f"Помилка: {exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("Перервано користувачем.", file=sys.stderr)
        return 130

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
