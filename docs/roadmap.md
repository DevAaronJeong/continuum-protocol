# Roadmap

This is not a traditional roadmap with deadlines and deliverables.

This is a **direction of exploration**.

We don't know if all of these ideas are feasible, ethical, or even desirable. But this outlines where we're looking next.

---

## Current Status: **Conceptual** (updated October 2026)

✅ What exists:
- Core philosophy (Manifesto)
- Ethics & privacy principles
- Minimal matching algorithm prototype
- Open questions document
- Theory of fit as dynamic stability, with a Phase 0 simulation ([fit-as-stability.md](fit-as-stability.md))
- Cosine vs. Manhattan comparison on synthetic data ([metric-analysis.md](metric-analysis.md), from [Issue #4](https://github.com/DevAaronJeong/continuum-protocol/issues/4))
- License: AGPL-3.0 for code, CC BY 4.0 for docs

❌ What doesn't exist yet:
- Real user data collection
- Production-ready implementation
- Community consensus on hard questions

### Status update (October 2026)

**Activity:** Most of the groundwork happened between December 30, 2025 and January 1, 2026. The project then paused for about ten months and resumed in October 2026.

**What we learned since then:**
- **The metric choice matters.** Cosine and Manhattan pick a different top match for about half of synthetic people. Whether Manhattan is the right choice still needs human data.
- **Our Phase 0 stability check has a flaw.** The simulation measures $s_j$ in the order new levels first appear, not over time. In tests it labels steadily rising effort (burnout) as stable and noisy-but-flat effort as unstable. We'll discuss a time-based fix in [Discussion #7](https://github.com/DevAaronJeong/continuum-protocol/discussions/7) before changing it (Experiment 2.4).
- **Engagement is below the Phase 1 target.** One external person has engaged critically so far. The target is 10.

**Next, in order** (no dates; this list gets updated as items finish):
1. ~~Decide a license~~ ✅
2. Fix the stability check (Experiment 2.4)
3. Retrospective fit survey (Experiment 2.5)
4. Weekly adjustment diary pilot (Experiment 2.6)
5. Publish the results, including negative ones

---

## Phase 1: Foundation (Now)

**Goal:** Establish the philosophical and ethical groundwork.

### Artifacts to produce:
- [x] Manifesto (done)
- [x] Ethics & Privacy doc (done)
- [x] Why Not a Job Board explainer (done)
- [x] Simple matching example code (done)
- [x] License decision (AGPL-3.0 for code, CC BY 4.0 for docs)
- [x] Community contribution guidelines (basic version in CONTRIBUTING.md)

### Success criteria:
- At least 10 people engage critically with the ideas
- At least 3 people point out serious flaws
- We can articulate what this project is NOT

**Progress (October 2026):** One external contributor has engaged critically and reframed "fit" as dynamic stability. We're short of the 10-person target.

**Timeline:** Ongoing

---

## Phase 2: Experimentation (Next)

**Status:** Started (October 2026)

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

**Status:** Partly done. [metric-analysis.md](metric-analysis.md) compares five metrics on synthetic profiles.

#### Experiment 2.3: Organization Profiling
- Scrape public data (meeting times on calendars, GitHub commit times, etc.)
- See if company "rhythms" can be inferred
- Test if this feels invasive or useful

**Hypothesis:** Organizations have observable rhythms, just like people.

#### Experiment 2.4: Fix the Stability Check
- Define $K(i)$ as a weekly self-report: "How much did you have to adjust yourself to your work this week?" (0–10)
- Judge stability by the trend of $K$ over time after a settling period, and flag when that trend speeds up
- Turn the Phase 0 failure cases into unit tests
- Discuss with the model's original author in [Discussion #7](https://github.com/DevAaronJeong/continuum-protocol/discussions/7) first

**Hypothesis:** A time-based check separates steady effort from rising effort, which the Phase 0 version could not.

#### Experiment 2.5: Retrospective Fit Survey
- About 100 people through free channels, open November 6–30, 2026; about 10 minutes, anonymous (no names, employers, or contact details)
- Each person describes their own rhythm, their current or most recent job, and optionally a contrasting job on the same dimensions, then rates how well each job fit (1–7)
- Compare which metric's alignment score tracks the fit ratings best
- Write down the hypothesis and decision rule before collecting any data
- Plan, written before data collection: [experiments/retrospective-fit-survey.md](experiments/retrospective-fit-survey.md)

**Hypothesis:** Manhattan-based alignment tracks reported fit better than cosine.

#### Experiment 2.6: Weekly Adjustment Diary (Pilot)
- 5–10 volunteers, 6–8 weeks, one question per week (the $K(i)$ from 2.4)
- Participants are identified only by a code word they choose
- The first real test of fit as dynamic stability

**Hypothesis:** People whose fit feels wrong show rising $K$; people whose fit feels right settle.

### Deliverables:
- [x] Synthetic data generator
- [x] Multiple matching algorithm implementations (cosine, Manhattan, Euclidean, Chebyshev)
- [ ] Write-up of findings (even if experiments fail). First one: [metric-analysis.md](metric-analysis.md)

---

## Phase 3: Reality Check (after Phase 2)

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

## Phase 4: Protocol Formalization (after Phase 3)

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

| Phase | When | Status (October 2026) |
|-------|------|--------|
| 1. Foundation | Ongoing | Mostly done; engagement below target |
| 2. Experimentation | Now | Started |
| 3. Reality Check | After Phase 2 | Conditional on Phase 2 |
| 4. Protocol Formalization | After Phase 3 | Conditional on Phase 3 |
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
