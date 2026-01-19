# Competitor Comparison: Deep Research Systems

This document compares the v3.1 deep research prompt against three production research systems: Perplexity Pro, Elicit, and Anthropic's Multi-Agent Research System.

---

## System Overview

| Feature | v3.1 GoT | Perplexity Pro | Elicit | Anthropic Research |
|---------|----------|----------------|--------|-------------------|
| Architecture | Graph of Thoughts | Real-time search + synthesis | Task decomposition + extraction | Multi-agent orchestration |
| Agent count | 4 roles | 6+ specialized | 5 pipelines | 7 agents |
| Citation handling | Inline during synthesis | Dedicated citation layer | Extraction-first | Dedicated CitationAgent |
| Reflexion | Partial (missing Evaluator) | N/A | Iterative refinement | Full feedback loops |
| Scaling | Manual tier selection | Automatic | Query-based | Complexity-adaptive |

---

## Perplexity Pro Analysis

### Architecture
```
Query → Classification → Multi-Source Search → Ranking → Synthesis → Citation
                              ↓
                    [Web, Academic, News, Forums]
```

### Strengths We Should Adopt

1. **Real-time source freshness**
   - Perplexity prioritizes recency with explicit date weighting
   - v3.1 has "Stale Data" failure category but no prevention mechanism
   - **Recommendation**: Add recency scoring to source quality (A-E) grades

2. **Parallel search with merge**
   - Fires searches across source types simultaneously
   - Merges with deduplication and ranking
   - v3.1 mentions parallel search but lacks merge protocol
   - **Recommendation**: Add explicit merge/dedup phase in Phase 3

3. **Citation-first display**
   - Citations rendered inline as clickable references
   - Enables immediate source verification
   - v3.1 treats citations as metadata
   - **Recommendation**: Add citation formatting requirements to output spec

### Weaknesses We Should Avoid

1. **Limited depth for complex queries**
   - Perplexity optimizes for speed over depth
   - Not suitable for Type D investigation queries
   - v3.1's extended GoT is appropriate for complex research

2. **No hypothesis testing**
   - Perplexity is retrieval-centric, not hypothesis-driven
   - v3.1's Phase 1.5 hypothesis formation is a strength

---

## Elicit Analysis

### Architecture
```
Query → Decomposition → Literature Search → Extraction → Synthesis → Quality Check
              ↓                  ↓                 ↓
      [Sub-questions]    [Semantic Scholar]   [Structured data]
```

### Strengths We Should Adopt

1. **Structured extraction**
   - Elicit extracts into structured fields: findings, methods, limitations
   - Enables systematic comparison across sources
   - v3.1 uses unstructured "key passages"
   - **Recommendation**: Add extraction schema to evidence indexing

2. **Automatic source tracing**
   - Tracks citation chains to find primary sources
   - Identifies when 5 articles cite the same study
   - v3.1 has R4 independence rule but manual enforcement
   - **Recommendation**: Add automated source tracing protocol

3. **Confidence calibration**
   - Elicit shows confidence intervals on extracted data
   - Distinguishes "paper says X" from "X is true"
   - v3.1 has claim taxonomy but not calibrated confidence
   - **Recommendation**: Add confidence intervals to C1 claims

4. **Tiered interaction**
   - Simple queries: instant answer
   - Complex queries: interactive refinement
   - v3.1 always runs full adaptive refinement
   - **Recommendation**: Add "instant mode" for high-clarity queries

### Weaknesses We Should Avoid

1. **Academic bias**
   - Elicit heavily weighted toward peer-reviewed literature
   - Misses industry reports, news, primary data
   - v3.1's multi-source approach is more comprehensive

2. **Limited real-time data**
   - Elicit works from indexed corpus
   - Cannot access breaking news or recent releases
   - v3.1's WebSearch/WebFetch provides real-time access

---

## Anthropic Multi-Agent Research System Analysis

### Architecture (from 2024 documentation)
```
Orchestrator
    ├── ResearchPlanner (decomposes query)
    ├── SearchAgent (executes searches)
    ├── ExtractorAgent (pulls key info)
    ├── SynthesisAgent (combines findings)
    ├── CitationAgent (verifies citations)
    ├── QAAgent (quality checks)
    └── WriterAgent (formats output)
```

### Strengths We Should Adopt

1. **Detailed agent task descriptions**
   - Each agent has explicit:
     - Objective (what to accomplish)
     - Output format (exact schema)
     - Boundaries (what NOT to do)
     - Success criteria (how to verify)
   - v3.1 has 4-line role descriptions
   - **Recommendation**: Expand agent specs to full task descriptions

2. **Dedicated CitationAgent**
   - Specialized agent for citation verification
   - Checks: URL validity, quote accuracy, claim-citation match
   - v3.1 includes citation audit in Phase 6 but not dedicated
   - **Recommendation**: Add CitationAgent as Phase 6.5

3. **Explicit handoff protocols**
   - Defines what each agent passes to the next
   - Uses structured JSON for inter-agent communication
   - v3.1's agent output contract is informal
   - **Recommendation**: Add JSON schemas for agent outputs

4. **Complexity-adaptive scaling**
   - Agent count scales with query complexity
   - Simple: 2 agents, Complex: 7+ agents
   - v3.1 has intensity tiers but vague scaling
   - **Recommendation**: Add explicit agent count formulas

### Weaknesses We Should Avoid

1. **Overhead for simple queries**
   - Full multi-agent orchestration adds latency
   - v3.1's Type A bypass is appropriate

2. **Rigid agent boundaries**
   - Agents can't dynamically adjust scope
   - v3.1's flexible role activation is better

---

## Feature Gap Analysis

### Features v3.1 Has That Competitors Lack

| Feature | v3.1 | Perplexity | Elicit | Anthropic |
|---------|------|------------|--------|-----------|
| Hypothesis testing | ✅ | ❌ | ❌ | Partial |
| Graph-based reasoning | ✅ | ❌ | ❌ | ❌ |
| Red Team phase | ✅ | ❌ | ❌ | Partial |
| Extended thinking triggers | ✅ | ❌ | ❌ | ❌ |
| Reflection memory | ✅ | ❌ | ❌ | ❌ |

### Features Competitors Have That v3.1 Lacks

| Feature | v3.1 | Perplexity | Elicit | Anthropic |
|---------|------|------------|--------|-----------|
| Dedicated CitationAgent | ❌ | ✅ | ✅ | ✅ |
| Structured extraction schema | ❌ | Partial | ✅ | ✅ |
| Automated source tracing | ❌ | ❌ | ✅ | Partial |
| Confidence intervals | ❌ | ❌ | ✅ | ❌ |
| Real-time freshness scoring | ❌ | ✅ | ❌ | ❌ |
| Detailed agent specs | ❌ | N/A | ✅ | ✅ |
| Instant mode bypass | ❌ | ✅ | ✅ | ❌ |

---

## Recommended Adoptions for v4

### From Perplexity
1. **Recency weighting in source quality** - Add date factor to A-E grades
2. **Parallel search merge protocol** - Explicit deduplication step
3. **Citation-first formatting** - Inline numbered references

### From Elicit
1. **Structured extraction schema** - Define fields for evidence extraction
2. **Source tracing automation** - Check for citation chain convergence
3. **Confidence calibration** - Add uncertainty ranges to C1 claims
4. **Instant mode** - Skip refinement for score ≥16 queries

### From Anthropic Research System
1. **Detailed agent task descriptions** - Full spec for each role
2. **Dedicated CitationAgent** - Specialized citation verification phase
3. **JSON handoff schemas** - Structured inter-agent communication
4. **Explicit scaling rules** - Agent count = f(complexity)

---

## Competitive Positioning

### v3.1 Strengths to Preserve
- Graph of Thoughts architecture for complex reasoning
- Hypothesis-driven research (not just retrieval)
- Red Team adversarial review
- Reflection memory for continuous improvement
- Extended thinking integration

### v4 Differentiation Strategy
Position as the **depth-optimized** research system:
- Perplexity: Speed-first, breadth-oriented
- Elicit: Academic-first, extraction-oriented
- Anthropic: General-purpose, agent-oriented
- **v4 GoT**: Investigation-first, evidence-oriented

Target use cases where v4 excels:
- Type C/D queries requiring judgment
- High-stakes decisions needing audit trails
- Novel topics with conflicting evidence
- Research requiring hypothesis testing

---

## Implementation Priority Matrix

| Feature | Impact | Effort | Priority |
|---------|--------|--------|----------|
| Detailed agent specs | High | Medium | P0 |
| CitationAgent phase | High | Low | P0 |
| Structured extraction | Medium | Medium | P1 |
| Source tracing | Medium | High | P1 |
| Instant mode | Medium | Low | P1 |
| Recency weighting | Low | Low | P2 |
| Confidence intervals | Medium | Medium | P2 |
| JSON handoff schemas | Medium | Medium | P2 |
