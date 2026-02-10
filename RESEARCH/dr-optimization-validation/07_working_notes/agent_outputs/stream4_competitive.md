# Stream 4: Competitive Analysis — Deep Research Tools

## How Perplexity Pro, Gemini Deep Research, and OpenAI Deep Research Actually Work

Research conducted: 2026-02-10

---

## Table of Contents

1. [Perplexity Pro / Deep Research](#1-perplexity-pro--deep-research)
2. [Gemini Deep Research](#2-gemini-deep-research)
3. [OpenAI Deep Research](#3-openai-deep-research)
4. [Anthropic Claude Advanced Research](#4-anthropic-claude-advanced-research)
5. [Head-to-Head Benchmarks](#5-head-to-head-benchmarks)
6. [Shared Architectural Patterns](#6-shared-architectural-patterns)
7. [Graph of Thoughts vs Alternatives](#7-graph-of-thoughts-vs-alternatives)
8. [Key Takeaways for Our System](#8-key-takeaways-for-our-system)

---

## 1. Perplexity Pro / Deep Research

### Architecture Overview

Perplexity implements a **Retrieval-Augmented Generation (RAG)** architecture at its core, combining live web search, semantic embeddings, document parsing, and multi-step reasoning to deliver source-backed answers.

**Core pipeline** (C1 — verified across multiple sources):

1. **Query decomposition**: Pro Search decomposes complex prompts into sub-queries, follows up with clarifying questions
2. **Hybrid retrieval**: Uses both BM25 (lexical) and vector embeddings for semantic similarity matching
3. **Multi-stage reranking**: Earlier stages use lexical and embedding-based scorers optimized for speed; later stages use cross-encoder reranker models for final result sculpting
4. **On-demand crawling**: Rather than static indexes, employs lightweight crawlers for fresh web data plus API-based structured data ingestion
5. **Source authority evaluation**: Ranks by domain authority, content freshness, and cross-source agreement
6. **Synthesis with inline citations**: Source attribution is embedded directly into the answer generation step

Sources: [Behind Perplexity's Architecture](https://www.frugaltesting.com/blog/behind-perplexitys-architecture-how-ai-search-handles-real-time-web-data), [Perplexity Architecture Overview 2025](https://www.linkedin.com/pulse/perplexityai-architecture-overview-2025-priyam-biswas-3mekc)

### Sonar Deep Research (the API-accessible model)

Sonar Deep Research is Perplexity's research-centric model designed for multi-step, evidence-rich information synthesis. Rather than a single "retrieve-and-generate" step, Sonar:

- Decomposes the research task into many subqueries
- Runs multiple retrieval passes (diverse indexes, web snapshots)
- Compresses documents to claim-level evidence
- Scores each claim by relevance/credibility/recency
- Synthesizes a narrative where each claim traces to quotes and URLs

The backbone model is fine-tuned on Llama 3.1 70B for retrieval tasks. Additional frontier models (GPT-5.x, Claude 4.5, Gemini 3 Pro) are routed to for advanced reasoning, coding, or multimodal tasks.

Sources: [Sonar Deep Research Guide](https://toolkitbyai.com/sonar-deep-research-complete-guide/), [Perplexity Sonar Guide & Benchmarks](https://toolkitbyai.com/perplexity-sonar-complete-guide-2025/)

### Enterprise: Comet Mode (Multi-Agent Framework)

Perplexity's enterprise offering (Comet) uses a coordinated multi-agent research workflow (C2):

- **Retrieval agent**: Uses internal search stack to collect current data
- **Synthesis agent**: Employs GPT-5 or Claude 4.5 for structured insights
- **Verification agent**: Validates citations against live sources before final output

Currently deployed in finance, consulting, and education sectors.

Sources: [Perplexity Models and Modes Late 2025](https://www.datastudios.org/post/perplexity-ai-all-available-models-modes-and-how-they-differ-in-late-2025)

### Accuracy and Hallucination

- **SimpleQA benchmark**: 93.9% accuracy (C1 — cited by multiple sources)
- **Humanity's Last Exam**: 21.1% accuracy (C1)
- **Citation precision**: 99.98% (claimed by Perplexity; C2)
- **Hallucination rate**: ~7% due to strict grounding in real sources (C2)
- **Tow Center study finding**: Perplexity had the **lowest failure rate** among AI search engines tested, answering incorrectly 37% of the time — but notably, "more than half of its citations" were still inaccurate for news-specific queries (C1 — independent study)

**Important caveat**: The Tow Center study (Columbia University, March 2025) found that collectively, **AI search engines are inaccurate 60% of the time** on news citation tasks. Perplexity was the best performer but still had 37% error rate. Gemini and Grok were worst, with Gemini providing "more fabricated links than correct links."

Sources: [Tow Center Study via Nieman Lab](https://www.niemanlab.org/2025/03/ai-search-engines-fail-to-produce-accurate-citations-in-over-60-of-tests-according-to-new-tow-center-study/), [Perplexity AI Review 2025](https://www.glbgpt.com/hub/perplexity-ai-review-2025/), [LLM Hallucination Test](https://www.allaboutai.com/resources/llm-hallucination/)

### Speed

Perplexity completes most deep research tasks in **2-4 minutes** — significantly faster than OpenAI (5-30 min) and Gemini (up to 15 min).

Source: [Helicone Comparison](https://www.helicone.ai/blog/openai-deep-research)

---

## 2. Gemini Deep Research

### Architecture Overview

Gemini Deep Research is powered by Gemini 3 Pro, using a Mixture-of-Experts (MoE) transformer model. It autonomously plans, executes, and synthesizes multi-step research tasks using web search and user data.

### Multi-Step Process (C1 — verified from Google's own documentation):

1. **Planning**: Formulates a detailed research plan, breaking the problem into sub-tasks. Presents the plan to the user for approval before execution (human-in-the-loop)
2. **Execution**: Intelligently determines which sub-tasks can be parallel vs. sequential. Uses search and web browsing tools to fetch and reason over information. At each step, reasons over available information to decide next move
3. **Synthesis**: Critically evaluates information, identifies key themes and inconsistencies, structures report logically. Performs **multiple passes of self-critique** to enhance clarity and detail

Sources: [Google Blog on Deep Research](https://blog.google/products/gemini/google-gemini-deep-research/), [Gemini Deep Research API Docs](https://ai.google.dev/gemini-api/docs/deep-research), [Google Gemini Deep Research Guide](https://www.digitalapplied.com/blog/google-gemini-deep-research-guide)

### Key Architectural Features

- **Asynchronous task manager**: A novel system that maintains shared state between planner and task models, allowing graceful error recovery without restarting entire tasks (C2)
- **Specifically trained** to reduce hallucinations and maximize report quality during complex tasks
- **Source evaluation**: Prioritizes authoritative content, downranks low-quality pages; analyzes 100+ sources per research task
- **Maximum research time**: 60 minutes (most tasks complete within 20 minutes)
- **Multi-modal**: Can reason over text, images, and other input types simultaneously

Sources: [9to5Google on Deep Research](https://9to5google.com/2025/12/11/gemini-deep-research-agent/), [Build with Gemini Deep Research](https://blog.google/innovation-and-ai/technology/developers-tools/deep-research-agent-gemini-api/)

### Developer API Access

Available via the Interactions API with background execution mode (set `background=true`) for async polling. Returns an interaction ID for the client to disconnect without timeouts and poll asynchronously.

Source: [Gemini Deep Research API](https://ai.google.dev/gemini-api/docs/deep-research)

### Benchmark Performance (C1 — Google's published numbers, December 2025)

- **Humanity's Last Exam (HLE)**: 46.4% — state-of-the-art at time of publication
- **DeepSearchQA**: 66.1% (Google's own benchmark for comprehensive web research)
- **BrowseComp**: 59.2% (OpenAI's browsing benchmark)

These results surpass earlier models and represent the top tier of deep research performance.

Source: [Google Rolls Out Gemini Deep Research](https://www.therift.ai/news-feed/google-rolls-out-gemini-deep-research-and-open-sources-deepsearchqa-benchmark), [9to5Google](https://9to5google.com/2025/12/11/gemini-deep-research-agent/)

### Accuracy in Practice

Mixed real-world results. One systematic fact-check found reports "to be accurate," but the system also "relied on several sources that didn't include research-backed or survey-backed facts" and struggled when combining multiple data sources, making "logic errors that forgot some research and only used certain data points."

Source: [LivePlan Deep Research Test](https://www.liveplan.com/blog/planning/deep-research-chatgpt-vs-gemini)

---

## 3. OpenAI Deep Research

### Architecture Overview

Built on a specialized version of OpenAI's **o3 reasoning model**, trained via end-to-end reinforcement learning on complex browsing and reasoning tasks. Has an "expanded attention span" that maintains focus through long chains of thought — sometimes involving **hundreds of reasoning steps**.

Source: [PromptLayer: How Deep Research Works](https://blog.promptlayer.com/how-deep-research-works/)

### The Agent Loop (C1 — verified across multiple sources)

Follows the classic **Plan-Act-Observe (ReAct) paradigm**:

1. **Plan**: Model determines what research steps are needed (often implicit in chain-of-thought reasoning)
2. **Act**: Tool invocation — issuing search queries, fetching webpages, running code
3. **Observe**: Results are analyzed, feeding back into the next iteration

The model learned through reinforcement learning in simulated research environments to:
- Plan and execute multi-step search trajectories
- Backtrack when paths are unfruitful
- Pivot strategies based on new information

Sources: [PromptLayer](https://blog.promptlayer.com/how-deep-research-works/), [ByteBytego](https://blog.bytebytego.com/p/how-openai-gemini-and-claude-use)

### Multi-Phase Research Process

1. **Interactive clarification**: Follow-up questions to ensure accurate task understanding
2. **Query decomposition**: Breaks into sub-questions mapping to required information sections
3. **Iterative web searching**: Progressive query refinement where each result informs subsequent searches
4. **Content analysis**: Handles HTML, PDF files, and images with integrated Python code execution
5. **Synthesis**: Structured reports with inline citations traceable to source text

### Tools Available

- Web search capabilities for real-time queries
- Browser tools for page content extraction and navigation
- Code interpreter for calculations and visualization
- File parsers for PDFs and images

### Hard Limits (C2 — from PromptLayer analysis)

| Parameter | Typical Range |
|-----------|--------------|
| Wall-clock time | 5-30 minutes |
| Search calls | 30-60 queries |
| Page fetches | 120-150 pages |
| Reasoning loops | 150-200 iterations |

### Stopping Mechanisms

**Coverage-based**: Threshold of sources per sub-question met (2+ independent), novelty exhaustion, confidence thresholds reached

**Hard limits**: Wall-clock time, search call caps, page fetch caps, iteration maximums

Source: [PromptLayer](https://blog.promptlayer.com/how-deep-research-works/)

### Benchmark Performance (C1)

- **Humanity's Last Exam**: 26.6% (at launch in Feb 2025 — 183% improvement over prior models)
- **GAIA benchmark**: 72.57% average accuracy (previous top: 63.64%)
- **BrowseComp**: 51.5% (vs GPT-4o with browsing at 1.9%, o1 at 9.9%)
- Perfectly solved 16% of BrowseComp tasks but failed entirely on 14%

Sources: [TechRadar on HLE](https://www.techradar.com/computing/artificial-intelligence/openais-deep-research-smashes-records-for-the-worlds-hardest-ai-exam-with-chatgpt-o3-mini-and-deepseek-left-in-its-wake), [Helicone](https://www.helicone.ai/blog/openai-deep-research), [BrowseComp Paper](https://arxiv.org/html/2504.12516v1)

### Accuracy Concerns

OpenAI Deep Research may "fabricate sources, misinterpret data, or cite incorrect facts — which can be hidden in lengthy reports." It also "struggles with generating novel hypotheses or interpreting nuanced academic discussions."

Human testers rated outputs as "better than intern work" in blind evaluations. One architectural project estimated to require 6-8 hours of human effort produced a comparable 15,000-word analysis.

Sources: [Helicone](https://www.helicone.ai/blog/openai-deep-research), [PromptLayer](https://blog.promptlayer.com/how-deep-research-works/)

---

## 4. Anthropic Claude Advanced Research

### Architecture (C1 — from Anthropic's own engineering blog)

Uses an **orchestrator-worker pattern**:

- **Lead agent** (Claude Opus 4): Analyzes user queries, develops strategy, spawns subagents
- **Subagents** (Claude Sonnet 4): 3-5 subagents in parallel, each independently performing searches, evaluating results, and reporting findings
- **Citation agent**: Processes documents to identify specific claim locations, ensuring all claims are attributed

### Key Design Choices

- **Extended thinking**: Lead agent uses visible thinking as a "controllable scratchpad" for planning and evaluating quality gaps
- **Parallel tool calling**: Subagents use 3+ tools simultaneously, reducing research time by "up to 90% for complex queries"
- **Dynamic search strategy**: Starts with "short, broad queries" before progressively narrowing focus; adapts based on intermediate findings

### Scaling Guidelines

| Task Complexity | Agents | Tool Calls |
|----------------|--------|------------|
| Simple fact-finding | 1 agent | 3-10 tool calls |
| Direct comparisons | 2-4 subagents | 10-15 calls each |
| Complex research | 10+ subagents | Divided responsibilities |

### Performance (C1 — Anthropic's published data)

- Multi-agent system (Opus 4 lead + Sonnet 4 subagents) **outperformed single-agent Opus 4 by 90.2%** on internal research eval
- Token usage: Individual agents use ~4x more tokens than chat; multi-agent systems use ~15x more tokens
- **Token usage alone explains 80% of variance** in BrowseComp evaluation performance
- Number of tool calls and model choice explain the remaining 15%

Source: [Anthropic Engineering Blog](https://www.anthropic.com/engineering/multi-agent-research-system)

---

## 5. Head-to-Head Benchmarks

### Humanity's Last Exam (HLE) — Most Comprehensive Comparison

| System | Score | Date |
|--------|-------|------|
| Gemini Deep Research | **46.4%** | Dec 2025 |
| OpenAI Deep Research | 26.6% | Feb 2025 |
| Perplexity Deep Research | 21.1% | ~Mar 2025 |
| OpenAI o3-mini (high) | 13.0% | Feb 2025 |
| DeepSeek R1 | 9.4% | Feb 2025 |
| Gemini Thinking (earlier) | 6.2% | ~2025 |

**Note**: Gemini Deep Research's 46.4% was published in December 2025, ~10 months after OpenAI's 26.6%. Direct comparison is complicated by temporal gaps. (C1 — scores from respective publishers, but not measured simultaneously)

Sources: [Artificial Analysis HLE Leaderboard](https://artificialanalysis.ai/evaluations/humanitys-last-exam), [Scale AI Leaderboard](https://scale.com/leaderboard/humanitys_last_exam), [Therift.ai](https://www.therift.ai/news-feed/google-rolls-out-gemini-deep-research-and-open-sources-deepsearchqa-benchmark)

### BrowseComp (Hard-to-Find Facts)

| System | Score |
|--------|-------|
| Gemini Deep Research | **59.2%** |
| OpenAI Deep Research | 51.5% |
| o1 | 9.9% |
| GPT-4o (with browsing) | 1.9% |

Source: [9to5Google](https://9to5google.com/2025/12/11/gemini-deep-research-agent/), [BrowseComp Paper](https://arxiv.org/html/2504.12516v1)

### SimpleQA (Factual Accuracy)

| System | Score |
|--------|-------|
| Perplexity Deep Research | **93.9%** |
| Others | Not directly comparable |

Source: [Helicone](https://www.helicone.ai/blog/openai-deep-research)

### Speed Comparison

| System | Typical Time |
|--------|-------------|
| Perplexity Deep Research | **2-4 minutes** |
| Gemini Deep Research | Up to 15 minutes |
| OpenAI Deep Research | 5-30 minutes |

### Cost Comparison

| System | Monthly Cost |
|--------|-------------|
| Gemini Deep Research | $20/month (Advanced) |
| Perplexity Deep Research | Free tier available; Pro ~$20/month |
| OpenAI Deep Research | $200/month (Pro tier) |

Source: [Helicone](https://www.helicone.ai/blog/openai-deep-research)

### Tow Center Citation Study Results (March 2025)

200 news articles tested across 8 AI search engines (C1 — independent academic study):

| System | Error Rate |
|--------|-----------|
| Perplexity | **37%** (best) |
| Perplexity Pro | ~40% |
| ChatGPT Search | ~55% |
| Gemini | ~75% |
| Grok-3 Search | 94% (worst) |

**Overall**: AI search engines are inaccurate 60% of the time on news citation tasks.

Source: [Nieman Lab / Tow Center](https://www.niemanlab.org/2025/03/ai-search-engines-fail-to-produce-accurate-citations-in-over-60-of-tests-according-to-new-tow-center-study/)

### Qualitative Assessments (C2)

- **Perplexity** excels at: Factual transparency, speed, real-time data, inline citations
- **Gemini** excels at: Comprehensive analysis, conservative/reliable for policy questions, multimodal integration, integrated Google Workspace workflows
- **OpenAI** excels at: Deep reasoning, lengthy structured reports, creative analysis
- **All tools** struggle with: Combining multiple data sources, logic errors across extended analyses, novel hypothesis generation

Sources: [Aryabh Consulting Comparison](https://www.aryabhconsulting.com/blog/deep-research-ai-tools-comparison-2025-gemini-vs-chatgpt-vs-perplexity-for-business-research), [CBTW Comparison](https://cbtw.tech/insights/deep-research-tools-comparison-a-side-by-side-evaluation-of-ai-platforms)

---

## 6. Shared Architectural Patterns Across Best Tools

### What the Best Tools Have in Common (C1)

All top-performing deep research tools share these core patterns:

1. **Plan-Execute-Synthesize loop**: Every system decomposes queries into sub-tasks, executes them (often in parallel), then synthesizes results. This is the ReAct paradigm applied to research.

2. **Multi-step iterative retrieval**: None of these tools use a single-shot RAG approach. They all perform multiple rounds of search, with each round informed by prior findings. Perplexity explicitly "runs multiple retrieval passes." OpenAI performs "progressive query refinement." Gemini "browses over hundreds of webpages."

3. **Citation tracking throughout**: All systems track source-content pairs from retrieval through synthesis. Content and citation are paired throughout to ensure every piece of information is traceable.

4. **Source quality evaluation**: All systems evaluate source authority, freshness, and cross-source agreement before inclusion.

5. **Sub-question decomposition**: Every system breaks complex queries into manageable sub-questions, then aggregates answers.

Source: [ByteBytego](https://blog.bytebytego.com/p/how-openai-gemini-and-claude-use)

### Multi-Agent vs Single-Agent

The evidence strongly favors multi-agent approaches:

- Anthropic's multi-agent system **outperformed single-agent by 90.2%** (C1)
- Perplexity's enterprise Comet uses 3 specialized agents (retrieval, synthesis, verification) (C2)
- Token usage explains 80% of BrowseComp performance variance — more agents = more tokens = better results (C1)

**However**: Not all systems use explicit multi-agent architectures:
- OpenAI Deep Research appears to be a **single-agent** system with tool access (o3 model with browsing)
- Perplexity's consumer product is primarily a sophisticated RAG pipeline, not multi-agent
- Gemini Deep Research uses a planner + task execution model, closer to single-agent with parallelism

The distinction matters: You can achieve strong results with a single capable model + sufficient compute. Multi-agent adds overhead (~15x token usage) but improves breadth of coverage.

Sources: [Anthropic Engineering](https://www.anthropic.com/engineering/multi-agent-research-system), [ByteBytego](https://blog.bytebytego.com/p/how-openai-gemini-and-claude-use)

### Verification Approaches

| System | Verification Method |
|--------|-------------------|
| Perplexity (enterprise) | Dedicated verification agent validates citations against live sources |
| Gemini | Multiple passes of self-critique; specifically trained to reduce hallucinations |
| OpenAI | Extended chain-of-thought allows self-checking; no explicit separate verification step visible |
| Anthropic | Citation agent + human evaluation for edge cases |

**Key insight**: No system relies solely on automated verification. All still recommend human oversight for high-stakes applications.

### Hallucination Reduction Techniques

Common across all systems:
1. **Grounding in retrieved sources**: Never generate from parametric memory alone
2. **Citation-first architecture**: Require sources before making claims
3. **Multiple retrieval passes**: Cross-reference across sources
4. **Self-critique / self-consistency**: Multiple reasoning paths to check for agreement

Source: [Anthropic Engineering](https://www.anthropic.com/engineering/multi-agent-research-system)

---

## 7. Graph of Thoughts vs Alternatives for Research Tasks

### Comparative Framework

| Method | Structure | Key Capability | Weakness |
|--------|-----------|---------------|----------|
| **Chain of Thought (CoT)** | Linear sequence | Simple, low cost, effective for straightforward reasoning | Cannot explore alternatives or aggregate |
| **Tree of Thoughts (ToT)** | Branching tree | Can explore multiple paths, backtrack | High compute cost, no aggregation |
| **Graph of Thoughts (GoT)** | Arbitrary graph | Aggregation of thoughts into synergistic solutions | Highest compute cost, complex implementation |
| **Adaptive GoT (AGoT)** | Dynamic graph | Best of all approaches, adapts structure per problem | Newest, less battle-tested |

### Benchmark Results (C1 — from original papers)

**Sorting tasks** (GoT paper, 2023):
- GoT increases quality by **62% over ToT** while reducing costs by **>31%**
- GoT median error ~65% lower than CoT, ~83% lower than IO (direct prompting)

**Adaptive GoT (AGoT) results** (2025):
- GPQA Diamond reasoning: AGoT 57.6% vs CoT 49.0% vs AIoT 48.0%
- HotpotQA retrieval: AGoT 80% vs AIoT 76% vs IO 72%
- MoreHopQA: AGoT 72% (+30.9% improvement over baseline)
- Game of 24: AGoT 50% (+400% vs IO baseline)

Sources: [GoT Paper](https://arxiv.org/abs/2308.09687), [AGoT Paper](https://arxiv.org/html/2502.05078v1)

### When GoT Excels

GoT is best for problems that **decompose into smaller sub-problems whose solutions can be merged**:
- Sorting (merge-based approach)
- Set operations (intersection, union)
- Any task requiring synthesis of multiple independent analyses

GoT is **not clearly better** for:
- Simple Q&A (CoT sufficient, much cheaper)
- Linear reasoning chains (ToT may be better)
- Document merging (less noticeable advantage)
- Tasks where compute cost matters more than accuracy

Source: [Cameron Wolfe's Analysis](https://cameronrwolfe.substack.com/p/graph-based-prompting-and-reasoning)

### Critical Assessment for Research Applications

**GoT's theoretical advantage for research**: Research tasks naturally decompose into sub-questions, and the ability to aggregate findings from multiple sub-investigations into a coherent synthesis is exactly what GoT enables. The "thought aggregation" capability — combining multiple thoughts into a single, better one — maps directly to research synthesis.

**However** (C3): The original GoT paper benchmarked on narrow, well-defined tasks (sorting, set operations). There are **no published benchmarks** comparing GoT to simpler approaches specifically for open-ended research tasks like "analyze the state of X technology." The actual deep research tools (Perplexity, Gemini, OpenAI) use **ReAct-style agent loops** rather than formal GoT, suggesting the industry has found agent loops more practical for research.

**The practical reality**: The most successful research tools use a pattern that is *conceptually similar* to GoT (decompose, explore in parallel, aggregate) but implemented as **agent orchestration** rather than formal graph-based prompting. The key GoT insight — that you need aggregation, not just branching — is correct and valuable. But the implementation is better as multi-agent coordination than as a prompting framework.

### Compute Cost Tradeoff

GoT and ToT "pose computational inefficiencies" due to "heavy reliance on numerous LLM queries, sometimes numbering in the hundreds for a singular problem." This matters when:
- Budget is constrained (cost per research task)
- Latency matters (real-time vs. background)
- Scale is needed (many research tasks per day)

Source: [Demystifying Chains, Trees, and Graphs of Thoughts](https://arxiv.org/abs/2401.14295)

---

## 8. Key Takeaways for Our System

### What We Should Learn from the Best Tools

1. **Multi-step iterative retrieval is table stakes**: Every competitive tool does multiple rounds of search with progressive refinement. Single-pass RAG is insufficient.

2. **Citation tracking from retrieval through synthesis is critical**: The Tow Center study shows even the best tools fail 37% of the time on citation accuracy. Our system MUST track source-claim pairs throughout.

3. **Speed matters more than we might think**: Perplexity dominates developer adoption partly because it's 5-10x faster than competitors. Our system should optimize for speed where possible.

4. **Multi-agent gives 90% improvement but at 15x token cost**: The tradeoff is real. For resource-constrained scenarios, a single capable model with sufficient compute can still perform well. Multi-agent should be the "deep" mode, not the default.

5. **GoT's aggregation insight is correct, but agent loops are the practical implementation**: Rather than formal Graph of Thoughts prompting, we should implement the *concept* (decompose, parallel explore, aggregate, self-critique) through agent orchestration.

6. **Human-in-the-loop planning improves quality**: Gemini's approach of presenting the research plan for user approval before execution leads to better-focused research.

7. **Self-critique in multiple passes matters**: Gemini's "multiple passes of self-critique" and Anthropic's citation agent approach both show that dedicated verification steps improve output quality.

8. **The best benchmark results come from December 2025 Gemini (HLE: 46.4%, BrowseComp: 59.2%)**: This is the current frontier to benchmark against.

9. **All tools still hallucinate and fabricate sources**: This is not a solved problem. Our QA/verification phase is not unnecessary overhead — it's essential.

10. **Token usage is the strongest predictor of research quality**: Anthropic found token usage explains 80% of BrowseComp performance variance. Budget-constrained systems should optimize *where* tokens are spent, not minimize total tokens.

### Competitive Positioning

| Dimension | Our System's Approach | Industry Standard |
|-----------|----------------------|-------------------|
| Search strategy | Multi-step with HyDE expansion | Multi-step iterative (same) |
| Verification | Multi-path C1 verification + independence check | Citation agent or self-critique |
| Synthesis | GoT-inspired aggregation | ReAct agent loops |
| QA | Dedicated reflexion phase | Self-critique passes |
| Speed | Unknown (needs testing) | 2-30 minutes depending on tool |
| Human-in-loop | Research contract at start | Plan approval (Gemini) or clarification (OpenAI) |

### What We Do Better (Potential Advantages)

- **Explicit independence checking** (most tools don't verify source independence)
- **Structured claim taxonomy** (C1/C2/C3 with different evidence requirements)
- **Dedicated QA/reflexion phase** (rather than inline self-critique)
- **Persistent graph state** for auditability

### What We Should Improve

- **Speed**: Our process may be slower than competitors
- **Parallel execution**: Should be default, not optional
- **Verification agent**: Consider Perplexity's approach of a dedicated agent that validates citations against live sources
- **Self-critique integration**: Add Gemini-style multiple self-critique passes during synthesis, not just at QA phase

---

## Source Catalog

### Primary Sources (Grade A-B)

| Source | Type | Grade | URL |
|--------|------|-------|-----|
| Anthropic Engineering Blog | Primary technical documentation | A | [Link](https://www.anthropic.com/engineering/multi-agent-research-system) |
| Google Blog (Deep Research) | Primary documentation | A | [Link](https://blog.google/products/gemini/google-gemini-deep-research/) |
| Gemini API Docs | Primary documentation | A | [Link](https://ai.google.dev/gemini-api/docs/deep-research) |
| GoT Paper (Besta et al.) | Academic paper | A | [Link](https://arxiv.org/abs/2308.09687) |
| AGoT Paper (2025) | Academic paper | A | [Link](https://arxiv.org/html/2502.05078v1) |
| Tow Center / Columbia Study | Academic research | A | [Link](https://www.niemanlab.org/2025/03/ai-search-engines-fail-to-produce-accurate-citations-in-over-60-of-tests-according-to-new-tow-center-study/) |
| BrowseComp Paper | Academic benchmark | A | [Link](https://arxiv.org/html/2504.12516v1) |
| HLE Leaderboard (Scale AI) | Benchmark leaderboard | A | [Link](https://scale.com/leaderboard/humanitys_last_exam) |
| PromptLayer Analysis | Technical analysis | B | [Link](https://blog.promptlayer.com/how-deep-research-works/) |
| ByteBytego Comparison | Technical analysis | B | [Link](https://blog.bytebytego.com/p/how-openai-gemini-and-claude-use) |
| Helicone Comparison | Technical analysis | B | [Link](https://www.helicone.ai/blog/openai-deep-research) |
| Demystifying X-of-Thought | Academic survey | A | [Link](https://arxiv.org/abs/2401.14295) |

### Secondary Sources (Grade C)

| Source | Type | Grade | URL |
|--------|------|-------|-----|
| Perplexity Architecture (FrugalTesting) | Technical blog | C | [Link](https://www.frugaltesting.com/blog/behind-perplexitys-architecture-how-ai-search-handles-real-time-web-data) |
| Sonar Deep Research Guide | Product guide | C | [Link](https://toolkitbyai.com/sonar-deep-research-complete-guide/) |
| Cameron Wolfe SubStack | Technical analysis | B | [Link](https://cameronrwolfe.substack.com/p/graph-based-prompting-and-reasoning) |
| Therift.ai on Gemini | News reporting | C | [Link](https://www.therift.ai/news-feed/google-rolls-out-gemini-deep-research-and-open-sources-deepsearchqa-benchmark) |
| Aryabh Consulting Comparison | Industry analysis | C | [Link](https://www.aryabhconsulting.com/blog/deep-research-ai-tools-comparison-2025-gemini-vs-chatgpt-vs-perplexity-for-business-research) |
| CBTW Comparison | Industry evaluation | C | [Link](https://cbtw.tech/insights/deep-research-tools-comparison-a-side-by-side-evaluation-of-ai-platforms) |
| Perplexity Models Late 2025 | Product guide | C | [Link](https://www.datastudios.org/post/perplexity-ai-all-available-models-modes-and-how-they-differ-in-late-2025) |
| LivePlan Test | User evaluation | C | [Link](https://www.liveplan.com/blog/planning/deep-research-chatgpt-vs-gemini) |

---

## Unverified Claims / Gaps

1. [Source needed] Perplexity's claimed 99.98% citation precision — only found in Perplexity's own marketing, not independently verified
2. [Unverified] Exact token budgets and search call limits for OpenAI Deep Research (estimates from PromptLayer analysis, not OpenAI's official documentation)
3. [Source needed] Direct apples-to-apples benchmark comparing ALL four tools (Perplexity, Gemini, OpenAI, Claude) on the same tasks at the same time — no such comprehensive comparison exists
4. [Unverified] Whether GoT-style prompting specifically improves open-ended research quality vs. agent loops — no published research compares these for research tasks
5. [Source needed] Gemini Deep Research's internal verification architecture details — Google has not published specifics of how it verifies claims internally
