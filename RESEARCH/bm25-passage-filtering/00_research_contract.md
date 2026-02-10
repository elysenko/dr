# Research Contract: BM25 Passage Pre-Filtering for RAG Retrieval Pipelines

## Core Question
What is the optimal BM25 passage pre-filtering implementation for a CLI-based deep research tool that fetches web pages and extracts evidence passages?

## Decision Context
Implementing R4 from search-quality-improvement research. The deep research CLI currently passes full fetched page content to the LLM for extraction. BM25 pre-filtering would reduce context noise and improve passage relevance before LLM processing.

## Audience
Technical — the developer implementing this feature.

## Scope
- Python implementations of BM25 (libraries and custom)
- Web content chunking strategies (HTML-aware)
- Comparison with alternative lightweight retrievers
- Top-K parameter optimization for pre-filtering
- Hybrid approaches achievable without embedding models or APIs
- Failure modes and when BM25 hurts rather than helps
- Production implementation patterns from LangChain, LlamaIndex, Anthropic

## Constraints
- Zero or near-zero external Python package dependencies (CLI tool)
- No embedding models or external APIs for the base implementation
- Must handle messy web content (HTML artifacts, boilerplate, varying structure)
- Latency budget: <100ms for scoring a single page's passages

## Output Format
Implementation-focused report with:
- Concrete library recommendation
- Specific parameter values (chunk size, overlap, top-K, k1, b)
- Reference implementation code
- Decision matrix for tradeoffs
- Failure mode catalog with mitigations

## Definition of Done
Clear, evidence-backed recommendation on: library, chunk size, top-K, and whether hybrid approach is warranted. Includes working reference implementation.

## Complexity
Type C: ANALYSIS — Multiple dimensions of judgment with clear decision context.

## Intensity
Standard: 3-5 agents, GoT depth 3, stop score > 8.
