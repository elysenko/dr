# Research Report: Evidence Verdict on /dr Pipeline Improvement Plan

**Research Question**: Do the proposed fixes to the /dr multi-phase research pipeline address real, evidence-backed problems — and will they produce measurable improvements?

**Method**: 5 parallel research streams covering multi-agent verification, retrieval optimization, prompt engineering/synthesis, competitive analysis, and LLM self-evaluation reliability. ~45 academic sources reviewed, majority Grade A/B (top-tier venues: ICML, ACL, ICLR, EMNLP, NeurIPS, TACL, Nature, AAAI).

---

## TL;DR

**The plan is directionally right but the priorities are wrong.** The retrieval and synthesis fixes have overwhelming evidence. The verification fixes are partially theater. The prompt pruning fix (dismissed as Tier 3) should be Tier 1. Here's the evidence-based reordering.

---

## Revised Fix Priority (Evidence-Ranked)

### Tier 1: Strong Evidence — Implement Now

| Priority | Fix | Evidence Strength | Expected Impact | Key Source |
|----------|-----|------------------|----------------|-----------|
| **#1** | **Fix 5: Iterative query refinement** | 6 peer-reviewed papers, +15-22% | HIGH | IRCoT (ACL 2023), RQ-RAG, FLARE (EMNLP 2023) |
| **#2** | **Fix 10: Prompt pruning/splitting** (promoted from Tier 3) | Multiple studies, degradation at 3K+ tokens | HIGH | Liu et al. (TACL 2024), instruction competition research |
| **#3** | **Fix 4: Contrastive synthesis** | +52.9% on reasoning, personas don't help | MEDIUM-HIGH | Jiang et al. 2024, Mollick et al. 2025 (Wharton) |
| **#4** | **Fix 3: Research contract binding** | Aligns with Gemini best practice | MEDIUM | Gemini architecture, Anthropic context engineering |

### Tier 2: Supported — Implement After Tier 1

| Priority | Fix | Evidence Strength | Expected Impact | Key Source |
|----------|-----|------------------|----------------|-----------|
| **#5** | **Fix 6: Evidence-based suggestions** (structured output) | Indirect evidence, competitive gap | MEDIUM | RARR (ACL 2023), structured output research |
| **#6** | **Fix 7: Binary checklists** (replace 1-10 scoring) | Binary: 0.989 reliability vs scalar: 0.421-0.732 | MEDIUM | LLM-as-Judge survey, CIP study |
| **#7** | **Fix 1: Verification paths** (REDESIGNED) | +4-7% from isolation, much more from tool grounding | MEDIUM | SAFE (NeurIPS 2024), Du et al. (ICML 2024) |
| **#8** | **Fix 8: Source diversity + anti-SEO** | Moderate evidence, documented failure mode | LOW-MEDIUM | Anthropic engineering blog, triangulation literature |

### Tier 3: Redesign Needed — Don't Implement as Originally Designed

| Priority | Fix | Issue | Recommended Change |
|----------|-----|-------|-------------------|
| **#9** | **Fix 9: Independence estimation** | LLMs can't assess independence | Replace with structural heuristics (shared URLs, authors, stats) |
| **#10** | **Fix 2: Site-targeted search** (downgraded from Tier 1) | Risks recall loss; Perplexity does the opposite | Make supplementary only, not primary |

---

## The Three Findings That Should Change Everything

### 1. Iterative Query Refinement Is the Highest-ROI Fix

Six peer-reviewed studies converge on +5 to +22 point improvements:

| Study | Venue | Improvement |
|-------|-------|------------|
| IRCoT | ACL 2023 | +21 pts retrieval, +15 pts QA |
| RQ-RAG | 2024 | +22.6% average on multi-hop QA |
| FLARE | EMNLP 2023 | Superior to all baselines |
| FAIR-RAG | 2025 | +8.3 F1 over strongest iterative baseline |
| Self-RAG | ICLR 2024 | Outperforms ChatGPT + RAG-Llama2 |
| PRISM | 2025 | 90.9% vs 61.5% recall |

**The core pattern**: Use initial retrieval results to extract domain terminology and refine follow-up queries, like a human researcher who reads the first few sources and adjusts their search strategy. Cap at 2 refinement rounds (diminishing returns beyond that).

This was Fix 5, buried in the middle of Tier 1. It should be the absolute first thing implemented.

### 2. The 930-Line Prompt Is Measurably Degrading Performance

This was Tier 3 Fix 10 ("only if research confirms prompt length degrades instruction following"). **Research confirms it.**

- Reasoning degrades at ~3,000 tokens; 930 lines ≈ 3,000-4,650 tokens — right at the threshold
- 19 competing requirements dropped GPT-4o accuracy from 98.7% to 85.0% — a 13.7% loss
- Bayesian prompt optimization achieved +3.8% accuracy by reducing prompt length 41-45%
- Claude 4.x docs explicitly warn against aggressive "CRITICAL: You MUST" phrasing
- "Lost in the middle" effect degrades attention to content in the middle of long prompts

**Action**: Audit the prompt. Remove instructions Claude follows naturally. Replace aggressive phrasing. Expected: +3-5% instruction following from pruning alone, before any structural splitting.

### 3. LLM Self-Evaluation Without External Tools Is Fundamentally Unreliable

Three independent research programs converge:

- **Huang et al. (ICLR 2024)**: Self-correction drops CommonSenseQA from 75.8% to 38.1%
- **Kamoi et al. (TACL 2024)**: No successful self-correction without external feedback in any study
- **NAACL 2024 Survey**: LLMs overconfident in 84.3% of scenarios; ECE of 11-74.8%

This means:
- The current self-assigned confidence scores (Phase 4) are unreliable
- The Reflexion evaluator's 1-10 scoring (Phase 6) has 0.421-0.732 reliability
- Self-consistency (3 paths in same context) is modest improvement at best
- **BUT**: External tool-grounded verification (SAFE, CoVe, Self-RAG) genuinely works

**Implication for Fix 1**: Isolated agents are better than single-agent, but the real gain is from making verification agents use web search to find confirming/disconfirming evidence — not just reasoning over cached evidence.

---

## Detailed Evidence by Fix

### Fix 1: Isolated C1 Verification Paths

**Evidence FOR:**
- Du et al. (ICML 2024): Multi-agent debate yields +7.8 pts factual accuracy, +14.8 pts arithmetic [A]
- Khan et al. (ICML 2024 Best Paper): Debate improves truthfulness by +28pp for non-experts [A]
- 3 agents × 2 rounds is the empirical sweet spot [A]

**Evidence AGAINST:**
- Wang et al. (ACL 2024): **Single agent with strong demonstrations MATCHES 6-agent discussion** (75.63% vs 74.46%). Multi-agent only wins when prompts are weak [A]
- Huang et al. (ICLR 2024): Self-correction without external feedback drops accuracy from 75.8% to 38.1% [A]
- ColMAD (EMNLP 2024): Multi-agent error detection only +4% over single agent; adversarial attacks cause -40% [A]
- Self-preference bias of 0.520: LLMs structurally favor own outputs (Panickssery et al., NeurIPS 2024) [A]

**Verdict**: Isolated agents are mildly better (+4-7%), but the transformative improvement is from **external tool grounding**. Google's SAFE achieves superhuman factuality at $0.19/response via LLM + web search. **Redesign**: Make at least 2 of 3 paths use `WebSearch` to find confirming/disconfirming evidence, not just reason over cached evidence.

### Fix 2: Site-Targeted Search

**Evidence FOR:**
- Domain-specific databases contain higher-quality content by definition
- Anthropic documented agents favoring "SEO-optimized content farms" without heuristics [B]

**Evidence AGAINST:**
- Specialized medical search engines found "no better than general search engines" (Gusenbauer 2020) [B]
- Perplexity explicitly prioritizes "comprehensiveness over precision" at retrieval stage [B]
- Site-targeting restricts search space, risking recall loss

**Verdict**: **Downgrade to supplementary.** Run broad queries first, add 1-2 site-targeted queries as quality supplement.

### Fix 3: Research Contract Binding

**Evidence FOR:**
- Gemini's distinguishing feature is human-in-the-loop plan approval before execution [A]
- Anthropic recommends passing condensed structured context between sub-agents [B]
- "Retrieve-then-solve" improved GPT-4o by up to 4% on RULER benchmarks [B]

**Evidence AGAINST:**
- No direct study compares binding vs advisory contracts in LLM pipelines
- Risk of over-constraining if contract is wrong

**Verdict**: **Keep as designed.** Add escape valve for when Phase 3 discoveries contradict contract assumptions.

### Fix 4: Non-Generic Synthesis (Contrastive Prompting)

**Evidence FOR:**
- Contrastive prompting: **+52.9% on GSM8K** (Jiang et al. 2024) [B]
- Expert persona prompting does NOT improve factual accuracy (Mollick et al. 2025, Wharton) [B]
- Structured output schemas: format compliance 35.9% → 100% [B]
- Self-Refine: +20% average across 7 tasks (Madaan et al., NeurIPS 2023) [A]

**Evidence AGAINST:**
- Contrastive evidence mostly from math/reasoning, not open-ended synthesis
- CoT losing value for frontier models: +2.9-3.1% at 20-80% time cost [B]

**Verdict**: **Implement with specific patterns:** (1) "What is uniquely true HERE vs generically true?" (2) Belief-anchoring: "You believed X at Y% confidence. Evidence [confirms/challenges] because..." (3) Decision-anchoring. (4) Drop persona prompting.

### Fix 5: Iterative Query Refinement

**Evidence FOR:** See "Finding #1" above — 6 peer-reviewed papers, +5 to +22 points.

**Evidence AGAINST:**
- Over-refinement diminishing returns for already-capable models [B]
- Each step adds latency and cost

**Verdict**: **#1 PRIORITY. Implement immediately.** Cap at 2 refinement rounds. Use quality of initial results to decide if refinement is needed.

### Fix 6: Evidence-Based Suggestion Generation

**Evidence FOR:**
- Structured output with attribution eliminates boilerplate [B]
- RARR preserved >90% content intent while improving attribution [A]
- Competitive gap: no tool does this well

**Evidence AGAINST:**
- No direct study on this as a technique
- LLMs tend toward generic best practices regardless of evidence

**Verdict**: **Implement with structured output enforcement.** Require JSON schema with finding, suggestion, evidence_cited, evidence_strength, and applies_because fields.

### Fix 7: Binary Checklists

**Evidence FOR:**
- Binary: **0.989-0.990 reliability** vs scalar: **0.421-0.732** [B]
- Scale format dramatically affects results: same content scored 1.68 (numerical) vs 3.17 (categorical) [C]

**Verdict**: **Implement.** Replace all 1-10 scoring with binary YES/NO or ternary SUPPORTED/CONTRADICTED/UNCERTAIN.

### Fix 8: Source Diversity Gate

**Evidence FOR:**
- Gemini's 111 citations correlated with highest quality score on DeepResearchBench [B]
- Anthropic documented SEO-content-farm bias [B]

**Verdict**: **Implement as anti-SEO heuristic**, not hard gate. Require explicit check that sources don't all trace to same original.

### Fix 9: Honest Independence Estimation

**Evidence AGAINST:**
- **No evidence LLMs can reliably assess source independence** [HIGH confidence]
- "Independence checks relying on LLM judgment alone are largely theatrical"

**Verdict**: **Redesign completely.** Replace LLM-judged independence with structural heuristics: same domain → DEPENDENT, same author → DEPENDENT, same unique statistics → DEPENDENT, different methodology + org → LIKELY INDEPENDENT.

### Fix 10: Prompt Pruning/Splitting (Promoted from Tier 3)

**Evidence FOR:**
- Reasoning degrades at ~3,000 tokens; 930 lines is at threshold [C]
- 19 competing instructions: 98.7% → 85.0% accuracy (13.7% drop) [B]
- Bayesian optimization: +3.8% from 41-45% length reduction [B]
- Claude 4.x warns against aggressive "CRITICAL: You MUST" phrasing [B]
- Lost in the Middle (TACL 2024): middle content degraded [A]

**Verdict**: **Promote to Tier 1.** Prune first (remove natural-behavior instructions, aggressive phrasing), then split into phase-specific files.

---

## What Competitors Actually Do

### All top tools share:
1. Iterative multi-step retrieval (no single-shot RAG)
2. Sub-question decomposition before search
3. Citation tracking throughout pipeline (not bolted on)
4. ReAct agent loops (Plan-Act-Observe), not formal GoT
5. Some form of self-critique during synthesis

### Benchmarks:
| Tool | HLE (Dec 2025) | BrowseComp | Citation Accuracy (Tow Center) |
|------|----------------|------------|-------------------------------|
| Gemini | **46.4%** | **59.2%** | ~25% |
| OpenAI | 26.6% | 51.5% | — |
| Perplexity | 21.1% | — | **63%** |

**All tools fail on citation accuracy** — 60%+ error rate (Tow Center study). Dedicated verification is essential, but it must be tool-grounded.

### The uncomfortable finding:
> "Regular mode with web search often outperformed corresponding dedicated deep research tools" — DeepResearchBench

This means the pipeline's value comes from structured evidence gathering and verification, not elaborate prompting frameworks.

---

## What to Do With Already-Implemented Fixes (1, 2, 3)

Three fixes were partially implemented before this research:

**Fix 1 (Isolated verification)** — **Keep but redesign.** Add `WebSearch` to the Inverse Query and Direct Evidence agents so they ground verification in external evidence, not just cached evidence. The isolation is mildly helpful (+4-7%); external grounding is transformative.

**Fix 2 (Site-targeted search)** — **Downgrade.** Already implemented as supplementary alongside general queries, which is acceptable. Don't make it primary.

**Fix 3 (Research contract binding)** — **Keep as-is.** Add escape valve for when Phase 3 contradicts contract assumptions.

---

## Addressing the Research Contract

### Was the user's belief confirmed or challenged?

**Belief**: "Most fixes are directionally correct but magnitude uncertain. Biggest risk is verification theater." (60% confidence)

**Updated assessment:**
- Fixes 5, 4, 3, 6, 7, 10: **80-90% confidence** they'll help (strong evidence)
- Fix 1: **60% confidence** in current design (needs tool-grounding redesign)
- Fix 8: **65% confidence** (moderate evidence)
- Fix 2: **40% confidence** as primary strategy (evidence says supplementary only)
- Fix 9: **30% confidence** as designed (LLMs can't judge independence)

**The user was right about verification theater** — but the solution isn't "more verification." It's "tool-grounded verification." LLM self-evaluation without external feedback is unreliable (3 independent confirmations). With external feedback (web search, code execution), it works.

---

## Sources

### Grade A (Peer-Reviewed, Top Venues)
- Du et al. "Improving Factuality and Reasoning" (ICML 2024) — [arXiv:2305.14325](https://arxiv.org/abs/2305.14325)
- Wang et al. "Rethinking Multi-Agent Discussion" (ACL 2024) — [arXiv:2402.18272](https://arxiv.org/abs/2402.18272)
- Khan et al. "Debate Improves Truthfulness" (ICML 2024 Best Paper) — [arXiv:2402.06782](https://arxiv.org/abs/2402.06782)
- Huang et al. "LLMs Cannot Self-Correct Reasoning Yet" (ICLR 2024) — [arXiv:2310.01798](https://arxiv.org/abs/2310.01798)
- Kamoi et al. "When Can LLMs Self-Correct" (TACL 2024) — [arXiv:2406.01297](https://arxiv.org/abs/2406.01297)
- Trivedi et al. "IRCoT: Interleaving Retrieval with CoT" (ACL 2023) — [arXiv:2212.10509](https://arxiv.org/abs/2212.10509)
- Jiang et al. "FLARE: Active Retrieval Augmented Generation" (EMNLP 2023) — [arXiv:2305.06983](https://arxiv.org/abs/2305.06983)
- Asai et al. "Self-RAG" (ICLR 2024) — [arXiv:2310.11511](https://arxiv.org/abs/2310.11511)
- Liu et al. "Lost in the Middle" (TACL 2024) — [arXiv:2307.03172](https://arxiv.org/abs/2307.03172)
- Madaan et al. "Self-Refine" (NeurIPS 2023) — [arXiv:2303.17651](https://arxiv.org/abs/2303.17651)
- Besta et al. "Graph of Thoughts" (AAAI 2024) — [arXiv:2308.09687](https://arxiv.org/abs/2308.09687)
- Wei et al. "SAFE: LLM Agents for Factuality" (NeurIPS 2024) — [arXiv:2403.18802](https://arxiv.org/abs/2403.18802)
- Panickssery et al. "LLM Self-Preference Bias" (NeurIPS 2024) — [arXiv:2404.13076](https://arxiv.org/abs/2404.13076)
- Farquhar et al. "Semantic Entropy" (Nature 2024) — [doi:10.1038/s41586-024-07421-0](https://www.nature.com/articles/s41586-024-07421-0)
- NAACL 2024 "Confidence Calibration Survey" — [ACL Anthology](https://aclanthology.org/2024.naacl-long.366/)
- Wang et al. "Self-Consistency" (ICLR 2023) — [arXiv:2203.11171](https://arxiv.org/abs/2203.11171)
- Min et al. "FActScore" (EMNLP 2023) — [arXiv:2305.14251](https://arxiv.org/abs/2305.14251)
- ColMAD "Adversarial Multi-Agent Debate" (EMNLP 2024) — [ACL Anthology](https://aclanthology.org/2024.findings-emnlp.407/)

### Grade B (Strong Preprints, Industry Reports)
- RQ-RAG (2024) — [arXiv:2404.00610](https://arxiv.org/abs/2404.00610)
- FAIR-RAG (2025) — [arXiv:2510.22344](https://arxiv.org/abs/2510.22344)
- PRISM (2025) — [arXiv:2510.14278](https://arxiv.org/abs/2510.14278)
- Jiang et al. "Contrastive Reasoning" (2024) — [arXiv:2403.08211](https://arxiv.org/abs/2403.08211)
- Mollick et al. "Expert Personas Don't Help" (Wharton 2025) — [SSRN:5879722](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5879722)
- Wharton GAIL "CoT Decreasing Value" — [Report](https://gail.wharton.upenn.edu/research-and-insights/tech-report-chain-of-thought/)
- Anthropic "Multi-Agent Research System" — [Blog](https://www.anthropic.com/engineering/multi-agent-research-system)
- Anthropic "Context Engineering" — [Blog](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- Claude 4.x Best Practices — [Docs](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-4-best-practices)
- DeepResearchBench — [Website](https://deepresearch-bench.github.io/)
- Tow Center Citation Study — [Nieman Lab](https://www.niemanlab.org/2025/03/ai-search-engines-fail-to-produce-accurate-citations-in-over-60-of-tests-according-to-new-tow-center-study/)
- Instruction Competition (2025) — [arXiv:2505.13360](https://arxiv.org/abs/2505.13360)
- Context Length Hurts (2025) — [arXiv:2510.05381](https://arxiv.org/abs/2510.05381)
- 2025 Self-Correction Benchmark — [arXiv:2510.16062](https://arxiv.org/abs/2510.16062)
- LLM-as-Judge Survey (2024) — [arXiv:2411.15594](https://arxiv.org/abs/2411.15594)
- Bias in LLM-as-Judge (NeurIPS 2024) — [arXiv:2410.02736](https://arxiv.org/abs/2410.02736)

### Grade C (Practitioner Content)
- MLOps Community "Prompt Bloat Impact" — [Blog](https://mlops.community/the-impact-of-prompt-bloat-on-llm-output-quality/)
- CIP "LLM Judges Are Unreliable" — [Blog](https://www.cip.org/blog/llm-judges-are-unreliable)
- Humanloop "Structured Outputs" — [Blog](https://humanloop.com/blog/structured-outputs)

---

*Full stream reports: `RESEARCH/dr-optimization-validation/07_working_notes/agent_outputs/`*
*Research conducted: 2026-02-10*
