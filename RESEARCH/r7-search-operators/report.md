# R7: Search Operator Optimization — Implementation Report

## Executive Summary

R7 is the simplest remaining improvement in the pipeline: prompt-only changes to improve query precision using search operators. But the original R7 spec has a fundamental blind spot — **it was written assuming Google-style search operators, but the WebSearch tool is powered by Brave Search**, which supports a different (and experimental) operator set. More importantly, the WebSearch tool already provides `blocked_domains` and `allowed_domains` parameters that are more reliable than query-string operators for domain filtering.

**Bottom line**: R7 is worth implementing, but the implementation looks different from what the original spec proposed. The highest-value changes are: (1) using `blocked_domains` parameter for low-quality site exclusion, (2) quote operators for exact terminology discovered during refinement, and (3) `filetype:pdf` for academic/report-heavy topics. Date range operators and `-site:` exclusions should NOT go in the query string — they should use the tool's native parameters instead.

**Effort estimate**: 0.5 days is realistic for the prompt changes. The implementation is 4 specific edits to `agents/deep-research.md`.

**Impact estimate**: The original +2-5% is honest for what this is. I would not expect more than +3% in practice, and it is unmeasurable without A/B testing infrastructure.

---

## 1. What Search Operators Work with WebSearch?

### The Backend: Brave Search

Claude's WebSearch tool uses Brave Search as its backend ([TechCrunch, March 2025](https://techcrunch.com/2025/03/21/anthropic-appears-to-be-using-brave-to-power-web-searches-for-its-claude-chatbot/)). An independent test found 86.7% overlap between Claude's cited results and Brave's top non-sponsored results.

### The Tool Interface (Claude Code)

The WebSearch tool in Claude Code exposes:
- `query` (string, required) — the search query string
- `allowed_domains` (optional string array) — only include results from these domains
- `blocked_domains` (optional string array) — never include results from these domains

These are **tool-level parameters**, not query-string operators. They are implemented server-side by Anthropic and are reliable by design. This is critical: **the `blocked_domains` parameter is a more reliable mechanism for domain exclusion than `-site:` operators in the query string**.

### Brave Search Operator Support

Brave's official documentation lists these operators as **experimental** ([Brave Search Help](https://search.brave.com/help/operators)):

| Operator | Syntax | Status | Relevance to R7 |
|----------|--------|--------|-----------------|
| `site:` | `site:arxiv.org` | Experimental | LOW — use `allowed_domains` parameter instead |
| `-site:` | `-site:pinterest.com` | Experimental | LOW — use `blocked_domains` parameter instead |
| `filetype:` | `filetype:pdf` | Experimental | MEDIUM — useful for papers/reports |
| `ext:` | `ext:pdf` | Experimental | MEDIUM — alias for filetype |
| `intitle:` | `intitle:term` | Experimental | LOW — rarely useful for research |
| `"exact"` | `"exact phrase"` | Experimental | HIGH — useful for discovered terminology |
| `+term` | `+required` | Experimental | LOW — search engines usually do this |
| `-term` | `-excluded` | Experimental | MEDIUM — useful for disambiguation |
| `lang:` | `lang:en` | Experimental | LOW — niche use case |

**NOT supported by Brave (as of Feb 2026):**
- `before:` / `after:` date range operators — not documented
- `inurl:` — not listed in Brave's docs
- Google-specific operators (`cache:`, `related:`, `info:`, etc.)

### The Pass-Through Question

There is no public documentation confirming whether Anthropic's WebSearch layer passes Brave operators through to the Brave API unmodified, strips them, or treats them as literal search terms. The Brave API documentation says operators can be included in the `q` parameter. But Anthropic's layer sits between Claude Code and Brave, and could modify queries.

**Risk assessment**: If operators are not passed through, they degrade to literal search terms. A query like `filetype:pdf RAG retrieval` becomes a search for the literal string "filetype:pdf" plus "RAG retrieval". This would return irrelevant results about search operators rather than PDFs about RAG.

**Mitigation**: Only use operators in supplementary queries, not primary queries. If a `filetype:pdf` query returns results about search operators rather than actual PDFs, the agent can detect this and fall back to the non-operator query. This is already consistent with the pipeline's design — site-targeted queries are documented as supplements to broad search (line 158 of the agent prompt).

---

## 2. Current Query Generation Flow

### Phase 3 Query Generation Points (lines 152-273)

There are **5 distinct points** where queries are generated:

1. **Step 2 (line 198)**: Initial broad queries — "WebSearch: original query + HyDE variants (broad, no site restriction)"
2. **Step 5 (lines 226-232)**: Refinement queries — "Generate refined queries using learned vocabulary"
3. **Step 6 (line 233)**: Site-targeted supplementary queries — "add 1-2 site-targeted queries"
4. **Contract-Driven Queries (lines 260-265)**: Disconfirmation and surprise queries
5. **Query Failure Recovery (line 269)**: Broadened/rephrased fallback queries

### Where Operators Should NOT Go

- **Step 2 (initial broad queries)**: Adding operators here restricts recall on the first pass. The prompt already says "broad, no site restriction". This is correct — broad first, narrow later.
- **Step 4 (Query Failure Recovery)**: When queries already fail, adding operators makes them more restrictive, which is the opposite of what you want.

### Where Operators SHOULD Go

- **Step 5 (refinement queries)**: This is the natural injection point. By this stage, the agent has found initial results and knows what terminology matters. Quote operators for exact phrases discovered in A/B sources are high-value here.
- **Step 6 (site-targeted supplements)**: Already uses `site:` operator syntax. Can be extended with `filetype:pdf` for academic topics.
- **blocked_domains on ALL WebSearch calls**: This is a new capability that should be used from Step 2 onwards. Unlike query-string operators, this is a reliable server-side mechanism.

### Existing Domain Filtering

The prompt currently has:
- **Line 200**: "block SEO farms" — mentioned as an MMR filter criterion but with no specific domain list
- **Line 273**: "Anti-SEO check" — at the gate level, checking if sources trace to the same original
- **Source Quality grading (line 564)**: Grade E = "Anecdotal, speculative, SEO spam"
- **Domain-Aware Source Targeting (lines 160-166)**: `site:` operators for authoritative domains, used as supplements

**What's missing**: There is no concrete list of domains to block. "Block SEO farms" at line 200 is an instruction without specifics. The agent must use judgment every time, which is inconsistent.

---

## 3. Recommended Implementation

### Change 1: Add `blocked_domains` Parameter Guidance (NEW SECTION)

**Location**: After line 168 (after "Domain-Aware Source Targeting" section), add a new subsection.

**What to add**:

```markdown
### Low-Quality Domain Exclusion

Use the `blocked_domains` WebSearch parameter to exclude known low-quality domains from ALL searches.
This is more reliable than `-site:` query operators because it is enforced server-side.

Default blocked list (apply to every WebSearch call):
```
blocked_domains: [
  "pinterest.com",
  "pinterest.co.uk",
  "quora.com",
  "medium.com",
  "linkedin.com",
  "facebook.com",
  "instagram.com",
  "tiktok.com",
  "twitter.com",
  "x.com",
  "reddit.com"
]
```

**When to REMOVE domains from the block list**: If the research topic is specifically about
social media platforms or user-generated content, remove the relevant platform from blocked_domains.
If searching for a specific known article on Medium or LinkedIn, use allowed_domains instead.

**When to ADD domains**: If initial results surface low-quality aggregator sites
(e.g., sites that rewrite press releases or scrape Stack Overflow), add them to blocked_domains
for subsequent queries.
```

**Rationale**: The R7 spec says `-site:pinterest.com -site:quora.com` but putting these in the query string wastes query tokens and relies on experimental operator support. The `blocked_domains` parameter does the same thing reliably.

**Important caveat on the block list**: Medium and LinkedIn host legitimate expert content. Reddit hosts valuable technical discussions. Blocking them is a tradeoff — less noise but occasionally missed good content. The list above is aggressive. An alternative conservative list would only block `pinterest.com` and add domains dynamically based on observed spam.

### Change 2: Add Quote Operators to Refinement Step (MODIFY EXISTING)

**Location**: Line 229, modify the refinement query generation instruction.

**Current text** (line 229):
```
         - Generate refined queries using learned vocabulary
```

**Replace with**:
```
         - Generate refined queries using learned vocabulary
         - Use "exact phrases" in quotes for: specific named concepts, paper titles,
           technical terms discovered in A/B sources, and author names.
           Example: found "retrieval-augmented generation" → search `"retrieval-augmented generation" evaluation benchmark`
```

**Rationale**: Quote operators are the most universally supported search operator across all engines. Even if the backend changes from Brave to something else, quotes will still work. They are especially high-value during refinement because the agent has already identified specific terminology from initial results.

### Change 3: Add `filetype:pdf` to Site-Targeted Supplements (MODIFY EXISTING)

**Location**: Line 233, modify the site-targeted query instruction.

**Current text** (line 233):
```
      6. If results lack authoritative sources, add 1-2 site-targeted queries
```

**Replace with**:
```
      6. If results lack authoritative sources, add 1-2 site-targeted queries.
         For academic/technical topics, try `filetype:pdf` to find papers and reports:
         e.g., `filetype:pdf "retrieval augmented generation" benchmark 2025`
         Note: filetype operator is experimental in Brave Search. If results seem
         irrelevant (about search operators rather than PDFs), drop the operator.
```

**Rationale**: `filetype:pdf` is useful specifically for finding academic papers, government reports, and technical whitepapers that often exist only as PDFs. But it needs a fallback instruction because the operator is experimental and may not work reliably.

### Change 4: Add Domain-Specific Operator Guidance to HyDE Section (MINOR ADD)

**Location**: After line 175 (after HyDE Multi-Framing), add a brief note.

**What to add**:

```markdown
### Query Enhancement (Refinement Rounds Only)

In refinement rounds (not initial searches), enhance queries with:
- **Exact phrases**: `"discovered term"` for specific concepts found in initial results
- **Term exclusion**: `-ambiguous_term` to disambiguate when results mix unrelated topics
- **filetype**: `filetype:pdf` when seeking papers/reports (academic/policy topics only)

Do NOT use operators in initial broad searches — they reduce recall.
```

**Rationale**: This consolidates the operator guidance in one visible place near the query generation instructions, so the agent sees it at the right time.

---

## 4. What NOT to Implement

### Date Range Operators

The original R7 spec says "date range operators for recency-sensitive topics." Brave Search does NOT support `before:`/`after:` operators. The Brave API has a `freshness` parameter, but Anthropic's WebSearch tool does not expose it. There is no way to do date filtering through the current tool.

**Skip this entirely.** The agent already handles recency through the MMR scoring heuristic (line 201: "freshness (+2 <1yr)") which is applied post-search. This is adequate.

### `-site:` in Query Strings

Use `blocked_domains` parameter instead. More reliable, does not consume query tokens, and works regardless of operator support.

### `site:` in Query Strings for Authoritative Sources

The prompt already uses `site:` operators in the Domain-Aware Source Targeting table (lines 160-166). An alternative would be to use `allowed_domains` parameter instead, but this would be a more invasive change and the existing approach works well enough — the `site:` operator in Brave is one of the better-supported ones. Leave as-is.

### Aggressive Operator Stacking

Do NOT combine multiple operators in a single query (e.g., `site:arxiv.org filetype:pdf "transformer" lang:en`). Brave's operators are experimental and stacking increases the probability of unexpected behavior. One operator per query maximum.

---

## 5. Assessment of Original Estimates

### Effort: 0.5 Days — REALISTIC

The implementation is 4 prompt edits, none longer than 10 lines. The actual typing takes 30 minutes. The remaining time is testing to verify that operators work as expected and do not degrade results.

Recommended testing approach:
1. Run a Type C research with the modified prompt
2. Check the query log for operator usage
3. Verify that `blocked_domains` is being applied
4. Spot-check that `filetype:pdf` queries return actual PDFs
5. Confirm quote operators produce more specific results

### Impact: +2-5% — PROBABLY OPTIMISTIC

Honest assessment:

| Operator | Expected Impact | Confidence |
|----------|----------------|------------|
| `blocked_domains` for low-quality sites | +1-2% noise reduction | Medium — depends on how often Pinterest/Quora currently pollute results |
| Quote operators in refinement | +1-2% precision on specific lookups | Medium — depends on how well the agent already phrases queries |
| `filetype:pdf` | +0-1% for academic topics, 0% for others | Low — experimental operator, may not work |
| **Combined** | **+1-3% realistic** | Low-Medium |

The +2-5% range in the original spec is an upper bound. The lower end (+2%) is plausible. The upper end (+5%) would require all operators to work reliably AND for current results to be significantly polluted by low-quality domains — which is not established.

The honest answer is: **we do not know the actual impact and cannot measure it without A/B testing infrastructure**. This is consistent with the original spec's "GENERAL BEST PRACTICE" categorization and its admission of "Unknown, likely small."

---

## 6. Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Operators treated as literal text | Medium | Medium — wastes a search on irrelevant results | Only use operators in supplementary queries; instruct agent to detect irrelevant results and retry without operators |
| `blocked_domains` blocks legitimate content | Low-Medium | Medium — misses a useful source | Make block list configurable; instruct agent to remove domains when topic requires them |
| Prompt bloat from operator instructions | Low | Low — 15-20 lines added to a 584-line prompt | Operators guidance is 3-4% of total prompt; well within acceptable range |
| Brave changes operator support | Low | Low — fallback to non-operator queries | Operators are always supplementary, never primary |
| Operator syntax conflicts with future backend changes | Low | Medium — if Anthropic switches from Brave to another backend | Only use universally-supported operators (quotes, exclusion); use tool parameters over query-string operators |

---

## 7. Exact Diff for `agents/deep-research.md`

### Edit A: After line 168, insert new section (~20 lines)

Insert after: `Use only when initial broad results lack authoritative sources.`

```markdown
### Low-Quality Domain Exclusion

Use the `blocked_domains` WebSearch parameter on ALL searches to filter known noise sources.
This is enforced server-side and more reliable than `-site:` query operators.

Default exclusion list:
```
blocked_domains: ["pinterest.com", "quora.com"]
```

Extend dynamically: if initial results surface content-farm aggregators or irrelevant social media,
add those domains to blocked_domains for subsequent searches in that subquestion.

Remove selectively: if the research topic involves social media platforms, user-generated content,
or a specific article known to be on a blocked domain, remove the relevant entry.
```

**Note**: I reduced the block list to just Pinterest and Quora in the actual diff. The aggressive 11-domain list from Section 3 is an option but risks blocking legitimate content on Medium, LinkedIn, and Reddit. Start conservative; the agent can add domains dynamically.

### Edit B: Replace line 229

Replace:
```
         - Generate refined queries using learned vocabulary
```
With:
```
         - Generate refined queries using learned vocabulary
         - Use "exact phrases" in quotes for specific technical terms, paper titles,
           or named concepts discovered in A/B sources
```

### Edit C: Replace line 233

Replace:
```
      6. If results lack authoritative sources, add 1-2 site-targeted queries
```
With:
```
      6. If results lack authoritative sources, add 1-2 site-targeted queries.
         For academic topics, also try filetype:pdf to surface papers and reports.
         If filetype: returns irrelevant results, drop the operator and retry.
```

### Edit D: After line 175, insert query enhancement note (~5 lines)

Insert after: `3. **Skeptical**: "Critics argue that assumptions about [topic] overlook..."`

```markdown
### Query Operators (Refinement Rounds Only)

In refinement rounds — not initial broad searches — enhance queries with:
- `"exact phrase"` for discovered terminology from A/B sources
- `-term` to disambiguate when results mix unrelated topics
- `filetype:pdf` for papers/reports (academic and policy topics only)
```

---

## 8. What is Missing from the Current Implementation to Implement R7

**Nothing is structurally missing.** R7 is purely a prompt change. No new scripts, no new dependencies, no new tool integrations.

Specifically:
1. **WebSearch tool already supports `blocked_domains`** — just not used in the prompt
2. **Quote operators** — already work in any search backend; just need prompt guidance
3. **`filetype:pdf`** — supported by Brave (experimentally); needs prompt guidance
4. **The agent already has query refinement logic** — R7 adds operator-enhanced variants to existing refinement rounds

The only "missing" thing is the prompt text itself. The 4 edits above are the complete implementation.

### What Would Make R7 Higher Impact (But Is Out of Scope)

1. **Freshness parameter exposure**: If Anthropic exposed Brave's `freshness` API parameter in the WebSearch tool, date filtering would become reliable. Currently impossible.
2. **A/B testing infrastructure**: Without it, we cannot measure whether R7 actually improves results. The +2-5% estimate is a guess.
3. **Operator support validation**: A test harness that verifies which Brave operators actually pass through Anthropic's WebSearch layer. A one-time manual test with 5-10 operator queries would take 15 minutes and provide definitive answers.

---

## Sources

- [Anthropic Web Search Tool Documentation](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-search-tool)
- [Brave Search Operators Documentation](https://search.brave.com/help/operators)
- [Brave Search API Operators](https://api-dashboard.search.brave.com/documentation/resources/search-operators)
- [TechCrunch: Anthropic appears to be using Brave to power web search](https://techcrunch.com/2025/03/21/anthropic-appears-to-be-using-brave-to-power-web-searches-for-its-claude-chatbot/)
- [Inside Claude Code's Web Tools: WebFetch vs WebSearch](https://mikhail.io/2025/10/claude-code-web-tools/)
- [BruceClay: Advanced Search Operators for Bing and Google](https://www.bruceclay.com/blog/bing-google-advanced-search-operators/)
- [Brave Search API vs Bing API](https://brave.com/search/api/guides/brave-search-api-vs-bing-api/)
