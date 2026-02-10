# Executive Summary: BM25 Passage Pre-Filtering for RAG Retrieval Pipelines

## One-Line Answer

**Implement a ~60-line pure-Python BM25 scorer (no external dependencies), chunk web content into ~200-word paragraphs splitting on double-newlines, and pass the top-10 passages to the LLM instead of the full page.** This will cut context noise by 60-80% with minimal risk of filtering out relevant content.

## Recommendation Summary

| Decision | Recommendation | Confidence |
|----------|---------------|------------|
| Library | Custom pure-Python (~60 lines) | HIGH |
| Chunk strategy | Paragraph-based splitting on `\n\n`, fallback to ~200 words | HIGH |
| Chunk overlap | None (paragraph boundaries are natural) | MEDIUM |
| Top-K | 10 passages (with fallback: if page < 15 chunks, pass all) | MEDIUM |
| BM25 variant | BM25 Okapi (k1=1.5, b=0.75) | HIGH |
| Hybrid approach | Not for v1. Add query term expansion as v2 enhancement | HIGH |
| Tokenizer | Simple `.lower().split()` with stopword removal | HIGH |

## Hypothesis Outcomes

| Hypothesis | Prior | Posterior | Verdict |
|-----------|-------|-----------|---------|
| H1: rank_bm25 is the best library | 70% | 30% | REJECTED — custom pure-Python is better for this use case (zero deps, tiny corpus, simpler) |
| H2: 300-500 word chunks optimal | 60% | 55% | PARTIALLY CONFIRMED — 200-word paragraph-based chunks slightly outperform, but 300-500 is acceptable |
| H3: BM25 alone sufficient for pre-filtering | 55% | 75% | CONFIRMED — hybrid approaches add complexity without proportional benefit for pre-filtering (not full retrieval) |
| H4: Top-K of 5-10 optimal | 50% | 70% | CONFIRMED — K=10 balances precision and recall; K=5 is too aggressive for noisy web content |
| H5: Implementable in <100 lines zero deps | 65% | 90% | CONFIRMED — core BM25 Okapi is ~40-60 lines of pure Python |

## Key Findings

### 1. Custom Pure-Python Beats Libraries for This Use Case [C1]
For single-page pre-filtering (corpus of 10-50 chunks), the overhead of importing numpy/scipy via rank_bm25 or bm25s is unjustified. BM25 Okapi scoring is mathematically simple: IDF weighting + saturated term frequency + length normalization. A pure-Python implementation using only `math.log` and dictionaries handles this in ~60 lines with zero startup cost.

**Evidence**: rank_bm25 requires numpy (18MB); bm25s requires numpy+scipy (55MB combined). Both are designed for large corpora (millions of docs). For 10-50 chunks per page, the algorithmic overhead is negligible — the bottleneck is tokenization, not scoring. [S01, S02, S03]

### 2. Paragraph-Based Chunking Outperforms Fixed-Size for Web Content [C1]
Web content has natural paragraph boundaries (`\n\n` in markdown/text). Splitting on these preserves semantic coherence better than arbitrary 512-token windows. NVIDIA's benchmark found 512-1024 token chunks optimal for analytical queries, while Chroma's evaluation found 200-token chunks optimal for precision [S04, S05]. The reconciliation: for **pre-filtering** (not full retrieval), smaller chunks are better because they produce tighter relevance signals.

**Recommended approach**: Split on `\n\n` first, then split oversized paragraphs (>300 words) at sentence boundaries. Minimum chunk size: 50 words (discard smaller fragments as likely boilerplate).

### 3. BM25 Alone Is Sufficient for Pre-Filtering [C2]
Anthropic's contextual retrieval data shows BM25 + embeddings reduces failure rate by 49% vs embeddings alone [S07]. But this is for **full retrieval from a large knowledge base**, not pre-filtering within a single page. For single-page pre-filtering, the vocabulary overlap between the query and relevant passages is naturally high (the page was already selected by the search engine for that query). BM25's vocabulary mismatch weakness is mitigated.

### 4. Top-K=10 With a Short-Page Bypass [C2]
Evidence converges on K=3-5 for precision-critical tasks and K=10-20 for recall-critical tasks [S07, multiple RAG evaluation sources]. For pre-filtering before LLM extraction (where the LLM handles final judgment), recall matters more than precision. K=10 provides a safety margin.

**Critical safeguard**: If the page produces fewer than 15 total chunks, pass ALL chunks to the LLM. Pre-filtering short pages risks losing content with no noise-reduction benefit.

### 5. BM25 Fails Predictably — and Gracefully [C1]
BM25 fails on: (a) vocabulary mismatch between query terms and passage terms, (b) very short queries (1-2 words), (c) semantic queries where meaning matters more than keywords. But the failure mode is **graceful degradation** — it returns slightly-less-optimal passages, not garbage. The LLM still sees relevant content; it just may not be the most relevant. [S13, S14, S16]

**Mitigation**: Always include a small bonus for the first 2-3 passages of the page (lead bias — web pages typically front-load key information).

## What Would Change These Conclusions

- Evidence that LLM extraction quality degrades significantly with BM25-filtered input vs full page (requires A/B testing on the actual pipeline)
- A pure-Python BM25 implementation proving too slow for pages with >100 chunks (unlikely given the math is trivial)
- Discovery that web content vocabulary mismatch with research queries is higher than assumed

## Implementation Effort
**1 day** for the core implementation (BM25 scorer + chunker + integration). No external dependencies needed.
