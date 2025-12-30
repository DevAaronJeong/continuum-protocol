# Open Questions

These are questions we don't have answers to yet.

If you have thoughts, critique, or alternative perspectives, please open an issue or discussion.

---

## 1. Modeling & Methodology

### How do we define "lifestyle" without being reductive?

- What dimensions actually matter?
- Are we missing crucial factors?
- Is quantification inherently dehumanizing?

**Current approach:**
- Energy rhythm (morning/evening/distributed)
- Interaction density (solo vs. collaborative)
- Change tolerance (routine vs. variety)
- Intensity preference (low-key vs. high-intensity)

**Concerns:**
- This might be too simplistic
- Cultural differences may not translate
- Neurodivergent patterns might not fit these categories

---

### Can we model "effort" without measuring hours?

We claim consistency is a form of effort, but:
- How do we measure consistency without surveillance?
- Is "maintaining a rhythm" even the right proxy for effort?
- What about people whose lives are inherently unstable (caregivers, etc.)?

**Unresolved:**
- Should effort even be scored?
- Or should we only measure alignment, not "virtue"?

---

### How do we handle temporal change?

People and organizations change over time.
- Morning person → night owl (due to life change)
- Stable company → chaotic pivot
- High-intensity worker → burned out, needs low-key work

**Questions:**
- Do we track drift and proactively suggest re-matching?
- How often should vectors be recalculated?
- What triggers a "you should leave" signal?

---

### Which distance metric best captures "fit"?

**This section explores whether mathematical distance metrics can approximate the human feeling of "this fits my life."**

**Current implementation:** Weighted Manhattan Distance

We chose Manhattan Distance because:
- It respects magnitude differences (0.9 ≠ 0.3)
- Each dimension contributes independently
- Easy to explain ("you differ by 0.6 on this dimension")
- Simple to weight dimensions differently

**But we don't know if this matches human perception of "fit".**

By "fit," we mean **a state where work does not require continuous self-adjustment** — where your natural rhythms can persist without constant adaptation.

**Alternative approaches to consider:**

| Metric | What it measures | Pros | Cons |
|--------|------------------|------|------|
| **Manhattan Distance** (current) | Sum of absolute differences | Interpretable, tunable | May not penalize large mismatches enough |
| **Euclidean Distance** | Geometric straight-line distance | Penalizes large mismatches more heavily | Less interpretable |
| **Cosine Similarity** | Direction/pattern similarity | Good for finding similar patterns | Ignores magnitude (0.9 vs 0.3 treated as "same direction") |
| **Mahalanobis Distance** | Accounts for correlation between dimensions | Statistically sophisticated | Requires correlation data, harder to explain |

**Open questions:**

1. **When someone says "this job feels right," what are they actually sensing?**
   - Is it the absence of friction across many small dimensions?
   - Or the absence of one dealbreaking mismatch?
   - Does "feeling right" emerge immediately, or over time?

2. **Should different dimensions use different metrics?**
   - Energy rhythm: Maybe absolute difference matters (Manhattan)
   - Communication style: Maybe pattern matters more (Cosine)
   - Intensity: Maybe large mismatches should be heavily penalized (Euclidean)

3. **Can we learn the "right" metric from user feedback?**
   - Collect: "How well did this match work out?"
   - Reverse-engineer: "What distance function predicts satisfaction best?"

4. **Are there cultural differences in how "fit" is perceived?**
   - Western individualism vs. Eastern collectivism
   - Different professional cultures (tech vs. academia vs. healthcare)

**Why this matters:**

The choice of distance metric is not just mathematical—it's **philosophical**.
- It defines what we mean by "similar lifestyles"
- It determines which mismatches are tolerable vs. dealbreaking
- It affects whether the system feels accurate or arbitrary to users

**Experiment ideas:**

1. **A/B test different metrics** with synthetic data, ask users which rankings "feel right"
2. **Interview people** about past job matches: "What made it work/not work?"
3. **Collect mismatch stories:** When did a small difference matter a lot? When did a large difference not matter?

**We need your input:**
- Have you experienced a job that "should have" matched but didn't? Or vice versa?
- What factors made the biggest difference in your subjective sense of fit?
- Do you think patterns matter more than magnitudes, or vice versa?

---

### Is there a "best" representation of lifestyle rhythms?

Currently we use vectors with normalized [0, 1] values.

But maybe:
- **Categorical** is more honest? ("morning person" vs. "evening person", not 0.9 vs 0.1)
- **Probabilistic** is more accurate? ("60% chance I prefer mornings, 40% evenings")
- **Time-series** captures reality better? (actual activity logs over weeks)
- **Narrative** descriptions preserve nuance that numbers lose?

**Tension:**
- Numbers enable computation and comparison
- But lived experience is not reducible to numbers

Can we find middle ground?

---

## 2. Ethics & Privacy

### Can lifestyle profiling ever be non-invasive?

Even with good intentions, is this fundamentally creepy?

**Possible approaches:**
- Self-reported rhythms only (no passive tracking)
- Coarse-grained signals (morning/evening, not precise timestamps)
- Federated learning (raw data never leaves user's device)

**Still concerning:**
- Even self-reports can be gamed
- Organizations might pressure users to share data
- "Voluntary" ≠ truly consensual if employment depends on it

---

### How do we prevent misuse?

Scenarios we're worried about:
1. **Employer exploitation:** "Your alignment score dropped, so we're cutting your pay."
2. **Discrimination:** "Evening people are less reliable" (unfounded bias)
3. **Manipulation:** "Work a few more hours to improve your consistency score."

**Mitigation ideas:**
- License restrictions (e.g., Hippocratic License)
- Two-way transparency (companies also profiled)
- Community-driven reputation for organizations

**Still unresolved:**
- Can technical safeguards prevent social pressure?
- Is open-source enough, or do we need legal protections?

---

### Who owns the matching algorithm?

- If we make this open-source, anyone can fork it
- A corporation could take the code and strip out ethics safeguards
- How do we prevent "surveillance-as-a-service" forks?

**Options:**
- Ethical Source licenses (restrict harmful use)
- Copyleft licenses (require derivative works to stay open)
- Trademark the protocol name (prevent misuse of branding)

**Tradeoff:**
- Strong restrictions → less adoption
- Permissive license → easier to misuse

---

## 3. Organizational Evaluation

### How do we profile organizations fairly?

If we measure people's rhythms, we must measure companies too.

**Challenges:**
- Companies will game this (like they game Glassdoor reviews)
- How do we detect "performative flexibility" (claims vs. reality)?
- What if a team's rhythm is healthy but the org's rhythm is toxic?

**Ideas:**
- Measure actual behavior (meeting times, message timestamps)
- Cross-reference employee churn with stated culture
- Use differential privacy to aggregate patterns without identifying individuals

**Unresolved:**
- Is this level of organizational surveillance ethical?
- How do we avoid creating a "corporate credit score"?

---

### What counts as a "bad actor" organization?

We want to flag companies that exploit alignment data, but:
- Who decides what counts as exploitation?
- What if an organization is trying to improve but scores poorly?
- Do startups get penalized for being chaotic by nature?

**Needs community input.**

---

## 4. Matching Mechanics

### What does "continuous matching" actually mean?

We say matching is not a one-time event, but a gradient:
```
weak signal → exploration → sustained work → natural exit
```

**Unclear:**
- What does "exploration" look like in practice?
- How do people get paid during weak-signal phases?
- Is this even compatible with traditional employment contracts?

---

### How do we handle misalignment detection?

If alignment degrades over time, should the system:
- Alert the person? ("This might not be working anymore")
- Alert the organization? ("This person might leave soon")
- Stay silent and let natural processes play out?

**Tension:**
- Proactive alerts = helpful
- Proactive alerts = pressure to stay/leave before you're ready

---

### Can alignment be predicted, or only observed?

We model alignment at time $t$, but:
- Can we predict alignment at $t+6$ months?
- Or is prediction inherently flawed (too many variables)?

**If we can't predict:**
- Continuous re-matching is essential
- But how do organizations plan hiring?

**If we can predict:**
- Risk of reinforcing biases ("night owls don't last long here")

---

## 5. Practical Implementation

### How do we collect rhythm data ethically?

**Options we're considering:**

| Method | Pros | Cons |
|--------|------|------|
| Self-reported surveys | Fully consensual | Inaccurate, effort-intensive |
| Browser/device tracking | Accurate | Invasive, privacy nightmare |
| Federated learning | Data stays local | Complex, hard to audit |
| Calendar/email metadata | Objective behavioral signal | Still feels like surveillance |

**No perfect solution yet.**

---

### What does an MVP actually look like?

We have conceptual code, but:
- Is a matching algorithm enough?
- Do we need a UI?
- Should we partner with existing platforms (e.g., freelance marketplaces)?

**Tension:**
- Too abstract → no one uses it
- Too practical → becomes just another job board

---

### How do we fund this without compromising ethics?

Possible models:
- Grant funding (but from whom? and with what strings attached?)
- Freemium (but what's behind the paywall?)
- Cooperative ownership (users pay in, users own the system)
- Advertising (absolutely not)

**Unresolved.**

---

## 6. Philosophical Foundations

### Is work actually a "state"?

We claim work is a temporary role, not an identity.

**But:**
- Many people derive meaning from their work
- "It's just a state" might feel dismissive
- Is there a middle ground?

**Alternative framing:**
- Work is *one* state among many (parent, friend, learner, etc.)
- Work can be meaningful *while* being temporary

---

### Does this reinforce precarity?

By normalizing short-term alignment, are we:
- Helping people find better fits?
- Or justifying gig-economy exploitation?

**Concern:**
- "Alignment-based work" could become an excuse for no benefits, no stability
- Companies might say "we're just aligning rhythms!" while offering zero job security

**How do we avoid this?**

---

### Can a mathematical model ever respect human complexity?

We're modeling humans as vectors.

**The risk:**
- Reducing people to numbers
- Reinforcing algorithmic bias
- Claiming objectivity where there is none

**Our stance:**
- Models are approximations, not truths
- Humans are not reducible
- But preferences, rhythms, and patterns exist and can be respected

**Still debating:**
- Is any quantification inherently disrespectful?
- Or is refusing to model rhythms itself a form of neglect?

---

## 7. Scope & Boundaries

### What types of work is this even for?

This model probably doesn't work for:
- Emergency services (inherently unpredictable)
- Highly regulated industries (compliance over rhythm)
- Mission-critical infrastructure (24/7 ops)

**This might only work for:**
- Knowledge work
- Creative roles
- Project-based collaboration
- Remote/async-first teams

**Is that okay? Or is this too narrow to matter?**

---

### Do we need an organization to implement this?

Could this just be:
- A protocol / standard / philosophy
- That anyone implements however they want?

Or does it need:
- A central platform
- A governing body
- Enforceable rules

**Unresolved.**

---

## How You Can Help

If any of these questions resonate with you:
1. Open a GitHub issue
2. Tag it with `philosophy`, `ethics`, or `technical` (depending on the question)
3. Propose an answer, or explain why the question itself is flawed

**We need skeptics as much as supporters.**

If you think this entire project is misguided, tell us why.
If you have a better framing, share it.

This is an experiment. Experiments fail.
We'd rather fail transparently than succeed unethically.

---

**These questions are not bugs. They're the project.**
