# Context and Scope

## Background
The deep research CLI tool (`/dr`) fetches web pages during Phase 3 (Iterative Querying) and passes their content to an LLM for evidence extraction. Currently, the full page content — often 3,000-10,000+ words including navigation, boilerplate, sidebars, and tangential content — is sent to the LLM.

This creates two problems:
1. **Context noise**: The LLM must sift through irrelevant content, increasing the chance of extracting low-quality passages or missing relevant ones buried in noise.
2. **Token waste**: Full pages consume significant context window, limiting the number of pages that can be processed per LLM call.

R4 from the prior search-quality-improvement research recommended BM25 passage pre-filtering as a P1 improvement with ~1.5 day implementation effort and expected +5-10% passage relevance improvement.

## Current Pipeline Flow
```
WebSearch (query) -> URLs
  -> WebFetch (URL) -> Full page markdown
    -> LLM extraction (full page + subquestion) -> Evidence passages
```

## Proposed Pipeline Flow
```
WebSearch (query) -> URLs
  -> WebFetch (URL) -> Full page markdown
    -> Chunk (page -> passages)
      -> BM25 Score (passages vs subquestion)
        -> Top-K selection
          -> LLM extraction (top-K passages + subquestion) -> Evidence passages
```

## Scope Boundaries

### In Scope
- BM25 scoring algorithm selection and implementation
- Text chunking strategy for web-sourced markdown content
- Top-K parameter selection
- Lightweight hybrid approaches (no external APIs)
- Failure mode analysis and mitigations
- Reference implementation code

### Out of Scope
- Embedding-based retrieval (requires models/APIs)
- Cross-encoder reranking (covered by R5 as separate recommendation)
- Full knowledge base retrieval (this is single-page pre-filtering only)
- HTML parsing improvements (the tool already converts to markdown via WebFetch)
- Query reformulation (covered by R3)

## Key Constraint
The implementation must work as a Python script invoked by the Claude Code agent via Bash. It receives page content and a query, and outputs filtered passages. Zero or near-zero external Python package dependencies.
