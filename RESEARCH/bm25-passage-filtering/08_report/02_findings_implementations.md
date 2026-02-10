# Finding 1: BM25 Implementation Comparison

## The Three Options

### Option A: rank_bm25 (pip package)
- **Repository**: github.com/dorianbrown/rank_bm25 [S02]
- **Stars**: 1.3k | **Last release**: Feb 2022 (v0.2.2) | **Commits**: 58
- **Dependencies**: numpy
- **Variants**: BM25Okapi, BM25L, BM25+ (BM25-Adpt and BM25T incomplete)
- **Default parameters**: k1=1.5, b=0.75, epsilon=0.25
- **Speed**: 0.04-47.6 queries/sec depending on corpus size [S01]
- **Code size**: ~257 lines total for all variants
- **Tokenization**: User-provided (no built-in preprocessing)

**Strengths**: Readable code, well-tested, simple API. `get_scores(query)` returns array of scores.

**Weaknesses**: Requires numpy (18MB). Last updated 2022. The authors themselves recommend "retriv" for production. Speed degrades significantly on large corpora (>1M docs), but this is irrelevant for our 10-50 chunk use case.

### Option B: bm25s (pip package)
- **Repository**: github.com/xhluca/bm25s [S01, S03]
- **Dependencies**: numpy (18MB) + scipy (37MB)
- **Variants**: Robertson, ATIRE, BM25L, BM25+, Lucene
- **Speed**: 12-953 queries/sec — up to 500x faster than rank_bm25 [S01]
- **Features**: Memory-mapped indexes, sparse matrix storage, optional Numba backend

**Speed comparison (queries/sec on CPU)** [C1, S01]:

| Dataset (corpus size) | bm25s | rank_bm25 | Speedup |
|----------------------|-------|-----------|---------|
| MS MARCO (8.8M docs) | 12.20 | 0.07 | 174x |
| NQ (2.7M docs) | 41.85 | 0.10 | 419x |
| SciFact (5K docs) | 952.92 | 47.60 | 20x |
| HotpotQA (5.2M docs) | 20.88 | 0.04 | 522x |

**Strengths**: Dramatically faster for large corpora. Comparable to Elasticsearch without Java/server setup.

**Weaknesses**: Heavier dependencies (55MB total). Speed advantage is irrelevant for our use case (10-50 chunks). More complex API.

### Option C: Custom Pure-Python Implementation
- **Dependencies**: None (stdlib only: `math`, `collections`)
- **Code size**: ~40-60 lines for BM25 Okapi
- **Speed**: Adequate for <100 documents (our use case)

**The BM25 Okapi algorithm is mathematically straightforward** [S02, S12]:

```python
import math
from collections import Counter

class BM25:
    def __init__(self, corpus, k1=1.5, b=0.75):
        self.k1 = k1
        self.b = b
        self.corpus = corpus
        self.doc_len = [len(doc) for doc in corpus]
        self.avgdl = sum(self.doc_len) / len(corpus) if corpus else 1
        self.doc_freqs = {}  # term -> number of docs containing it
        self.tf = []  # per-doc term frequencies
        self.N = len(corpus)

        for doc in corpus:
            frequencies = Counter(doc)
            self.tf.append(frequencies)
            for term in frequencies:
                self.doc_freqs[term] = self.doc_freqs.get(term, 0) + 1

    def _idf(self, term):
        n = self.doc_freqs.get(term, 0)
        return math.log((self.N - n + 0.5) / (n + 0.5) + 1)

    def score(self, query, doc_idx):
        score = 0.0
        doc_tf = self.tf[doc_idx]
        dl = self.doc_len[doc_idx]
        for term in query:
            tf = doc_tf.get(term, 0)
            idf = self._idf(term)
            numerator = tf * (self.k1 + 1)
            denominator = tf + self.k1 * (1 - self.b + self.b * dl / self.avgdl)
            score += idf * numerator / denominator
        return score

    def get_scores(self, query):
        return [self.score(query, i) for i in range(self.N)]

    def get_top_n(self, query, n=10):
        scores = self.get_scores(query)
        ranked = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
        return ranked[:n], [scores[i] for i in ranked[:n]]
```

**Strengths**: Zero dependencies. Trivially readable. No import overhead. Easy to modify (e.g., add BM25+ variant). Fits the CLI tool's philosophy.

**Weaknesses**: No numpy vectorization (irrelevant for <100 docs). No disk persistence (irrelevant — we score and discard). Not battle-tested like libraries.

## Recommendation: Option C (Custom Pure-Python) [C1]

**Rationale**:
1. **The corpus is tiny.** We are scoring 10-50 chunks from a single web page. At this scale, the performance difference between numpy-vectorized and pure-Python is microseconds. bm25s's 500x speedup over rank_bm25 is meaningless when both complete in <1ms on 50 documents.

2. **Zero dependencies is the right call.** The CLI tool invokes Python scripts via Bash. Adding numpy (18MB) or scipy (37MB) as a dependency creates installation friction, version conflicts, and a larger attack surface — all for a 40-line algorithm.

3. **The algorithm is well-understood.** BM25 Okapi has been stable since the 1990s. There is no risk of subtle implementation bugs that a library would protect against. The math is a single formula.

4. **Customization is easy.** Need to add lead-passage bias? Adjust IDF floor? Switch to BM25+? With custom code, it is a 2-line change. With a library, you are constrained by its API.

**When to reconsider**: If the tool later needs to maintain a persistent BM25 index across multiple pages (batch scoring), rank_bm25 or bm25s would become worthwhile. For single-page pre-filtering, they are overkill.

## BM25 Parameters

The standard defaults are well-established [S02, S12]:

| Parameter | Default | Purpose | When to adjust |
|-----------|---------|---------|----------------|
| k1 | 1.5 | Term frequency saturation | Lower (1.2) for short passages, higher (2.0) for long documents |
| b | 0.75 | Document length normalization | Lower (0.5) if chunks are similar length, higher (0.9) if highly variable |
| epsilon | 0.25 | IDF floor (rank_bm25-specific) | Only relevant for negative IDF handling |

For our use case (web page chunks of similar size), **k1=1.2, b=0.75** is a reasonable starting point. The lower k1 prevents a single query term from dominating the score in short passages.
