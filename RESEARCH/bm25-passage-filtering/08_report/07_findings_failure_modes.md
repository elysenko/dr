# Finding 6: BM25 Failure Modes — When Does It Hurt?

## Failure Mode Catalog

### FM1: Vocabulary Mismatch [C1, S13, S16]
**Description**: Query uses different terms than the passage for the same concept. "heart attack" vs "myocardial infarction", "car" vs "automobile", "ML" vs "machine learning".

**Severity for our use case**: MODERATE. Research queries from the deep research tool tend to use precise terminology that matches the pages being searched (because the search engine selected those pages for the same terms). The mismatch risk is lower than in open-domain QA.

**Example**:
- Query: "How does BM25 handle vocabulary gaps?"
- Relevant passage: "Term mismatch is a fundamental limitation of lexical retrieval..."
- BM25 score: Low (no overlapping terms except common words)
- Result: Passage filtered out incorrectly

**Mitigation**:
1. The LLM's subquestions typically contain multiple formulations of the concept
2. Lead passage bonus ensures the introduction (which often uses varied terminology) is included
3. K=10 provides enough headroom that moderately-scored passages still make the cut
4. For v2: lightweight synonym expansion

### FM2: Very Short Queries (1-2 words) [C2, S16]
**Description**: BM25 scoring with 1-2 query terms produces poor discrimination. IDF of a single common term is near-zero, making all passages score similarly.

**Severity for our use case**: LOW. The deep research tool generates subquestions, not keywords. A typical subquestion is 10-20 words ("What are the failure modes of BM25 pre-filtering for passage retrieval?"), providing rich query terms.

**Mitigation**: Not needed. If it arises, split the subquestion into key phrases as multiple query terms.

### FM3: Semantic Queries [C2, S13, S14]
**Description**: Queries asking "why" or "how" where the answer uses entirely different vocabulary. "Why did the project fail?" might be answered by "Budget overruns and scope creep led to cancellation."

**Severity for our use case**: MODERATE. Some research subquestions are inherently semantic ("What would change these conclusions?"). However, relevant passages typically still share SOME vocabulary with the query.

**Evidence**: On conversational/semantic queries, dense retrieval "typically outperforms BM25" [S13]. The COIL paper shows BM25's exact match requirement is its core weakness for semantic tasks.

**Mitigation**:
1. K=10 provides recall headroom
2. Lead passage bonus captures introductory context
3. The bypass threshold (pass all chunks for short pages) prevents aggressive filtering
4. The LLM can still extract from adjacent-but-not-top-scored passages

### FM4: Boilerplate Contamination [C2, observed in web content]
**Description**: Web page boilerplate (navigation, footer, sidebars) contains query-relevant terms that inflate boilerplate chunk scores. Example: A tech blog about "BM25" has "BM25" in its navigation sidebar, category tags, and related article links.

**Severity for our use case**: LOW-MODERATE. The chunking strategy (50-word minimum, boilerplate detection) handles most cases. But some boilerplate sections are long enough to pass the minimum.

**Mitigation**:
1. Minimum chunk size filter (50 words) eliminates most nav/footer boilerplate
2. Boilerplate signal detection (cookie notices, subscribe prompts)
3. BM25's term frequency saturation prevents boilerplate with repeated keywords from scoring disproportionately high

### FM5: Query-Document Length Mismatch [C2, S12]
**Description**: When query length is very different from chunk length, BM25 scoring can be biased. Very long queries have many terms, inflating scores for chunks that match ANY subset.

**Severity for our use case**: LOW. Subquestions are typically 10-30 words. Chunks are 100-300 words. The ratio is reasonable.

**Mitigation**: k1 parameter tuning. Lower k1 (1.2 instead of 1.5) reduces the impact of repeated terms in longer queries.

### FM6: Domain-Specific Jargon Without Context [C2, S13]
**Description**: Technical content uses jargon that BM25 treats as any other token. "NDCG" is just a string — BM25 does not know it relates to "ranking quality" or "information retrieval metrics."

**Severity for our use case**: LOW. If the page is about IR metrics and the query mentions "NDCG", the overlap exists. The problem arises only when query and passage use different levels of abstraction.

**Mitigation**: None needed. This is an inherent limitation of any keyword-based method, and it is mild in practice for within-page pre-filtering.

### FM7: Tables and Structured Data [C2, S16]
**Description**: BM25 treats all text equally. Tabular data (numbers, column headers) is tokenized alongside prose but may not score well because individual cells are short and fragmented.

**Severity for our use case**: MODERATE. Web pages often contain data tables, comparison charts, and specification lists that are highly relevant but score poorly with BM25.

**Mitigation**:
1. Chunk tables as single units (don't split a table across chunks)
2. Prepend table headers/context to table chunks
3. For v2: detect table-like structures and apply boosted scoring

## When BM25 Pre-Filtering Actively Hurts

BM25 pre-filtering is net-negative when ALL of these conditions hold simultaneously:

1. **The page is short** (< 15 chunks) — filtering removes too much from too little
2. **The query is semantic** — vocabulary overlap is low
3. **The relevant content is in the middle/end** — lead bias does not help
4. **The relevant content uses different terminology** — BM25 scores it low

This combination is uncommon for our use case because:
- The bypass threshold handles short pages
- Search engine selection ensures baseline vocabulary overlap
- Web content front-loads key information

**Estimated frequency**: 5-10% of pages might see suboptimal filtering. The degradation is mild (slightly-less-relevant passages selected, not garbage).

## The Critical Insight: Graceful Degradation

BM25 pre-filtering's worst case is **returning the wrong subset of an already-relevant page**. The LLM still sees relevant content — just not the most relevant. Compare to the worst case of no filtering: the LLM sees everything but may be distracted by noise or hit context limits.

The failure mode is symmetrical:
- **BM25 fails**: LLM sees 10 slightly-less-optimal passages from a relevant page
- **No filtering fails**: LLM sees 25-50 passages including 15-40 of noise from a relevant page

BM25 filtering fails gracefully. No filtering fails noisily.
