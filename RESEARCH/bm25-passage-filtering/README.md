# BM25 Passage Pre-Filtering for RAG Retrieval Pipelines

## Status: COMPLETE

## Research Question
What is the optimal BM25 passage pre-filtering implementation for a CLI-based deep research tool?

## One-Line Answer
Implement a ~60-line pure-Python BM25 scorer (zero dependencies), chunk web content into ~200-word paragraphs at `\n\n` boundaries, and pass the top-10 passages to the LLM instead of the full page. This cuts context noise by 60-80% with graceful degradation on failure.

## Decision Context
Implementing R4 from search-quality-improvement research. Need concrete library/parameter/architecture choices for zero-dependency CLI tool.

## Key Decisions

| Decision | Recommendation |
|----------|---------------|
| Library | Custom pure-Python (~60 lines, zero deps) |
| Chunk strategy | Paragraph-based splitting on `\n\n` |
| Chunk size | ~200 words target |
| Overlap | None |
| Top-K | 10 (bypass filter for pages with < 15 chunks) |
| BM25 variant | BM25 Okapi (k1=1.2, b=0.75) |
| Hybrid | Not for v1; add query expansion as v2 |
| Tokenizer | `lower().split()` + stopword removal |

## Report Files

| File | Contents |
|------|----------|
| `00_research_contract.md` | Scope, constraints, definition of done |
| `01_research_plan.md` | 7 subquestions with query strategies |
| `01a_perspectives.md` | 5 expert perspectives analyzed |
| `03_source_catalog.csv` | 18 sources graded A-C |
| `04_evidence_ledger.csv` | 15 claims with verification status |
| `05_contradictions_log.md` | 4 contradictions resolved |
| `08_report/00_executive_summary.md` | Recommendations + hypothesis outcomes |
| `08_report/01_context_scope.md` | Problem statement and pipeline flow |
| `08_report/02_findings_implementations.md` | rank_bm25 vs bm25s vs custom (SQ1) |
| `08_report/03_findings_chunking.md` | Chunk size + overlap evidence (SQ2) |
| `08_report/04_findings_comparison.md` | BM25 vs TF-IDF vs alternatives (SQ3) |
| `08_report/05_findings_topk.md` | Top-K optimization (SQ4) |
| `08_report/06_findings_hybrid.md` | Hybrid approaches without embeddings (SQ5) |
| `08_report/07_findings_failure_modes.md` | 7 failure modes cataloged (SQ6) |
| `08_report/08_findings_production.md` | LangChain, LlamaIndex, Anthropic, Crawl4AI (SQ7) |
| `08_report/09_recommendations.md` | Decision matrix + full reference implementation |
| `08_report/10_limitations.md` | 5 limitations, 6 open questions |
| `09_references.md` | All 18+ sources with URLs |
| `09_qa/qa_report.md` | Citation audit, claim coverage, numeric verification |

## Implementation Effort
Estimated: 1 day (core implementation + integration + basic testing)

## Complexity Classification
Type C: ANALYSIS | Intensity: Standard | GoT Depth: 3
