# AgentJudge

AgentJudge is a Python CLI tool for automatic LLM-as-a-Judge evaluation of AI model answers.

## Features

- **Single-Word Command**: Just run `agentjudge` in your terminal.
- **Interactive CLI Menu**: Easy numbered selection for scenarios and AI models.
- **Auto-Formatting**: Generates and evaluates `.txt` files automatically without needing to type extensions.
- **Smart Generation**: Creates a separate `_questions.txt` file for easy copy-pasting to AI chats, alongside the main template.
- **API Key Persistence**: Securely saves your API keys locally so you don't have to enter them every time.
- Supports OpenAI, Groq, local Ollama, Anthropic Claude, and Google Gemini.
- Prints evaluation progress, calculates average score, and writes a readable `report.txt`.

## Usage

Run the interactive menu from anywhere:

```powershell
agentjudge
```

Or use the CLI arguments for automation:

List scenarios:
```powershell
agentjudge scenarios
```

Generate a scenario file (creates `programming.txt` and `programming_questions.txt`):
```powershell
agentjudge generate --package programming --output programming
```

Fill the `=== AI Answer ===` sections in `programming.txt`, then evaluate:
```powershell
agentjudge evaluate --input programming --provider openai --model gpt-4o-mini --report report
```

Evaluate through local Ollama:
```powershell
agentjudge evaluate --input programming --provider ollama --model llama3.1 --base-url http://localhost:11434/v1
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
- `mathematics` - Mathematics
- `physics` - Physics
- `chemistry` - Chemistry
- `biology` - Biology
- `history` - History
- `geography` - Geography
- `economics` - Economics
- `philosophy` - Philosophy
- `psychology` - Psychology
- `medicine` - Medicine
- `space-exploration` - Space Exploration
- `machine-learning` - Machine Learning
- `blockchain` - Blockchain
- `game-development` - Game Development
- `music-theory` - Music Theory
- `art-history` - Art History
- `law-and-ethics` - Law and Ethics
- `cooking-and-nutrition` - Cooking and Nutrition
- `environmental-science` - Environmental Science
- `sports-analytics` - Sports Analytics
