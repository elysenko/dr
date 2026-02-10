# Finding 2: Passage Chunking Strategy for Web Content

## The Evidence on Chunk Size

Three independent benchmarks provide overlapping but not identical guidance:

### NVIDIA Chunking Benchmark [C1, S04]
Tested: 128, 256, 512, 1024, 2048 tokens across 4 datasets (FinanceBench, Earnings, RAGBattlePacket, KG-RAG).

| Chunk size | Average accuracy | Notes |
|-----------|-----------------|-------|
| 128 tokens | ~0.59 | Good for factoid queries |
| 256 tokens | ~0.61 | Solid baseline |
| 512 tokens | **0.645** | Best for analytical queries (Earnings peaked at 0.681) |
| 1024 tokens | **0.643** | Best for complex queries (RAGBattlePacket: 0.804) |
| 2048 tokens | ~0.58 | Diminishing returns |
| Page-level | **0.648** | Most consistent (lowest std dev: 0.107) |

**Key finding**: 512-1024 tokens optimal for analytical content. Extreme sizes (128, 2048) hurt.
**Overlap**: 15% performed best on FinanceBench with 1024-token chunks.

### Chroma Chunking Evaluation [C1, S05]
Tested: 200, 250, 300, 400 tokens with 0, 125, 400 overlap.

| Configuration | Recall | Precision | IoU |
|--------------|--------|-----------|-----|
| 200 tokens, no overlap | 88.1% | 7.0% | 6.9% |
| 400 tokens, no overlap | 89.5% | 3.6% | 3.6% |
| 800 tokens, 400 overlap | 85.4% | 1.5% | 1.5% |

**Key finding**: 200-token chunks with no overlap maximized precision and IoU.
**OpenAI's default of 800 tokens + 400 overlap produced "notably weak results."** [C1, S05]

### Multi-Dataset Chunk Size Analysis (arxiv 2505.21700) [C1, S06]
Tested: 64, 128, 256, 512, 1024 tokens across NarrativeQA, SQuAD, TechQA, NewsQA.

Key results (Recall@1):
- **SQuAD** (factoid): 64 tokens = 64.1%, 512 tokens = 49.8% — smaller is better
- **TechQA** (technical): 64 tokens = 4.9%, 512 tokens = 61.4% — larger is better
- **NarrativeQA** (long-form): 1024 tokens = 10.7% — larger is better
- **NewsQA** (news): 512 tokens = 55.9% — medium is best

**Key finding**: Optimal chunk size is highly task-dependent. No universal winner.

## Reconciling the Evidence

The three benchmarks appear to disagree, but the disagreement resolves when you distinguish between **retrieval** and **pre-filtering**:

| Context | Optimal chunk size | Why |
|---------|-------------------|-----|
| Full retrieval (finding needle in haystack) | 512-1024 tokens | Larger chunks carry more context for matching |
| Pre-filtering (reducing noise in already-relevant page) | 200-300 tokens | Smaller chunks produce sharper relevance signals |

For our use case (pre-filtering within a single already-selected page), **smaller chunks are better** because:
1. Each chunk's BM25 score is more discriminative (one relevant sentence in a 200-word chunk dominates; in a 1000-word chunk it is diluted)
2. We are not trying to find a needle — the page is already relevant. We are trimming fat.
3. The LLM sees multiple top-K passages, so context builds from combination, not from individual chunk size.

## Recommended Chunking Strategy for Web Content

### Primary: Paragraph-Based Splitting

Web content (converted to markdown by WebFetch) has natural paragraph boundaries marked by `\n\n`. This is the most semantically meaningful split point for web text.

```python
def chunk_page(text, min_words=50, max_words=300):
    """Split web page text into passages at paragraph boundaries."""
    # Split on double newlines (paragraph boundaries)
    raw_chunks = text.split('\n\n')

    chunks = []
    current = []
    current_len = 0

    for para in raw_chunks:
        para = para.strip()
        if not para:
            continue
        words = len(para.split())

        # Skip tiny fragments (likely boilerplate)
        if words < 10 and not current:
            continue

        # If adding this paragraph exceeds max, flush current
        if current_len + words > max_words and current:
            chunks.append('\n\n'.join(current))
            current = []
            current_len = 0

        current.append(para)
        current_len += words

        # If this single paragraph exceeds max, split at sentences
        if current_len > max_words:
            chunks.append('\n\n'.join(current))
            current = []
            current_len = 0

    # Don't forget the last chunk
    if current:
        chunk_text = '\n\n'.join(current)
        if len(chunk_text.split()) >= min_words:
            chunks.append(chunk_text)

    return chunks
```

### Why No Overlap?

Overlap is designed to prevent information loss at chunk boundaries when you are **discarding** non-selected chunks permanently. In our case:
1. We are only pre-filtering — the LLM sees the top-K chunks, which are typically adjacent or near-adjacent, providing natural context.
2. Paragraph-based splitting already preserves semantic units. A thought that starts in one paragraph and continues in the next will both score high on the same query terms.
3. Overlap increases chunk count, diluting BM25 scores and adding duplicate content to the LLM context.

**Recommendation**: No overlap for paragraph-based chunking. If you switch to fixed-size chunking, add 10-15% overlap.

### Handling HTML Artifacts

WebFetch converts HTML to markdown, but artifacts remain:
- Navigation menus, headers, footers (typically short lines with links)
- Cookie consent / subscription prompts
- Image alt text and captions
- Table-of-contents sections

**Mitigation**: The 50-word minimum chunk size filter handles most of these. Very short fragments (nav items, button text) are discarded automatically. If needed, add a simple boilerplate detector:

```python
BOILERPLATE_SIGNALS = [
    'cookie', 'subscribe', 'sign up', 'log in', 'privacy policy',
    'terms of service', 'all rights reserved', 'follow us',
    'share this', 'related articles', 'advertisement'
]

def is_boilerplate(text):
    text_lower = text.lower()
    hits = sum(1 for s in BOILERPLATE_SIGNALS if s in text_lower)
    return hits >= 2 or (hits >= 1 and len(text.split()) < 30)
```

## Chunk Size Recommendation

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Split method | Paragraph (`\n\n`) | Natural semantic boundaries in web content |
| Target chunk size | ~200 words (±100) | Chroma data shows 200 tokens optimal for precision; paragraph-based naturally clusters here |
| Min chunk size | 50 words | Discard boilerplate fragments |
| Max chunk size | 300 words | Split oversized paragraphs at sentence boundaries |
| Overlap | None | Paragraph boundaries preserve semantics; LLM sees multiple adjacent top-K passages |
