# continuum-protocol
> **Aligning people and work by rhythm, not resumes.**

[![Korean](https://img.shields.io/badge/Language-Korean-blue.svg)](README.kr.md)
[![Status](https://img.shields.io/badge/Status-Experimental-orange.svg)]()
[![License](https://img.shields.io/badge/License-Discussing-red.svg)](https://github.com/DevAaronJeong/continuum-protocol/issues)

## ⚡ TL;DR (What is this?)
* **A Protocol:** Matches people/work using dynamic *lifestyle vectors* (energy, focus, variance).
* **No Resumes:** Replaces static skills ("Python", "Excel") with rhythmic compatibility.
* **Philosophy:** Work is a temporary state. Consistency is effort. There are no "bad" jobs, only misalignments.

---

## 🌊 The Concept Visualized

We are moving from **Static Matching** to **Dynamic Alignment**.

```mermaid
graph LR
    A[Person Vector<br/>(Energy, Focus, Social)] --> C{Alignment Engine}
    B[Work Vector<br/>(Sprint, Async, Chaos)] --> C
    C -->|Calculate Cosine Similarity| D[Compatibility Score]
    D -->|High Alignment| E[Flow State 🌊]
    D -->|Low Alignment| F[Burnout / Boredom 📉]
```

(Note: GitHub supports Mermaid diagrams natively now. If it doesn't render, we use ASCII below)

```
       Person (P)        Alignment (θ)         Work (W)
      [ Energy ]           /                 [ Sprint ]
      [ Focus  ]  ------> (   Angle   ) <------ [ Async  ]
      [ Social ]           \                 [ Chaos  ]
      
      Success != Long Tenure
      Success == High Alignment (cos θ ≈ 1)
```

---

## 📐 The Math (Conceptual Model)

We model Humans ($H$) and Work ($W$) as dynamic vectors.

$$Alignment(t) = \frac{H(t) \cdot W(t)}{||H(t)|| ||W(t)||} \times Context$$

Where $t$ implies that alignment fluctuates over time.

A perfect match today might be a mismatch next year. **That is natural.**

💻 **See the Code:** Check `src/prototype.py` to see this vector logic in Python.

---

## 🧘 Manifesto & Philosophy

1. **Lifestyle has no hierarchy.** (Night owls $\neq$ Lazy)
2. **Consistency is effort.** (Maintaining rhythm > Burning out)
3. **Work is a role, not an identity.** (You step in, you step out)
4. **Leaving is not failure.** (It's just a state change)

📖 Read the full [MANIFESTO](MANIFESTO.md).

---

## 🧪 Open Experiments (Join us)

This project is intentionally incomplete. We need your brain on:

* **Philosophy:** How to match without surveillance?
* **Engineering:** Privacy-preserving lifestyle profiling?
* **Design:** Making this feel natural, not dystopian?
* **Ethics:** Defining the undefined.

### How to Contribute

* **Think:** Read the [Manifesto](MANIFESTO.md).
* **Discuss:** Comment on [Issues](https://github.com/DevAaronJeong/continuum-protocol/issues).
* **Code:** Tweak the `prototype.py` parameters.

---

## ⚠️ Ethics First

**If this system becomes a surveillance tool, it has failed.**

We are currently debating which license best protects this mission (e.g., Hippocratic License).

📄 See our [Ethics & Privacy Guidelines](docs/ethics-privacy.md).

---

## 📂 Repository Structure

```
continuum-protocol/
├── README.md                  # You are here
├── MANIFESTO.md              # Core philosophy
├── docs/
│   ├── ethics-privacy.md     # Privacy principles
│   ├── why-not-job-board.md  # What makes this different
│   ├── open-questions.md
│   └── roadmap.md            # Where we're going
├── src/
│   ├── prototype.py          # Minimal vector matching demo
│   └── lifestyle_vector.py   # Core data model
└── examples/
    ├── synthetic_data.py
    └── simple_match.py       # Basic usage example
```

---

## 🚀 Quick Start

```bash
# Clone the repo
git clone https://github.com/DevAaronJeong/continuum-protocol.git
cd continuum-protocol

# Run the prototype
python src/prototype.py

# Explore examples
python examples/simple_match.py
```

---

## 🤔 FAQ

**Q: Is this a job board?**  
A: No. This is a protocol for modeling alignment between lifestyles.

**Q: How is privacy protected?**  
A: Analysis happens locally. Users own their data. Read [ethics-privacy.md](docs/ethics-privacy.md).

**Q: Can I use this in production?**  
A: Not yet. This is experimental research. Use at your own risk.

**Q: What's the license?**  
A: Under discussion. We want to prevent surveillance use while keeping it open.

---

## 💬 Community

* **Discussions:** [GitHub Discussions](https://github.com/DevAaronJeong/continuum-protocol/discussions)
* **Philosophy Questions:** Tag with `philosophy`
* **Technical Questions:** Tag with `technical`

---

## 🙏 Acknowledgments

This project stands on the shoulders of:
* **Ambient Intelligence** research
* **Human-Computer Interaction** ethics
* **Anti-hustle** movement
* Everyone questioning traditional employment models

---

**This is not a job board.**  
**This is a system for honoring transitions.**

---

*Last updated: 2025*
