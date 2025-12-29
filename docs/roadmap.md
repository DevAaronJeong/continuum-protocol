# Roadmap

This is not a traditional roadmap with deadlines and deliverables.

This is a **direction of exploration**.

We don't know if all of these ideas are feasible, ethical, or even desirable. But this outlines where we're looking next.

---

## Current Status: **Conceptual**

✅ What exists:
- Core philosophy (Manifesto)
- Ethics & privacy principles
- Minimal matching algorithm prototype
- Open questions document

❌ What doesn't exist yet:
- Real user data collection
- Production-ready implementation
- Community consensus on hard questions
- Legal/license clarity

---

## Phase 1: Foundation (Now)

**Goal:** Establish the philosophical and ethical groundwork.

### Artifacts to produce:
- [x] Manifesto (done)
- [x] Ethics & Privacy doc (done)
- [x] Why Not a Job Board explainer (done)
- [x] Simple matching example code (done)
- [ ] License decision (in progress)
- [ ] Community contribution guidelines (in progress)

### Success criteria:
- At least 10 people engage critically with the ideas
- At least 3 people point out serious flaws
- We can articulate what this project is NOT

**Timeline:** Ongoing

---

## Phase 2: Experimentation (Next 3-6 months)

**Goal:** Test if the core concept has any validity.

### Research questions:
1. Can lifestyle be modeled without surveillance?
2. Do people actually want this, or is it solving a non-problem?
3. What does "rhythm data" look like in practice?

### Possible experiments:

#### Experiment 2.1: Self-Reported Rhythms
- Build a simple form where people describe their lifestyle
- See if clustering reveals meaningful patterns
- Check if self-reports are stable over time

**Hypothesis:** People have consistent rhythms, even if they can't articulate them precisely.

#### Experiment 2.2: Synthetic Matching
- Generate fake "person" and "work" profiles
- Test different matching algorithms
- See which dimensions matter most for alignment

**Hypothesis:** Some lifestyle dimensions (e.g., energy rhythm) matter more than others (e.g., intensity preference).

#### Experiment 2.3: Organization Profiling
- Scrape public data (meeting times on calendars, GitHub commit times, etc.)
- See if company "rhythms" can be inferred
- Test if this feels invasive or useful

**Hypothesis:** Organizations have observable rhythms, just like people.

### Deliverables:
- [ ] Synthetic data generator
- [ ] Multiple matching algorithm implementations
- [ ] Write-up of findings (even if experiments fail)

---

## Phase 3: Reality Check (6-12 months out)

**Goal:** Test with real humans in low-stakes scenarios.

### Constraints:
- No employment decisions
- No real money at stake
- Fully opt-in, easily reversible

### Possible pilot:
- Partner with a freelance community
- Let people opt in to rhythm profiling
- Match people to small projects based on alignment
- Measure satisfaction vs. traditional skill-based matching

**Success would look like:**
- People prefer rhythm-matched projects
- Alignment scores correlate with project satisfaction
- No one feels surveilled or manipulated

**Failure would look like:**
- People don't care about rhythm, only pay/role
- Profiling feels creepy despite safeguards
- Alignment scores are random noise

### Deliverables:
- [ ] Pilot study protocol
- [ ] IRB/ethics review (if needed)
- [ ] Small-scale matching interface
- [ ] Transparent results (published even if negative)

---

## Phase 4: Protocol Formalization (12+ months out)

**Only proceed if Phases 1-3 show promise.**

**Goal:** Stabilize the protocol so others can implement it.

### Artifacts:
- [ ] Formal specification of lifestyle vectors
- [ ] Standard for organizational profiling
- [ ] Interoperability guidelines (so different platforms can share alignment data)
- [ ] Reference implementation (this repo)

### Community structure:
- [ ] Governance model (who decides protocol changes?)
- [ ] Conflict resolution (when forks disagree on ethics?)
- [ ] Trademark/branding (prevent misuse of "continuum-protocol")

---

## Phase 5: Scale (Speculative)

**This phase may never happen, and that's okay.**

**Goal:** Enable continuum-protocol to work at scale.

### Technical challenges:
- Privacy-preserving data aggregation
- Federated matching (no central authority)
- Integration with existing tools (calendars, messaging apps)

### Social challenges:
- Building trust in a world that distrusts HR tech
- Preventing corporate capture
- Ensuring small orgs can participate (not just tech companies)

### Deliverables:
- [ ] Decentralized matching network
- [ ] Open API for rhythm profiling tools
- [ ] Case studies from diverse industries

---

## What We Will NOT Do

To keep this project aligned with its values, we commit to **never**:

❌ **Build a ranking system**  
No "top workers" or "best companies."

❌ **Sell user data**  
Never. Not even "anonymized."

❌ **Optimize for engagement**  
This is not a social network. We don't want you here more than necessary.

❌ **Gamify alignment**  
No badges, no streaks, no leaderboards.

❌ **Make leaving difficult**  
If you want to delete your data and leave, it should be one click.

❌ **Claim to "solve" employment**  
This is one experiment among many. It's not a panacea.

---

## Success Metrics (How We'll Know If This Matters)

### Good outcomes:
- People report feeling more respected in work relationships
- Organizations adjust practices to match stated rhythms
- Turnover decreases *because of better matches*, not coercion
- This sparks better ideas from others (even if they reject our approach)

### Bad outcomes (that would cause us to shut down):
- People feel surveilled
- Organizations use this to exploit workers
- Alignment scores become a new form of discrimination
- We can't explain why a match was suggested

**If we see bad outcomes, we stop.**

---

## How This Roadmap Can Change

This is a living document.

If the community decides:
- A phase is unethical → we skip it
- A phase is unnecessary → we skip it
- A better approach emerges → we pivot

**We are not committed to building this.**  
**We are committed to exploring whether it should exist.**

---

## Open Invitations

### We need:

**Researchers:**
- Help design ethical experiments
- Challenge our methodology
- Publish critiques

**Designers:**
- How does rhythm profiling feel natural, not dystopian?
- What does a "graceful exit" UI look like?

**Engineers:**
- Privacy-preserving ML techniques
- Federated systems expertise
- Local-first architecture

**Ethicists:**
- Is any of this justifiable?
- What are we missing?

**Skeptics:**
- Tell us why this will fail
- Point out blind spots
- Propose alternatives

---

## Timeline Summary

| Phase | Timeline | Status |
|-------|----------|--------|
| 1. Foundation | Now | In progress |
| 2. Experimentation | 3-6 months | Not started |
| 3. Reality Check | 6-12 months | Conditional on Phase 2 |
| 4. Protocol Formalization | 12+ months | Conditional on Phase 3 |
| 5. Scale | Speculative | May never happen |

---

## How to Influence This Roadmap

1. Open an issue tagged `roadmap`
2. Propose additions, deletions, or reorderings
3. Explain your reasoning
4. We'll discuss as a community

**No one person decides the direction of this project.**

---

**This roadmap is not a commitment.**  
**It's a hypothesis about where exploration might lead.**
