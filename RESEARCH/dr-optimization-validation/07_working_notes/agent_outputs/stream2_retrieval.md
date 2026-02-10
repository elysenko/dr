# Stream 2: Retrieval Quality -- Site-Targeted Search, Iterative Query Refinement, and Advanced Retrieval Techniques

## Research Sub-Question

Do site-targeted search queries and iterative query refinement actually improve retrieval quality in LLM research agents? What techniques produce deeply relevant sources vs surface-level content?

---

## 1. Site-Targeted Searching (Domain Filtering)

### Finding: Mixed evidence; helps precision but may hurt recall

**Evidence from systematic reviews of academic search systems:**

Gusenbauer (2020) evaluated 28 academic search systems including Google Scholar, PubMed, and Web of Science for systematic review suitability. Key findings:
- Topic-specific databases (e.g., ERIC, PubMed, APA PsycINFO) are useful because they are "already limited in scope" -- reducing noise without requiring broad term filtering [Source: PMC7079055]
- However, **one study found specialized medical search engines "are no better than general search-engines in sourcing consumer information"** -- suggesting domain-specific tools do not universally guarantee superior results [Source: PMC7079055]
- Different systems offer dramatically different filtering capabilities: EbscoHost, ProQuest, and Web of Science provide "up to 18 different options for filtering content" while AMiner, arXiv, and CiteSeerX "do not provide any post-query refinements" [Source: PMC7079055]

**The precision-recall tradeoff is fundamental:**

- Restricting to specific domains (via site: operators) improves precision (higher ratio of relevant results) but risks lowering recall (missing relevant content from unexpected sources)
- The IR literature is clear: "Generally, the more you improve recall, the worse your precision becomes" [Source: Standard IR literature]
- For research agents doing comprehensive investigation, **high recall matters more than high precision in early retrieval stages** -- you can always re-rank and filter later, but you cannot find what you never retrieved

**Practical implications for LLM research agents:**

The Perplexity architecture explicitly addresses this: it "does not force a choice between lexical and semantic retrieval; rather, it queries the search index via both modalities and merges the results into a hybrid candidate set, with **priority given to comprehensiveness over precision** at this stage" [Source: Perplexity/Vespa architecture documentation]. This suggests the industry trend is toward broad retrieval first, then aggressive re-ranking.

**Assessment:** Site-targeted search is useful as ONE strategy among several (especially for known high-quality domains like PubMed for medical, SEC for financial), but should NOT be the primary retrieval strategy. Using it exclusively risks missing relevant sources from unexpected domains. Better approach: use site-targeting for specific subqueries alongside broader searches, then apply quality filtering post-retrieval.

---

## 2. Iterative Query Refinement / Adaptive Retrieval

### Finding: Strong evidence of significant improvement -- one of the most validated techniques

### 2a. FLARE (Forward-Looking Active Retrieval)

**Paper:** Jiang et al., "Active Retrieval Augmented Generation" (EMNLP 2023)

FLARE iteratively generates the next sentence, checks token probabilities, and triggers retrieval when confidence is low. Key mechanism:
- If any token probability falls below a threshold, FLARE uses the generated sentence as a retrieval query
- Applied to GPT-3.5 at inference time without additional training
- **Results:** "Superior or competitive performance compared to single-time and multi-time retrieval baselines across all tasks" on multihop QA, commonsense reasoning, long-form QA, and open-domain summarization [Source: arxiv.org/abs/2305.06983]

**Significance for research agents:** FLARE demonstrates that using model-generated content as queries (rather than only the original question) substantially improves retrieval quality. The key insight is that **the model's own uncertainty signals when additional retrieval is needed**.

### 2b. IRCoT (Interleaving Retrieval with Chain-of-Thought)

**Paper:** Trivedi et al., "Interleaving Retrieval with Chain-of-Thought Reasoning" (ACL 2023)

IRCoT interleaves retrieval with each step of chain-of-thought reasoning:
- **Retrieval improvement: up to 21 points** on HotpotQA, 2WikiMultihopQA, MuSiQue, and IIRC [Source: arxiv.org/abs/2212.10509]
- **Downstream QA improvement: up to 15 points** [Source: arxiv.org/abs/2212.10509]
- IRCoT "reduces model hallucination, resulting in factually more accurate CoT reasoning"
- Similar gains observed in out-of-distribution settings and with smaller models (Flan-T5-large)

**Significance:** This is one of the strongest empirical demonstrations that interleaving retrieval with reasoning steps beats retrieve-once approaches.

### 2c. Self-RAG (Self-Reflective Retrieval-Augmented Generation)

**Paper:** Asai et al. (2023), ICLR 2024

Self-RAG trains a model to adaptively decide WHEN to retrieve using special reflection tokens:
- **REL** (relevance), **SUP** (support), **USE** (utility) tokens
- Model can retrieve "multiple times during generation, or completely skip retrieval"
- **Results:** Self-RAG (7B and 13B) "significantly outperforms state-of-the-art LLMs and retrieval-augmented models on a diverse set of tasks" including open-domain QA, reasoning, and fact verification [Source: arxiv.org/abs/2310.11511]
- Outperforms ChatGPT and retrieval-augmented Llama2-chat on multiple benchmarks

### 2d. RQ-RAG (Learning to Refine Queries)

**Paper:** Chan et al. (2024)

Trains a 7B Llama2 model for dynamic query refinement through rewriting, decomposing, and clarifying ambiguities:
- **Single-hop QA:** Surpasses previous SOTA by average of 1.9% across 3 datasets
- **Multi-hop QA:** Average enhancement of **22.6%** across 3 multi-hop datasets [Source: arxiv.org/abs/2404.00610]
- Outshines SAIL-7B by 20.3% on average across 3 QA tasks

### 2e. FAIR-RAG (Faithful Adaptive Iterative Refinement)

**Paper:** 2025

Uses Structured Evidence Assessment (SEA) as gating mechanism:
- Deconstructs initial query into checklist of required findings
- Identifies confirmed facts vs explicit gaps
- Gaps trigger Adaptive Query Refinement for targeted sub-queries
- **Results:** F1-score of 0.453 on HotpotQA -- **8.3 points improvement** over strongest iterative baseline [Source: arxiv.org/abs/2510.22344]

### 2f. IM-RAG (Inner Monologue RAG)

Simulates inner monologue alternating between generation and retrieval:
- **+5.3 F1 / +7.2 EM on HotPotQA** using iterative retrieval refinement [Source: RAG survey literature]

### Summary of Iterative Refinement Evidence

| Method | Year | Key Metric | Improvement |
|--------|------|-----------|-------------|
| FLARE | 2023 | Multi-task | Superior to single/multi retrieval baselines |
| IRCoT | 2023 | Retrieval | Up to +21 points |
| IRCoT | 2023 | QA accuracy | Up to +15 points |
| Self-RAG | 2023 | Multi-task | Outperforms ChatGPT + RAG-Llama2 |
| RQ-RAG | 2024 | Multi-hop QA | +22.6% average |
| FAIR-RAG | 2025 | HotpotQA F1 | +8.3 points over best iterative baseline |
| IM-RAG | 2024 | HotpotQA | +5.3 F1 / +7.2 EM |

**Assessment:** Iterative query refinement is one of the most robustly validated techniques in the RAG literature. Every major study shows significant improvement over retrieve-once baselines. The key mechanism is using intermediate reasoning outputs to formulate better follow-up queries.

---

## 3. HyDE (Hypothetical Document Embeddings)

### Finding: Strong improvement for zero-shot retrieval, but with important caveats

**Paper:** Gao et al., "Precise Zero-Shot Dense Retrieval without Relevance Labels" (ACL 2023)

**How it works:** Generate a hypothetical answer document, embed it, and use that embedding to find similar real documents.

**Performance:**
- On TREC DL19: HyDE achieved mAP of **41.8** vs Contriever's 24.0 and BM25's 30.1 [Source: arxiv.org/abs/2212.10496]
- "Significantly outperforms the state-of-the-art unsupervised dense retriever Contriever"
- "Shows strong performance comparable to fine-tuned retrievers" across web search, QA, fact verification

**Known Limitations:**
1. **Domain sensitivity:** "If the domain is rare or not well represented in the LLM's training corpus, the hypothetical document might be way off, misleading retrieval" [Source: Milvus documentation]
2. **Hallucination propagation:** "The document captures relevance patterns but is unreal and may contain false details" -- if the LLM hallucinates, the vector pulls in documents related to hallucinated details [Source: Pondhouse Data blog]
3. **Specific factual queries:** "A particular failure mode to watch is when the query asks for very specific or numerical information" [Source: Milvus documentation]
4. **Cost at scale:** Extra LLM call per query; "If your system is at scale (say millions of queries per day), HyDE could significantly increase operational cost" [Source: Milvus documentation]
5. **Confidence calibration:** When topic familiarity is low (model confidence < 5/10), broader keyword search first is recommended before HyDE

**Assessment:** HyDE is highly effective for bridging vocabulary gaps and improving recall, especially in zero-shot settings. However, it should be used with awareness of domain familiarity. The recommendation to generate 2-3 hypothetical documents from different framings (academic, practitioner, skeptical) is supported by the evidence -- this mitigates single-viewpoint bias. For a research agent, HyDE is most valuable when the agent is exploring unfamiliar territory and needs to translate a research question into the vocabulary of the target domain.

---

## 4. Commercial Deep Research System Architectures

### 4a. OpenAI Deep Research

**Architecture:**
- Powered by o3 model variant optimized for web browsing and data analysis
- Trained via **end-to-end reinforcement learning** on complex browsing and reasoning tasks
- Follows **Plan-Act-Observe** (ReAct) paradigm [Source: OpenAI system card, cdn.openai.com]
- Learned to "plan and execute multi-step search trajectories, backtrack when paths are unfruitful, and pivot strategies based on new information" [Source: OpenAI system card]

**Search behavior:**
- Typical session: **30-60 web searches per task**, caps of **120-150 pages maximum** [Source: blog.promptlayer.com/how-deep-research-works]
- One observed session: 21 different sources across 28 minutes of processing
- Coverage requirement: 2+ independent sources per sub-question, or 1 if authoritative
- Searches are iterative: "does a search, reads some results, then decides on the next search query based on what it learned"
- Adaptively pivots when encountering obstacles (e.g., paywalled content)

**DeepResearchBench performance:** Overall RACE score 46.98 (2nd place), instruction-following 49.27 (highest), citation accuracy 77.96% [Source: deepresearch-bench.github.io]

### 4b. Google Gemini Deep Research

**Architecture:**
- Powered by Gemini 3 Pro, "specifically trained to reduce hallucinations and maximize report quality"
- Uses **multi-step reinforcement learning for search**
- Novel **asynchronous task manager** maintains shared state between planner and task models
- Three-phase process: Planning -> Research & Iterative Searching -> Synthesis [Source: Google AI blog, Gemini API docs]

**Search behavior:**
- Standard research: **~80 search queries** [Source: ai.google.dev/gemini-api/docs/deep-research]
- Complex research: **up to ~160 search queries** [Source: ai.google.dev/gemini-api/docs/deep-research]
- Agent "autonomously determines how much reading and searching is necessary"
- Intelligently determines which sub-tasks can be tackled simultaneously vs sequentially
- "Formulates queries, reads results, identifies knowledge gaps, and searches again"
- Maximum research time: 60 minutes (most complete within 20 minutes)

**DeepResearchBench performance:** Overall RACE score **48.88** (1st place), 111.21 average effective citations (dramatically highest), citation accuracy 81.44% [Source: deepresearch-bench.github.io]

### 4c. Anthropic Claude Research (Multi-Agent)

**Architecture:**
- **Orchestrator-worker pattern** with lead agent (Claude Opus 4) coordinating subagents (Claude Sonnet 4) [Source: anthropic.com/engineering/multi-agent-research-system]
- Lead agent decomposes query, spawns 3-5 parallel subagents
- Each subagent independently performs web searches, evaluates results using interleaved thinking

**Search behavior:**
- Subagents use **3+ tools in parallel**, cutting research time "by up to 90% for complex queries"
- Scaling: simple queries = 1 agent (3-10 calls); comparisons = 2-4 subagents (10-15 calls each); complex = 10+ subagents
- Extended thinking used as "controllable scratchpad" for planning approach
- Source quality problem identified: agents favor "SEO-optimized content farms over authoritative but less highly-ranked sources like academic PDFs or personal blogs" -- addressed through added heuristics

**Performance:** Multi-agent system outperformed single-agent Claude Opus 4 by **90.2%** on internal research evaluation [Source: anthropic.com/engineering/multi-agent-research-system]

**Token economics:** Agents use ~4x more tokens than chat; multi-agent systems use ~15x more tokens than chat. Token usage explains **80% of performance variance** in BrowseComp evaluation. [Source: anthropic.com/engineering/multi-agent-research-system]

### 4d. Perplexity

**Architecture:**
- Uses Vespa AI as search backend for massive RAG architecture [Source: vespa.ai/perplexity]
- **Hybrid retrieval:** queries via both lexical and semantic modalities, merged into hybrid candidate set
- **Multi-stage ranking:** "progressively advanced ranking, with earlier stages relying on lexical and embedding-based scorers optimized for speed, and later stages using more powerful cross-encoder reranker models" [Source: Perplexity architecture blog]
- Multi-model architecture dynamically routes queries to different engines based on task type

**Scale:** 200 million daily queries; 100+ million queries per week [Source: Perplexity architecture blog]

**DeepResearchBench performance:** RACE score 42.25 (3rd), citation accuracy **90.24%** (highest precision), 31.26 effective citations [Source: deepresearch-bench.github.io]

### Comparative Analysis

| System | Search Volume | Architecture | Key Strength |
|--------|--------------|-------------|-------------|
| OpenAI | 30-60 queries | RL-trained ReAct agent | Instruction following (49.27) |
| Gemini | 80-160 queries | RL + async task manager | Volume of citations (111.21) |
| Claude | 3-10 per subagent, parallel | Multi-agent orchestrator | Speed (90% faster via parallelism) |
| Perplexity | N/A (production search) | Hybrid retrieval + multi-stage ranking | Citation accuracy (90.24%) |

**Key insight from DeepResearchBench:** "Regular mode with web search often outperformed their corresponding dedicated deep research tools" for iterative research [Source: DeepResearchBench evaluation]. This is a striking finding -- suggesting that the elaborate multi-step pipelines sometimes underperform simpler iterative approaches.

---

## 5. Query Decomposition Strategies

### Finding: Significant and consistent improvement, especially for multi-hop questions

**PRISM (Agentic Retrieval for Multi-Hop QA):**
- HotpotQA: **90.9% recall** vs 61.5% for single-query (OneR) and 72.8% for IRCoT [Source: arxiv.org/abs/2510.14278]
- MuSiQue: **83.2% recall** vs 44.6% (OneR) and 57.1% (IRCoT) -- largest margin
- 2WikiMultihopQA: 91.1% recall vs 68.1% (OneR)

**Query Expansion Results:**
- "Most substantial gains occur when moving from single-query to dual-query generation, with an average improvement of **6.7%**" [Source: EMNLP 2025 findings]
- RT-RAG: average increase of **7.0% F1 and 6.0% EM** from hierarchical reasoning structure

**Decomposition + Interpretation (Zhong et al., 2025):**
- "Decomposition alone is insufficient; adding interpretation significantly improves retrieval"
- "Decomposition plus interpretation achieving the highest effectiveness across both retrieval paradigms" [Source: arxiv.org/html/2509.06544v1]
- Downstream gains: **6.0-9.9% increase in citation support, 6.7-8.5% in nugget coverage, and 7.3-9.6% in sentence support** [Source: arxiv.org/abs/2510.18633]

**Assessment:** Query decomposition is highly effective, with the literature consistently showing large improvements. The critical nuance is that decomposition ALONE is not enough -- it must be paired with interpretation/rewriting of sub-queries to maximize effectiveness. Simply splitting a complex question into sub-questions without reformulating them for retrieval yields suboptimal results.

---

## 6. Source Diversity and Research Quality

### Finding: Well-established principle in research methodology; limited quantitative evidence specific to LLM agents

**Triangulation (established research methodology):**
- "Triangulation in research means using multiple datasets, methods, theories, and/or investigators to address a research question" [Source: Scribbr methodology guide]
- Four types: Data triangulation, Methodological triangulation, Investigator triangulation, Theoretical triangulation
- Benefits: "increasing confidence in research data, creating innovative ways of understanding a phenomenon, revealing unique findings, challenging or integrating theories" [Source: Delvetool.com]

**From DeepResearchBench evaluation:**
- Gemini's 111.21 effective citations (from diverse sources) correlated with highest overall RACE score (48.88)
- Perplexity's highest citation accuracy (90.24%) but fewer citations (31.26) correlated with lower overall score (42.25)
- This suggests **breadth of sources matters for research quality**, not just precision [Source: deepresearch-bench.github.io]

**Anthropic's finding on source quality:**
- Agents tend to favor "SEO-optimized content farms over authoritative but less highly-ranked sources like academic PDFs or personal blogs" [Source: anthropic.com/engineering/multi-agent-research-system]
- This is a concrete, documented failure mode: without explicit source diversity heuristics, LLM agents naturally gravitate toward SEO-optimized content

**Assessment:** The triangulation principle is well-established in research methodology but there is limited quantitative evidence specifically measuring how source TYPE diversity (academic + practitioner + government) affects LLM research agent output quality. The DeepResearchBench data indirectly supports it: more diverse citations correlate with higher quality scores. The Anthropic team's explicit discovery that agents favor SEO content over authoritative sources validates the need for deliberate source diversity mechanisms.

---

## 7. Expert Terminology Bootstrapping

### Finding: Addresses the fundamental vocabulary mismatch problem; well-supported by IR literature

**The vocabulary mismatch problem:**
- "Occurs when query-document relevance is not correctly estimated due to missing exact lexical match" [Source: Sease blog on vocabulary mismatch]
- "A relevant document with no overlapping terms with a query will not be retrieved during candidate generation and hence will never be evaluated by downstream neural models" [Source: soyuj.com/blog/document-expansion]
- This affects the ENTIRE retrieval pipeline -- documents missed at candidate generation cannot be recovered

**Query expansion techniques (comprehensive survey: Azad & Deepak, 2019):**
- Data sources: "documents used in retrieval process, hand-built knowledge resources, external text collections and resources, and hybrid data sources" [Source: ScienceDirect survey]
- "Hybrid ontology-based methods have been found to be more accurate for query expansion compared to linguistic and ontology-based methods"
- Word embedding techniques (word2vec-based K-nearest neighbor) are widely used for finding semantically similar terms

**Pseudo-relevance feedback (iterative terminology learning):**
- Use top-k retrieved documents to extract additional query terms
- Generative PRF (using LLMs) "improves over comparable PRF techniques by around 10% on both precision and recall-oriented measures" [Source: arxiv.org/abs/2305.07477]
- Neural PRF like ColBERT-PRF "increases MAP by up to 26%" [Source: arxiv.org/abs/2305.07477]
- LLM-based PRF methods outpace traditional RM3 "by 10-24% NDCG@10"

**Domain-specific applications:**
- MeSH thesaurus in biomedical retrieval: ~26,000 controlled vocabulary terms
- "Document expansion is particularly useful in scenarios where documents are sparse or use domain-specific jargon"
- "Task-oriented systems address vocabulary mismatch through synonym-aware bootstrapping or embedding-based similarity matching" [Source: IJITCS 2025]

**Assessment:** Expert terminology bootstrapping is a well-supported technique. The most effective approach is a two-stage process: (1) initial broad queries to discover domain vocabulary from high-quality results, then (2) refined queries using discovered terminology. This is essentially pseudo-relevance feedback applied to research workflows. The LLM-based variants (generative PRF) show particularly strong results, suggesting that using the LLM itself to extract and reformulate domain terms from initial results is highly effective.

---

## 8. Emerging Research: DeepResearcher (End-to-End RL for Search)

**Paper:** Zheng et al., "DeepResearcher: Scaling Deep Research via Reinforcement Learning in Real-world Environments" (EMNLP 2025)

First comprehensive framework for end-to-end training of LLM research agents via RL with live web search:
- **Up to 28.9 points improvement** over prompt engineering baselines [Source: arxiv.org/abs/2504.03160]
- **Up to 7.2 points improvement** over RAG-based RL agents
- Uses Group Relative Policy Optimization (GRPO) algorithm
- Trains agents to interact directly with live search engines (not static corpora)

**Emergent behaviors from RL training:**
- Ability to formulate plans
- Cross-validate information from multiple sources
- Self-reflection to redirect research
- Maintain honesty when unable to find definitive answers

**Significance:** This validates that end-to-end reinforcement learning for search (as used by OpenAI and Gemini in their commercial products) produces agents with qualitatively better search strategies than prompt-engineered approaches. The emergent cross-validation behavior is particularly notable.

---

## 9. Cross-Cutting Synthesis and Practical Recommendations

### What the evidence says works, ranked by strength of evidence:

1. **Iterative query refinement** (VERY STRONG evidence): Every major study shows +5 to +22 point improvements. Use intermediate results to inform follow-up queries. This is the single most impactful technique.

2. **Query decomposition + interpretation** (STRONG evidence): Breaking complex queries into sub-queries with reformulation yields 60-90% recall vs 44-68% for single queries. Must combine decomposition with interpretation -- decomposition alone is insufficient.

3. **HyDE for vocabulary bridging** (STRONG evidence for zero-shot): mAP nearly doubles vs unsupervised baselines (41.8 vs 24.0). Best used when domain familiarity is moderate-to-low. Multiple hypothetical framings recommended.

4. **Parallel multi-agent search** (STRONG evidence from industry): Anthropic's 90.2% improvement over single-agent. But note: 15x more tokens. Token usage explains 80% of quality variance.

5. **Pseudo-relevance feedback / terminology bootstrapping** (MODERATE evidence): 10-26% improvement in various metrics. Use initial results to learn domain vocabulary for follow-up queries.

6. **Source diversity** (MODERATE evidence, strong theoretical basis): Triangulation is well-established in research methodology. DeepResearchBench data indirectly supports it. Explicit heuristics needed to counter SEO content farm bias.

7. **Site-targeted search** (WEAK/MIXED evidence): Improves precision for known high-quality domains but risks recall loss. Best used selectively alongside broader searches, not as primary strategy.

### What the evidence says about failure modes:

- **SEO content farm bias:** Documented by Anthropic -- agents naturally prefer SEO-optimized content over academic sources without explicit heuristics [Source: anthropic.com]
- **HyDE hallucination propagation:** When the LLM generates a wrong hypothetical document, it can pull in irrelevant results [Source: multiple]
- **Over-refinement:** "Although LLM augmentation can help weaker models, the strongest model has decreased performance across all metrics with all rewriting techniques" [Source: RAG survey] -- there is a point of diminishing returns
- **Quality vs quantity tradeoff:** DeepResearchBench shows Gemini's 111 citations correlated with highest quality, but Perplexity's 31 citations had highest accuracy -- more is not always better per-citation

---

## Sources

### Academic Papers
- [FLARE: Active Retrieval Augmented Generation (Jiang et al., EMNLP 2023)](https://arxiv.org/abs/2305.06983)
- [IRCoT: Interleaving Retrieval with Chain-of-Thought (Trivedi et al., ACL 2023)](https://arxiv.org/abs/2212.10509)
- [Self-RAG: Learning to Retrieve, Generate, and Critique (Asai et al., 2023)](https://arxiv.org/abs/2310.11511)
- [HyDE: Precise Zero-Shot Dense Retrieval (Gao et al., ACL 2023)](https://arxiv.org/abs/2212.10496)
- [RQ-RAG: Learning to Refine Queries (Chan et al., 2024)](https://arxiv.org/abs/2404.00610)
- [FAIR-RAG: Faithful Adaptive Iterative Refinement (2025)](https://arxiv.org/abs/2510.22344)
- [DeepResearcher: Scaling Deep Research via RL (Zheng et al., EMNLP 2025)](https://arxiv.org/abs/2504.03160)
- [DeepResearchBench: Benchmark for Deep Research Agents (2025)](https://deepresearch-bench.github.io/)
- [PRISM: Agentic Retrieval for Multi-Hop QA (2025)](https://arxiv.org/abs/2510.14278)
- [Reasoning-enhanced Query Understanding (Zhong et al., 2025)](https://arxiv.org/html/2509.06544v1)
- [Query Decomposition for RAG: Balancing Exploration-Exploitation (2025)](https://arxiv.org/abs/2510.18633)
- [Survey of LLM-based Deep Search Agents (2025)](https://arxiv.org/abs/2508.05668)
- [Generative and Pseudo-Relevant Feedback for Retrieval (2023)](https://arxiv.org/abs/2305.07477)
- [Query Expansion Techniques Survey (Azad & Deepak, IPM 2019)](https://www.sciencedirect.com/science/article/abs/pii/S0306457318305466)
- [Academic Search Systems for Systematic Reviews (Gusenbauer, 2020)](https://pmc.ncbi.nlm.nih.gov/articles/PMC7079055/)

### Industry Technical Documentation
- [Anthropic: How We Built Our Multi-Agent Research System](https://www.anthropic.com/engineering/multi-agent-research-system)
- [OpenAI: Introducing Deep Research](https://openai.com/index/introducing-deep-research/)
- [OpenAI Deep Research System Card](https://cdn.openai.com/deep-research-system-card.pdf)
- [How OpenAI's Deep Research Works (PromptLayer)](https://blog.promptlayer.com/how-deep-research-works/)
- [Gemini Deep Research API Documentation](https://ai.google.dev/gemini-api/docs/deep-research)
- [How Perplexity Uses Vespa.ai](https://vespa.ai/perplexity/)
- [Perplexity Architecture Overview (FrugalTesting)](https://www.frugaltesting.com/blog/behind-perplexitys-architecture-how-ai-search-handles-real-time-web-data)
- [How OpenAI, Gemini, and Claude Use Agents (ByteByteGo)](https://blog.bytebytego.com/p/how-openai-gemini-and-claude-use)

### Reference and Methodology
- [Triangulation in Research (Scribbr)](https://www.scribbr.com/methodology/triangulation/)
- [Vocabulary Mismatch (Sease)](https://sease.io/2022/01/tackling-vocabulary-mismatch-with-document-expansion.html)
- [HyDE Limitations (Milvus)](https://milvus.io/ai-quick-reference/what-is-hyde-hypothetical-document-embeddings-and-when-should-i-use-it)
- [Stanford IR Book: Query Expansion](https://nlp.stanford.edu/IR-book/pdf/09expand.pdf)
