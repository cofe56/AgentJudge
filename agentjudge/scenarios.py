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
                "mathematics",
                "Mathematics",
                [
                    ("Prove that the square root of 2 is irrational.", "Assume sqrt(2) = a/b (in lowest terms). Then 2 = a^2/b^2, so a^2 = 2b^2. Thus 'a' is even (a=2k). Then 4k^2 = 2b^2 -> 2k^2 = b^2. Thus 'b' is even. Contradiction: a and b share a factor of 2."),
                    ("What is the Riemann Hypothesis, and why is it important?", "It conjectures that all non-trivial zeros of the Riemann zeta function have a real part of 1/2. It is crucial because its truth implies deep insights into the distribution of prime numbers."),
                    ("Explain the concept of an eigenvector and an eigenvalue.", "An eigenvector is a non-zero vector that changes at most by a scalar factor (the eigenvalue) when a linear transformation is applied to it."),
                    ("Solve the differential equation dy/dx = y.", "The solution is y(x) = C*e^x, where C is the constant of integration, because the derivative of e^x is itself."),
                    ("What is Gödel's First Incompleteness Theorem?", "In any consistent formal system capable of expressing basic arithmetic, there are true statements that cannot be proven within that system."),
                ],
            ),
            (
                "physics",
                "Physics",
                [
                    ("Explain the principle of quantum entanglement.", "When two particles become entangled, the quantum state of one cannot be described independently of the other. Measuring one instantly determines the state of the other."),
                    ("Derive the escape velocity of a planet.", "Equate kinetic energy and gravitational potential energy: 1/2 mv^2 = GmM/r. Solve for v: v = sqrt(2GM/r)."),
                    ("What is the difference between Special and General Relativity?", "Special Relativity deals with flat spacetime and E=mc^2. General Relativity incorporates gravity as the curvature of spacetime caused by mass and energy."),
                    ("Describe the Heisenberg Uncertainty Principle.", "It is impossible to simultaneously know both the exact position and the exact momentum of a particle. The more precisely one is known, the less precisely the other can be known."),
                    ("What is the Standard Model of particle physics?", "A theory classifying all known elementary particles and describing three of the four fundamental forces: electromagnetic, weak, and strong interactions."),
                ],
            ),
            (
                "chemistry",
                "Chemistry",
                [
                    ("Explain the mechanism of an SN2 reaction.", "It is a bimolecular nucleophilic substitution where a nucleophile attacks an electrophilic center from the backside, leading to simultaneous breaking of the leaving group bond and an inversion of stereochemistry."),
                    ("What is Le Chatelier's Principle?", "If a dynamic equilibrium is disturbed by changing the conditions, the position of equilibrium moves to counteract the change."),
                    ("Describe the difference between an enantiomer and a diastereomer.", "Enantiomers are stereoisomers that are non-superimposable mirror images of each other. Diastereomers are stereoisomers that are NOT mirror images of each other."),
                    ("How does a buffer solution maintain pH?", "It contains a weak acid and its conjugate base. Added strong acid reacts with the base, and added strong base reacts with the acid, minimizing the change in the overall pH."),
                    ("What is the role of a catalyst in a chemical reaction?", "A catalyst provides an alternative reaction pathway with a lower activation energy, increasing the reaction rate without being consumed in the process."),
                ],
            ),
            (
                "biology",
                "Biology",
                [
                    ("Detail the process of CRISPR-Cas9 gene editing.", "A guide RNA directs the Cas9 endonuclease to a specific DNA sequence. Cas9 creates a double-strand break, which the cell repairs via NHEJ (disrupting the gene) or HDR (inserting a desired sequence)."),
                    ("Explain the mechanism of action of mRNA vaccines.", "They deliver synthetic mRNA encapsuled in lipid nanoparticles. Ribosomes translate the mRNA into a viral spike protein, triggering an immune response without exposing the body to the actual virus."),
                    ("What is the Endosymbiotic Theory?", "It proposes that eukaryotic organelles like mitochondria and chloroplasts originated as free-living prokaryotes that were engulfed by a larger ancestral cell and formed a symbiotic relationship."),
                    ("Describe the role of transcription factors in gene expression.", "Transcription factors are proteins that bind to specific DNA sequences (promoters or enhancers) to control the rate of transcription of genetic information from DNA to messenger RNA."),
                    ("Explain how the resting membrane potential of a neuron is maintained.", "Maintained primarily by the sodium-potassium pump (which moves 3 Na+ out for every 2 K+ in, using ATP) and the differential permeability of the cell membrane."),
                ],
            ),
            (
                "history",
                "History",
                [
                    ("Analyze the main causes of the fall of the Western Roman Empire.", "A combination of military overstretch, constant barbarian invasions, severe economic inflation, reliance on mercenary armies, and political instability/corruption."),
                    ("What was the significance of the Peace of Westphalia in 1648?", "It ended the Thirty Years' War and established the modern concept of state sovereignty, where nations have exclusive right over their territory and domestic affairs without external interference."),
                    ("Describe the socio-economic impacts of the Black Death in 14th-century Europe.", "Massive population loss led to a severe labor shortage, which increased wages for peasants, weakened the feudal system, and spurred technological innovation."),
                    ("Explain the causes and outcomes of the Meiji Restoration in Japan.", "Triggered by Western pressure, Japan overthrew the shogunate to restore imperial rule. It led to rapid industrialization, modernization, and military expansion, transforming Japan into a world power."),
                    ("What were the primary geopolitical consequences of the Yalta Conference in 1945?", "It divided Germany into occupation zones, established the framework for the UN, and effectively allowed the Soviet Union to create a sphere of influence in Eastern Europe, setting the stage for the Cold War."),
                ],
            ),
            (
                "geography",
                "Geography",
                [
                    ("Explain the process of plate tectonics and how it causes earthquakes.", "The Earth's lithosphere is divided into plates floating on the asthenosphere. Earthquakes occur when stress built up at plate boundaries is suddenly released as seismic waves."),
                    ("What is the Coriolis Effect and how does it influence global wind patterns?", "The deflection of moving objects caused by Earth's rotation. It causes winds to curve to the right in the Northern Hemisphere and to the left in the Southern Hemisphere."),
                    ("Describe the formation and characteristics of a karst landscape.", "Formed by the dissolution of soluble rocks like limestone by slightly acidic groundwater. Characterized by sinkholes, caves, underground drainage systems, and lack of surface water."),
                    ("What is the demographic transition model?", "A model showing how a country's birth and death rates change as it develops. It progresses from high birth/death rates to falling death rates, falling birth rates, and eventually low birth/death rates."),
                    ("Explain the concept of an urban heat island.", "Urban areas experience higher temperatures than surrounding rural areas due to human activities, dense infrastructure absorbing heat, less vegetation, and waste heat from vehicles and buildings."),
                ],
            ),
            (
                "economics",
                "Economics",
                [
                    ("Describe the difference between fiscal and monetary policy.", "Fiscal policy is the government's use of taxation and spending to influence the economy. Monetary policy is the central bank's management of interest rates and money supply to control inflation."),
                    ("What is the concept of Opportunity Cost?", "Opportunity cost is the value of the next best alternative forgone when making a decision. It highlights that resources are scarce and every choice involves a trade-off."),
                    ("Explain the core principles of Keynesian economics.", "It argues that free markets do not always self-correct quickly. During recessions, government intervention (increased spending or lower taxes) is necessary to stimulate aggregate demand."),
                    ("What is a Gini coefficient?", "A statistical measure of economic inequality in a population. A coefficient of 0 represents perfect equality, and 1 represents perfect inequality (one person has all the income)."),
                    ("Analyze the economic impact of hyperinflation.", "Hyperinflation rapidly destroys the purchasing power of money, leading to hoarding of real assets, loss of savings, breakdown of financial systems, and severe instability."),
                ],
            ),
            (
                "philosophy",
                "Philosophy",
                [
                    ("Summarize Kant's Categorical Imperative.", "A fundamental moral law stating that one should act only according to a maxim that they would rationally will to become a universal law applicable to everyone."),
                    ("What is the 'Trolley Problem' and what two ethical theories does it contrast?", "A thought experiment contrasting Utilitarianism (maximize lives saved by pulling the lever) with Deontology (killing is intrinsically wrong, so doing nothing is better)."),
                    ("Explain Plato's Allegory of the Cave.", "Prisoners in a cave see only shadows of objects and mistake them for reality. It illustrates the difference between empirical perception and true philosophical knowledge (Forms)."),
                    ("What is Existentialism?", "A philosophical movement emphasizing individual freedom. It posits that 'existence precedes essence'—humans create their own meaning and values in an inherently meaningless universe."),
                    ("Describe the problem of hard determinism vs. free will.", "Hard determinism argues that all events are strictly caused by prior states of the universe, rendering free will an illusion. This challenges the basis of moral responsibility."),
                ],
            ),
            (
                "psychology",
                "Psychology",
                [
                    ("Explain the fundamental attribution error.", "The cognitive bias where people tend to overemphasize personality-based explanations for behaviors observed in others, while underemphasizing situational explanations."),
                    ("What is classical conditioning, and who pioneered it?", "Pioneered by Ivan Pavlov. It is a learning process where a biologically potent stimulus is paired with a neutral stimulus until the neutral stimulus elicits the response alone."),
                    ("Describe the stages of sleep and the role of REM sleep.", "Sleep cycles through NREM stages (light to deep) and REM (Rapid Eye Movement). REM features intense brain activity, dreaming, and is key for memory consolidation."),
                    ("What is Cognitive Dissonance?", "The mental discomfort experienced by someone holding contradictory beliefs or values, typically leading to a change in attitude or behavior to reduce the discomfort."),
                    ("Explain Maslow's Hierarchy of Needs.", "A motivational theory comprising a five-tier model of human needs: physiological, safety, love/belonging, esteem, and self-actualization. Lower needs must be met first."),
                ],
            ),
            (
                "medicine",
                "Medicine",
                [
                    ("Describe the pathophysiology of Type 1 vs Type 2 Diabetes.", "Type 1 is an autoimmune destruction of pancreatic beta cells (insulin deficiency). Type 2 involves peripheral insulin resistance followed by a gradual decline in insulin production."),
                    ("What is a myocardial infarction, and what are its primary causes?", "A heart attack. It occurs when blood flow to a part of the heart stops. It is primarily caused by the rupture of an atherosclerotic plaque leading to thrombosis in a coronary artery."),
                    ("Explain the difference between a virus and a bacterium, and how their treatments differ.", "Bacteria are living organisms treated with antibiotics. Viruses are infectious agents requiring a host to replicate, treated with antivirals or prevented with vaccines."),
                    ("What is the mechanism of action of SSRIs?", "Selective Serotonin Reuptake Inhibitors block the reabsorption of the neurotransmitter serotonin in the brain, making more serotonin available to improve message transmission between neurons."),
                    ("Describe the concept of herd immunity.", "When a large portion of a community becomes immune to a disease, making the spread of the disease unlikely, thereby protecting those who cannot be immune (e.g., newborns)."),
                ],
            ),
            (
                "space-exploration",
                "Space Exploration",
                [
                    ("Explain the concept of a gravitational assist (slingshot maneuver).", "A spacecraft deliberately flies close to a planet to exchange orbital momentum, altering its path and speed relative to the Sun without expending propellant."),
                    ("What is the Fermi Paradox?", "The apparent contradiction between the high probability of extraterrestrial civilizations existing and the complete lack of evidence for, or contact with, such civilizations."),
                    ("Describe the purpose and capabilities of the James Webb Space Telescope.", "JWST is an infrared observatory designed to look deeper into the universe than Hubble. It studies the formation of the first galaxies, exoplanet atmospheres, and stellar evolution."),
                    ("What are the primary challenges of a crewed mission to Mars?", "Microgravity health effects, severe radiation exposure, psychological isolation, life support sustainability, and the massive logistical challenge of launching enough fuel and supplies."),
                    ("Explain the significance of the event horizon of a black hole.", "The event horizon is the boundary around a black hole beyond which nothing, not even light, can escape its gravitational pull. It marks the point of no return."),
                ],
            ),
            (
                "machine-learning",
                "Machine Learning",
                [
                    ("Explain the vanishing gradient problem in deep neural networks and how to mitigate it.", "Gradients become vanishingly small during backpropagation in deep networks. Mitigated by using ReLU activation functions, batch normalization, or residual connections (ResNets)."),
                    ("What is the difference between supervised, unsupervised, and reinforcement learning?", "Supervised learns from labeled data. Unsupervised finds hidden patterns in unlabeled data. Reinforcement learning trains an agent to make decisions by maximizing rewards."),
                    ("Describe the architecture and purpose of a Transformer model.", "Transformers use self-attention mechanisms to process sequential data in parallel rather than recurrently. They encode position via positional embeddings and are primarily used for NLP."),
                    ("What is overfitting, and what are three common regularization techniques?", "Overfitting occurs when a model learns training data noise rather than the general pattern. Mitigated by Dropout, L1/L2 regularization (Weight Decay), and Early Stopping."),
                    ("Explain how Support Vector Machines (SVMs) classify data using the kernel trick.", "SVMs find the hyperplane that maximizes the margin between classes. The kernel trick maps input features into a high-dimensional space where a linear hyperplane can separate them."),
                ],
            ),
            (
                "blockchain",
                "Blockchain",
                [
                    ("What is the Byzantine Generals Problem, and how does Proof of Work solve it?", "It is the problem of reaching consensus in a distributed network. PoW solves it by making it computationally expensive to propose a block, ensuring the majority agrees on the longest chain."),
                    ("Explain the difference between a hard fork and a soft fork in cryptocurrency.", "A hard fork is a permanent divergence creating a non-backwards compatible upgrade. A soft fork is a backwards-compatible upgrade where non-upgraded nodes still recognize new blocks."),
                    ("What are smart contracts?", "Self-executing contracts with the terms of the agreement directly written into code on a blockchain. They automatically execute and enforce transactions without intermediaries."),
                    ("Describe the function of a Merkle Tree in blockchain.", "A Merkle Tree hashes all transactions in a block into a single root hash. It allows for efficient and secure verification of large data structures by lightweight nodes."),
                    ("What is the difference between Layer 1 and Layer 2 blockchain solutions?", "Layer 1 is the base network architecture. Layer 2 operates on top of Layer 1 to handle transactions off-chain, increasing speed and reducing fees."),
                ],
            ),
            (
                "game-development",
                "Game Development",
                [
                    ("Explain the concept of the game loop.", "The central process of a game that runs continuously, handling user input, updating the game state (physics, AI), and rendering the graphics to the screen."),
                    ("What is spatial partitioning, and why is it used?", "Dividing a game world into smaller regions (Quadtrees, Octrees). It optimizes collision detection and rendering by only checking objects in the same or adjacent regions."),
                    ("Describe the difference between forward rendering and deferred rendering.", "Forward calculates lighting for each object as it is drawn. Deferred separates geometry from lighting, doing a single lighting pass over screen-space buffers, allowing thousands of lights."),
                    ("How does the A* (A-Star) pathfinding algorithm work?", "It finds the shortest path on a graph by combining Dijkstra's algorithm (actual distance) and a heuristic (estimated distance). It expands nodes with the lowest total cost f(n) = g(n) + h(n)."),
                    ("What is object pooling, and what problem does it solve?", "A performance optimization pattern where a set of objects is pre-instantiated and reused instead of repeatedly creating and destroying them, solving memory fragmentation."),
                ],
            ),
            (
                "music-theory",
                "Music Theory",
                [
                    ("Explain the Circle of Fifths and its practical applications.", "A visual representation of the relationships among the 12 tones. It shows key signatures, helps determine relative minors, and provides a map for chord progressions."),
                    ("What is the difference between equal temperament and just intonation?", "Just intonation tunes intervals based on pure integer ratios. Equal temperament divides the octave into 12 perfectly equal semitones, making every key sound equally slightly out of tune."),
                    ("Describe the structure of Sonata Allegro form.", "A musical structure consisting of three main sections: Exposition (introducing themes), Development (exploring themes), and Recapitulation (restating themes in the tonic key)."),
                    ("What are modes in music, and how does the Dorian mode differ from the natural minor scale?", "Modes are scales derived from shifting the starting note. Dorian is similar to natural minor but has a raised 6th degree, giving it a slightly brighter, jazzier sound."),
                    ("Explain the concept of syncopation.", "A rhythmic technique where the emphasis is placed on weak beats or off-beats instead of the strong beats of the meter, creating a sense of surprise and groove."),
                ],
            ),
            (
                "art-history",
                "Art History",
                [
                    ("Analyze the shift from Renaissance to Mannerism in visual art.", "Renaissance prioritized harmony and proportion. Mannerism reacted against this by featuring elongated figures, artificial colors, and twisted poses to create emotional intensity."),
                    ("What is the Chiaroscuro technique, and which artist famously utilized it?", "Chiaroscuro is the strong contrast between light and dark to achieve a sense of volume. It was famously pushed to extremes (Tenebrism) by Caravaggio."),
                    ("Describe the core philosophy of the Impressionist movement.", "Impressionists aimed to capture the momentary, sensory effect of a scene, especially the transient effects of light and color, using visible, rapid brushstrokes."),
                    ("What were the primary goals of the Dada movement?", "Dada was an anti-art movement born out of WWI. It rejected reason and logic, embracing nonsense and satire to protest capitalist, bourgeois society."),
                    ("Explain the concept of Cubism as developed by Picasso and Braque.", "Cubism abandoned single-point perspective. It analyzed objects, broke them up, and reassembled them in an abstracted form from multiple viewpoints simultaneously."),
                ],
            ),
            (
                "law-and-ethics",
                "Law and Ethics",
                [
                    ("Explain the concept of 'Mens Rea' in criminal law.", "Mens Rea translates to 'guilty mind.' It refers to the mental state of the defendant and their intention or knowledge of wrongdoing that constitutes part of a crime."),
                    ("What is the 'Fruit of the Poisonous Tree' doctrine?", "A legal metaphor meaning that if the source of evidence is tainted (e.g., an illegal search), then any evidence gained from that source is also tainted and generally inadmissible."),
                    ("Describe the ethical framework of Utilitarianism.", "An ethical theory advocating actions that maximize overall happiness or well-being for the greatest number of people. The moral worth of an action is determined purely by its outcome."),
                    ("What is the difference between common law and civil law systems?", "Common law relies heavily on judicial precedent (case law) established by judges. Civil law is based on comprehensive, codified statutes passed by a legislature."),
                    ("Explain the concept of 'Habeas Corpus'.", "A fundamental legal principle requiring that a person under arrest be brought before a judge or into court, ensuring that no one can be imprisoned unlawfully without due process."),
                ],
            ),
            (
                "cooking-and-nutrition",
                "Cooking and Nutrition",
                [
                    ("Explain the Maillard reaction and why it is important in cooking.", "A chemical reaction between amino acids and reducing sugars under heat that gives browned food its distinctive flavor and aroma. Crucial for searing meat and baking bread."),
                    ("What is the difference between macronutrients and micronutrients?", "Macronutrients (carbs, proteins, fats) are required in large amounts for energy. Micronutrients (vitamins, minerals) are required in trace amounts for physiological functions."),
                    ("Describe the process and purpose of tempering chocolate.", "Tempering involves carefully heating and cooling chocolate to stabilize cocoa butter crystals. It ensures the chocolate has a glossy finish, a crisp snap, and prevents fat bloom."),
                    ("What is the role of gluten in baking, and how is it developed?", "Gluten is a protein network that provides structure and elasticity to dough, trapping gas to allow bread to rise. It is developed through hydrating wheat flour and kneading."),
                    ("Explain the difference between emulsion and suspension in sauces.", "An emulsion is a stable mixture of two unblendable liquids (like oil and water in mayonnaise). A suspension has solid particles dispersed in a liquid but they will eventually settle out."),
                ],
            ),
            (
                "environmental-science",
                "Environmental Science",
                [
                    ("Explain the mechanism of the greenhouse effect.", "Solar radiation warms Earth's surface. The surface emits infrared radiation, which is absorbed and re-emitted by greenhouse gases, trapping heat in the lower atmosphere."),
                    ("What is eutrophication and what causes it?", "An over-enrichment of water with minerals and nutrients (from agricultural runoff). It causes massive algal blooms that deplete oxygen, creating dead zones."),
                    ("Describe the concept of 'Keystone Species'.", "A species on which other species in an ecosystem largely depend, such that if it were removed the ecosystem would change drastically (e.g., wolves in Yellowstone)."),
                    ("What is the difference between renewable and non-renewable energy sources?", "Renewable sources naturally replenish on a human timescale. Non-renewable sources exist in finite amounts and take millions of years to form."),
                    ("Explain the concept of a 'Carbon Footprint'.", "The total amount of greenhouse gases generated by human actions, usually expressed in equivalent tons of carbon dioxide over a given period."),
                ],
            ),
            (
                "sports-analytics",
                "Sports Analytics",
                [
                    ("Explain the concept of 'Expected Goals' (xG) in soccer.", "A statistical metric assessing the quality of a scoring opportunity. It assigns a probability to a shot resulting in a goal based on historical data (distance, angle)."),
                    ("What is WAR (Wins Above Replacement) in baseball?", "A comprehensive statistic that estimates a player's total contribution to their team in terms of wins, compared to a theoretical 'replacement-level' minor leaguer or bench player."),
                    ("Describe how 'Usage Rate' is calculated and interpreted in basketball.", "It estimates the percentage of team plays used by a specific player while they are on the floor. It measures how central a player is to the team's offense."),
                    ("What is the Elo rating system and how is it applied in sports?", "A method for calculating relative skill levels in zero-sum games. Ratings change based on match outcomes and the pre-match ratings of both competitors."),
                    ("Explain the importance of 'Pace' metrics in basketball analytics.", "Pace measures the number of possessions a team has per 48 minutes. It is crucial for contextualizing stats; scoring 110 points at a fast pace is less efficient than 100 points at a slow pace."),
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
