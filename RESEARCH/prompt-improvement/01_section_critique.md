# Section-by-Section Critique: Deep Research v3.1

This document analyzes each phase of the current prompt, identifying issues and proposing improvements based on academic research and production AI system patterns.

---

## Phase 0: Complexity Classification (Lines 101-115)

### Current Implementation
```markdown
| Type | Characteristics | Process |
|------|-----------------|---------|
| **A: LOOKUP** | Single fact, authoritative source | Direct search → answer. Skip GoT. |
| **B: SYNTHESIS** | Multiple facts, aggregation needed | Abbreviated GoT: 2-3 agents, depth 2. |
| **C: ANALYSIS** | Judgment required, multiple perspectives | Full 7-phase GoT. |
| **D: INVESTIGATION** | Novel, high uncertainty, conflicting evidence | Extended GoT + hypothesis testing + Red Team. |
```

### Issues Identified

1. **No explicit scaling rules** - Says "2-3 agents" for Type B but no guidance on when to use 2 vs 3
2. **Missing complexity indicators** - No measurable criteria for classification
3. **Abrupt transitions** - Type A skips entirely to answer, no graduated approach

### Evidence
- **Anthropic Multi-Agent System**: Uses explicit agent count scaling based on task complexity
- **Perplexity**: Dynamically adjusts search depth based on query classification

### Recommendations
- Add explicit agent count formulas: `agents = ceil(complexity_score / 2)`
- Add measurable indicators: word count, entity count, temporal scope
- Add "micro-GoT" option between LOOKUP and SYNTHESIS

---

## Phase 1: Question Scoping (Lines 117-193)

### Current Implementation
Uses a 1-5 scoring on 4 dimensions, with threshold of 12 for "clear" vs "ambiguous".

### Issues Identified

1. **Refinement overhead** - Adaptive refinement (Steps 1-4) adds latency for simple queries
2. **Missing decision context depth** - "Decision context" dimension is binary (known/unknown) vs nuanced
3. **No rapid-fire mode** - Always runs full scoping even for obvious queries

### Evidence
- **Meincke et al. 2025**: Chain-of-thought overhead decreases value for simple tasks
- **Elicit**: Uses tiered scoping - instant for simple, interactive for complex

### Recommendations
- Add "instant scope" path for scores ≥16 (all dimensions 4+)
- Merge Phase 1.5 (hypotheses) and 1.6 (perspectives) INTO Phase 1 to reduce overhead
- Add estimated time investment before refinement

---

## Phase 1.5: Hypothesis Formation (Lines 215-229)

### Current Implementation
```markdown
1. Generate 3-5 testable hypotheses
2. Assign prior probability: High (70-90%) / Medium (40-70%) / Low (10-40%)
3. Design research to confirm or disconfirm each
4. Track probability shifts as evidence accumulates
5. Report hypothesis outcomes, not just facts
```

### Issues Identified

1. **Probability tracking not operationalized** - How/where to store probability updates?
2. **No hypothesis revision triggers** - When to update vs when to discard?
3. **Overhead for simple queries** - Type A/B queries don't need hypothesis testing

### Evidence
- **Shinn et al. 2023 (Reflexion)**: Hypothesis updates need explicit feedback loops

### Recommendations
- Move hypothesis formation INTO Phase 1 (conditional on Type C/D)
- Add hypothesis state tracking in `graph_state.json`
- Add revision trigger conditions (e.g., contradictory evidence threshold)

---

## Phase 1.6: Perspective Discovery (Lines 231-258)

### Current Implementation
Requires 4+ perspectives including adversarial and practical viewpoints.

### Issues Identified

1. **Separate phase overhead** - Creates artificial break before retrieval
2. **Perspective requirements too rigid** - "4 minimum" may be overkill for narrow queries
3. **No perspective prioritization** - All perspectives treated equally

### Evidence
- **Anthropic Research System**: Integrates perspective generation INTO planning, not separate

### Recommendations
- Merge INTO Phase 1 as "Perspective-Informed Scoping"
- Make perspective count dynamic: `perspectives = min(4, complexity_type + 1)`
- Add perspective weighting based on query domain

---

## Phase 2: Retrieval Planning (Lines 260-283)

### Current Implementation
Creates research plan with 3-7 subquestions, planned source types, query strategy.

### Issues Identified

1. **Static query planning** - All queries planned upfront vs adaptive
2. **No query failure handling** - What if planned queries return nothing?
3. **Source class requirements vague** - "2+ source classes" undefined

### Evidence
- **Perplexity**: Uses adaptive query generation based on intermediate results

### Recommendations
- Add query fallback strategies (broaden, rephrase, pivot)
- Define source classes explicitly: Academic, Government, Industry, News, Primary
- Add contingency queries for each subquestion

---

## Phase 3: Iterative Querying (Lines 285-328)

### Current Implementation
Uses HyDE query expansion, evidence indexing, checkpoint aggregation.

### Issues Identified

1. **HyDE implementation incomplete** - Only mentions "2-3 hypothetical documents" without operationalizing
2. **No query reformulation on failure** - Checkpoint aggregation doesn't address failed queries
3. **Parallel research guidance weak** - "Fire searches for 2-3 subquestions" lacks coordination rules

### Evidence
- **Liu et al. 2024**: Multi-framing HyDE improves recall by 15-20%
- **Anthropic Research System**: Explicit query reformulation strategies

### Recommendations
- Add HyDE template: academic, practitioner, skeptical framings
- Add query failure recovery: broaden → rephrase → related terms → manual intervention
- Add parallel coordination rules: dependency graph, merge points

---

## Phase 4: Triangulation (Lines 330-356)

### Current Implementation
```markdown
### Contradiction Triage
| Conflict Type | Resolution |
|---------------|------------|
| Data disagreement | Find primary source; use most recent; note range |
| Interpretation | Present both with evidence strength; don't pick winner |
| Methodological | Evaluate study quality (A-E); weight accordingly |
| Paradigm conflict | Flag unresolved; present both; let user decide |
```

### Issues Identified

1. **No self-consistency sampling** - Single reasoning path for claim verification
2. **Independence check operationalization missing** - How to trace source origins?
3. **Contradiction resolution too manual** - No automated triage

### Evidence
- **Wang et al. 2023**: Self-consistency with 3+ paths improves accuracy significantly
- **Elicit**: Uses automated source tracing for independence verification

### Recommendations
- Add self-consistency requirement for C1 claims: 3+ reasoning paths must agree
- Add source tracing protocol: DOI lookup, author affiliation check, funding source
- Add contradiction severity scoring to prioritize resolution

---

## Phase 5: Synthesis (Lines 358-396)

### Current Implementation
Requires executive summary, findings by subquestion, implications engine (SO WHAT, NOW WHAT, etc.).

### Issues Identified

1. **Thinking trigger underspecified** - "Think harder" lacks token budget
2. **Red Team activation condition unclear** - "depth 3+ when aggregate > 8.0" - what aggregate?
3. **No output length calibration** - Same structure for all complexity types

### Evidence
- **Anthropic Prompt Best Practices**: Extended thinking needs explicit budget allocation
- **Perplexity**: Output length scales with query complexity

### Recommendations
- Add token budget for "think harder": allocate 30% of response budget
- Clarify Red Team trigger: "when synthesis confidence score > 8.0"
- Add output templates by complexity type (A: 1 page, D: 10+ pages)

---

## Phase 6: Quality Assurance - Reflexion (Lines 398-483)

### Current Implementation
7-step QA process with failure categories, reflection memory, fix verification.

### Issues Identified

1. **CRITICAL: Incomplete Reflexion architecture** - Missing Evaluator component
   - Shinn et al. 2023 Reflexion has 3 components:
     1. **Actor** - generates actions/outputs
     2. **Evaluator** - scores outputs (MISSING)
     3. **Self-Reflection** - generates verbal feedback
   - Current implementation jumps from Actor directly to Self-Reflection

2. **No explicit feedback loop** - "Re-run QA on modified sections" but no structured evaluation
3. **Reflection memory format unspecified** - What schema for `reflection_memory.json`?
4. **Max 3 cycles arbitrary** - No evidence for this limit

### Evidence
- **Shinn et al. 2023**: Reflexion with full 3-component architecture achieves 91% on HumanEval
- **Anthropic Research System**: Uses dedicated QA agent with explicit scoring rubric

### Recommendations
- Add Evaluator component with explicit scoring rubric
- Add feedback format: structured JSON with severity, category, suggested fix
- Specify reflection memory schema
- Make cycle limit dynamic based on improvement rate

---

## Phase 7: Output Packaging (Lines 485-493)

### Current Implementation
Brief file list output.

### Issues Identified

1. **No citation verification phase** - Citations assumed correct from Phase 4
2. **No output validation** - Format compliance not checked
3. **No delivery confirmation** - User acceptance not verified

### Evidence
- **Anthropic Research System**: Dedicated CitationAgent for final verification
- **Elicit**: Output validation layer before delivery

### Recommendations
- Add CitationAgent phase between Phase 6 and 7
- Add format validation checklist
- Add user confirmation prompt for high-stakes deliverables

---

## Agent Roles Section (Lines 580-602)

### Current Implementation
```markdown
<role name="orchestrator">Controls flow, manages budget, makes routing decisions. Always active.</role>
<role name="researcher">Search, fetch, extract, initial scoring. Phases 2-3.</role>
<role name="verifier">Triangulation, independence checks, contradiction resolution. Phase 4+.</role>
<role name="critic">Red Team, QA audits, final review. Phase 5+.</role>
```

### Issues Identified

1. **CRITICAL: Underspecified roles** - No objectives, output format, boundaries
2. **Missing CitationAgent** - No specialized citation verification
3. **No handoff protocols** - How do agents pass work between phases?
4. **Output contract too brief** - 5 items but no format specification

### Evidence
- **Anthropic 2024**: 90.2% improvement when agents have detailed task descriptions including:
  - Explicit objectives
  - Expected output format
  - Boundaries/constraints
  - Success criteria
- **Perplexity**: Uses 6 specialized agents with detailed specifications

### Recommendations
- Expand each role to full specification (see `03_annotated_rewrite.md`)
- Add CitationAgent role
- Add explicit handoff protocols
- Add output schemas (JSON) for each agent

---

## Critical Rules Section (Lines 10-42, 605-622)

### Current Implementation
Rules at start and repeated at end.

### Issues Identified

1. **Position bias partially addressed** - Good start/end placement, but middle section rules get lost
2. **Rule priority unclear** - "critical" vs "high" but no enforcement mechanism
3. **Checklist at end only** - Should appear before each major phase

### Evidence
- **Liu et al. 2024 "Lost in the Middle"**: Information in middle of prompts has lowest recall

### Recommendations
- Add rule reminders before Phases 3, 4, 5 (retrieval, triangulation, synthesis)
- Add enforcement mechanism: phase gates that explicitly check rules
- Add inline rule references: "Per R2, verify evidence for this claim"

---

## Structural Issues

### Sub-Phase Proliferation
Current: 0 → 1 → 1.1 → 1.5 → 1.6 → 2 → 3 → 4 → 5 → 6 → 7

Problem: Non-sequential numbering (1.1, 1.5, 1.6) creates confusion and suggests organic growth rather than designed architecture.

Recommendation: Consolidate into 8 clean phases:
1. Classify & Scope
2. Plan & Hypothesize
3. Retrieve
4. Triangulate
5. Synthesize
6. Cite & Verify
7. Reflect & Fix
8. Package

### Missing Explicit Scaling
No clear guidance on resource allocation by complexity type.

Recommendation: Add scaling table:
| Type | Agents | Max Searches | Max Fetches | Target Time |
|------|--------|--------------|-------------|-------------|
| A | 1 | 5 | 3 | 2 min |
| B | 2-3 | 15 | 10 | 10 min |
| C | 4-6 | 30 | 20 | 30 min |
| D | 8-12 | 50+ | 40+ | 60+ min |

---

## Summary of Critical Fixes

| Priority | Issue | Fix | Source |
|----------|-------|-----|--------|
| P0 | Incomplete Reflexion | Add Evaluator component | Shinn et al. 2023 |
| P0 | Underspecified agents | Add detailed task descriptions | Anthropic 2024 |
| P0 | Missing CitationAgent | Add dedicated citation phase | Anthropic Research System |
| P1 | Position bias | Add mid-prompt rule reminders | Liu et al. 2024 |
| P1 | No self-consistency | Require 3+ paths for C1 | Wang et al. 2023 |
| P1 | Sub-phase overhead | Merge 1.5, 1.6 into Phase 1 | Meincke et al. 2025 |
