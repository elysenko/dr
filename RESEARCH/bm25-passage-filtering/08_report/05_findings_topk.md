# Finding 4: Optimal Top-K for Pre-Filtering Before LLM Extraction

## What the Evidence Says

### Anthropic's Contextual Retrieval [C1, S07]
- Tested top-5, top-10, and top-20 chunk retrieval
- **Top-20 proved "most performant"** compared to smaller K values
- For reranking: retrieved top-150, then reranked to top-20
- Failure rate at top-20: 1.9% (with reranking) to 5.7% (embeddings only)

Note: Anthropic's context is full knowledge base retrieval (thousands of chunks across many documents), not single-page pre-filtering. Their optimal K=20 includes diversity across documents.

### RAG Evaluation Literature [C2, multiple sources]
The consensus from RAG evaluation guides:
- **K=3-5**: High precision, risk of missing information. Best for simple factoid queries.
- **K=5-10**: Balanced. Going from 1 to 3 documents greatly improves answer correctness.
- **K=10-20**: High recall, some noise. Best for complex analytical queries.
- **K>20**: Diminishing returns. Context noise starts degrading LLM performance.

The typical finding: "going from 5 to 10 starts to hurt due to precision drops and confusion increases" for direct QA tasks, but helps for synthesis tasks where breadth matters.

### The "Lost in the Middle" Problem [C2, referenced in prior search-quality-improvement research]
LLMs pay more attention to content at the beginning and end of their context window. Passages in the middle get less attention. This means:
- Fewer, more relevant passages > many noisy passages
- But BM25 scoring naturally puts the most relevant passages first, partially mitigating this

## Reconciling for Our Use Case

Our use case has specific characteristics that affect the K decision:

| Factor | Implication for K |
|--------|-------------------|
| **Single-page pre-filtering** (not multi-doc retrieval) | K can be lower — content is already relevant |
| **Web pages average 20-40 chunks** (at 200 words/chunk) | K=10 means ~25-50% of chunks pass through |
| **LLM does final judgment** (not direct answer generation) | Recall matters more than precision — the LLM can ignore irrelevant passages |
| **Research queries are complex** (not simple factoids) | Higher K needed for multi-faceted questions |
| **Context window is shared** with the subquestion prompt | Don't waste too many tokens on one page |

## The Short-Page Problem

A critical edge case: if a page produces only 8-12 chunks, setting K=10 means passing nearly everything to the LLM — which is fine! The problem arises when K=5 on a short page accidentally filters out 60% of a small, mostly-relevant page.

**Solution**: Dynamic K with a bypass threshold.

```python
def select_top_k(scores, chunks, k=10, bypass_threshold=15):
    """Select top-K passages, bypassing filter for short pages."""
    if len(chunks) <= bypass_threshold:
        # Short page: pass everything through
        return list(range(len(chunks)))

    ranked = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
    return ranked[:k]
```

## Score Threshold as Alternative to Fixed K

Instead of a fixed K, some systems use a score threshold (e.g., Crawl4AI's `bm25_threshold=1.0`). This adapts to content quality automatically:
- Pages with many relevant passages: more chunks pass
- Pages with concentrated relevance: fewer chunks pass

**Problem**: BM25 scores are not normalized. A score of 5.0 might be excellent for one query and mediocre for another. Threshold-based filtering requires calibration per query, which adds complexity.

**Recommendation**: Use fixed K with bypass, not thresholds. Simpler, more predictable, and the LLM handles precision filtering.

## Recommendation: K=10, Bypass at 15 [C2]

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Default K | 10 | Balances recall (don't miss relevant passages) and noise reduction (cut 50-75% of content) |
| Bypass threshold | 15 chunks | If page has fewer than 15 chunks, pass all — pre-filtering adds no value |
| Minimum K | 3 | Even on very long pages, always pass at least 3 passages |

### Expected Impact

For a typical 5,000-word web page (25 chunks at 200 words):
- **Before filtering**: 5,000 words to LLM (~7,000 tokens)
- **After filtering (K=10)**: 2,000 words to LLM (~2,800 tokens) — 60% reduction
- **Token savings per page**: ~4,200 tokens
- **Across 20 pages per research session**: ~84,000 tokens saved

This also means the LLM can process more pages per call, or handle longer subquestion prompts.

### What K=10 Means in Practice

On a page about "BM25 algorithms" with 25 chunks:
- **Top 1-3**: Chunks directly defining BM25, containing the query terms densely
- **Top 4-7**: Chunks discussing BM25 parameters, variants, applications
- **Top 8-10**: Chunks with related terms (TF-IDF comparison, retrieval metrics)
- **Filtered out**: Navigation, author bio, related articles, cookie notices, tangential sections

The LLM receives a focused, relevant subset that preserves the key information while eliminating noise.
