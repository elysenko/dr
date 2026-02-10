# Executive Summary: Evidence Verdict on /dr Pipeline Fixes

## The Bottom Line

**Your suspicion was right — but not in the way you expected.** The verification-focused fixes (1, 7, 9) ARE partially theater, but not because multi-agent doesn't work. It's because **LLM self-evaluation without external feedback is fundamentally unreliable** (3 independent research programs confirm this). The fixes that target *retrieval* and *synthesis* have the strongest evidence base. The fix prioritization should be substantially reordered.

## Verdict by Fix (Evidence-Based)

| Fix | Proposed | Evidence Verdict | Recommended Action |
|-----|----------|-----------------|-------------------|
| **5** | Iterative query refinement | **STRONGLY SUPPORTED** (+15-22% across 6 studies) | **#1 PRIORITY — implement first** |
| **4** | Non-generic synthesis (contrastive prompting) | **SUPPORTED** (+52.9% on reasoning tasks) | **#2 PRIORITY — implement** |
| **3** | Research contract binding | **SUPPORTED** (aligns with Gemini's plan-approval pattern) | **#3 PRIORITY — implement** |
| **6** | Evidence-based suggestions | **SUPPORTED** (structured output + attribution works) | **#4 PRIORITY — implement** |
| **1** | Isolated C1 verification paths | **PARTIALLY SUPPORTED — redesign needed** | **Redesign: external-tool-grounded, not just isolated agents** |
| **2** | Site-targeted search | **WEAK/MIXED** (risks recall loss) | **Downgrade to supplementary, not primary** |
| **7** | Binary checklists | **SUPPORTED** (binary >> scalar for LLM judges) | **Implement — but won't fix the deeper self-eval problem** |
| **8** | Source diversity gate | **MODERATELY SUPPORTED** (breadth correlates with quality) | **Implement with anti-SEO heuristics** |
| **9** | Honest independence estimation | **UNSUPPORTED as designed** (LLMs can't assess independence) | **Replace with structural heuristics, not LLM judgment** |
| **10** | Split 930-line prompt | **STRONGLY SUPPORTED** (930 lines ≈ 3-4.6K tokens, at degradation threshold) | **Implement — Bayesian pruning showed +3.8% from 41-45% reduction** |

## Key Findings That Should Change the Plan

1. **Iterative query refinement is the highest-ROI fix** — 6 peer-reviewed papers show +5 to +22 point gains. This was Tier 1 Fix 5 but should be #1 priority.

2. **The 930-line prompt is a measurable problem** — this was Tier 3 Fix 10 ("only if research confirms"). Research confirms it. Instruction competition drops accuracy 13.7% with 19 competing requirements. Promote to Tier 1.

3. **Fix 1 (isolated verification) needs redesign** — isolated agents are better than single-agent, but the real improvement comes from *external tool grounding* (web search verification), not just context isolation. SAFE achieves superhuman factuality at $0.19/response by combining LLMs with search. Redesign Fix 1 to use tool-augmented verification.

4. **Fix 9 (independence estimation) is theater as designed** — no evidence LLMs can assess source independence. Replace with structural heuristics (shared URLs, authors, data points, publication dates).

5. **Fix 2 (site-targeted search) should be supplementary only** — Perplexity explicitly prioritizes "comprehensiveness over precision" at retrieval stage. Site-targeting risks recall loss. Use it as a secondary strategy alongside broad search.

6. **LLM confidence scores are broken** — 84.3% overconfidence rate, ECE of 11-74.8%. Any fix relying on self-assigned confidence (including the current 0-10 scoring) is building on sand. Binary/ternary classification is more reliable.

## What Competitors Actually Do

All top tools (Perplexity, Gemini, OpenAI, Claude) share: iterative multi-step retrieval, sub-question decomposition, citation tracking throughout (not bolted on), and some form of self-critique. **None use formal Graph of Thoughts** — they all use ReAct agent loops. GoT's core insight (decompose + parallel + aggregate) is sound but the industry implements it as agent orchestration.

## Revised Priority Order

1. **Iterative query refinement** (Fix 5) — strongest evidence, highest ROI
2. **Prompt pruning** (Fix 10, promoted) — measurable degradation at current length
3. **Contrastive synthesis** (Fix 4) — strong evidence for non-generic output
4. **Research contract binding** (Fix 3) — aligns with Gemini best practice
5. **Evidence-based suggestions with structured output** (Fix 6)
6. **Binary checklists** (Fix 7) — quick win, binary >> scalar
7. **Tool-grounded verification** (Fix 1, redesigned) — external search, not just isolation
8. **Source diversity with anti-SEO heuristics** (Fix 8)
9. **Structural independence checks** (Fix 9, redesigned) — heuristics, not LLM judgment
10. **Site-targeted search as supplement** (Fix 2, downgraded)
