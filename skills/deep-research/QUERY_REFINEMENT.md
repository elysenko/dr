# Adaptive Query Refinement for /dr (Enhanced)

## Overview

This document describes the **enhanced adaptive refinement** system integrated into Phase 1 of `/dr`. The system now focuses on **generative questioning**—questions that expand the user's thinking and surface unknown unknowns, not just capture logistics.

### Core Philosophy

Traditional refinement asks: "What format do you want?"
Enhanced refinement asks: "What would surprise you if the research revealed it?"

The goal is to help users discover what they actually need to know, including things they didn't realize they needed.

---

## The Problem with Surface-Level Refinement

The old approach focused on administrative questions:
- Geographic focus (often irrelevant)
- Citation strictness (premature optimization)
- Output format (putting cart before horse)

What it missed:
- **Prior beliefs** that might bias how research is received
- **Decision stakes** that determine how thorough to be
- **Unknown unknowns** the user hasn't thought to ask about
- **Stakeholder context** that shapes what evidence is needed
- **Constraints vs preferences** that determine trade-off space

Result: Research that technically answers the question but doesn't move the user forward.

---

## The Solution: Five-Phase Adaptive Refinement

```
User: "/dr [vague query]"
       ↓
Step 0: Clarity check (score 1-20)
       ↓
┌──────────────┬──────────────┐
│ Score ≥ 12   │ Score < 12   │
│ CLEAR        │ AMBIGUOUS    │
└──────┬───────┴──────┬───────┘
       │              │
       ▼              ▼
  Standard       Enhanced
  scoping        refinement
                      │
                      ▼
              Phase 1: Core Understanding
              (The real question, prior beliefs, stakes)
                      │
                      ▼
              Phase 2: Unknown Unknowns
              (Surprises, assumptions, blind spots)
                      │
                      ▼
              Phase 3: Stakeholder & Constraints
              (Who cares, dealbreakers vs preferences)
                      │
                      ▼
              Phase 4: Evidence Requirements
              (Confidence level, evidence types)
                      │
                      ▼
              Phase 5: Practical Scoping
              (Boundaries, depth, format—LAST)
                      │
                      ▼
              Confirm & Launch
```

---

## Phase 1: Core Understanding (Always Ask)

These questions establish the foundation. Never skip them.

### 1.1 The Real Question

Don't accept the first framing. The stated question often isn't the real question.

**Prompt:**
```
You asked about: "[ORIGINAL_QUERY]"

Before we dive in:
- What triggered this question? What happened that made you want to research this now?
- If you had a perfect answer, what would you DO differently tomorrow?
```

**Why this matters:** "Should we use Kubernetes?" might really be "How do I convince my CTO we've outgrown Heroku?" The trigger and intended action reveal the actual need.

### 1.2 Current Mental Model

Understand what they already believe so research can challenge or confirm appropriately.

**Prompt:**
```
What's your current understanding or hypothesis?
- What do you think is likely true?
- How confident are you (gut check: 20%? 60%? 90%)?
- Where did this belief come from?
```

**Why this matters:** Research that ignores prior beliefs often gets rejected. If someone is 90% confident in something wrong, research needs to directly address their sources.

### 1.3 The Stakes

Decision context determines research depth and evidence standards.

**Prompt:**
```
What decision does this inform?
□ High-stakes, hard to reverse (major investment, architecture, hire/fire)
□ Medium-stakes, somewhat reversible (product feature, vendor selection)
□ Low-stakes, easily reversible (process tweak, tool trial)
□ No decision—just learning

What's the cost of being WRONG?
□ Catastrophic (company-ending, safety-critical)
□ Expensive (significant money/time lost)
□ Annoying (rework, delays, but recoverable)
□ Minimal (easy to course-correct)
```

**Why this matters:** "Best database for my side project" vs "Best database for our core product" require completely different research depth.

---

## Phase 2: Discovering Unknown Unknowns (High Value)

These questions surface things the user hasn't thought to ask about. This is where refinement adds the most value.

### 2.1 Surprise Calibration

**Prompt:**
```
What would SURPRISE you if the research revealed it?
- What finding would make you say "I didn't expect that"?
- What's something that, if true, would change your entire approach?
```

**Why this matters:** This reveals the user's implicit expectations, which research can then validate or challenge.

### 2.2 Assumption Surfacing

**Prompt:**
```
What are you assuming to be true that MIGHT NOT BE?
- Industry "common knowledge" that might be outdated
- Things "everyone knows" that you've never verified
- Constraints you're treating as fixed that might be flexible
```

**Why this matters:** The most valuable research often challenges assumptions the user didn't know they had.

### 2.3 Blind Spot Probing

**Prompt:**
```
What might you be missing?
- Who has tried this before and failed? Do you know why?
- What would a skeptic say is wrong with your current thinking?
- What's the contrarian view you haven't seriously considered?
```

**Why this matters:** Explicitly inviting contrary evidence prevents confirmation bias in the research.

---

## Phase 3: Stakeholder & Constraint Mapping

Ask these for decision-oriented research. Skip for pure learning.

### 3.1 Who Else Cares?

**Prompt:**
```
Who are the stakeholders?
- Who will this research need to convince?
- Who might push back? What would change their mind?
- Whose approval/buy-in do you need?
```

**Why this matters:** Research for "convincing my CFO" needs different evidence than research for "my own understanding."

### 3.2 Constraints vs. Preferences

**Prompt:**
```
Let's separate dealbreakers from nice-to-haves:

HARD CONSTRAINTS (non-negotiable):
- Budget ceiling?
- Timeline deadline?
- Technical requirements that cannot be compromised?
- Regulatory/legal must-haves?

PREFERENCES (would trade off if needed):
- Ideal but flexible requirements?
- Things you'd sacrifice for cost/time?
```

**Why this matters:** Research that ignores hard constraints wastes time. Research that treats preferences as constraints misses options.

### 3.3 Alternative Paths

**Prompt:**
```
What alternatives are you comparing?
- Is this "should we do X?" or "X vs Y vs Z?"
- What's the default if you do nothing?
- What's the "good enough" option you might settle for?
```

**Why this matters:** Research for "should we migrate to AWS?" is different if the alternative is Azure vs staying on-prem vs shutting down.

---

## Phase 4: Confidence & Evidence Requirements

Ask for important decisions. Skip for casual exploration.

### 4.1 How Certain Do You Need to Be?

**Prompt:**
```
What confidence level do you need?
□ Directional (70%+ confident in general direction)
□ Solid (85%+ confident, can defend the position)
□ High conviction (95%+ confident, betting significant resources)
□ Near-certainty (99%+ confident, safety/legal/critical)
```

**Why this matters:** Over-researching low-stakes decisions wastes time. Under-researching high-stakes decisions is dangerous.

### 4.2 Evidence Standards

**Prompt:**
```
What evidence would convince you?
□ Expert consensus / authoritative sources
□ Quantitative data / studies / benchmarks
□ Case studies / real-world examples
□ First-principles reasoning
□ Multiple independent sources agreeing

What evidence would you REJECT?
- Sources you don't trust?
- Argument types that don't work for your audience?
```

**Why this matters:** Some audiences need academic citations, others need practitioner testimonials, others need data.

### 4.3 Dealing with Uncertainty

**Prompt:**
```
If research is inconclusive:
□ Tell me "we don't know" and explain why
□ Give best estimate with confidence intervals
□ Present competing views and let me decide
□ Recommend how to get better information
```

**Why this matters:** Sets expectations about how to handle ambiguity.

---

## Phase 5: Practical Scoping

Ask these LAST, and only when relevant. The mistake is asking these first.

### 5.1 Boundaries

Only if topic has geographic, temporal, or industry dimensions:

**Prompt:**
```
Scope boundaries:
- Geographic: [Global / Regional / Specific]
- Temporal: [Historical / Current / Forward-looking]
- Industry: [Cross-industry / Specific sector]
- Scale: [Enterprise / SMB / Consumer / All]
```

### 5.2 Depth vs. Breadth

**Prompt:**
```
Given limited time, prefer:
□ Broader coverage, less depth (survey the landscape)
□ Deeper analysis, narrower focus (master one aspect)
□ Balanced (reasonable coverage with depth on key areas)

What deserves MOST depth? What can be covered lightly?
```

### 5.3 Output & Format

Only if user has specific delivery needs:

**Prompt:**
```
How will you use the output?
□ Read myself → detailed document fine
□ Present to others → needs to be presentation-ready
□ Reference later → needs good structure
□ Make specific decision → needs clear recommendation
□ Defend a position → needs strong sourcing
```

---

## Adaptive Question Selection

### By Query Type

| Query Type | Must Ask | Should Ask | Skip |
|------------|----------|------------|------|
| **Learning** | 1.1, 1.2, 2.1 | 2.2, 5.2 | 3.x, 4.x |
| **Decision** | 1.1-1.3, 3.1-3.3 | 2.1-2.3, 4.1-4.2 | 5.x (unless needed) |
| **Comparison** | 1.1, 1.3, 3.3, 4.1 | 2.1, 3.2 | Others as needed |
| **Risk/Due Diligence** | 1.1-1.3, 2.1-2.3, 4.x | 3.1-3.2 | 5.x (unless needed) |
| **Exploratory** | 1.1, 1.2, 2.1-2.3 | 5.2 | 3.x, 4.x |

### By Clarity Score

| Score | Tier | Questions |
|-------|------|-----------|
| 10-12 | Light | 3-5 from Phase 1-2 |
| 5-9 | Medium | 5-8 from Phase 1-3 |
| < 5 | Full | 8-12 across all phases |

---

## Question Combination Templates

### Learning/Understanding Query

Combine into single AskUserQuestion:

```
1. What triggered your interest in [TOPIC]? What would you do differently with the answer?
2. What do you currently believe about this? (Confidence: low/medium/high?)
3. What would surprise you if the research revealed it?
4. [If recon found multiple facets]: Which aspect interests you most?
5. Broader coverage or deeper focus?
```

### Decision Support Query

```
1. What triggered this? What will you DO with a perfect answer?
2. What's your current hypothesis? How confident are you?
3. What's at stake? Cost of being wrong?
4. What assumptions might be wrong? What would a skeptic say?
5. Who needs to be convinced? What evidence would convince them?
6. What alternatives are you comparing? What's the default?
7. What constraints are non-negotiable vs. nice-to-have?
```

### Risk/Due Diligence Query

```
1. What triggered this investigation? What action does it inform?
2. What's your current assessment? Where did that come from?
3. What's the worst case if your current view is wrong?
4. What assumptions are you making? What might you be missing?
5. Who has tried this and failed? What would a skeptic say?
6. What confidence level do you need? What evidence would convince you?
7. What sources would you reject? What argument types don't work?
```

---

## Anti-Patterns

1. **Format before substance** - Don't ask "bullet points or paragraphs?" before understanding what they need
2. **Accepting first framing** - "Should we use X?" is rarely the real question
3. **Skipping prior beliefs** - Research that ignores what they already believe often gets rejected
4. **Equal weighting** - Some questions need exploration, others need a checkbox
5. **Constraints without alternatives** - Constraints only matter relative to trade-offs
6. **Geographic questions for technical topics** - "What region?" for "how does TCP work?"
7. **Citation questions for exploratory research** - Premature optimization

---

## Output Template

After refinement, produce a research contract:

```markdown
### RESEARCH QUESTION
[One clear sentence—often reframed from original]

### UNDERLYING NEED
[What decision/action this enables; what triggered the question]

### CURRENT HYPOTHESIS
[What user believes; confidence; source]
→ Research should: [confirm/challenge/expand] this view

### STAKES & REVERSIBILITY
[Decision type; cost of being wrong; urgency]

### KEY UNCERTAINTIES TO RESOLVE
1. [Specific unknown that would most change thinking]
2. [Second most important uncertainty]
3. [Third if applicable]

### STAKEHOLDERS & CONSTRAINTS
- Convince: [Who]
- Hard constraints: [Non-negotiable]
- Preferences: [Would trade off]

### COMPARISON FRAME
- Alternatives: [X vs Y vs Z]
- Default: [What happens if do nothing]
- Good enough: [Acceptable fallback]

### EVIDENCE REQUIREMENTS
- Confidence needed: [Level]
- Convincing evidence: [Types]
- Reject: [Sources/arguments to avoid]

### SCOPE
- Deep dive: [Areas for depth]
- Cover lightly: [Areas to skim]
- Exclude: [Out of scope]
- Depth: [Quick/Standard/Deep/Exhaustive]

### SUCCESS CRITERIA
[What makes this research valuable]

### SURPRISES TO INVESTIGATE
- [Contrarian view to explore]
- [Assumption to test]
- [Blind spot to probe]
```

---

## What Happens to /dr-refine?

Still available as standalone skill for users who want to:
- Refine a question WITHOUT starting research
- Explore what they want before committing
- Generate a structured prompt to modify

But now `/dr` handles vague queries automatically with enhanced refinement—`/dr-refine` is optional but uses the same enhanced question framework.
