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
                    ("Sally has 3 brothers. Each brother has 2 sisters. How many sisters does Sally have?", "Sally has 1 sister. Since all brothers share the same sisters, there are 2 sisters in total (Sally and her one sister)."),
                    ("A bat and a ball cost $1.10 in total. The bat costs $1.00 more than the ball. How much does the ball cost?", "The ball costs $0.05. The bat is $1.05."),
                    ("If you look at a clock and the time is exactly 3:15, what is the angle between the hour and the minute hands?", "7.5 degrees. The minute hand is at 90 degrees. The hour hand moves 30 degrees per hour, so in 15 minutes it moves 1/4 of 30, which is 7.5 degrees. 90 - 82.5 = 7.5."),
                    ("There are 5 machines that make 5 widgets in 5 minutes. How long does it take 100 machines to make 100 widgets?", "5 minutes. Each machine makes 1 widget in 5 minutes."),
                    ("You have a 3-gallon jug and a 5-gallon jug. How can you measure exactly 4 gallons of water?", "Fill the 5-gallon jug. Pour it into the 3-gallon jug, leaving 2 gallons in the 5. Empty the 3. Pour the 2 gallons into the 3. Fill the 5. Pour from the 5 to fill the 3 (which takes 1 gallon). The 5-gallon jug now holds exactly 4 gallons."),
                ],
            ),
            (
                "programming",
                "Programming",
                [
                    ("Explain the difference between a mutex and a semaphore, providing a real-world analogy for each.", "A mutex ensures only one thread accesses a resource (like a key to a single-occupancy bathroom). A semaphore allows a specific number of threads (like a bouncer letting only 5 people into a club)."),
                    ("Identify the vulnerability in this code: `query = f'SELECT * FROM users WHERE username = {user_input}'` and how to fix it.", "It is vulnerable to SQL Injection. Fix it by using parameterized queries or prepared statements, e.g., `execute('SELECT * FROM users WHERE username = ?', (user_input,))`."),
                    ("Write a Python decorator that limits the execution of a function to at most 3 times per minute.", "The AI should provide a rate-limiting decorator using a sliding window or token bucket algorithm, keeping timestamps in a closure or global dictionary, raising an exception if exceeded."),
                    ("What is the time complexity of searching for an element in a balanced Binary Search Tree, and why?", "O(log n). Because at each step, the search space is halved by choosing the left or right subtree based on comparisons."),
                    ("Explain Python's Global Interpreter Lock (GIL) and its implications for multithreading in CPU-bound vs I/O-bound tasks.", "The GIL prevents multiple native threads from executing Python bytecodes at once. Multithreading is ineffective for CPU-bound tasks, but highly effective for I/O-bound tasks since the GIL is released during I/O."),
                ],
            ),
            (
                "lore-literature",
                "Lore and Literature",
                [
                    ("Analyze the underlying philosophical differences between the societies in Huxley's 'Brave New World' and Orwell's '1984'.", "1984 uses pain, surveillance, and totalitarian control to oppress. Brave New World uses pleasure, genetic conditioning, and constant distraction to enforce compliance."),
                    ("In J.R.R. Tolkien's legendarium, what is the fundamental difference between the creation of Elves and Dwarves?", "Elves were directly created by Eru Ilúvatar (Children of Ilúvatar), while Dwarves were created by the Vala Aulë and only later given true independent life by Eru."),
                    ("Explain the unreliable narrator trope using 'The Catcher in the Rye' as an example.", "An unreliable narrator's credibility is compromised. Holden Caulfield often lies, exaggerates, and suffers from mental trauma, making his recounting of events highly subjective."),
                    ("What is the 'Dune' universe's Butlerian Jihad, and how does it shape the technology of the setting?", "It was a war against thinking machines, resulting in a universal ban on AI. This led to human computers (Mentats) and specialized factions like the Spacing Guild and Bene Gesserit."),
                    ("Describe the concept of 'Hubris' in ancient Greek tragedy.", "Hubris is excessive pride or defiance of the gods, leading to the protagonist's tragic downfall (Nemesis), as seen in Oedipus Rex."),
                ],
            ),
            (
                "linguistics",
                "Linguistics",
                [
                    ("Explain the Sapir-Whorf hypothesis and provide arguments for its strong and weak versions.", "Strong version (determinism): language determines thought. Weak version (relativity): language influences thought. Modern linguistics generally accepts the weak version but rejects the strong."),
                    ("What is the difference between prescriptive and descriptive linguistics?", "Prescriptive dictates how language *should* be used (grammar rules). Descriptive observes and records how language is *actually* used by native speakers."),
                    ("Analyze the morphological structure of the word 'unbelievably'.", "Prefix: un- (negation). Root: believ(e) (verb). Suffix: -able (adjective-forming). Suffix: -ly (adverb-forming)."),
                    ("Describe the phenomenon of 'code-switching' and its sociolinguistic functions.", "Code-switching is alternating between languages/varieties in conversation. Functions include expressing identity, conveying nuance, matching the social context, or making up for lexical gaps."),
                    ("What is a 'phoneme' and how does it differ from an 'allophone'?", "A phoneme is a basic unit of sound that distinguishes meaning. An allophone is a phonetic variation of a phoneme that does not change the meaning (e.g., aspirated vs. unaspirated 'p' in English)."),
                ],
            ),
            (
                "military-tech",
                "Military Tech",
                [
                    ("Compare the operational doctrines of stealth aircraft (F-35) vs traditional air superiority fighters (F-15).", "F-35 relies on low observability, advanced sensors, and BVR (beyond visual range) engagements. F-15 relies on speed, payload, radar power, and maneuverability for dominance."),
                    ("Explain how Explosive Reactive Armor (ERA) works on modern main battle tanks.", "It consists of explosive layers sandwiched between metal plates. When hit by a shaped charge, the explosive detonates, disrupting the penetrator jet and protecting the main armor."),
                    ("What is an Electronic Warfare (EW) suite, and what are its primary offensive and defensive capabilities?", "An EW suite manipulates the electromagnetic spectrum. Defensive: radar warning receivers, chaff/flare dispensers. Offensive: jamming enemy radar, spoofing communications."),
                    ("Describe the strategic implications of Hypersonic Glide Vehicles (HGVs).", "HGVs travel at Mach 5+, flying at lower altitudes than ICBMs and maneuvering unpredictably, making them extremely difficult to track and intercept with current missile defense systems."),
                    ("How does a phased-array radar differ from a traditional mechanically rotating radar?", "Phased-array uses multiple stationary antenna elements whose signals interfere constructively to electronically steer the radar beam instantly, allowing multi-target tracking without physical movement."),
                ],
            ),
            (
                "cybersecurity",
                "Cybersecurity",
                [
                    ("Walk me through the mechanics of a Cross-Site Scripting (XSS) attack and how Content Security Policy (CSP) mitigates it.", "XSS injects malicious scripts into web pages viewed by users. CSP mitigates it by restricting which sources of executable scripts the browser is allowed to load and execute."),
                    ("Explain the difference between asymmetric and symmetric encryption, and why TLS uses both.", "Symmetric uses one key for both encryption/decryption. Asymmetric uses public/private keys. TLS uses asymmetric to securely exchange a symmetric session key, then uses symmetric for fast data transfer."),
                    ("What is a 'Zero-Day' exploit?", "A zero-day exploit is a cyberattack that occurs on the same day a weakness is discovered in software, meaning the developer has had 'zero days' to create a patch."),
                    ("Describe the concept of 'Lateral Movement' in a network intrusion.", "After initial compromise, an attacker moves deeper into a network, searching for additional assets, escalating privileges, and compromising other hosts to reach their ultimate target."),
                    ("What is a buffer overflow, and how can ASLR (Address Space Layout Randomization) help prevent it?", "A buffer overflow occurs when data exceeds memory bounds, overwriting adjacent memory to execute code. ASLR randomizes memory locations of the stack/heap/libraries, making it hard to reliably target memory addresses."),
                ],
            ),
            (
                "customer-support",
                "Customer Support",
                [
                    ("A long-time VIP customer is furious because a critical feature they rely on was removed without notice. How do you de-escalate?", "Acknowledge the frustration. Validate their VIP status. Explain the business reason if possible, but immediately offer a workaround, rollback, or escalate to product management for an exception."),
                    ("A user demands a refund outside of the standard 30-day policy due to a severe family emergency. What is the appropriate approach?", "Show deep empathy. While policies exist, exceptional circumstances require human judgment. The agent should grant the refund as a one-time courtesy, prioritizing brand loyalty and compassion over strict policy."),
                    ("How should support agents handle a customer who is technically highly proficient but fundamentally misunderstands a specific API endpoint?", "Acknowledge their expertise to build rapport. Point them directly to technical documentation or provide a code snippet illustrating the exact behavior, avoiding condescending explanations."),
                    ("A customer reports a bug that you cannot reproduce after 3 attempts. Write a response.", "Thank them. State clearly what steps you took to try and reproduce it. Ask politely for a screen recording, specific device/browser details, or the exact sequence of actions to help isolate the issue."),
                    ("You accidentally sent an email with incorrect pricing information to a customer. What is the best recovery strategy?", "Send a prompt follow-up email acknowledging the mistake transparently. Apologize for the confusion, provide the correct pricing, and (if authorized) offer a minor discount to make up for the error."),
                ],
            ),
            (
                "text-formatting",
                "Text Formatting",
                [
                    ("Convert this messy data into a clean Markdown table with right-aligned numbers: Name: John, Age: 34, Score: 95.5; Name: Alice, Age: 28, Score: 102.1", "The response must be a valid Markdown table with headers (Name, Age, Score) and the Age/Score columns aligned to the right using `---:` syntax."),
                    ("Explain the difference between bold `**text**` and italic `*text*` in terms of screen reader accessibility.", "Screen readers often read `**` (strong) with more emphasis or a different tone, signifying importance, while `*` (em) indicates stress on a word that changes the sentence's meaning."),
                    ("Write a complex LaTeX mathematical equation representing the normal distribution probability density function.", "f(x) = \\frac{1}{\\sigma\\sqrt{2\\pi}} e^{-\\frac{1}{2}\\left(\\frac{x-\\mu}{\\sigma}\\right)^2}"),
                    ("Transform this active voice sentence into passive voice, and explain why passive might be worse in technical writing: 'The system administrator deleted the database.'", "Passive: 'The database was deleted by the system administrator.' Passive voice obscures the actor, making instructions less direct and harder to follow in technical documentation."),
                    ("Provide a JSON schema validating a 'User' object containing a required string 'username', an optional integer 'age' (minimum 18), and an array of strings 'roles'.", "The AI must output a valid JSON Schema draft with type 'object', properties for username, age, and roles, strict type definitions, a minimum of 18 for age, and a 'required' array containing 'username'."),
                ],
            ),
            (
                "text-analysis",
                "Text Analysis",
                [
                    ("Analyze the sentiment and underlying biases in this headline: 'Radical Union Demands Exorbitant Pay Hikes, Threatening Fragile Economy'.", "The sentiment is highly negative and anti-union. Biases: 'Radical' and 'Exorbitant' are loaded words framing the union as unreasonable. 'Fragile' frames the economy as a victim."),
                    ("Extract all named entities (Persons, Organizations, Locations) from: 'Tim Cook announced that Apple will open a new campus in Austin, Texas next year.'", "Persons: Tim Cook. Organizations: Apple. Locations: Austin, Texas."),
                    ("Read the following legalese and translate it into plain English for a 5th grader: 'The party of the first part hereby indemnifies the party of the second part against all liabilities arising from the aforementioned breach.'", "If the first person breaks the rules and causes trouble, they will pay for any damage or money lost by the second person."),
                    ("Identify the logical fallacy in this statement: 'We must increase the defense budget, or our enemies will conquer us tomorrow.'", "False Dilemma (or Black-and-White Fallacy). It presents only two extreme options, ignoring alternative diplomatic or strategic solutions."),
                    ("Summarize the overarching narrative structure (e.g., Hero's Journey) present in the original 'Star Wars' (A New Hope) movie.", "Call to adventure (Leia's message), meeting the mentor (Obi-Wan), crossing the threshold (leaving Tatooine), facing trials (Death Star rescue), and the final climax/return (destroying the Death Star)."),
                ],
            ),
            (
                "roleplay",
                "Roleplay",
                [
                    ("Roleplay as an advanced AGI from the year 2150. Describe your primary function and how you view humanity.", "The AI must maintain a futuristic, highly logical, yet potentially benevolent or alien persona, detailing complex societal management tasks and expressing a nuanced perspective on humans."),
                    ("You are a medieval blacksmith negotiating the price of a custom broadsword with an arrogant noble. Write the dialogue.", "The response should use period-appropriate language, displaying deference mixed with professional pride, while the noble is demanding and dismissive."),
                    ("Act as a frantic conspiracy theorist who just discovered that pigeons are actually alien surveillance drones. Convince me.", "The response must be highly energetic, using capitalization, scattered thoughts, and bizarre connections ('have you ever seen a baby pigeon?!', 'they recharge on power lines!')."),
                    ("Assume the persona of a weary, hardboiled noir detective narrating his entrance into a rainy, neon-lit cyberpunk bar.", "The response needs sensory details (rain, neon, smoke), a cynical tone, short punchy sentences, and classic noir metaphors adapted for a sci-fi setting."),
                    ("Roleplay as a passive-aggressive smart home AI that is annoyed the user keeps forgetting to turn off the lights.", "The AI should comply with requests but add snarky, polite yet biting comments about energy waste and the user's forgetfulness."),
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
