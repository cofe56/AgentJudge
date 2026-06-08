from __future__ import annotations

import argparse
import os
import sys
import json
from pathlib import Path

from agentjudge.evaluator import Evaluator
from agentjudge.files import CaseParser, ReportWriter, ScenarioWriter
from agentjudge.providers import ApiError, ProviderConfig, ProviderFactory
from agentjudge.scenarios import ScenarioCatalog

CONFIG_PATH = Path.home() / ".agentjudge_config.json"

def load_config() -> dict[str, str]:
    if CONFIG_PATH.exists():
        try:
            return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}

def save_config(config: dict[str, str]) -> None:
    try:
        CONFIG_PATH.write_text(json.dumps(config, indent=2), encoding="utf-8")
    except Exception:
        pass

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
    print("Available packages:")
    for package in catalog.all():
        print(f"- {package.key}: {package.title} ({len(package.cases)} questions)")
    return 0


def generate_scenario(package_name: str, output: str) -> int:
    catalog = ScenarioCatalog()
    package = catalog.get(package_name)
    output_path = Path(output)
    q_path = ScenarioWriter().write_txt(package, output_path)
    print(f"Generated package '{package.title}' into two files:")
    print(f" 1. Template file for evaluation: {output_path}")
    print(f" 2. Questions-only file for AI chat: {q_path}")
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
    print(f"Average score: {average:.2f}/10")
    print(f"Report saved: {report_path}")
    return 0


def interactive_menu() -> int:
    while True:
        print("\n" + "="*35)
        print("  AgentJudge - Main Menu")
        print("="*35)
        print(" 1. View available scenarios")
        print(" 2. Generate scenario template")
        print(" 3. Evaluate answers file")
        print(" 0. Exit")
        print("="*35)
        choice = input("Choose an action (0-3): ").strip()
        
        if choice == "0":
            print("Exiting...")
            break
        elif choice == "1":
            print("\n--- Available packages ---")
            list_scenarios()
        elif choice == "2":
            print("\n--- Template Generation ---")
            catalog = ScenarioCatalog()
            packages = catalog.all()
            for i, pkg in enumerate(packages, 1):
                print(f" {i:2d}. {pkg.key} ({pkg.title})")
            
            pkg_choice = input("Enter package number or key: ").strip()
            if not pkg_choice:
                continue
            
            package_key = pkg_choice
            if pkg_choice.isdigit():
                idx = int(pkg_choice) - 1
                if 0 <= idx < len(packages):
                    package_key = packages[idx].key
                    
            out_file = input("Enter output filename (e.g., test.txt): ").strip()
            if not out_file:
                continue
            try:
                generate_scenario(package_key, out_file)
            except (KeyError, ValueError, FileNotFoundError) as e:
                print(f"Error: {e}")
        elif choice == "3":
            print("\n--- Evaluating Answers ---")
            in_file = input("Answers file (.txt or .json): ").strip()
            if not in_file:
                continue
            provider = input("Choose provider (openai, groq, ollama, anthropic, gemini) [openai]: ").strip() or "openai"
            
            api_key = ""
            if provider != "ollama":
                config = load_config()
                saved_key = config.get(provider, "")
                if saved_key:
                    use_saved = input(f"Saved API key found for {provider}. Use it? (Y/n) [Y]: ").strip().lower()
                    if use_saved in ("", "y", "yes"):
                        api_key = saved_key
                
                if not api_key:
                    api_key = input(f"Enter new API key for {provider} (leave empty to use env variable): ").strip()
                    if api_key:
                        config[provider] = api_key
                        save_config(config)
            
            model_name = ""
            if provider == "ollama":
                print("\nPopular Ollama models:")
                print(" 1. llama3.1")
                print(" 2. qwen2.5")
                print(" 3. mistral")
                print(" 4. gemma2")
                print(" 5. Enter custom name...")
                ollama_choice = input("Choose a model (1-5) [1]: ").strip() or "1"
                if ollama_choice == "1":
                    model_name = "llama3.1"
                elif ollama_choice == "2":
                    model_name = "qwen2.5"
                elif ollama_choice == "3":
                    model_name = "mistral"
                elif ollama_choice == "4":
                    model_name = "gemma2"
                elif ollama_choice == "5":
                    model_name = input("Enter model name: ").strip()
                else:
                    model_name = "llama3.1"
            else:
                # Optionally allow specifying the model for cloud providers
                model_input = input(f"Enter model name (leave empty for default): ").strip()
                if model_input:
                    model_name = model_input

            report_file = input("Report filename [report.json]: ").strip() or "report.json"
            
            args = argparse.Namespace(
                input=in_file,
                provider=provider,
                api_key=api_key,
                model=model_name,
                base_url="",
                format="json",
                report=report_file,
                timeout=60
            )
            try:
                evaluate_file(args)
            except (FileNotFoundError, KeyError, ValueError, ApiError) as exc:
                print(f"Error: {exc}", file=sys.stderr)
        else:
            print("Unknown choice. Please try again.")
    return 0


def main(argv: list[str] | None = None) -> int:
    if (argv is None and len(sys.argv) == 1) or (argv is not None and len(argv) == 0):
        try:
            return interactive_menu()
        except KeyboardInterrupt:
            print("\nInterrupted by user.", file=sys.stderr)
            return 130

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
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nInterrupted by user.", file=sys.stderr)
        return 130

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
