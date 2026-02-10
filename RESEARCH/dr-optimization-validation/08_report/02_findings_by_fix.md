# Detailed Evidence Findings by Proposed Fix

---

## Fix 1: Isolated C1 Verification Paths

### Evidence FOR
- Du et al. (ICML 2024): Multi-agent debate yields +7.8 pts factual accuracy, +14.8 pts arithmetic accuracy [Grade A]
- Khan et al. (ICML 2024 Best Paper): Debate improves truthfulness by +28 percentage points for non-experts [Grade A]
- ChatEval (ICLR 2024): Multi-agent with diverse roles improves +6.2% alignment with human preference [Grade A]
- 3 agents × 2 rounds is the empirical sweet spot (Du et al.) [Grade A]

### Evidence AGAINST
- **Wang et al. (ACL 2024): Single agent with strong demonstrations MATCHES 6-agent discussion** — 75.63% vs 74.46% average. Multi-agent only wins when prompts are weak [Grade A]
- Huang et al. (ICLR 2024): Self-correction without external feedback drops CommonSenseQA from 75.8% to 38.1% [Grade A]
- Kamoi et al. (TACL 2024): No study demonstrates successful self-correction without external feedback [Grade A]
- ColMAD (EMNLP 2024): Multi-agent error detection only +4% over single agent; adversarial attack causes -40% [Grade A]
- Self-preference bias of 0.520 (Panickssery et al., NeurIPS 2024): LLMs favor their own outputs structurally [Grade A]

### Net Assessment
**Isolated agents are better than single-agent self-consistency, but the gain is modest (+4-7%) and fragile.** The transformative improvement comes from *external tool grounding*, not context isolation. Google's SAFE achieves superhuman factuality at $0.19/response by combining LLM reasoning with web search verification [Grade A, NeurIPS 2024].

### Recommended Redesign
Keep 3 isolated agents, but make at least 2 of the 3 paths use **external tools** (web search for counter-evidence, web search for independent confirmation) rather than just reasoning over cached evidence. The Inverse Query agent should actively search the web, not just reason over the evidence index.

---

## Fix 2: Site-Targeted Search Queries

### Evidence FOR
- Domain-specific databases (PubMed, SEC EDGAR) contain higher-quality content by definition
- Anthropic documented that agents favor "SEO-optimized content farms over authoritative sources" without explicit heuristics [Grade B]

### Evidence AGAINST
- One study found specialized medical search engines "no better than general search engines" (Gusenbauer 2020) [Grade B]
- Perplexity's architecture explicitly prioritizes "comprehensiveness over precision" at retrieval stage [Grade B]
- Site-targeting restricts the search space, risking recall loss on cross-domain topics
- DeepResearchBench: "Regular mode with web search often outperformed dedicated deep research tools" [Grade B]

### Net Assessment
**Mixed evidence. Site-targeting improves precision for known-quality domains but at the cost of recall.** All competitive tools use broad retrieval first, then aggressive reranking — not restricted search.

### Recommended Change
Downgrade from primary strategy to supplementary. Run broad queries first, then add 1-2 site-targeted queries per domain as a quality supplement. Don't restrict the primary search.

---

## Fix 3: Research Contract Binding

### Evidence FOR
- Gemini Deep Research's distinguishing feature is human-in-the-loop plan approval before execution — this is functionally equivalent to a binding research contract [Grade A]
- Anthropic recommends passing condensed structured context (1,000-2,000 tokens) between sub-agents [Grade B]
- "Retrieve-then-solve" strategy improved GPT-4o by up to 4% on RULER benchmarks [Grade B]
- Structurally passing upstream decisions downstream is a core pattern in all competitive tools

### Evidence AGAINST
- No direct study compares "binding contract" vs "advisory contract" in LLM pipelines
- Risk of over-constraining: if the contract is wrong, all downstream phases are locked into a wrong framing

### Net Assessment
**Supported by competitive practice and indirect evidence.** The contract should bind structural decisions (which subquestions to pursue, which beliefs to challenge) but not lock in specific search strategies.

### Recommended: Keep as designed, with escape valve
Add an explicit "contract violation with justification" mechanism — if Phase 3 discovers something that contradicts the contract assumptions, it can deviate with documented reasoning.

---

## Fix 4: Non-Generic Synthesis (Contrastive Prompting)

### Evidence FOR
- **Contrastive prompting improved GSM8K accuracy from 35.9% to 88.8% (+52.9%)** (Jiang et al. 2024) [Grade B]
- Persona/expert role prompting does NOT improve factual accuracy (Mollick et al. 2025, Wharton) — decision-context anchoring is superior [Grade B]
- Structured output schemas jump format compliance from 35.9% to 100% [Grade B]
- Self-Refine (generate-critique-refine) shows +20% average improvement across 7 tasks (Madaan et al., NeurIPS 2023) [Grade A]

### Evidence AGAINST
- Contrastive prompting evidence is mostly from math/reasoning tasks, not open-ended synthesis
- No published study tests "anchoring synthesis to user's stated beliefs" specifically
- CoT is losing value for frontier models: only +2.9-3.1% gains at 20-80% time increase (Wharton 2025) [Grade B]

### Net Assessment
**Supported, with caveats about transfer from reasoning to synthesis tasks.** Contrastive prompting ("what's uniquely true vs generically true") is the best-evidenced technique for non-generic output. Decision-context anchoring (tying findings to user's specific decision) is supported by negative evidence against persona prompting.

### Recommended: Implement with these specific patterns
1. Contrastive: "What is uniquely true about THIS situation vs. generically true of the category?"
2. Belief-anchoring: "The user believed X at Y% confidence. The evidence [confirms/challenges] this because..."
3. Decision-anchoring: "For your decision about [specific action], this means..."
4. Drop persona prompting — it doesn't help factual accuracy

---

## Fix 5: Iterative Query Refinement

### Evidence FOR (THE STRONGEST EVIDENCE BASE OF ANY FIX)
- IRCoT (ACL 2023): **+21 points retrieval, +15 points QA** on multi-hop benchmarks [Grade A]
- RQ-RAG (2024): **+22.6% average** on multi-hop QA datasets [Grade B]
- FLARE (EMNLP 2023): Superior to all single/multi retrieval baselines [Grade A]
- FAIR-RAG (2025): **+8.3 F1 points** over strongest iterative baseline [Grade B]
- Self-RAG (ICLR 2024): Outperforms ChatGPT and RAG-augmented Llama2 [Grade A]
- PRISM: **90.9% recall** vs 61.5% single-query on HotpotQA [Grade B]
- Terminology bootstrapping: **+10-24% NDCG@10** over traditional methods [Grade B]

### Evidence AGAINST
- Over-refinement diminishing returns: strongest models show decreased performance with excessive rewriting [Grade B]
- Each refinement step adds latency and token cost
- Requires analyzing intermediate results, adding pipeline complexity

### Net Assessment
**THE single most evidence-backed fix. Six peer-reviewed studies converge on +5 to +22 point improvements.** This should be the #1 implementation priority.

### Recommended Implementation
1. After first retrieval batch per subquestion, analyze what was found and what's missing
2. Extract domain-specific terminology from high-quality early results
3. Generate refined follow-up queries using learned vocabulary
4. Cap at 2 refinement rounds (diminishing returns beyond that)
5. Use quality of initial results to decide whether refinement is needed (if A/B sources found, may skip)

---

## Fix 6: Evidence-Based Suggestion Generation

### Evidence FOR
- Structured output with required attribution fields eliminates boilerplate and forces grounding [Grade B]
- RARR preserved >90% content intent while improving attribution [Grade A]
- All competitive tools struggle with actionable recommendations — this is a real gap
- Evidence-strength grading aligns with how clinical guidelines work (GRADE methodology)

### Evidence AGAINST
- No direct study on "LLM evidence-based recommendation generation" as a distinct technique
- LLMs tend to produce generic best practices regardless of specific evidence (documented across all tools)
- Conditional suggestions ("if X then Y") add complexity that may reduce clarity

### Net Assessment
**Supported by indirect evidence and competitive gap analysis.** No tool does this well, which means doing it well is a genuine differentiator — but it's also hard and there's no proven playbook.

### Recommended: Implement with structured output enforcement
1. Require JSON schema: `{"finding": "...", "suggestion": "...", "evidence_cited": "...", "evidence_strength": "STRONG|MODERATE|WEAK", "applies_because": "..."}`
2. Force the model to fill every field — structured output compliance goes to 100%
3. Add explicit labels: EVIDENCE-SUPPORTED / INFERENCE / GENERAL BEST PRACTICE
4. Include "what this does NOT tell us" per recommendation

---

## Fix 7: Binary Checklists (Replace 1-10 Scoring)

### Evidence FOR
- LLM judges achieve **0.989-0.990 reliability on binary tasks** but only **0.421-0.732 on scalar evaluation** [Grade B]
- Scale format dramatically affects results: numerical 1-5 scored 1.68 vs categorical A-E scored 3.17 on identical content [Grade C]
- Position bias shifts scalar scores >10%; less impact on binary [Grade A]
- Pairwise comparisons > absolute scoring for human alignment (LLM-as-Judge survey) [Grade B]

### Evidence AGAINST
- Limited direct studies on binary vs scalar for *claim verification* specifically
- Binary loses granularity that may matter for prioritization

### Net Assessment
**Supported.** Binary/ternary classification is more reliable than scalar scoring for LLM self-evaluation. Replace "7/10" with "YES/NO" or "SUPPORTED/CONTRADICTED/UNCERTAIN."

---

## Fix 8: Source Diversity Gate

### Evidence FOR
- Triangulation across source types is a foundational research methodology principle [Grade C]
- DeepResearchBench: Gemini's 111 citations correlated with highest overall quality score [Grade B]
- Anthropic documented SEO-content-farm bias without explicit diversity heuristics [Grade B]

### Evidence AGAINST
- Five outlets reprinting the same wire story = diverse in name, not substance
- Forcing diversity may reduce quality if best sources cluster in one type
- More beneficial for complex research (Type C/D) than simple lookups (Type A)

### Net Assessment
**Moderately supported.** Implement as anti-SEO heuristic rather than hard gate. Require that the agent explicitly checks whether all sources trace to the same original.

---

## Fix 9: Honest Independence Estimation

### Evidence FOR
- Acknowledging that independence is hard to assess is more honest than binary claims
- Heuristic-based approaches (shared URLs, authors, dates, data points) are more reliable than LLM judgment

### Evidence AGAINST
- **No evidence that LLMs can reliably assess source independence** [HIGH confidence finding from Stream 5]
- LLM reasoning about provenance chains, funding structures, and methodological relationships is unreliable
- "Independence checks that rely on LLM judgment alone are largely theatrical" [Stream 5 conclusion]

### Net Assessment
**The proposed fix (HIGH/MEDIUM/LOW confidence levels) is better than binary, but still fundamentally limited.** LLM judgment of independence is unreliable regardless of how you grade it.

### Recommended Redesign
Replace LLM-judged independence with **structural heuristics**:
- Same domain/URL → DEPENDENT
- Same author names → DEPENDENT
- Same unique statistics/numbers → DEPENDENT (likely citing same original)
- Different publication dates + different methodologies + different organizations → LIKELY INDEPENDENT
- When uncertain, say "INDEPENDENCE UNCERTAIN" rather than guessing

---

## Fix 10: Split 930-Line Prompt (Promoted from Tier 3 to Tier 1)

### Evidence FOR
- **Reasoning degrades at ~3,000 tokens** (MLOps Community); 930 lines ≈ 3,000-4,650 tokens [Grade C]
- **Lost in the Middle** (Liu et al., TACL 2024): U-shaped attention; middle content degraded [Grade A]
- **Input length alone degrades performance** even with perfect retrieval (arXiv 2025) [Grade B]
- **19 competing requirements dropped GPT-4o from 98.7% to 85.0%** [Grade B]
- **Bayesian prompt optimization: +3.8% performance from 41-45% length reduction** [Grade B]
- **Claude 4.x is "more responsive to system prompt"** — aggressive phrasing causes overtriggering [Grade B]

### Evidence AGAINST
- Modern context windows are 128K-1M tokens; 930 lines is small in absolute terms
- Lost-in-the-middle is less severe in Claude models (Anthropic's own testing)
- Splitting increases complexity of the orchestration layer

### Net Assessment
**Strongly supported.** The prompt is at the threshold where instruction competition becomes measurable. The fix should be:
1. **Prune first** — remove instructions Claude follows naturally, aggressive "CRITICAL: You MUST" language
2. **Then split** — load phase-specific instructions only when entering that phase
3. Expected gain: +3-5% instruction following from pruning alone

---
