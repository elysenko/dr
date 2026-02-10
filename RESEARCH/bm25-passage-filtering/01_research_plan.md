# Research Plan

## Subquestions

### SQ1: BM25 Implementation Comparison
Libraries evaluated: rank_bm25, bm25s, custom pure-Python
Metrics: speed (queries/sec), dependencies, code complexity, accuracy equivalence

### SQ2: Passage Chunking Strategy for Web Content
Variables: chunk size (128-1024 tokens), overlap (0-20%), HTML awareness
Metrics: recall@K, precision, token efficiency

### SQ3: BM25 vs TF-IDF vs Other Lightweight Retrievers
Comparison: BM25 Okapi, BM25+, TF-IDF, sparse learned (SPLADE-like)
Metrics: NDCG@10 on BEIR, computational cost

### SQ4: Optimal Top-K for Pre-Filtering
Variables: K = 3, 5, 10, 15, 20
Metrics: downstream extraction quality, recall of relevant passages, context noise

### SQ5: Hybrid Approaches Without Embedding Models
Approaches: BM25 + query expansion, BM25 + RRF with multiple query variants, BM25+ for short passages
Constraint: No embedding models, no external APIs

### SQ6: BM25 Failure Modes
Categories: vocabulary mismatch, short queries, domain jargon, semantic queries, boilerplate contamination
Evidence: concrete examples and degradation percentages

### SQ7: Production RAG Pre-Filtering Implementations
Systems: LangChain BM25Retriever, LlamaIndex BM25 retriever, Anthropic contextual retrieval, Crawl4AI BM25ContentFilter
Extract: defaults, architecture patterns, integration points

## Budget Tracking
- Searches used: ~18/25
- Fetches used: ~12/20
- Deep reads: ~8/10
