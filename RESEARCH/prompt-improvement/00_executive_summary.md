# Executive Summary: Deep Research Prompt Improvement

## Overview

Analysis of the 620-line Graph of Thoughts (GoT) deep research prompt (v3.1) identified **15 specific improvements** backed by academic papers and production AI research systems.

## Critical Findings

| # | Issue | Evidence Source | Impact |
|---|-------|-----------------|--------|
| 1 | **Prompt length (~620 lines)** | Liu et al. 2024: performance degradation at ~3000 tokens | Instruction-following degrades as length increases |
| 2 | **Multi-agent roles underspecified** | Anthropic 2024: 90.2% improvement with detailed task descriptions | Agents lack clear objectives, output formats, boundaries |
| 3 | **Reflexion implementation incomplete** | Shinn et al. 2023: requires Actor/Evaluator/Self-Reflection | Phase 6 QA misses Evaluator feedback loops |
| 4 | **No position bias mitigation** | Liu et al. 2024: "Lost in the Middle" effect | Critical rules buried in middle sections |
| 5 | **No dedicated citation agent** | Anthropic research system: dedicated CitationAgent | Citation accuracy suffers without specialized verification |

## Prioritized Recommendations

### Critical (Must-Have for v4)

1. **Restructure for position bias** - Front-load critical rules, repeat at end
2. **Add detailed agent task descriptions** - Objectives, output format, boundaries for each role
3. **Add dedicated CitationAgent phase** - Specialized citation verification after synthesis
4. **Fix Reflexion architecture** - Implement full 3-component system with trigger conditions
5. **Add explicit scaling rules** - Simple queries = 1 agent, complex = 10+ agents

### High Priority

6. **Add self-consistency sampling** - For C1 claims, require 3+ reasoning paths
7. **Merge sub-phases** - Consolidate 1.5 and 1.6 into Phase 1 to reduce overhead
8. **Add token budget guidance** - Explicit allocation for extended thinking triggers
9. **Improve HyDE implementation** - Multiple hypothetical framings, not just one
10. **Add confidence-based early stopping** - Exit when confidence threshold met

### Medium Priority

11. **Add query failure recovery** - Explicit fallback strategies when searches fail
12. **Strengthen source triangulation** - Minimum 3 independent sources for C1 claims
13. **Add temporal validation** - Check for outdated data with explicit recency rules
14. **Improve contradiction handling** - Decision tree for resolution strategies
15. **Add output length calibration** - Match output depth to query complexity

## Key Metrics

| Metric | v3.1 | v4 Target |
|--------|------|-----------|
| Prompt length | ~620 lines | ~500 lines |
| Agent specifications | 4 brief roles | 5 detailed specs |
| Position-critical rules | 2 locations | 3 locations (start/middle/end) |
| Reflexion components | 1 (partial) | 3 (complete) |
| Sub-phases | 4 (0, 1, 1.5, 1.6, 2...) | 8 (consolidated) |

## Evidence Base

### Academic Sources
- **Liu et al. 2024** - "Lost in the Middle: How Language Models Use Long Contexts"
- **Shinn et al. 2023** - "Reflexion: Language Agents with Verbal Reinforcement Learning"
- **Wang et al. 2023** - "Self-Consistency Improves Chain of Thought Reasoning"
- **Besta et al. 2023** - "Graph of Thoughts: Solving Elaborate Problems with Large Language Models"
- **Meincke et al. 2025** - "The Decreasing Value of Chain-of-Thought"

### Production Systems
- **Anthropic Multi-Agent Research System** (2024) - Agent architecture patterns
- **Anthropic Claude Prompt Best Practices** - Task description guidelines
- **Perplexity Pro** - Real-time research system architecture
- **Elicit** - Scientific research automation methodology

## Implementation Approach

### Phase 1: Research Documentation
Create comprehensive analysis in `./RESEARCH/prompt-improvement/`:
- Section-by-section critique
- Competitor comparison
- Annotated rewrite proposals
- Evidence mapping table

### Phase 2: v4 Implementation
Create `/home/ubuntu/dr/agents/deep-research-v4.md`:
- Implement all 5 critical fixes
- Implement high-priority items 6-10
- Add medium-priority items as conditional features

### Phase 3: Verification
- Compare v3.1 vs v4 structure
- Validate all changes traced to sources
- Document breaking changes

## Success Criteria

- [ ] 15 improvements documented with academic/production evidence
- [ ] Section-by-section critique complete with specific line references
- [ ] Annotated rewrite with before/after examples
- [ ] Comparison against Perplexity and Elicit architectures
- [ ] New v4 prompt implements all critical fixes
- [ ] v3.1 preserved as backup

## Risk Assessment

| Risk | Mitigation |
|------|------------|
| Prompt too condensed | Test with sample queries before finalizing |
| Breaking existing workflows | Preserve v3.1, document migration path |
| Over-engineering agents | Start with minimum viable specs, iterate |

## Next Steps

1. Review detailed critique in `01_section_critique.md`
2. Compare against competitors in `02_competitor_comparison.md`
3. See annotated changes in `03_annotated_rewrite.md`
4. Verify evidence mapping in `04_evidence_table.md`
5. Review concrete examples in `05_before_after_examples.md`
