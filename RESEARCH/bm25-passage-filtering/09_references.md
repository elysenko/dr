# References

## Primary Sources (Grade A — used for C1 claims)

- [S01] BM25S Official Benchmarks. https://bm25s.github.io/ — Speed benchmarks comparing bm25s, rank_bm25, and Elasticsearch across BEIR datasets.

- [S04] NVIDIA. "Finding the Best Chunking Strategy for Accurate AI Responses." NVIDIA Technical Blog, 2025. https://developer.nvidia.com/blog/finding-the-best-chunking-strategy-for-accurate-ai-responses/ — Chunk size benchmarks (128-2048 tokens) across 4 datasets with overlap testing.

- [S05] Chroma Research. "Evaluating Chunking Strategies for Retrieval." 2024. https://research.trychroma.com/evaluating-chunking — Precision/recall/IoU benchmarks for chunk sizes 200-800 with multiple embedding models.

- [S06] "Rethinking Chunk Size for Long-Document Retrieval: A Multi-Dataset Analysis." arXiv:2505.21700v2, 2025. https://arxiv.org/html/2505.21700v2 — Recall@1 benchmarks across SQuAD, TechQA, NarrativeQA, NewsQA.

- [S07] Anthropic. "Contextual Retrieval." 2024. https://www.anthropic.com/news/contextual-retrieval — Hybrid BM25 + embeddings benchmark showing 49% failure rate reduction with contextual BM25.

- [S08] Thakur et al. "BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models." NeurIPS Datasets and Benchmarks, 2021. https://datasets-benchmarks-proceedings.neurips.cc/paper/2021/file/65b9eea6e1cc6bb9f0cd2a47751a186f-Paper-round2.pdf — BM25 NDCG@10 scores on 18 diverse datasets.

- [S13] Gao et al. "COIL: Revisit Exact Lexical Match in Information Retrieval with Contextualized Inverted List." NAACL 2021. https://aclanthology.org/2021.naacl-main.241.pdf — Analysis of BM25's vocabulary mismatch limitations.

## Secondary Sources (Grade B — used for C2 claims)

- [S02] rank_bm25 GitHub Repository. https://github.com/dorianbrown/rank_bm25 — Source code, API, default parameters (k1=1.5, b=0.75). 1.3k stars, Apache-2.0 license.

- [S03] "BM25 for Python: Achieving high performance while simplifying dependencies with BM25S." HuggingFace Blog. https://huggingface.co/blog/xhluca/bm25s — Library comparison and performance analysis.

- [S09] Crawl4AI Documentation. "Fit Markdown with Pruning & BM25." https://docs.crawl4ai.com/core/fit-markdown/ — BM25ContentFilter implementation for web crawling.

- [S10] LangChain. "BM25 Integration." https://python.langchain.com/docs/integrations/retrievers/bm25/ — BM25Retriever defaults (K=4, text.split() tokenizer, BM25Okapi/BM25+).

- [S11] Pinecone. "Chunking Strategies." https://www.pinecone.io/learn/chunking-strategies/ — Chunking overview with HTML-aware approaches.

- [S12] Elastic. "Practical BM25 - Part 2: The BM25 Algorithm and its Variables." https://www.elastic.co/blog/practical-bm25-part-2-the-bm25-algorithm-and-its-variables — BM25 parameter explanations and tuning guidance.

- [S16] Emergent Mind. "BM25 Retrieval: Methods and Applications." https://www.emergentmind.com/topics/bm25-retrieval — Survey of BM25 methods, variants, and applications.

- [S17] Unstructured. "Chunking for RAG: Best Practices." https://unstructured.io/blog/chunking-for-rag-best-practices — Overlap guidance (10-20%) for RAG chunking.

## Tertiary Sources (Grade C — used for context only)

- [S14] Dataquest. "Metadata Filtering and Hybrid Search for Vector Databases." https://www.dataquest.io/blog/metadata-filtering-and-hybrid-search-for-vector-databases/ — Example where BM25 hybrid hurt performance on academic abstracts.

- [S15] Towards AI. "Enhance Your LLM Agents with BM25: Lightweight Retrieval That Works." https://towardsai.net/p/artificial-intelligence/enhance-your-llm-agents-with-bm25-lightweight-retrieval-that-works — Overview of BM25 for LLM agent applications.

- [S18] Haystack. "Advanced RAG: Query Expansion." https://haystack.deepset.ai/blog/query-expansion — Query expansion techniques for BM25 recall improvement.

## Additional Sources Referenced

- LlamaIndex BM25 Retriever documentation: https://developers.llamaindex.ai/python/examples/retrievers/bm25_retriever/
- bm25-benchmarks repository: https://github.com/xhluca/bm25-benchmarks/
- Milvus RAG chunk size guide: https://milvus.io/ai-quick-reference/what-is-the-optimal-chunk-size-for-rag-applications
- LlamaIndex RAG chunk size evaluation: https://www.llamaindex.ai/blog/evaluating-the-ideal-chunk-size-for-a-rag-system-using-llamaindex-6207e5d3fec5
- NetApp Hybrid RAG blog: https://community.netapp.com/t5/Tech-ONTAP-Blogs/Hybrid-RAG-in-the-Real-World-Graphs-BM25-and-the-End-of-Black-Box-Retrieval/ba-p/464834
- ParadeDB Reciprocal Rank Fusion: https://www.paradedb.com/learn/search-concepts/reciprocal-rank-fusion
