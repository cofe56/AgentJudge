# AgentJudge

AgentJudge is a Python CLI tool for automatic LLM-as-a-Judge evaluation of AI model answers.

## Features

- Interactive CLI menu (just run `python -m agentjudge`).
- Generates built-in scenario packages as `.txt` files.
- Parses filled `.txt` scenario files and JSON arrays.
- Supports OpenAI-compatible APIs: OpenAI, Groq, and local Ollama.
- Supports separate clients for Anthropic Claude and Google Gemini.
- Prints evaluation progress, calculates average score, and writes `report.json`.
- Uses only files and Python's standard `json` module. No database is required.

## Usage

Run the interactive menu from the project directory:

```powershell
python -m agentjudge
```

Or use the CLI arguments for automation:

List scenarios:
```powershell
python -m agentjudge scenarios
```

Generate a scenario file:
```powershell
python -m agentjudge generate --package programming --output programming.txt
```

Fill the `=== AI Answer ===` sections, then evaluate:
```powershell
python -m agentjudge evaluate --input programming.txt --provider openai --api-key YOUR_KEY --model gpt-4o-mini --report report.json
```

Evaluate through local Ollama:
```powershell
python -m agentjudge evaluate --input programming.txt --provider ollama --model llama3.1 --base-url http://localhost:11434/v1
```

JSON input can be either an array or an object with a `cases` array:
```json
[
  {
    "question": "What is encapsulation?",
    "reference": "Encapsulation hides internal state behind controlled methods.",
    "ai_answer": "It is hiding object details and exposing methods."
  }
]
```

## Built-In Packages

- `basic-logic` - Basic Logic
- `programming` - Programming
- `lore-literature` - Lore and Literature
- `linguistics` - Linguistics
- `military-tech` - Military Tech
- `cybersecurity` - Cybersecurity
- `customer-support` - Customer Support
- `text-formatting` - Text Formatting
- `text-analysis` - Text Analysis
- `roleplay` - Roleplay
