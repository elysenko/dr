# Recommendations and Reference Implementation

## Decision Matrix

| Decision | Option A | Option B | Option C | **Recommended** |
|----------|----------|----------|----------|-----------------|
| **Library** | rank_bm25 (numpy dep) | bm25s (numpy+scipy) | Custom pure-Python | **C: Custom** |
| **Chunk strategy** | Fixed 512 tokens | Sentence-based | Paragraph-based (\n\n) | **C: Paragraph** |
| **Chunk size** | 128 words | 200 words | 300 words | **B: ~200 words** |
| **Overlap** | 10-15% | None | 50 words | **B: None** |
| **Top-K** | 5 | 10 | 20 | **B: 10** |
| **BM25 variant** | BM25 Okapi | BM25+ | BM25L | **A: Okapi** |
| **Tokenizer** | Stemming + stopwords | lower().split() | NLTK/spaCy | **B: lower().split() + stopwords** |
| **Hybrid** | BM25 + embeddings | BM25 + query expansion | BM25 only | **C + lead bonus** |

## Complete Reference Implementation

```python
#!/usr/bin/env python3
"""
BM25 passage pre-filtering for web page content.
Zero external dependencies — uses only Python stdlib.

Usage:
    echo '{"query": "...", "content": "..."}' | python bm25_filter.py
    python bm25_filter.py --query "..." --file page.md

Output: JSON array of top-K passages with scores.
"""

import json
import math
import sys
from collections import Counter

# --- Configuration ---
DEFAULT_K = 10
BYPASS_THRESHOLD = 15  # Pass all chunks if fewer than this
MIN_CHUNK_WORDS = 50
MAX_CHUNK_WORDS = 300
BM25_K1 = 1.2
BM25_B = 0.75
LEAD_BONUS = 0.15  # Position bonus as fraction of max score

# Common English stopwords (top 50 — enough for pre-filtering)
STOPWORDS = frozenset([
    'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from',
    'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'or', 'she',
    'that', 'the', 'to', 'was', 'were', 'will', 'with', 'you', 'your',
    'this', 'they', 'but', 'have', 'had', 'what', 'when', 'where',
    'which', 'who', 'how', 'not', 'no', 'can', 'do', 'does', 'if',
    'than', 'then', 'so', 'we', 'our'
])

BOILERPLATE_SIGNALS = [
    'cookie', 'subscribe', 'sign up', 'log in', 'privacy policy',
    'terms of service', 'all rights reserved', 'follow us',
    'share this', 'related articles', 'advertisement', 'newsletter'
]


# --- Tokenizer ---
def tokenize(text):
    """Simple tokenizer: lowercase, split, remove stopwords and short tokens."""
    return [
        w for w in text.lower().split()
        if w not in STOPWORDS and len(w) > 2 and w.isalpha()
    ]


# --- Chunker ---
def chunk_page(text, min_words=MIN_CHUNK_WORDS, max_words=MAX_CHUNK_WORDS):
    """Split web page text into passages at paragraph boundaries."""
    raw_chunks = text.split('\n\n')
    chunks = []
    current_parts = []
    current_len = 0

    for para in raw_chunks:
        para = para.strip()
        if not para:
            continue

        words = para.split()
        word_count = len(words)

        # Skip tiny fragments (likely boilerplate/nav)
        if word_count < 8 and not current_parts:
            continue

        # Check for boilerplate
        if _is_boilerplate(para):
            continue

        # If adding this paragraph exceeds max, flush current buffer
        if current_len + word_count > max_words and current_parts:
            chunks.append('\n\n'.join(current_parts))
            current_parts = []
            current_len = 0

        current_parts.append(para)
        current_len += word_count

        # If buffer exceeds max, flush it
        if current_len >= max_words:
            chunks.append('\n\n'.join(current_parts))
            current_parts = []
            current_len = 0

    # Flush remaining
    if current_parts:
        chunk_text = '\n\n'.join(current_parts)
        if len(chunk_text.split()) >= min_words:
            chunks.append(chunk_text)
        elif chunks:
            # Append small trailing content to last chunk
            chunks[-1] += '\n\n' + chunk_text

    return chunks


def _is_boilerplate(text):
    """Detect likely boilerplate content."""
    text_lower = text.lower()
    hits = sum(1 for s in BOILERPLATE_SIGNALS if s in text_lower)
    word_count = len(text.split())
    return hits >= 2 or (hits >= 1 and word_count < 30)


# --- BM25 Scorer ---
class BM25:
    """BM25 Okapi scorer. Zero dependencies."""

    def __init__(self, corpus, k1=BM25_K1, b=BM25_B):
        self.k1 = k1
        self.b = b
        self.N = len(corpus)
        self.doc_len = [len(doc) for doc in corpus]
        self.avgdl = sum(self.doc_len) / self.N if self.N > 0 else 1
        self.doc_freqs = {}
        self.tf = []

        for doc in corpus:
            freq = Counter(doc)
            self.tf.append(freq)
            for term in freq:
                self.doc_freqs[term] = self.doc_freqs.get(term, 0) + 1

    def _idf(self, term):
        n = self.doc_freqs.get(term, 0)
        return math.log((self.N - n + 0.5) / (n + 0.5) + 1)

    def score(self, query, doc_idx):
        s = 0.0
        dl = self.doc_len[doc_idx]
        tf = self.tf[doc_idx]
        for term in query:
            f = tf.get(term, 0)
            if f == 0:
                continue
            idf = self._idf(term)
            num = f * (self.k1 + 1)
            den = f + self.k1 * (1 - self.b + self.b * dl / self.avgdl)
            s += idf * num / den
        return s

    def get_scores(self, query):
        return [self.score(query, i) for i in range(self.N)]


# --- Main Pipeline ---
def filter_passages(content, query, k=DEFAULT_K, bypass_threshold=BYPASS_THRESHOLD):
    """
    Pre-filter web page content using BM25 scoring.

    Args:
        content: Full page text (markdown)
        query: The search subquestion
        k: Number of top passages to return
        bypass_threshold: Pass all if fewer chunks than this

    Returns:
        List of dicts: [{"text": ..., "score": ..., "index": ...}, ...]
    """
    # Chunk the page
    chunks = chunk_page(content)

    if not chunks:
        return [{"text": content[:3000], "score": 0.0, "index": 0}]

    # Bypass filter for short pages
    if len(chunks) <= bypass_threshold:
        return [
            {"text": c, "score": 1.0, "index": i}
            for i, c in enumerate(chunks)
        ]

    # Tokenize chunks and query
    tokenized_chunks = [tokenize(c) for c in chunks]
    tokenized_query = tokenize(query)

    if not tokenized_query:
        # Query produced no usable tokens — return all
        return [
            {"text": c, "score": 1.0, "index": i}
            for i, c in enumerate(chunks)
        ]

    # Score with BM25
    bm25 = BM25(tokenized_chunks)
    scores = bm25.get_scores(tokenized_query)

    # Add lead passage bonus
    max_score = max(scores) if scores else 1.0
    if max_score > 0:
        for i in range(len(scores)):
            position_factor = max(0, 1 - (i / len(scores)))
            scores[i] += LEAD_BONUS * position_factor * max_score

    # Select top-K
    ranked = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
    top_indices = ranked[:k]

    # Return in original document order (preserves reading flow)
    top_indices.sort()

    return [
        {"text": chunks[i], "score": round(scores[i], 4), "index": i}
        for i in top_indices
    ]


# --- CLI Interface ---
if __name__ == '__main__':
    if '--help' in sys.argv or '-h' in sys.argv:
        print(__doc__)
        sys.exit(0)

    # Read from stdin (JSON with "query" and "content" fields)
    if not sys.stdin.isatty():
        data = json.load(sys.stdin)
        query = data.get('query', '')
        content = data.get('content', '')
        k = data.get('k', DEFAULT_K)
    else:
        # Read from arguments
        import argparse
        parser = argparse.ArgumentParser(description='BM25 passage pre-filtering')
        parser.add_argument('--query', required=True, help='Search query')
        parser.add_argument('--file', required=True, help='Path to page content')
        parser.add_argument('--k', type=int, default=DEFAULT_K, help='Top-K passages')
        args = parser.parse_args()
        query = args.query
        with open(args.file) as f:
            content = f.read()
        k = args.k

    results = filter_passages(content, query, k=k)
    json.dump(results, sys.stdout, indent=2)
    print()  # Trailing newline
```

## Integration Points

### How the Agent Uses This

The deep research agent invokes this script during Phase 3 after fetching a page:

```
1. WebFetch returns page markdown content
2. Agent saves content to temp file
3. Agent runs: echo '{"query":"<subquestion>","content":"<page_content>"}' | python bm25_filter.py
4. Agent receives JSON array of top-10 passages
5. Agent uses passages (not full page) for evidence extraction
```

### Fallback Behavior

The script degrades gracefully in all edge cases:
- **Empty content**: Returns truncated original content
- **Short page (< 15 chunks)**: Returns all chunks unfiltered
- **No usable query tokens**: Returns all chunks unfiltered
- **Single chunk**: Returns that chunk
- **All scores zero**: Returns first K chunks (lead bias still applies)

## Configuration Recommendations

### For Different Research Types

| Research Type | K | bypass_threshold | Rationale |
|--------------|---|-----------------|-----------|
| Type A (Lookup) | 5 | 10 | Narrow focus, precision matters |
| Type B (Synthesis) | 10 | 15 | Balanced (default) |
| Type C (Analysis) | 10 | 15 | Balanced (default) |
| Type D (Investigation) | 15 | 20 | Broader recall for complex topics |

### Performance Expectations

| Metric | Expected Value |
|--------|---------------|
| Scoring latency (50 chunks) | < 5ms |
| Chunking latency (5000 words) | < 2ms |
| Total pipeline overhead | < 10ms per page |
| Token reduction per page | 50-75% |
| Relevant passage retention | 85-95% (estimated) |

## What to Measure After Implementation

1. **Passage relevance**: Compare LLM extraction quality with and without BM25 filtering on 20+ research sessions
2. **False negative rate**: How often does BM25 filter out passages that the LLM would have extracted from?
3. **Token savings**: Actual token reduction across different page types
4. **Latency**: Verify < 10ms overhead in practice
5. **Edge cases**: Pages where filtering clearly hurt (log for failure mode analysis)

## Implementation Checklist

- [ ] Create `bm25_filter.py` based on reference implementation
- [ ] Add to CLI tool's utility scripts
- [ ] Integrate into Phase 3 agent prompts (invoke after WebFetch)
- [ ] Add bypass for short pages (< 15 chunks)
- [ ] Add lead passage bonus
- [ ] Test on 10 diverse web pages (short, long, technical, news, academic)
- [ ] Compare extraction quality: full page vs BM25-filtered
- [ ] Tune K if needed based on test results
- [ ] Document in pipeline architecture notes
