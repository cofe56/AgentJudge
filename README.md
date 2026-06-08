# AgentJudge ⚖️

AgentJudge is a powerful, interactive command-line tool designed for the automated **LLM-as-a-Judge** evaluation of AI answers. It comes packed with a rich selection of evaluation scenarios, supports all major LLM providers (including local running models via Ollama), caches configuration settings securely, and automatically handles formatting with user-friendly plain-text workflows.

---

## 🌟 Key Features

*   **🚀 Single-Word Command**: Simply type `agentjudge` anywhere in your terminal to start the interactive console.
*   **💻 Interactive CLI Menu**: Numbered menus let you navigate scenarios, generate files, choose providers, and select models without remembering complex commands.
*   **📂 Text-First Dual Generation**: Outputs a clean template `.txt` for testing, and a separate `_questions.txt` containing only the raw questions to easily copy-paste into the AI model's chat.
*   **🔒 Local Configuration & API Key Cache**: Saves your API keys securely in your home directory (`~/.agentjudge_config.json`), prompting you only when necessary.
*   **🌐 Multi-Provider Support**: Compatible out-of-the-box with **OpenAI**, **Anthropic**, **Google Gemini**, **Groq**, and **local Ollama** instances.
*   **📊 Comprehensive Reporting**: Calculates average scores (1-10) and compiles human-readable evaluation reports detailing the judge's exact reasoning.
*   **📚 29 Built-in Packages**: 145 professional, hand-crafted evaluation scenarios across Logic, Programming, Science, Philosophy, Law, and more.

---

## 🛠️ Normal Launch & Installation

To install AgentJudge and configure it for local executable launch:

### 1. Prerequisites
Ensure you have **Python >= 3.10** installed.

### 2. Install the package in editable mode
Clone the repository and install it using `pip` from the root directory:

```bash
git clone https://github.com/cofe56/AgentJudge.git
cd AgentJudge
pip install -e .
```

### 3. Run the interactive console
Once installed, the CLI shortcut is fully integrated. Just type:

```bash
agentjudge
```

If your Python scripts folder is not in your system's PATH, you can always run the application as a Python module:

```bash
python -m agentjudge
```

---

## 🔄 Step-by-Step Workflow

Evaluating an AI model takes just four quick steps:

```
[1. Choose Scenario] ---> [2. Copy Raw Questions] ---> [3. Get AI Responses & Paste] ---> [4. Run Judge]
```

### Step 1: Generate the Scenario Files
Launch the menu (`agentjudge`), select option **2**, and choose a scenario package (e.g., `programming`). Provide an output name (e.g., `my_test`).

This generates two files in your folder:
1.  **`my_test.txt`**: The evaluation template containing clear structural markers.
2.  **`my_test_questions.txt`**: A clean file containing just the questions.

### Step 2: Feed Questions to the Target AI
Open `my_test_questions.txt` and copy the questions. Paste them into the AI model you want to evaluate (e.g., ChatGPT, Claude, Llama 3) and copy its responses.

### Step 3: Paste AI Responses into the Template
Open the `my_test.txt` template. Paste the AI's responses directly under the appropriate `=== AI Answer ===` markers. 

Example:
```txt
=== Question ===
Explain the difference between a mutex and a semaphore.

=== Reference ===
A mutex ensures only one thread accesses a resource. A semaphore allows a specific number of threads.

=== AI Answer ===
[Paste the AI model's response here]
```

### Step 4: Run the Judge
Choose option **3** in the interactive menu:
1.  Enter your answers filename (e.g., `my_test` — no need to type `.txt`).
2.  Select your preferred Judge Provider (OpenAI, Groq, Ollama, Anthropic, Gemini).
3.  Reuse your cached API key or enter a new one. (For Ollama, you'll be shown a quick list of popular local models like `llama3.1`, `qwen2.5`, etc.).
4.  View the evaluation result directly in the terminal and open the generated `report.txt` file to read the model's scores and reasoning.

---

## 🧭 CLI Commands (Alternative Automation)

In addition to the interactive menu, you can fully automate evaluations using command-line arguments:

### List available packages
```bash
agentjudge scenarios
```

### Generate template files programmatically
```bash
agentjudge generate --package programming --output my_test
```

### Evaluate filled files
```bash
# Evaluate using OpenAI
agentjudge evaluate --input my_test.txt --provider openai --model gpt-4o-mini --report my_report.txt

# Evaluate using local Ollama instance
agentjudge evaluate --input my_test.txt --provider ollama --model llama3.1 --base-url http://localhost:11434/v1 --report my_report.txt
```

---

## 📚 Built-in Scenario Packages

AgentJudge features 145 scenarios across 29 specialized domains. Use the package keys below to generate templates:

| Package Key | Title | Focus Area / Description |
| :--- | :--- | :--- |
| `basic-logic` | Basic Logic | Riddles, logic problems, and spatial reasoning. |
| `programming` | Programming | Algorithms, concurrency, safety, and core design. |
| `lore-literature` | Lore & Literature | Book analysis, tropes, lore structures, and themes. |
| `linguistics` | Linguistics | Morphological, semantic, and syntax concepts. |
| `military-tech` | Military Tech | Aerospace, armor systems, and electronic warfare. |
| `cybersecurity` | Cybersecurity | Application vulnerabilities, protocols, and network attacks. |
| `customer-support` | Customer Support | De-escalation strategies, policy overrides, and tone control. |
| `text-formatting` | Text Formatting | Outputting Markdown tables, LaTeX, and JSON schemas. |
| `text-analysis` | Text Analysis | Bias checking, summary extraction, and logical fallacies. |
| `mathematics` | Mathematics | Proofs, linear algebra, calculus, and mathematical logic. |
| `physics` | Physics | Relativity, quantum mechanics, and thermodynamics. |
| `chemistry` | Chemistry | Organic mechanisms, equilibrium, and buffer systems. |
| `biology` | Biology | CRISPR technology, cellular pathways, and genetics. |
| `history` | History | Geopolitical summits, treaties, and socio-economic shifts. |
| `geography` | Geography | Plate tectonics, landforms, and urban heat models. |
| `economics` | Economics | Fiscal tools, inflation, inequality indexes, and trade-offs. |
| `philosophy` | Philosophy | Moral imperatives, thought experiments, and existentialism. |
| `psychology` | Psychology | Cognitive biases, conditioning, and behavioral hierarchy. |
| `medicine` | Medicine | Pathophysiology, mechanisms of drugs, and epidemiology. |
| `space-exploration`| Space Exploration | Orbital mechanics, deep-space probes, and astrophysics. |
| `machine-learning` | Machine Learning | Gradient issues, transformer systems, and classification. |
| `blockchain` | Blockchain | Consensus algorithms, forks, smart contracts, and Layer-2 scaling.|
| `game-development` | Game Development | Rendering pipelines, pathfinding, and optimization. |
| `music-theory` | Music Theory | Temperament differences, compositional forms, and chord scales. |
| `art-history` | Art History | Artistic movements, lighting techniques, and design philosophies.|
| `law-and-ethics` | Law and Ethics | Legal doctrines, civil vs common systems, and ethical duties. |
| `cooking-nutrition`| Cooking & Nutrition | Food chemistry, stabilization techniques, and dietary roles. |
| `environmental-sci`| Environmental Science| Greenhouse models, trophic changes, and carbon accounting. |
| `sports-analytics` | Sports Analytics | Advanced statistics, efficiency metrics, and rating systems. |

---

## 🔒 Configuration & API Keys

API keys entered in the interactive prompt are stored in a plaintext configuration file at:
*   **Windows**: `C:\Users\<Username>\.agentjudge_config.json`
*   **macOS / Linux**: `~/.agentjudge_config.json`

Alternatively, you can expose environment variables before running:
*   `OPENAI_API_KEY`
*   `GROQ_API_KEY`
*   `ANTHROPIC_API_KEY`
*   `GEMINI_API_KEY`

---

## 📝 Custom Evaluation Formats

### Plain-Text Files
You can create custom `.txt` files for evaluation by separating entries with the core markers. Make sure each question-block has the following format:
```txt
=== Question ===
[Custom Question]

=== Reference ===
[Reference Answer / Grading Rubric]

=== AI Answer ===
[AI's response to evaluate]
```

### JSON Files (Alternative)
You can evaluate pre-existing datasets saved as a JSON list or a JSON object containing a `"cases"` array:
```json
[
  {
    "question": "What is encapsulation?",
    "reference": "Encapsulation hides internal state behind controlled methods.",
    "ai_answer": "It is hiding object details and exposing methods."
  }
]
```

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
