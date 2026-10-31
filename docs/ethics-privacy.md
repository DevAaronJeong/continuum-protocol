# Ethics & Privacy Principles

## Core Commitment

**If this system becomes a surveillance tool, it has failed.**

The entire premise of `continuum-protocol` is to align people with work that respects their lives. Any implementation that violates privacy, enables coercion, or treats humans as optimizable resources contradicts our fundamental philosophy.

---

## Non-Negotiable Principles

### 1. User Owns Their Data

**Always.**

- Lifestyle data belongs to the person, not the system
- No third party can access raw personal data without explicit consent
- Users can export, delete, or modify their data at any time
- Data portability is not optional — it's fundamental

### 2. Local-First Analysis

**Process data on the user's device whenever possible.**

- Aggregation and matching should happen client-side first
- Only anonymized, consented signals should reach any server
- If cloud processing is unavoidable, it must be:
  - End-to-end encrypted
  - Auditable
  - Revocable

### 3. Explainability is Mandatory

**Users must always know WHY a match was suggested.**

- No black-box recommendations
- Every match must be traceable to specific lifestyle signals
- Users can see which factors contributed to alignment scores
- If the system can't explain it, it shouldn't suggest it

Example of good explainability:
```
Match Score: 0.78
Reasons:
- Your energy peak (evening) aligns with this role's async work style
- Your preference for low communication density matches this team's structure
- Your consistency score (0.85) suggests long-term alignment potential
```

### 4. Consent is Continuous

**Permission is not a one-time checkbox.**

- Users can opt out of any data collection at any time
- Consent must be granular (e.g., "track focus time" vs. "track social patterns")
- Silence is not consent
- Systems must function even if users choose minimal data sharing

### 5. No Manipulation

**This system does not nudge, gamify, or coerce.**

- We do not optimize for "engagement"
- We do not encourage users to work more
- We do not penalize people for maintaining boundaries
- Alignment scores reflect compatibility, not productivity

### 6. Organizations Are Also Evaluated

**Companies cannot hide behind opaque "culture" claims.**

If we profile individuals, we must profile organizations with equal rigor:
- Do they respect stated working hours?
- Do they maintain rhythm consistency?
- Do they impose unpredictable demands?
- Do they honor the lifestyles they claim to support?

**Organizations that exploit alignment data will be flagged.**

---

## What We Will Not Build

❌ **Productivity surveillance** — No tracking for the sake of optimization  
❌ **Behavioral modification systems** — No gamification of work  
❌ **Employer-controlled profiling** — Companies cannot force workers to share lifestyle data  
❌ **Algorithmic hiring bias** — No replacing human judgment with opaque scores  
❌ **Retention manipulation** — No using alignment data to trap people in roles  

---

## Implementation Safeguards

### Data Minimization

Collect only what is necessary for alignment, nothing more.

**Good:**
- "User is most active between 8-11 PM"
- "User prefers asynchronous communication"

**Bad:**
- "User opened email 47 times today"
- "User visited competitor website 3 times this week"

### Differential Privacy

When aggregating data across users:
- Add noise to prevent individual re-identification
- Use techniques like k-anonymity or epsilon-differential privacy
- Publish methods openly for audit

### Right to Disconnect

Users must be able to:
- Pause all profiling temporarily
- Delete their profile entirely
- Opt out of specific features without losing core functionality

---

## Accountability Mechanisms

### 1. Open Source as Accountability

Code must be public and auditable.
- Anyone can inspect how alignment is calculated
- Community can flag unethical features
- Forks can reject surveillance implementations

### 2. Ethics Review for Features

Before adding any new data collection or matching feature, ask:
1. Is this necessary for alignment, or just convenient?
2. Could this be used to coerce or manipulate?
3. Would we be comfortable if this data leaked?
4. Does this treat users as humans or as resources?

If any answer is concerning, **do not ship**.

### 3. User Advisory Board

Eventually, this project should include:
- A representative group of actual users
- Regular ethics audits
- Public transparency reports

---

## Hard Questions We're Still Debating

These are unresolved and need community input:

**Q: Can "lifestyle profiling" ever be truly non-invasive?**  
We don't know yet. We're exploring methods like:
- Self-reported rhythms instead of passive tracking
- Coarse-grained signals (morning/evening) instead of precise timestamps
- Federated learning to keep raw data local

**Q: How do we prevent misuse by bad-actor organizations?**  
Possible approaches:
- Require two-way transparency (companies must also share their rhythm data)
- Community-driven reputation systems for organizations
- Copyleft licensing (AGPL-3.0) so modified versions run as services stay inspectable

**Q: Is it ethical to model humans mathematically?**  
This is the deepest question. Our stance:
- Humans are not reducible to vectors
- But preferences, rhythms, and patterns are observable and can be respected
- The goal is not to "solve" humanity, but to honor diversity

---

## If You See a Violation

This is an open experiment. If you see this project, or any fork, violating these principles:

1. Open an issue labeled `ethics`
2. Provide specific examples
3. Suggest a corrective action

We will treat ethics concerns with the highest priority.

---

## License Considerations

**Decision (October 2026):**
- **Code:** GNU AGPL-3.0-or-later ([LICENSE](../LICENSE))
- **Documentation and figures:** CC BY 4.0 ([LICENSE-docs](../LICENSE-docs))

**Why not an ethical-source license such as the Hippocratic License?**
- **Licenses protect text and code, not ideas.** Anyone can re-implement rhythm-based matching from scratch, so no license can stop a surveillance product built on these ideas.
- **Ethical-source licenses aren't open source under the OSI definition.** Many organizations can't use them or contribute to them, and how well they can be enforced is untested.
- **AGPL covers what a license can realistically cover.** A modified version run as a service must publish its source, so forks stay inspectable and their matching stays explainable.

What a license can't do is the job of the rest of this document: design choices (local-first, no rankings, explainability), the roadmap's [What We Will NOT Do](roadmap.md#what-we-will-not-do), and the community.

If you think this is the wrong call, [open an issue](https://github.com/DevAaronJeong/continuum-protocol/issues/new). It can be revisited.

---

## Final Word

Technology is not neutral.

A system designed to "match people with work" can either:
- Respect human autonomy and rhythms, or
- Become another mechanism of control

We choose the former.

If we fail to uphold these principles, we ask the community to fork this project and build the version we should have made.

---

**Ethics is not a feature. It's the foundation.**
