# Contradictions Log

## CON1: Chunk Size — NVIDIA vs Chroma vs Arxiv

**Conflict type**: Data disagreement

| Source | Recommendation | Context |
|--------|---------------|---------|
| NVIDIA [S04] | 512-1024 tokens | Financial/analytical documents, accuracy metric |
| Chroma [S05] | 200 tokens | Precision + IoU metric, multiple embedding models |
| Arxiv [S06] | "Depends on dataset" | 64-1024 tested, no single winner |

**Resolution**: The disagreement is explained by context differences. NVIDIA optimized for answer accuracy (larger context helps the LLM). Chroma optimized for precision and token efficiency (smaller chunks reduce noise). For pre-filtering specifically, where the goal is noise reduction before LLM processing, Chroma's precision-focused finding (200 tokens) is more relevant. NVIDIA's finding applies to the downstream LLM step, not the pre-filtering step.

**Confidence in resolution**: MEDIUM. The distinction is logical but not experimentally validated for BM25 pre-filtering specifically.

## CON2: Top-K — Anthropic K=20 vs LangChain K=4

**Conflict type**: Methodological difference

| Source | K Value | Context |
|--------|---------|---------|
| Anthropic [S07] | 20 | Full knowledge base retrieval, many documents |
| LangChain [S10] | 4 | RAG pipeline, large chunks (~800 tokens) |

**Resolution**: K scales inversely with chunk size and directly with corpus scope. Anthropic retrieves from thousands of chunks across many documents (needs high recall). LangChain retrieves from a pre-chunked document set with large chunks (each chunk carries more context). K=10 with 200-word chunks is proportionally between these: 10 chunks x 200 words = 2,000 words, vs LangChain's 4 chunks x ~600 words = 2,400 words.

**Confidence in resolution**: HIGH. The scaling relationship is straightforward.

## CON3: BM25 Alone vs Hybrid — When to add complexity

**Conflict type**: Interpretation disagreement

| Source | Position | Evidence |
|--------|----------|----------|
| Anthropic [S07] | Hybrid (BM25+embeddings) is 49% better | Benchmark on knowledge base retrieval |
| RAG literature | Hybrid recommended as best practice | Multiple sources, multiple contexts |
| Crawl4AI [S09] | BM25-only is fine for web content | Production web crawling system |

**Resolution**: For single-page pre-filtering (not knowledge base retrieval), BM25-only is sufficient. The hybrid advantage comes from complementary strengths across large, diverse corpora where vocabulary mismatch is systemic. Within a single web page already selected for query relevance, vocabulary overlap is naturally high, reducing the marginal benefit of embeddings.

**Confidence in resolution**: MEDIUM. This is a reasonable inference but not directly tested.

## CON4: Overlap — 10-15% vs None

**Conflict type**: Methodological difference

| Source | Recommendation | Context |
|--------|---------------|---------|
| NVIDIA [S04] | 15% overlap | Fixed-size token chunking |
| Chroma [S05] | No overlap | Precision-focused evaluation |
| Industry practice | 10-20% overlap | General RAG best practice |

**Resolution**: Overlap is needed when fixed-size chunking splits content mid-sentence or mid-thought. Paragraph-based chunking preserves natural boundaries, making overlap unnecessary. Additionally, for pre-filtering (not permanent chunk selection), the consequences of a boundary miss are mild — the LLM sees multiple adjacent passages that provide overlapping context naturally.

**Confidence in resolution**: HIGH for paragraph-based chunking. If switching to fixed-size chunking, add 10-15% overlap.
