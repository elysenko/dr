# Competitive Comparison & Meta-Findings

---

## How the Best Tools Actually Work

### Architecture Comparison

| Feature | Perplexity Pro | Gemini Deep Research | OpenAI Deep Research | Claude Multi-Agent | /dr (current) |
|---------|---------------|---------------------|---------------------|-------------------|---------------|
| **Agent pattern** | RAG + reranking | RL-trained agent | RL-trained o3 agent | Opus 4 + Sonnet 4 workers | GoT 7-phase |
| **Searches/task** | Production-scale | 80-160 | 30-60 | 3-10 per subagent | Variable |
| **Plan approval** | No | Yes (human-in-loop) | No | No | Yes (research contract) |
| **Verification** | Multi-stage reranking | Multi-pass self-critique | Extended CoT | Parallel subagents | Self-consistency 3-path |
| **Speed** | 2-4 min | Up to 15 min | 5-30 min | Minutes | Variable |
| **Citation tracking** | Throughout pipeline | Throughout pipeline | Throughout pipeline | Throughout pipeline | Bolted on at Phase 4 |

### Benchmark Results (Head-to-Head)

| Benchmark | Gemini | OpenAI | Perplexity | What it Tests |
|-----------|--------|--------|------------|--------------|
| HLE (Dec 2025) | **46.4%** | 26.6% | 21.1% | Expert-level questions |
| BrowseComp | **59.2%** | 51.5% | — | Hard-to-find facts |
| SimpleQA | — | — | **93.9%** | Factual accuracy |
| Citation accuracy (Tow Center) | ~25% accurate | — | **63% accurate** | Citation reliability |
| RACE (DeepResearchBench) | **48.88** | 46.98 | 42.25 | Overall research quality |

### What They All Share
1. Multi-step iterative retrieval (no single-shot RAG)
2. Sub-question decomposition before search
3. Citation tracking throughout the pipeline (not bolted on)
4. Source quality evaluation
5. Some form of self-critique during synthesis

### What None of Them Use
- Formal Graph of Thoughts prompting
- Self-assigned confidence scores (0-10)
- Binary INDEPENDENT/DEPENDENT source classification
- 930-line monolithic system prompts

---

## The Meta-Question: Does Multi-Phase Complexity Help?

### Evidence: Yes, When Phases Add New Information

- Self-Refine (generate-critique-refine): +20% average improvement across 7 tasks [Grade A, NeurIPS]
- GoT: +62% sorting quality over ToT, -31% cost [Grade A, AAAI]
- Adaptive GoT: +46.2% on GPQA scientific reasoning [Grade B]
- Anthropic multi-agent: +90.2% over single-agent on BrowseComp [Grade B]

### Evidence: No, When Phases Just Reformat

- Single-agent multi-turn matched multi-agent at 90% lower cost for same-model homogeneous workflows [Grade B]
- Token usage explains 80% of quality variance — it's about WHERE tokens go, not HOW MANY agents [Grade B]
- CoT is losing value for frontier models: +2.9-3.1% at 20-80% time cost [Grade B]

### Conclusion

**Multi-phase is justified IFF each phase adds genuinely new information.** The /dr pipeline phases that add new information:
- Phase 1 (Refinement) → new: user context, beliefs, constraints
- Phase 3 (Retrieval) → new: external evidence from web
- Phase 4 (Verification) → new: cross-checking, contradiction detection — **but only if tool-grounded**
- Phase 6 (QA) → new: structured error detection — **if using binary checklists, not scalar self-scoring**

Phases that may NOT add new information:
- Phase 2 (Planning) → could be folded into Phase 1 with minor changes
- Phase 5 (Synthesis) → adds structure but not new evidence; could be Phase 3's output format
- Phase 7 (Packaging) → reformatting, not new information

---

## The Self-Evaluation Problem (The Elephant in the Room)

### What the Research Says

Three independent research programs converge:

1. **LLMs cannot self-correct reasoning without external feedback** (Huang et al. 2023, confirmed by Kamoi et al. 2024 and 2025 benchmarks) [Grade A]

2. **LLM confidence scores are overconfident 84.3% of the time** with ECE of 11-74.8% (NAACL 2024 survey) [Grade A]

3. **Self-preference bias is structural**: GPT-4 shows 0.520 bias score favoring own outputs, caused by lower-perplexity preference (Panickssery et al., NeurIPS 2024) [Grade A]

### What This Means for /dr

The current pipeline has several self-evaluation components:
- Self-consistency 3 paths (Phase 4)
- GoT scoring 0-10 (Phase 4)
- Reflexion evaluator scoring 1-10 (Phase 6)
- Confidence scores on claims

**All of these are building on unreliable foundations when they use the same model without external tools.**

### What Actually Works for Verification

| Technique | Evidence | Cost |
|-----------|----------|------|
| **External search verification** (SAFE-like) | Superhuman accuracy, agrees with humans 72%, right 76% when they disagree | $0.19/response |
| **Self-RAG** (retrieval-augmented self-evaluation) | 81% fact-checking accuracy | Moderate |
| **CoVe** (chain of verification with search) | +23% F1 improvement | Moderate |
| **Binary checklists** with clear rubrics | 0.989 reliability | Low |
| **Self-consistency** (5-10 paths, majority vote) | +6-18% on reasoning | Moderate |
| Self-correction without tools | **Degrades performance** (75.8% → 38.1%) | Wasted |
| Scalar self-scoring (1-10) | 0.421-0.732 reliability | Wasted |

---

## What Would Surprise the User (Contract Obligation)

The research contract stated belief at 60% confidence: "Most fixes are directionally correct but magnitude is uncertain. The biggest risk is verification theater."

### Findings that should update this belief:

1. **Fix 5 (iterative refinement) has MUCH stronger evidence than expected** — not just "directionally correct" but consistently +15-22% across 6 studies. This alone could be transformative.

2. **Fix 10 (prompt pruning) is more important than expected** — the 930-line prompt is at a measurable degradation threshold. This was Tier 3 but should be Tier 1.

3. **Fix 1 (isolated verification) is less valuable than expected** — the isolation itself adds only +4-7%. The real gain is from external tool grounding, which the current design doesn't emphasize enough.

4. **Fix 2 (site-targeted search) may actually HURT** — Perplexity explicitly avoids restricting search at the retrieval stage. This was Tier 1 but the evidence says downgrade it.

5. **No competitive tool uses formal GoT** — they all use ReAct agent loops. The GoT framing is defensible conceptually but has zero evidence for research tasks specifically.

6. **"Regular mode with web search often outperformed dedicated deep research tools"** (DeepResearchBench) — this challenges the entire premise that elaborate pipelines are necessary.

### Updated Belief Assessment
The user's 60% confidence that "most fixes are directionally correct" should update to roughly:
- Fixes 5, 4, 3, 6, 7, 10: **80-90% confidence** these will help (strong evidence)
- Fix 1: **60% confidence** in current design (needs redesign for external grounding)
- Fix 8: **65% confidence** (moderate evidence, clear anti-SEO use case)
- Fix 2: **40% confidence** as primary strategy (evidence suggests supplementary only)
- Fix 9: **30% confidence** as designed (LLMs can't assess independence; needs structural heuristics)

---

## Source Quality Summary

| Grade | Count | Description |
|-------|-------|-------------|
| **A** (peer-reviewed, top venues: ICML, ACL, ICLR, EMNLP, NeurIPS, TACL, Nature, AAAI) | ~20 | Core evidence base |
| **B** (strong preprints, industry engineering blogs with quantitative data) | ~15 | Supporting evidence |
| **C** (practitioner blogs, product documentation) | ~10 | Context and competitive intel |

Key Grade-A sources anchoring major claims:
- Du et al. (ICML 2024), Wang et al. (ACL 2024), Khan et al. (ICML 2024 Best Paper) — multi-agent debate
- Huang et al. (ICLR 2024), Kamoi et al. (TACL 2024) — self-correction limitations
- IRCoT (ACL 2023), FLARE (EMNLP 2023), Self-RAG (ICLR 2024) — iterative retrieval
- Liu et al. (TACL 2024) — lost in the middle
- Madaan et al. (NeurIPS 2023) — self-refine loops
- Besta et al. (AAAI 2024) — graph of thoughts
- NAACL 2024 Survey — confidence calibration
- Panickssery et al. (NeurIPS 2024) — self-preference bias
- Farquhar et al. (Nature 2024) — semantic entropy
