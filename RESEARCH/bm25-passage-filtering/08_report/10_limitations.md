# Limitations and Open Questions

## Research Limitations

### L1: No Direct A/B Testing
All evidence is extrapolated from adjacent contexts (BEIR benchmarks for full retrieval, RAG evaluations for knowledge bases, chunking studies for embedding-based retrieval). No published study tests BM25 pre-filtering specifically in the context of LLM evidence extraction from single web pages. Our recommendations are well-grounded inferences, not direct measurements.

**Impact**: The specific parameter recommendations (K=10, 200-word chunks, k1=1.2) may need tuning once tested on the actual pipeline. The directional recommendations (use BM25, use paragraph chunking, use pure Python) are high-confidence.

### L2: Chunk Size Evidence Is For Embedding-Based Retrieval
The NVIDIA, Chroma, and arxiv chunk size benchmarks all evaluate chunk sizes for embedding-based retrieval (measuring recall@K with vector similarity). BM25 scoring may have different optimal chunk sizes because:
- BM25 benefits from keyword density (smaller chunks = sharper signal)
- Embedding models benefit from semantic coherence (larger chunks = richer context)

We inferred that smaller chunks are better for BM25 pre-filtering, but this has not been directly measured.

### L3: Web Content Variability
Web pages vary enormously: news articles (well-structured, paragraphs), documentation pages (headers + code blocks), forum posts (threaded, messy), academic pages (formal, citation-heavy), product pages (mixed media). Our paragraph-based chunking strategy assumes mostly prose content. Pages that are primarily tables, code, or lists may chunk poorly.

### L4: Tokenization Simplicity
Our recommended tokenizer (`lower().split()` + stopwords) is intentionally simple. More sophisticated tokenization (stemming, lemmatization, n-grams) would improve BM25 accuracy but at the cost of:
- Added dependencies (NLTK, spaCy)
- Startup latency
- Complexity

We judged the tradeoff favors simplicity for this use case, but this is a judgment call, not a measured result.

### L5: Lead Passage Bonus Is a Heuristic
The lead passage bonus (10-20% of max BM25 score for early passages) is based on the observation that web pages front-load important content. This is generally true for news articles and blog posts but less true for:
- Documentation (structure is flat)
- Academic papers (abstract is first, but key findings may be in results/discussion)
- Forum threads (relevant answer may be anywhere)

The bonus is small enough to not cause harm, but its actual benefit is unquantified.

## Open Questions

### Q1: Does BM25 pre-filtering actually improve LLM extraction quality?
The strongest version of our hypothesis is that reducing context noise improves extraction precision. The weak version is just that it saves tokens. We do not have evidence for the strong version.

**How to test**: Run 20 research sessions with and without BM25 filtering. Compare: (a) number of evidence passages extracted, (b) relevance scores of extracted passages, (c) total tokens consumed, (d) researcher satisfaction with results.

### Q2: What is the actual false negative rate?
We estimate 5-15% of pages may have suboptimal filtering. But what percentage of truly relevant passages are filtered out? And does the LLM compensate by extracting from adjacent passages?

**How to test**: On 50 pages, have the LLM extract passages from both full content and BM25-filtered content. Compute set overlap.

### Q3: Should K scale with page length?
We recommend fixed K=10 with a bypass for short pages. An alternative: K = max(5, min(15, len(chunks) // 3)). This would adapt to page length automatically. Is this better?

**How to test**: Compare fixed K=10 vs dynamic K on 30 pages of varying length.

### Q4: Is BM25+ actually better than BM25 Okapi for short passages?
The theoretical argument is sound (BM25+ ensures positive contribution for all matched terms). But at chunk sizes of 100-300 words, the practical difference may be negligible.

**How to test**: Score 500 passage-query pairs with both variants, compare ranking agreement.

### Q5: When should pre-filtering be skipped entirely?
Beyond the short-page bypass, are there query types or page types where pre-filtering should be disabled? For example:
- Very short queries (< 5 words)?
- Pages with very low BM25 score variance (all chunks score similarly)?
- Pages from known high-quality sources (every section is potentially relevant)?

### Q6: Could the LLM generate better query terms for BM25 scoring?
Instead of using the subquestion directly as the BM25 query, the LLM could extract key terms or generate a hypothetical answer (HyDE-style) whose vocabulary matches the page content better. This would require an extra LLM call but could significantly improve BM25 accuracy.

## What We Would Do With 2x Budget

1. **Build a test harness**: 50 diverse web pages, manually annotated with relevant passages, to measure precision/recall of BM25 filtering.
2. **A/B test chunk sizes**: 100, 200, 300, 400, 500 words on the test set with BM25 scoring specifically (not embedding retrieval).
3. **Compare BM25 Okapi vs BM25+** on the test set with short passages.
4. **Test dynamic K** strategies vs fixed K=10.
5. **Measure LLM extraction quality** with and without filtering on 20 full research sessions.

## Unresolved Contradictions

### Chunk size tension
NVIDIA says 512-1024 tokens. Chroma says 200 tokens. Arxiv paper says "it depends on the dataset." We resolved this by distinguishing retrieval from pre-filtering contexts, but this resolution is inferred, not measured. The optimal chunk size for BM25 pre-filtering of web content specifically remains untested.

### K value tension
Anthropic says K=20. LangChain defaults to K=4. RAG literature says K=3-5 for precision, K=10-20 for recall. We chose K=10 as a middle ground, but the right answer depends on chunk size (which varies), page length (which varies), and query complexity (which varies). A truly optimal system would use dynamic K.
