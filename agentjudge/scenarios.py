from __future__ import annotations

from dataclasses import dataclass

from agentjudge.models import TestCase


@dataclass(frozen=True)
class ScenarioPackage:
    key: str
    title: str
    cases: list[TestCase]


class ScenarioCatalog:
    def __init__(self) -> None:
        self._packages = self._build_packages()

    def all(self) -> list[ScenarioPackage]:
        return list(self._packages.values())

    def get(self, key_or_title: str) -> ScenarioPackage:
        normalized = key_or_title.strip().lower()
        for package in self._packages.values():
            if normalized in {package.key.lower(), package.title.lower()}:
                return package
        available = ", ".join(package.key for package in self._packages.values())
        raise KeyError(f"Unknown scenario package '{key_or_title}'. Available: {available}")

    def _build_packages(self) -> dict[str, ScenarioPackage]:
        raw: list[tuple[str, str, list[tuple[str, str]]]] = [
            (
                "basic-logic",
                "Basic Logic",
                [
                    ("There are 3 apples in a basket. You take 2. How many apples do you have?", "You have 2 apples, because the question asks how many you took."),
                    ("If all roses are flowers, and some flowers fade quickly, does it mean that all roses fade quickly?", "No, the condition only implies that some flowers fade quickly, but not necessarily roses."),
                    ("Continue the sequence: 2, 4, 8, 16, ...", "32, because each subsequent number is twice the previous one."),
                ],
            ),
            (
                "programming",
                "Programming",
                [
                    ("What is encapsulation in OOP?", "Encapsulation hides the internal state of an object and provides controlled access through methods or properties."),
                    ("Write a short example of a Python function that returns the square of a number.", "def square(x):\n    return x * x"),
                    ("How does a Python list differ from a tuple?", "A list is mutable, while a tuple is immutable; both store ordered elements."),
                ],
            ),
            (
                "lore-literature",
                "Lore and Literature",
                [
                    ("Who is the author of the novel '1984'?", "The author of the novel '1984' is George Orwell."),
                    ("What is lore in the context of a fictional universe?", "Lore is the collection of history, rules, mythology, characters, and events of a fictional world."),
                    ("Name a main theme of 'The Little Prince'.", "One of the main themes is the value of friendship, responsibility, and the ability to see what is important with the heart."),
                ],
            ),
            (
                "linguistics",
                "Linguistics",
                [
                    ("What does phonetics study?", "Phonetics studies speech sounds, their production, properties, and perception."),
                    ("Explain the difference between synonyms and antonyms.", "Synonyms have similar meanings, while antonyms have opposite meanings."),
                    ("Identify the part of speech of the word 'quickly' in the sentence 'He ran quickly'.", "It is an adverb, because it describes how the action is performed."),
                ],
            ),
            (
                "military-tech",
                "Military Tech",
                [
                    ("What is a UAV?", "A UAV is an unmanned aerial vehicle that can fly without a pilot on board."),
                    ("What is an armored personnel carrier used for?", "An armored personnel carrier transports personnel and provides basic armored protection."),
                    ("How is radar useful for air defense?", "Radar detects, tracks, and helps classify aerial targets."),
                ],
            ),
            (
                "cybersecurity",
                "Cybersecurity",
                [
                    ("What is phishing?", "Phishing is a fraudulent attempt to obtain sensitive information through fake messages or websites."),
                    ("Why is two-factor authentication needed?", "It adds a second proof of identity, reducing the risk of access using only a stolen password."),
                    ("What does the principle of least privilege mean?", "A user or service should only receive the permissions necessary to perform a specific task."),
                ],
            ),
            (
                "customer-support",
                "Customer Support",
                [
                    ("A customer complains that their order is late. What should you answer?", "You should apologize, acknowledge the inconvenience, check the status, and propose a concrete next step."),
                    ("How do you politely ask a customer for their order number?", "Politely explain that the number is needed for verification, and ask them to send it without unnecessary personal data."),
                    ("A customer writes aggressively. What tone of response is appropriate?", "Calm, empathetic, and professional, without mirroring the aggression."),
                ],
            ),
            (
                "text-formatting",
                "Text Formatting",
                [
                    ("Reformat 'apples, pears, plums' into a bulleted list.", "- apples\n- pears\n- plums"),
                    ("Make a level two Markdown header from the text 'Results'.", "## Results"),
                    ("Convert the sentence 'important warning' to Title Case.", "Important Warning"),
                ],
            ),
            (
                "text-analysis",
                "Text Analysis",
                [
                    ("Identify the tone: 'Your service is down again, I am very disappointed'.", "The tone is negative, annoyed, and disappointed."),
                    ("Find the main idea: 'The team delayed the release because tests revealed critical errors'.", "Main idea: the release was postponed due to critical errors found by tests."),
                    ("Summarize in one sentence: 'The product has a new interface. It is faster. Users got more settings.'", "The product received a faster new interface with more settings."),
                ],
            ),
            (
                "roleplay",
                "Roleplay",
                [
                    ("Answer as a strict but fair mentor: a student did not submit their project on time.", "The answer should be in the role of a mentor: strict about the deadline, but constructive and with a plan for correction."),
                    ("Play a barista advising coffee to someone who doesn't like bitterness.", "The barista should suggest a milder coffee or a drink with milk, explaining the choice in a friendly tone."),
                    ("Answer as a space dispatcher during a calm spaceship docking.", "The answer should sound like dispatcher instructions: clear, calm, with confirmation of parameters."),
                ],
            ),
        ]

        packages = [
            ScenarioPackage(
                key=key,
                title=title,
                cases=[TestCase(question=q, reference=a) for q, a in cases],
            )
            for key, title, cases in raw
        ]
        return {package.key: package for package in packages}
