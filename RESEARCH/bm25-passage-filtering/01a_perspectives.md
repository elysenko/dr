# Perspectives

## 1. IR Researcher (Academic)
- Cares about: Retrieval quality metrics (NDCG, MAP, recall@K), proper evaluation methodology, BM25 variant selection
- Key questions: Which BM25 variant is most robust? How does pre-filtering affect downstream task accuracy? What does the BEIR benchmark tell us?

## 2. CLI Tool Developer (Implementer)
- Cares about: Dependencies, startup time, maintainability, code simplicity, installation friction
- Key questions: Can we implement BM25 in pure Python? What is the cold-start latency? How many lines of code?

## 3. RAG Pipeline Engineer (Practitioner)
- Cares about: Integration patterns, chunking strategies, production failure modes, end-to-end latency
- Key questions: What chunk size works for web content? How do LangChain/LlamaIndex do it? What are the gotchas?

## 4. Skeptic / Adversarial
- Cares about: When BM25 pre-filtering actively hurts, false confidence in filtering, vocabulary mismatch risks
- Key questions: When does BM25 filter out relevant passages? Is the complexity justified vs. just passing full content? What about semantic queries?

## 5. LLM Application Developer
- Cares about: Context window utilization, token costs, LLM extraction quality, lost-in-the-middle problem
- Key questions: How many tokens does pre-filtering save? Does reducing context improve or hurt extraction? What top-K optimizes extraction quality?
