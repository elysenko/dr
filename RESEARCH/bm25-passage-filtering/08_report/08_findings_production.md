# Finding 7: How Production RAG Systems Implement Passage Pre-Filtering

## LangChain BM25Retriever [C1, S10]

### Implementation Details
- **Library**: rank_bm25 (BM25Okapi by default)
- **Default K**: 4 documents
- **Default tokenizer**: `text.split()` (simple whitespace splitting)
- **BM25 variant**: BM25Okapi (default), BM25Plus available via `bm25_variant="plus"`
- **Parameters**: Passed via `bm25_params` dict (k1, b, delta for BM25+)
- **Preprocessing**: User-provided `preprocess_func`, default is `lambda text: text.split()`

### Architecture
LangChain wraps rank_bm25 as a retriever interface:
1. `from_texts()` or `from_documents()` creates the index
2. Documents are tokenized via `preprocess_func`
3. `_get_relevant_documents(query)` tokenizes the query the same way and calls `bm25.get_top_n()`
4. Returns top-K Document objects with metadata

### Key Design Decisions
- **No built-in chunking**: LangChain separates chunking (TextSplitters) from retrieval (Retrievers). The user chunks first, then builds the BM25 index.
- **K=4 is conservative**: LangChain defaults to 4 because it targets RAG pipelines where each "document" might be a large chunk (800+ tokens). For our smaller chunks, K=10 is more appropriate.
- **BM25Plus for short passages**: LangChain explicitly documents BM25+ as better for "short texts, passages, or chunked documents commonly used in RAG workflows."

### Relevance to Our Implementation
LangChain validates our approach: simple whitespace tokenization + BM25Okapi + configurable K is the production-standard pattern. Their K=4 is low because their default chunk size is larger.

## LlamaIndex BM25 Retriever [C2, referenced in search results]

### Implementation Details
- **Library**: rank_bm25 or bm25s (configurable)
- **Default similarity_top_k**: Variable (user-specified)
- **Tokenizer**: Configurable, defaults to simple splitting
- **Hybrid support**: `QueryFusionRetriever` with Reciprocal Rank Fusion for combining BM25 with vector retrieval

### Architecture
LlamaIndex's approach mirrors LangChain but with tighter integration:
1. Nodes (chunks) are created by NodeParsers (chunkers)
2. BM25Retriever indexes nodes
3. `retrieve(query)` returns scored nodes
4. Optional: fuse with vector retriever via RRF

### Key Design Decision
LlamaIndex emphasizes **hybrid retrieval** (BM25 + dense) as the default recommendation, not BM25 alone. This aligns with Anthropic's evidence but assumes embedding model availability.

## Anthropic Contextual Retrieval [C1, S07]

### Implementation Details
- **Chunk size**: "No more than a few hundred tokens" — cost calculations assume 800-token chunks from 8K-token documents
- **Top-K**: 20 (tested 5, 10, 20 — 20 was best)
- **BM25 role**: Combined with contextual embeddings via rank fusion
- **Reranking**: Top-150 initial retrieval, reranked to top-20
- **Context injection**: 50-100 tokens of context prepended to each chunk before indexing

### The "Contextual BM25" Innovation
Anthropic's key insight: BM25 scoring improves when each chunk is prepended with document-level context (e.g., "This chunk is from the section about BM25 parameters in a document about information retrieval"). This context adds relevant terms that the chunk alone might lack.

**Relevance**: This is impractical for single-page pre-filtering (we would need an LLM call per chunk to generate context, defeating the purpose of pre-filtering). But it validates that BM25's keyword limitation CAN be mitigated with term enrichment.

### Performance Numbers [C1, S07]
- Embeddings only: 5.7% failure rate
- Contextual Embeddings + Contextual BM25: 2.9% failure rate (-49%)
- + Reranking: 1.9% failure rate (-67%)
- Best K: 20 for retrieval, then reranked

## Crawl4AI BM25ContentFilter [C2, S09]

### Implementation Details
- **Parameters**: `user_query` (string), `bm25_threshold` (float, default 1.0)
- **Approach**: Score-based threshold filtering (not top-K)
- **Integration**: Built into the crawling pipeline — filters content during crawl, not after
- **Two-pass strategy**: First PruningContentFilter (removes HTML boilerplate by text density), then BM25ContentFilter (removes query-irrelevant content)

### Architecture
Crawl4AI's approach is notably different from RAG frameworks:
1. **Prune first**: Remove boilerplate by HTML structure analysis (text density, link density, tag importance)
2. **Then BM25 filter**: Score remaining content against query, remove low-scoring chunks
3. **Output**: "fit_markdown" — query-relevant content only

### Key Design Decision
Crawl4AI uses a **threshold** rather than top-K. This is appropriate for web crawling where page sizes vary wildly and a fixed K would be meaningless across 50-word pages and 10,000-word pages. For our use case (pre-filtering single pages for LLM extraction), top-K is simpler and more predictable.

### Relevance
The two-pass approach (structural pruning + BM25 scoring) is worth noting. Our chunking strategy (50-word minimum, boilerplate detection) achieves similar structural pruning without a separate pass.

## Synthesis: Production Patterns

| System | BM25 Library | Default K | Tokenizer | Hybrid? |
|--------|-------------|-----------|-----------|---------|
| LangChain | rank_bm25 | 4 | `text.split()` | Optional (EnsembleRetriever) |
| LlamaIndex | rank_bm25/bm25s | User-set | Configurable | Yes (QueryFusionRetriever) |
| Anthropic | Not disclosed | 20 | Not disclosed | Yes (RRF with embeddings) |
| Crawl4AI | Custom | Threshold-based | Not disclosed | No (BM25 only after HTML pruning) |

### Common Patterns
1. **Simple tokenization is standard.** `text.split()` is the default everywhere. No stemming, no lemmatization, no sophisticated NLP.
2. **BM25 Okapi is the universal default.** Nobody uses TF-IDF. BM25+ is available but not default.
3. **K varies by context.** Smaller K for large chunks (LangChain: K=4 with 800-token chunks), larger K for small chunks or recall-critical tasks (Anthropic: K=20).
4. **Hybrid is recommended but BM25-only is viable.** All frameworks support BM25 standalone.
5. **rank_bm25 is the most common library.** Despite being unmaintained since 2022, it remains the de facto standard.

### Implications for Our Implementation
- Our approach (custom pure-Python, paragraph chunking, K=10, simple tokenization) aligns with production patterns.
- The main deviation is not using rank_bm25 — justified by our zero-dependency constraint and tiny corpus size.
- K=10 with 200-word chunks is proportionally similar to LangChain's K=4 with 800-token chunks (both capture ~3,200-4,000 tokens of content).
