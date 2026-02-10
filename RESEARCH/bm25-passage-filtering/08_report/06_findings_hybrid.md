# Finding 5: Hybrid Approaches Without Embedding Models

## The Question

Can we improve on pure BM25 pre-filtering without adding embedding model dependencies or API calls?

## Anthropic's Evidence for Hybrid [C1, S07]

Anthropic's contextual retrieval benchmark provides the strongest evidence:

| Approach | Failure Rate | Improvement |
|----------|-------------|-------------|
| Embeddings only | 5.7% | baseline |
| Contextual Embeddings | 3.7% | -35% |
| Contextual Embeddings + Contextual BM25 | 2.9% | -49% |
| + Reranking | 1.9% | -67% |

This shows BM25 adds significant value ON TOP of embeddings. But this is full knowledge base retrieval, not single-page pre-filtering. The contexts are meaningfully different:

- **Knowledge base retrieval**: BM25 catches exact keyword matches that embedding similarity misses (complementary strengths)
- **Single-page pre-filtering**: The page is already keyword-relevant (selected by search engine). BM25's keyword matching is less differentiated.

## Hybrid Approaches Available Without Embeddings

### Approach 1: Multi-Query BM25 + Reciprocal Rank Fusion

Run BM25 multiple times with different query formulations, then fuse the rankings:

```python
def multi_query_bm25(chunks, queries, k=10):
    """Score chunks against multiple query variants, fuse with RRF."""
    # queries = [original_query, expanded_query, reformulated_query]
    rankings = []
    for query in queries:
        tokens = tokenize(query)
        bm25 = BM25(tokenized_chunks)
        scores = bm25.get_scores(tokens)
        ranked = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
        rankings.append(ranked)

    # Reciprocal Rank Fusion
    rrf_scores = {}
    for ranking in rankings:
        for rank, doc_id in enumerate(ranking):
            rrf_scores[doc_id] = rrf_scores.get(doc_id, 0) + 1.0 / (60 + rank)

    final = sorted(rrf_scores, key=rrf_scores.get, reverse=True)
    return final[:k]
```

**Pros**: Addresses vocabulary mismatch by trying multiple query phrasings. Zero dependencies.
**Cons**: Requires generating query variants (the LLM already does this). 3x the scoring computation (still trivial for 50 chunks).
**Verdict**: Useful if the LLM provides the subquestion in multiple formulations. Not worth generating variants automatically for v1.

### Approach 2: BM25 + Lead Passage Bonus

Web pages front-load important information. The first few paragraphs almost always contain the most relevant content. Add a position-based bonus:

```python
def score_with_position_bias(bm25_scores, n_chunks, lead_bonus=0.2):
    """Add position-based bonus for early passages."""
    adjusted = []
    for i, score in enumerate(bm25_scores):
        position_factor = max(0, 1 - (i / n_chunks))  # 1.0 at start, 0.0 at end
        adjusted.append(score + lead_bonus * position_factor * max(bm25_scores))
    return adjusted
```

**Pros**: Exploits web content structure. Ensures the introduction/summary is never filtered out. Zero cost.
**Cons**: Biases against deep content. Not effective for pages where key info is in the middle.
**Verdict**: Include as a lightweight enhancement. The bonus should be small (10-20% of max BM25 score).

### Approach 3: BM25 + Query Term Expansion via Synonyms

Expand query terms with lightweight synonyms before scoring:

```python
SYNONYMS = {
    'implement': ['implementation', 'implementing', 'build', 'develop'],
    'optimal': ['best', 'ideal', 'recommended'],
    'performance': ['speed', 'efficiency', 'throughput', 'latency'],
    # ... domain-specific expansions
}

def expand_query(tokens):
    expanded = list(tokens)
    for token in tokens:
        expanded.extend(SYNONYMS.get(token, []))
    return expanded
```

**Pros**: Directly addresses BM25's vocabulary mismatch weakness.
**Cons**: Requires maintaining a synonym dictionary. Risk of expanding to wrong sense (polysemy). Adds complexity.
**Verdict**: Not for v1. If vocabulary mismatch proves problematic in practice, this is a cheap fix.

### Approach 4: BM25+ Variant (Always-Positive Contribution)

BM25+ modifies the scoring formula to ensure matched terms always contribute positively, even when document length normalization would otherwise suppress them:

```python
# Standard BM25 Okapi: can score near-zero for matches in long docs
score += idf * (tf * (k1 + 1)) / (tf + k1 * (1 - b + b * dl / avgdl))

# BM25+: adds delta to ensure positive contribution
score += idf * ((tf * (k1 + 1)) / (tf + k1 * (1 - b + b * dl / avgdl)) + delta)
```

**Pros**: Mathematically principled fix for short-passage scoring. One parameter (delta, typically 0.5-1.0).
**Cons**: Marginal improvement for chunks of similar length.
**Verdict**: Easy to implement as a flag. Worth including in the code but not as default.

## Recommendation: BM25 + Lead Passage Bonus for v1 [C2]

The hybrid approaches add complexity with marginal benefit for single-page pre-filtering. The strongest justification for hybrid (Anthropic's -49%) comes from full knowledge base retrieval where BM25 and embeddings have complementary strengths.

For v1:
1. **Pure BM25 Okapi** as the core scorer
2. **Lead passage bonus** (10-20% of max score for first 3 chunks) as a cheap structural signal
3. **BM25+ variant available as a flag** for when testing reveals short-passage scoring issues

For v2 (if BM25 proves insufficient):
1. Multi-query BM25 + RRF (leverage the LLM's query reformulations)
2. Lightweight synonym expansion for domain-specific terms

**Do NOT add embeddings or API-based rerankers to the pre-filtering step.** That is a separate recommendation (R5 from prior research) that sits downstream of BM25 pre-filtering, not as a replacement for it.
