# Finding 3: BM25 vs TF-IDF vs Other Lightweight Retrievers

## BM25 vs TF-IDF

BM25 is a direct improvement over TF-IDF with two critical additions [C1, S08, S12]:

### Theoretical Differences

| Feature | TF-IDF | BM25 Okapi |
|---------|--------|------------|
| Term frequency | Linear (unbounded) | Saturating (bounded by k1) |
| Document length | No normalization | Normalized via parameter b |
| IDF formula | log(N/df) | log((N-df+0.5)/(df+0.5)+1) |
| Tuning knobs | None | k1 (saturation), b (length norm) |
| Short doc handling | Biased against | Controllable via b |

### Practical Impact

The key difference for passage pre-filtering is **term frequency saturation**. In TF-IDF, a passage mentioning "BM25" 10 times scores 10x higher than one mentioning it once. In BM25, the 10th occurrence adds almost nothing — the score asymptotes. This is critical for web content where:
- Marketing pages repeat keywords excessively
- Boilerplate sections repeat navigation terms
- Technical content uses domain terms densely but not always relevantly

### BEIR Benchmark Numbers [C1, S08]

BM25 NDCG@10 on key BEIR datasets:

| Dataset | BM25 NDCG@10 | Notes |
|---------|-------------|-------|
| NQ (Natural Questions) | 0.310 | Low — semantic queries hurt BM25 |
| HotpotQA | 0.601 | Good — multi-hop but keyword-rich |
| FEVER (fact verification) | 0.648 | Strong — factual claims have keyword overlap |
| SciFact | 0.620 | Good — scientific terms are specific |
| BEIR average (18 datasets) | 0.434 | Competitive zero-shot baseline |

For context, dense retrievers (E5, SGPT) achieve 0.45-0.52 on BEIR average, but require embedding models [S08]. TF-IDF benchmarks on BEIR are not widely reported because BM25 is the universally accepted lexical baseline — it consistently outperforms raw TF-IDF.

### Verdict on TF-IDF

**Do not use TF-IDF.** BM25 Okapi is strictly better and equally simple to implement. The only argument for TF-IDF would be if you needed scikit-learn's `TfidfVectorizer` for its ecosystem integrations — irrelevant here since we are writing custom code.

## BM25 Variants

Three variants are worth considering [S02, S03]:

| Variant | Key Difference | Best For |
|---------|---------------|----------|
| **BM25 Okapi** | Standard — term saturation + length norm | General purpose, well-studied defaults |
| **BM25+** | Guarantees positive contribution for matched terms | Short passages where term matches must always count |
| **BM25L** | Better handling of long documents via delta parameter | Long documents — not our case |

For passage pre-filtering of ~200-word chunks, **BM25+ has a slight theoretical advantage** because it ensures that every matched query term contributes positively to the score, even in very short passages. However, the practical difference from BM25 Okapi on chunks of similar length is minimal.

**Recommendation**: Start with BM25 Okapi (k1=1.2, b=0.75). If testing reveals that some clearly relevant short passages score 0 or near-0, switch to BM25+ by adding a delta (0.5-1.0) to the score formula.

## Other Lightweight Retrievers

### SPLADE / Learned Sparse Retrieval
SPLADE uses a pre-trained language model (BERT) to learn term weights and expansion terms. It significantly outperforms BM25 on BEIR (0.50+ average NDCG@10) [S16]. However, it requires:
- A pre-trained model (~100MB+)
- Inference time per query
- PyTorch or similar dependency

**Verdict**: Not viable for zero-dependency CLI. Dramatically overkill for single-page pre-filtering.

### TF-IDF with Subword Tokenization
Extending BM25/TF-IDF with subword tokens (byte-pair encoding) can partially bridge vocabulary mismatch [referenced in search results]. However, this requires a pre-trained tokenizer vocabulary, adding complexity without clear benefit for our use case.

**Verdict**: Interesting for v2 but not for initial implementation.

## Conclusion

For zero-dependency single-page pre-filtering, **BM25 Okapi is the clear winner**. It outperforms TF-IDF, requires no trained models, and has well-established default parameters. The alternatives (SPLADE, dense retrieval, learned sparse) solve problems that do not exist at our scale.
