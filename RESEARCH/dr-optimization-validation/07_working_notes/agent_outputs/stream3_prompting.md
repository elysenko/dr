# Stream 3: Prompt Engineering, Length Degradation, and Synthesis Quality

## Research Sub-Questions Investigated

1. Does prompt length degrade LLM instruction following? At what point?
2. What makes LLM synthesis non-generic and targeted?
3. What prompt patterns produce sharp insights vs boilerplate?
4. Does multi-phase pipeline outperform single-pass?
5. Does structurally passing upstream context improve coherence?

---

## 1. Prompt Length vs. Instruction Following

### 1.1 The "Lost in the Middle" Phenomenon

**Core Finding (C1):** LLMs exhibit a U-shaped performance curve where information at the beginning and end of context is processed most reliably, while information in the middle is significantly degraded.

- **Liu et al. (2023)** demonstrated this definitively across multi-document QA and key-value retrieval tasks. Performance was highest when relevant information appeared at the beginning or end of input context, and "significantly degrades when models must access relevant information in the middle of long contexts." Published in *Transactions of the Association for Computational Linguistics* (2024). [Source: [Lost in the Middle - arXiv](https://arxiv.org/abs/2307.03172), [ACL Anthology](https://aclanthology.org/2024.tacl-1.9/)]

- **Independent confirmation:** Anthropic's own benchmarking shows Claude Instant has a "monotonic inverse relationship between accuracy and passage distance from prompt end," while Claude 2 shows "slight mid-document dip at 95K tokens." [Source: [Anthropic Long Context Prompting](https://www.anthropic.com/news/prompting-long-context)]

**Verified independently by multiple research groups. High confidence.**

### 1.2 Context Length Degrades Performance Even With Perfect Retrieval

**Core Finding (C1):** Input length alone damages LLM performance, independent of retrieval quality and without any distraction from irrelevant content.

- **Key evidence:** When researchers tested with whitespace distractors (minimally distracting) and even with all distraction tokens *masked* (forcing attention only on evidence and questions), both Llama-3.1-8B and Mistral-v0.3-7B still exhibited consistent performance degradation. Llama's HumanEval accuracy dropped 50% at 30K masked tokens. [Source: [Context Length Alone Hurts LLM Performance](https://arxiv.org/html/2510.05381v1)]

- Even models claiming 128K token support experience degradation beyond 10% of their input capacity. [Source: [Needle in Haystack Medium Article](https://medium.com/@imrohitkushwaha2001/needle-in-a-haystack-evaluating-llm-performance-in-long-context-retrieval-99bf2887d974)]

- LLMs show "degradation in reasoning performance at around 3,000 tokens," well below context window limits. This threshold represents measurable performance decline. [Source: [MLOps Community - Prompt Bloat](https://mlops.community/the-impact-of-prompt-bloat-on-llm-output-quality/)]

**Critical implication for a 930-line system prompt:** At roughly 3-5 tokens per line, a 930-line prompt is approximately 3,000-4,650 tokens. This falls right at the threshold where reasoning degradation begins according to the MLOps Community analysis.

### 1.3 Instruction Density and Following Capacity

**Core Finding (C1):** LLM instruction-following performance degrades predictably as the number of constraints increases, with three distinct degradation patterns depending on model architecture.

- **Jaroslawicz et al. (2025)** tested 20 state-of-the-art models with up to 500 instructions and found three patterns:
  - **Threshold decay** (reasoning models like o3, gemini-2.5-pro): Near-perfect performance through 150+ instructions, then steeper decline
  - **Linear decay** (gpt-4.1, claude-3.7-sonnet): Steady, predictable decline across the entire spectrum
  - **Exponential decay** (gpt-4o, llama-4-scout): Rapid early degradation, stabilizing at low accuracy floors (7-15%)
  - Even the best model (gemini-2.5-pro) achieved only 68.9% accuracy at 500 instructions
  [Source: [How Many Instructions Can LLMs Follow at Once?](https://arxiv.org/html/2507.11538v1)]

- **RECAST research** found "consistent performance degradation across all models as constraint complexity increases." Most datasets test only 3-5 constraints; performance drops are significant beyond that. [Source: [RECAST - arXiv](https://arxiv.org/html/2505.19030v2)]

- **Underspecification paradox:** Adding more requirements actually harms performance. GPT-4o's accuracy dropped from 98.7% (individual requirements) to 85.0% (19 requirements together). ~37.5% of requirements showed >5% drops when competing with other specifications. A Bayesian optimizer improved performance by 3.8% while *reducing* prompt length by 41-45%. [Source: [What Prompts Don't Say - arXiv](https://arxiv.org/html/2505.13360v1)]

### 1.4 System Prompt Length Recommendations

**Practical Guidance (C2):**

- **Anthropic's official position:** "Find the smallest possible set of high-signal tokens that maximize the likelihood of some desired outcome." Context should be "treated as a finite resource with diminishing marginal returns." [Source: [Anthropic Context Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)]

- **Recommended system prompt budget:** No more than 5-10% of total context window for system prompts. Model degradation occurs at 80-90% window usage; use only 70-80% of full context. Most production use cases work within 8K-32K tokens with curated context. [Source: [DEV Community - Prompt Length vs Context Window](https://dev.to/superorange0707/prompt-length-vs-context-window-the-real-limits-behind-llm-performance-3h20)]

- A well-structured 16K-token prompt with RAG outperformed a monolithic 128K-token prompt in both accuracy and relevance. [Source: [PromptLayer - Disadvantage of Long Prompts](https://blog.promptlayer.com/disadvantage-of-long-prompt-for-llm/)]

- **Claude 4.x specific:** "Start by testing a minimal prompt with the best model available to see how it performs on your task, and then add clear instructions and examples." Claude Opus 4.6 is "more responsive to the system prompt" and may overtrigger on aggressive language that was needed for older models. [Source: [Claude 4 Best Practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-4-best-practices)]

### 1.5 Is a 930-Line Prompt Too Long?

**Assessment (C2):** A 930-line system prompt (~3,000-4,650 tokens) sits at the threshold of measurable reasoning degradation. Whether this is "too long" depends on:

1. **Token count matters more than line count.** 930 sparse lines may be fewer tokens than 200 dense lines.
2. **Relevance is critical.** Irrelevant information is actively harmful -- LLMs can recognize irrelevant content but fail to ignore it during generation ("identification without exclusion" problem). [Source: [MLOps Community](https://mlops.community/the-impact-of-prompt-bloat-on-llm-output-quality/)]
3. **Claude 4.x handles instructions more literally** and may overtrigger on aggressive phrasing like "CRITICAL: You MUST..." that was needed for older models. [Source: [Claude 4 Best Practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-4-best-practices)]
4. **Diminishing returns are real.** The underspecification research shows that intelligently choosing *which* requirements to include improved performance 3.8% while reducing prompt length 41-45%. [Source: [What Prompts Don't Say - arXiv](https://arxiv.org/html/2505.13360v1)]

**Bottom line:** The prompt is not catastrophically long for a 200K-token context model, but it almost certainly contains instructions that compete with each other, producing instruction dilution. Selective pruning based on which instructions the model naturally follows without prompting would likely improve performance while reducing length.

---

## 2. What Makes LLM Synthesis Non-Generic

### 2.1 Chain-of-Thought: Diminishing Returns

**Core Finding (C1):** Chain-of-thought prompting's value is decreasing as models improve, and it does not universally improve output quality.

- **Wharton Generative AI Labs (Meincke, Mollick et al., 2025)** tested 198 PhD-level questions across 8 models with 25 trials each:
  - Non-reasoning models: Variable results. Best gain was 13.5% (Gemini Flash 2.0); worst was a 17.2% *decrease* in perfect accuracy (Gemini Pro 1.5)
  - Reasoning models: Marginal gains only (o3-mini: 2.9%, o4-mini: 3.1%). Gemini Flash 2.5 showed a 3.3% *decrease*
  - Time cost: 35-600% increase for non-reasoning models, 20-80% for reasoning models
  - "Many models perform CoT-like reasoning by default," making explicit CoT potentially redundant
  [Source: [Wharton Tech Report - Chain of Thought](https://gail.wharton.upenn.edu/research-and-insights/tech-report-chain-of-thought/), [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5285532)]

- **Implication for synthesis:** Explicit "think step by step" instructions may not improve synthesis quality and may introduce errors on questions the model would otherwise get right. For frontier models, CoT is already internalized.

### 2.2 Expert Personas: No Effect on Factual Accuracy

**Core Finding (C1):** Telling LLMs to "act as an expert" does not improve factual accuracy and sometimes degrades it.

- **Wharton Prompting Science Report 4 (Basil, Mollick et al., 2025):** Tested 6 models on GPQA Diamond and MMLU-Pro:
  - In-domain expert personas had "no significant impact on performance" (exception: Gemini 2.0 Flash)
  - Domain-mismatched expert personas sometimes degraded performance
  - Low-knowledge personas ("act as a student") often reduced accuracy
  - This contradicts official guidance from Google, Anthropic, and OpenAI that recommend persona prompting
  [Source: [SSRN - Prompting Science Report 4](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5879722), [Wharton GAIL](https://gail.wharton.upenn.edu/research-and-insights/playing-pretend-expert-personas/)]

- **However, personas affect style:** "Personas clearly work for guiding tone or style when using LLMs for writing tasks." [Source: [PromptHub - Role Prompting](https://www.prompthub.us/blog/role-prompting-does-adding-personas-to-your-prompts-really-make-a-difference)]

**Implication:** For research synthesis, persona prompting won't improve factual accuracy but can steer output style. Replacing "You are an expert researcher" with specific behavioral instructions is likely more effective.

### 2.3 Contrastive Prompting: Generating Unique Insights

**Core Finding (C1):** Contrastive prompting -- asking LLMs to generate both correct and incorrect answers -- significantly improves reasoning and can produce more distinctive outputs.

- **Jiang et al. (2024):** "Large Language Models are Contrastive Reasoners"
  - Simple trigger: "Let's give a correct and a wrong answer"
  - GSM8K: 35.9% -> 88.8% accuracy (GPT-4)
  - AQUA-RAT: 41.3% -> 62.2% (GPT-4)
  - Outperformed zero-shot CoT on 4/6 arithmetic tasks
  - Requires no manual annotation of examples
  - Combining with CoT (Zero-shot-CoT-CP) yielded optimal results
  [Source: [LLMs are Contrastive Reasoners - arXiv](https://arxiv.org/html/2403.08211v1)]

**Implication for synthesis quality:** The contrastive pattern -- explicitly asking "what's uniquely true about THIS situation vs. generically true" -- can be adapted for research synthesis. Instead of "summarize findings," prompt "What findings are unique to this topic vs. what would be true of any similar topic?"

### 2.4 Context Anchoring and Specificity

**Core Finding (C2):** Providing specific user context, decision stakes, and constraints produces more targeted output than generic instructions.

- Structured prompts specifying audience, purpose, format, and constraints generate more actionable insights than open-ended requests. [Source: [Prompt Engineering Guide](https://www.promptingguide.ai/guides/context-engineering-guide)]

- "Contextual alignment was critical to the perceived usefulness of generated outputs." When prompts matched domain vocabulary, roles, and user realities, outputs were more useful. [Source: [Proto-Personas Through Prompt Engineering - arXiv](https://arxiv.org/html/2507.08594v1)]

- The COSTAR framework (Context, Objective, Style, Tone, Audience, Response) treats prompt writing as "a full-stack design challenge" and consistently produces more targeted outputs than unstructured prompting. [Source: [Parloa - Prompt Engineering Frameworks](https://www.parloa.com/knowledge-hub/prompt-engineering-frameworks/)]

**Key technique:** Rather than persona-based prompts, anchor the LLM to *the specific decision context*. "The user needs to decide whether to invest in X or Y" produces more targeted analysis than "You are a financial analyst."

### 2.5 Structured Output and Schema Enforcement

**Core Finding (C2):** Structured output schemas dramatically reduce generic responses by constraining the response space.

- Before structured outputs, getting LLMs to follow specific formats via prompting was ~35.9% reliable; with strict mode schema enforcement, it's 100% reliable. [Source: [Humanloop - Structured Outputs](https://humanloop.com/blog/structured-outputs)]

- JSON Schema-guided approaches "reduce hallucinations, ensuring that unexpected data is less likely to appear and only relevant information is included." [Source: [Generating Structured Outputs - arXiv](https://arxiv.org/html/2501.10868v1)]

**Implication:** Requiring structured output (e.g., JSON with specific fields for "unique_finding," "evidence," "confidence," "implication") forces the model to populate each field rather than generating boilerplate paragraphs.

---

## 3. Evidence-Based Recommendation Generation

### 3.1 Grounded Generation and Attribution

**Core Finding (C2):** Explicit attribution requirements in prompts reduce hallucination and increase specificity.

- Attribution approaches require models to provide evidence for claims and discard outputs that cannot be matched to sources, "which reduces hallucinations while allowing users to verify factual claims." [Source: [Lil'Log - Extrinsic Hallucinations](https://lilianweng.github.io/posts/2024-07-07-hallucination/)]

- Practical implementation: Adding inline citation requirements like "cite the source document using [Source: doc_id] for every factual claim" creates accountability that grounds responses in retrieved evidence. [Source: [MLJourney - Reduce Hallucination](https://mljourney.com/how-to-reduce-hallucination-in-llm-applications/)]

- A multi-layered defense combining RAG, prompting for uncertainty acknowledgment, automated validation, and structured outputs provides the strongest grounding. [Source: [MLJourney](https://mljourney.com/how-to-reduce-hallucination-in-llm-applications/)]

### 3.2 Self-Consistency for Verification

**Core Finding (C1):** Self-consistency prompting -- sampling multiple reasoning paths and selecting the most consistent answer -- provides significant accuracy gains without additional training.

- **Wang et al. (2022):** Accuracy gains on GSM8K (+17.9%), SVAMP (+11.0%), AQuA (+12.2%), StrategyQA (+6.4%). Entirely unsupervised, requiring no additional training or annotation. [Source: [Self-Consistency - arXiv](https://arxiv.org/abs/2203.11171)]

- Self-Verification extends this by verifying conclusions against original context through backward verification. [Source: [Self-Verification Prompting](https://learnprompting.org/docs/advanced/self_criticism/self_verification)]

### 3.3 Iterative Refinement (Self-Refine)

**Core Finding (C1):** Multi-turn self-refinement improves output quality by ~20% absolute on average.

- **Madaan et al. (2023):** Self-Refine generates output, provides self-feedback, then refines iteratively. Outputs improved by ~20% absolute on average across 7 tasks, with gains up to 49.2% absolute. No additional training required. [Source: [Self-Refine - arXiv](https://arxiv.org/abs/2303.17651), [Self-Refine Info](https://selfrefine.info/)]

- **RISE (2024):** Recursive Introspection improved LLaMa3-8B by 8.2% and Mistral-7B by 6.6% using only their own generated data. [Source: [RISE - NeurIPS 2024](https://proceedings.neurips.cc/paper_files/paper/2024/file/639d992f819c2b40387d4d5170b8ffd7-Paper-Conference.pdf)]

**Implication:** A generate-then-critique-then-refine pipeline is well-supported by evidence. This directly validates multi-phase approaches that include verification/QA steps.

---

## 4. Multi-Phase Pipeline vs. Single-Pass

### 4.1 Evidence For Multi-Phase Pipelines

**Core Finding (C2):** Multi-phase approaches improve quality for complex tasks, but the advantage comes from task decomposition rather than agent multiplication.

- **Decomposition-based workflows** achieved mean novelty of 4.17/5 vs. 2.17/5 for reflection-based approaches in research idea generation. [Source: [Evaluating Novelty in AI-Generated Research Plans - arXiv](https://arxiv.org/html/2601.09714)]

- **Graph of Thoughts** improved sorting quality by 62% over Tree of Thoughts while reducing costs by >31%. Adaptive GoT achieved up to 46.2% improvement on scientific reasoning (GPQA). [Source: [GoT - arXiv](https://arxiv.org/abs/2308.09687), [AGoT - arXiv](https://arxiv.org/html/2502.05078v1)]

- Self-Refine's iterative generate-feedback-refine cycle improved output by ~20% average. [Source: [Self-Refine](https://selfrefine.info/)]

- A multi-model consortium achieves "higher accuracy via cross-model agreement, reduced bias by incorporating diverse model behaviors." [Source: [Practical Guide for Agentic AI - arXiv](https://arxiv.org/html/2512.08769v1)]

### 4.2 Evidence Against (or Nuancing) Multi-Agent

**Core Finding (C1):** For homogeneous workflows (same model), a single agent can match multi-agent performance at dramatically lower cost.

- **"Rethinking the Value of Multi-Agent Workflow" (2025):** Single-agent matched or exceeded multi-agent on multiple benchmarks:
  - HumanEval: 92.1% (single) vs. 90.1% (multi)
  - MBPP: 81.4% vs. 78.8%
  - HotpotQA: 73.5% vs. 72.1%
  - Cost: $0.020 (single) vs. $0.198 (multi) -- 90% reduction
  - Key distinction: Homogeneous multi-agent (same LLM) can be simulated by single agent with KV cache reuse. Heterogeneous multi-agent (different LLMs) cannot.
  [Source: [Rethinking Multi-Agent Workflow - arXiv](https://arxiv.org/html/2601.12307v1)]

- **"When 'Better' Prompts Hurt" (2025):** Generic prompt improvements can degrade task-specific performance. Extraction accuracy dropped 10%, RAG compliance fell 13% when a generic "helpful assistant" wrapper was added. [Source: [When Better Prompts Hurt - arXiv](https://arxiv.org/html/2601.22025)]

### 4.3 Synthesis: When Multi-Phase Helps

**Assessment (C2):**

Multi-phase pipelines are justified when:
1. **Tasks involve verification** -- generate-then-verify catches errors single-pass misses (Self-Refine: +20%)
2. **Tasks require diverse perspectives** -- decomposition produces more novel outputs (4.17/5 vs. 2.17/5)
3. **Tasks involve structured reasoning** -- GoT/ToT outperform single-pass CoT on complex problems (62% quality improvement)

Multi-phase pipelines are NOT justified when:
1. **Using the same model for all phases** -- single multi-turn session achieves comparable results at 90% lower cost
2. **Phases don't add new information** -- passing the same context through multiple prompts without new evidence is waste
3. **Task is straightforward** -- CoT already shows diminishing returns on simpler tasks

**Key insight for our pipeline:** The plan-retrieve-verify-synthesize architecture is well-supported IF each phase adds genuinely new information (retrieval adds evidence, verification adds cross-checks). The risk is phases that merely reformat context without adding value.

---

## 5. Structurally Enforcing Context Across Phases

### 5.1 Context Engineering Principles

**Core Finding (C2):** Structurally passing context across phases improves coherence, but the key is selectivity -- passing the *right* context, not *all* context.

- **Anthropic's context engineering guidance:** "Context must be treated as a finite resource with diminishing marginal returns." Sub-agent architectures should explore extensively (tens of thousands of tokens) but return condensed summaries of 1,000-2,000 tokens. [Source: [Anthropic Context Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)]

- Context engineering "forces builders to make concrete decisions about what context to pass and when to pass it to the LLM, which eliminates assumptions and inaccuracies." [Source: [Prompt Engineering Guide - Context Engineering](https://www.promptingguide.ai/guides/context-engineering-guide)]

- The STROT Framework demonstrates that "structured prompting and feedback-driven transformation improve reliability and semantic alignment of LLM-based analytical workflows." [Source: [STROT Framework - arXiv](https://arxiv.org/abs/2505.01636)]

### 5.2 Compaction and Selective Passing

**Key Technique (C2):** The most effective approach is not passing the full research contract verbatim through every phase, but compacting it to the most relevant elements for each phase.

- Anthropic recommends "summarize conversations approaching context limits and reinitiate with compressed summaries. Preserve architectural decisions and critical details while discarding redundant outputs." [Source: [Anthropic Context Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)]

- For Claude 4.x specifically: "Use structured formats for state data" (JSON for status/structured info) and "unstructured text for progress notes." [Source: [Claude 4 Best Practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-4-best-practices)]

- The "retrieve-then-solve" strategy (model recites retrieved evidence in condensed form, then reasons over it) improved GPT-4o by up to 4% on RULER benchmarks. [Source: [Context Length Alone Hurts - arXiv](https://arxiv.org/html/2510.05381v1)]

### 5.3 Implications for Research Pipeline

**Assessment (C2):** Passing a structured research contract (scope, hypotheses, decision context) through downstream phases is well-supported -- but it should be:

1. **Condensed, not verbatim.** Pass a 200-token summary of the research contract, not the full document.
2. **Phase-appropriate.** Retrieval phases need scope and queries; synthesis phases need hypotheses and decision context; QA phases need claim taxonomy and evidence standards.
3. **Structured.** Use JSON or structured tags rather than free-text, enabling the model to parse specific fields rather than re-interpreting natural language each time.

---

## 6. Key Prompt Patterns That Produce Sharp vs. Generic Output

### Patterns That Produce Sharp Insights

| Pattern | Evidence | Effect |
|---------|----------|--------|
| **Contrastive analysis** ("What's unique here vs. generically true?") | Jiang et al. 2024: +52.9% on GSM8K | Forces distinctive reasoning |
| **Decision-context anchoring** ("User must decide between X and Y") | COSTAR framework research, context engineering guides | Focuses output on actionable distinctions |
| **Structured output schemas** (JSON with specific required fields) | 35.9% -> 100% format compliance | Eliminates vague boilerplate |
| **Attribution requirements** ("Cite [Source: id] for every claim") | Hallucination reduction surveys | Grounds claims in evidence |
| **Self-refine loops** (generate -> critique -> refine) | Madaan et al.: +20% avg quality | Catches and fixes generic first drafts |
| **Conditional framing** ("If X context, then Y recommendation") | Grounded generation research | Produces situation-specific advice |
| **Bayesian selective prompting** (only specify what the model doesn't naturally do) | 3.8% improvement, 41-45% shorter prompts | Reduces instruction competition |

### Patterns That Produce Generic/Boilerplate Output

| Anti-Pattern | Evidence | Effect |
|--------------|----------|--------|
| **Vague persona** ("Act as an expert analyst") | Mollick et al. 2025: No factual improvement | Wastes tokens, no quality gain |
| **Explicit CoT for frontier models** ("Think step by step") | Wharton report: Marginal gain, 35-600% time cost | Redundant; models already do this |
| **Kitchen-sink system prompts** (every possible instruction) | Underspecification research: 13.7% accuracy drop | Instructions compete, diluting focus |
| **Monolithic long context** (dump everything into prompt) | 16K+RAG > 128K monolithic | Drowns signal in noise |
| **Aggressive meta-instructions** ("CRITICAL: You MUST...") | Claude 4 docs: Causes overtriggering | Counterproductive with modern models |

---

## 7. Summary of Actionable Findings

### For the Deep Research Pipeline Specifically

1. **The 930-line system prompt is at the degradation threshold.** At ~3,000-4,650 tokens, it sits where measurable reasoning degradation begins. The underspecification research strongly suggests pruning to only instructions the model doesn't naturally follow would improve performance while reducing length 41-45%. **Recommendation: Audit each instruction block for whether Claude 4.x follows it without prompting, and remove redundant ones.**

2. **Multi-phase is justified, but only when phases add information.** The plan-retrieve-verify-synthesize architecture is well-supported by Self-Refine (+20%), GoT (+62% over ToT), and decomposition research (4.17/5 vs 2.17/5 novelty). But phases that merely reformat should be eliminated or merged. Single-agent multi-turn can match multi-agent at 90% lower cost for homogeneous workflows.

3. **Passing the research contract through phases works, but condense it.** Pass a 200-token structured summary (JSON/XML), not the full document. Make it phase-appropriate -- retrieval phases get different context than synthesis phases.

4. **To produce sharp synthesis, use contrastive prompting.** Instead of "summarize findings," prompt "What is uniquely true about this topic vs. what would be true of any similar topic?" This is backed by strong empirical evidence (Jiang et al. 2024).

5. **Anchor to the user's decision context, not a persona.** Decision-context framing ("The user needs to decide X") outperforms persona framing ("Act as expert Y") for factual tasks. Personas only help with style/tone.

6. **Require structured output with attribution.** JSON schemas with required fields for evidence, confidence, and source citation eliminate boilerplate more effectively than natural-language instructions to "be specific."

7. **Replace "CRITICAL: You MUST" language.** Claude 4.x models follow instructions more literally and may overtrigger on aggressive language that was needed for older models. Use normal phrasing.

8. **Self-refine loops are well-supported.** The QA/Reflexion phase in the pipeline has strong empirical backing (+20% average improvement). Ensure it's a genuine critique step, not just a formatting pass.

---

## Sources Catalog

### Peer-Reviewed / Academic

| Source | Grade | Key Finding |
|--------|-------|-------------|
| Liu et al. 2023 "Lost in the Middle" (TACL 2024) | A | U-shaped attention; middle content degraded |
| Wang et al. 2022 "Self-Consistency" (ICLR 2023) | A | +17.9% accuracy via multi-path sampling |
| Madaan et al. 2023 "Self-Refine" (NeurIPS 2023) | A | +20% avg via iterative self-feedback |
| Jiang et al. 2024 "Contrastive Reasoners" | B | +52.9% on GSM8K via contrastive prompting |
| Besta et al. 2023 "Graph of Thoughts" (AAAI 2024) | A | +62% quality over ToT on sorting |
| Meincke, Mollick et al. 2025 "Decreasing Value of CoT" | B | CoT marginal for reasoning models, time-costly |
| Basil, Mollick et al. 2025 "Expert Personas" | B | Personas don't improve factual accuracy |
| Jaroslawicz et al. 2025 "How Many Instructions" | B | Three degradation patterns; 68.9% max at 500 instructions |
| "What Prompts Don't Say" (2025) | B | 19 constraints drop accuracy 13.7%; selective specification better |
| "Context Length Alone Hurts" (2025) | B | Length degrades performance even with perfect retrieval |
| "Rethinking Multi-Agent Workflow" (2025) | B | Single agent matches multi-agent at 90% lower cost |
| "When Better Prompts Hurt" (2025) | B | Generic improvements can degrade task-specific performance |
| Yao et al. 2023 "Tree of Thoughts" (NeurIPS 2023) | A | Deliberate problem solving via tree search |
| AGoT (2025) "Adaptive Graph of Thoughts" | B | +46.2% on GPQA scientific reasoning |

### Industry / Technical Reports

| Source | Grade | Key Finding |
|--------|-------|-------------|
| Anthropic "Context Engineering for AI Agents" (2025) | B | Smallest high-signal token set; sub-agent condensation |
| Anthropic "Long Context Prompting" (2023) | B | Scratchpad + examples reduce recall errors 36% |
| Anthropic "Claude 4 Best Practices" (2025-2026) | B | Literal instruction following; reduce aggressive language |
| MLOps Community "Prompt Bloat" (2024) | C | Reasoning degrades at ~3,000 tokens; identification without exclusion |
| PromptLayer "Long Prompt Disadvantage" (2024) | C | 16K+RAG > 128K monolithic |
| Wharton GAIL Labs (multiple reports) | B | Systematic prompting experiments with statistical rigor |

### URLs for All Primary Sources

1. https://arxiv.org/abs/2307.03172
2. https://aclanthology.org/2024.tacl-1.9/
3. https://arxiv.org/html/2510.05381v1
4. https://arxiv.org/html/2507.11538v1
5. https://arxiv.org/html/2505.19030v2
6. https://arxiv.org/html/2505.13360v1
7. https://arxiv.org/html/2403.08211v1
8. https://arxiv.org/abs/2203.11171
9. https://arxiv.org/abs/2303.17651
10. https://arxiv.org/abs/2308.09687
11. https://arxiv.org/html/2502.05078v1
12. https://arxiv.org/html/2601.12307v1
13. https://arxiv.org/html/2601.22025
14. https://gail.wharton.upenn.edu/research-and-insights/tech-report-chain-of-thought/
15. https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5285532
16. https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5879722
17. https://gail.wharton.upenn.edu/research-and-insights/playing-pretend-expert-personas/
18. https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
19. https://www.anthropic.com/news/prompting-long-context
20. https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-4-best-practices
21. https://mlops.community/the-impact-of-prompt-bloat-on-llm-output-quality/
22. https://blog.promptlayer.com/disadvantage-of-long-prompt-for-llm/
23. https://selfrefine.info/
24. https://www.promptingguide.ai/guides/context-engineering-guide
25. https://arxiv.org/html/2512.08769v1
26. https://arxiv.org/html/2601.09714
27. https://arxiv.org/abs/2505.01636
28. https://www.prompthub.us/blog/role-prompting-does-adding-personas-to-your-prompts-really-make-a-difference
29. https://learnprompting.org/docs/advanced/self_criticism/self_verification
30. https://dev.to/superorange0707/prompt-length-vs-context-window-the-real-limits-behind-llm-performance-3h20
