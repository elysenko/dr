# Stream 1: Multi-Agent Verification vs. Single-Agent Self-Consistency

**Research Sub-Question**: Does isolated multi-agent verification actually catch more errors than single-agent self-consistency in LLM systems?

**Date**: 2026-02-10
**Status**: Complete

---

## Executive Summary

The evidence presents a nuanced picture that challenges simplistic narratives in both directions. Multi-agent verification approaches DO outperform single-agent baselines in specific, well-documented conditions -- but the advantage is smaller, more conditional, and more fragile than commonly assumed. The most important finding across this literature is that **the bottleneck is verification quality, not verification quantity**. A single agent with strong prompts can match multi-agent debate in many settings, while poorly designed multi-agent systems can actually degrade performance. The practical implication: invest in verification design (what you check and how) before scaling the number of verifiers.

---

## 1. Multi-Agent Debate Literature

### 1.1 Du et al. 2023 — "Improving Factuality and Reasoning through Multiagent Debate"

**Method**: Multiple LLM instances propose and debate individual responses over multiple rounds, arriving at consensus.

**Key Results** (C1):
- +7.8 pts factual accuracy over single-agent baselines
- +14.8 pts arithmetic accuracy over single-agent baselines
- GSM8K math: 5-10% absolute improvement over zero-shot CoT
- Three agents debating over two rounds was the standard configuration
- Published at ICML 2024 (peer-reviewed)

**Source**: [Du et al. 2023 — arXiv:2305.14325](https://arxiv.org/abs/2305.14325); [ICML 2024 proceedings](https://dl.acm.org/doi/10.5555/3692070.3692537); [MIT News summary](https://news.mit.edu/2023/multi-ai-collaboration-helps-reasoning-factual-accuracy-language-models-0918)

**Independence check**: The MIT News article reports on the same underlying paper, so these are NOT independent sources. The peer review at ICML provides validation of the methodology.

### 1.2 Liang et al. 2023 — "Encouraging Divergent Thinking through Multi-Agent Debate"

**Key Contribution**: Identified the **"Degeneration-of-Thought" (DoT) problem** in self-reflection -- once an LLM has established confidence in its solutions, it cannot generate novel thoughts through reflection even if its initial stance is incorrect.

**Method**: Multi-Agent Debate (MAD) framework where agents argue "tit for tat" with a judge managing the process.

**Key Results** (C1):
- Effective on commonsense machine translation and counter-intuitive arithmetic reasoning
- Adaptive break of debate and modest "tit for tat" state are required for good performance
- Published at EMNLP 2024 (peer-reviewed)

**Source**: [Liang et al. 2023 — arXiv:2305.19118](https://arxiv.org/abs/2305.19118); [EMNLP 2024 proceedings](https://aclanthology.org/2024.emnlp-main.992/)

**Critical nuance**: The DoT finding directly explains WHY multi-agent approaches can help -- they break the confidence trap that single agents fall into.

### 1.3 Wang et al. 2024 — "Rethinking the Bounds of LLM Reasoning: Are Multi-Agent Discussions the Key?" (ACL 2024)

**THIS IS THE CRITICAL COUNTERPOINT** (C1):

**Key Finding**: A single-agent LLM with strong prompts can achieve almost the same best performance as the best existing multi-agent discussion approach.

**Specific Numbers**:

| Method | ECQA | GSM8K | FOLIO-wiki | Average |
|--------|------|-------|-----------|---------|
| Single Agent (with demos) | 67% | 83% | 76.09% | 75.63% |
| CMD 6 Agents (with demos) | 63% | 83% | 77.39% | 74.46% |
| Single Agent (no demos) | 63% | 69% | 70.22% | 67.41% |
| CMD 6 Agents (no demos) | 64% | 75% | 73.26% | 70.75% |

**When multi-agent wins**: Only when there are NO demonstrations in the prompt. With demonstrations, single-agent matches or beats 6-agent discussion.

**Source**: [Wang et al. 2024 — arXiv:2402.18272](https://arxiv.org/abs/2402.18272); [ACL 2024 proceedings](https://aclanthology.org/2024.acl-long.331/)

**Independence check**: This is an independent team (HKUST) with independent experiments on independent benchmarks. Genuinely independent from Du et al. and Liang et al.

### 1.4 ChatEval (Chan et al. 2023) — Multi-Agent Evaluation via Debate

**Key Results** (C2):
- Multi-agent evaluation achieves higher alignment with human preference than single-agent
- Accuracy improvement: +6.2% for ChatGPT, +2.5% for GPT-4 as evaluators
- **Critical detail**: Diverse role prompts (different personas) are essential; using the same role description degrades performance
- Published at ICLR 2024

**Source**: [Chan et al. 2023 — arXiv:2308.07201](https://arxiv.org/abs/2308.07201); [ICLR 2024 proceedings](https://openreview.net/forum?id=FQepisCUWu)

### 1.5 Khan et al. 2024 — "Debating with More Persuasive LLMs Leads to More Truthful Answers" (ICML 2024 Best Paper)

**Key Results** (C1):
- Debate: 76% (non-expert models) and 88% (humans) accuracy
- Naive baselines: 48% (models) and 60% (humans)
- Improvement: +28 percentage points for both
- Optimizing debaters for persuasiveness improves truth identification
- "It is often easier to argue for the truth" on closed tasks

**Source**: [Khan et al. 2024 — arXiv:2402.06782](https://arxiv.org/abs/2402.06782); ICML 2024 Best Paper Award

**Independence check**: Independent team (UCL/NYU/Anthropic/Oxford). Different experimental setup from Du et al. (focuses on scalable oversight, not direct reasoning improvement). Genuinely independent.

---

## 2. Self-Consistency Sampling (Wang et al. 2022)

### 2.1 Core Results

**Method**: Sample multiple diverse reasoning paths (with temperature), take majority vote on final answer.

**Key Accuracy Improvements** (C1):

| Benchmark | Improvement |
|-----------|-------------|
| GSM8K | +17.9% (56.5% -> 74.4% with PaLM-540B) |
| SVAMP | +11.0% |
| AQuA | +12.2% |
| StrategyQA | +6.4% |
| ARC-challenge | +3.9% |

**Source**: [Wang et al. 2022 — arXiv:2203.11171](https://arxiv.org/abs/2203.11171)

### 2.2 Number of Samples and Plateau Effect

**Key Finding** (C1): Performance gains taper off after moderate sampling. The plateau occurs around 10-15 reasoning paths for modern models, though Wang et al. originally used 40 paths.

**Specific data from Loo 2025**:
- Math-500 (Gemini-2.5-Pro): 1 agent 98% -> 3 agents 99.2% -> 15 agents 99.6% (only +1.6% total)
- HotpotQA (Gemini-2.5-Flash-Lite): Difference between baseline and 20 agents roughly 0.4%
- Performance improvements plateau around 10-15 agents with diminishing returns thereafter

**Source**: [Loo 2025 — arXiv:2511.00751](https://arxiv.org/abs/2511.00751)

**Practical guidance** (C2): 5-10 samples with temperature ~0.7 captures most benefit. Advanced methods (CISC) can match 30-sample self-consistency with only 8 samples using confidence weighting.

**Source**: [Confidence Improves Self-Consistency — arXiv:2502.06233](https://arxiv.org/html/2502.06233v1)

---

## 3. LLM-as-Judge Reliability

### 3.1 Overall Reliability Assessment

**Key Finding** (C1): LLM judges exhibit "questionable reliability" (McDonald's omega < 0.7) on complex evaluation tasks.

**Specific reliability scores** (McDonald's omega):

| Model | BBH | SQuAD | MT-Bench |
|-------|-----|-------|----------|
| Starling-LM-7B | 0.677-0.713 | 0.598-0.639 | 0.462-0.618 |
| Llama-3-8B-Instruct | 0.661-0.712 | 0.533-0.655 | 0.421-0.602 |
| Gemma-1.1-7b-it | 0.723-0.803 | 0.640-0.770 | 0.585-0.732 |

**Critical exception**: On simpler binary tasks with clear ground truth, reliability jumps to 0.989-0.990.

**Source**: [Can You Trust LLM Judgments? — arXiv:2412.12509](https://arxiv.org/abs/2412.12509); [HTML version](https://arxiv.org/html/2412.12509v2)

### 3.2 Documented Biases

**Position Bias** (C1): LLMs select "Response B" 60-69% of the time. Swapping presentation order shifts accuracy by >10%. Robustness rates drop below 0.5 when evaluating 3-4 options.

**Verbosity Bias** (C1): Models prefer longer, more formal outputs regardless of substantive quality.

**Self-Enhancement Bias** (C1): Error rates for self-preference range from 1.16% (GPT-4-Turbo) to 16.1% (Qwen2). GPT-4 exhibits significant self-preference even under anonymization.

**Authority Bias** (C2): Quote and book-format citations proved more influential than URL references. Models susceptible to fake citations.

**Sentiment Bias** (C2): Fear-based emotional expressions had the most significant impact on model judgments. Lower accuracy when superior answers contain negative emotional language.

**Source**: [Justice or Prejudice? Quantifying Biases in LLM-as-a-Judge](https://arxiv.org/html/2410.02736v1); [CIP Blog on LLM Judge Unreliability](https://www.cip.org/blog/llm-judges-are-unreliable)

### 3.3 Domain-Specific Expert Agreement

**Key Finding** (C1): In expert domains (dietetics, mental health), agreement rates between LLM judges and human subject matter experts range from 60-68%. LLMs miss subtle clinical "red flags."

**Source**: [Survey on LLM-as-a-Judge — arXiv:2411.15594](https://arxiv.org/abs/2411.15594)

---

## 4. Can LLMs Detect Their Own Hallucinations?

### 4.1 Self-Correction: The Fundamental Limitation

**Huang et al. 2023** (C1): LLMs cannot self-correct reasoning without external feedback.

**Specific degradation evidence**:

| Benchmark | Standard | After Self-Correct R1 | After Self-Correct R2 |
|-----------|----------|----------------------|----------------------|
| GSM8K (GPT-3.5) | 75.9% | 75.1% (-0.8) | 74.7% (-1.2) |
| CommonSenseQA | 75.8% | 38.1% (-37.7) | 41.8% (-34.0) |
| HotpotQA | 26.0% | 25.0% (-1.0) | 25.0% (-1.0) |

**Critical detail**: When changes occur, "the model is more likely to modify a correct answer to an incorrect one than to revise an incorrect answer to a correct one."

**Source**: [Huang et al. 2023 — arXiv:2310.01798](https://arxiv.org/abs/2310.01798); [ICLR 2024 proceedings](https://openreview.net/forum?id=IkmD3fKBPQ)

### 4.2 Kamoi et al. 2024 — Critical Survey of Self-Correction

**Key Findings** (C1):
- No prior work demonstrates successful self-correction with feedback from prompted LLMs (except in tasks exceptionally suited for self-correction)
- Self-correction works well in tasks that can use reliable external feedback (code interpreters, search engines, symbolic reasoners)
- Large-scale fine-tuning enables self-correction
- **The bottleneck is in feedback generation** -- LLMs struggle to generate accurate feedback without external validation
- Many prior studies used "unfair settings" with oracle information, artificially inflating success rates

**Source**: [Kamoi et al. 2024 — TACL](https://aclanthology.org/2024.tacl-1.78/); [arXiv:2406.01297](https://arxiv.org/abs/2406.01297)

### 4.3 FActScore: What LLMs Actually Get Wrong

**Min et al. 2023** — FActScore benchmark for biography factuality (C1):

| Model | % Atomic Facts Supported |
|-------|--------------------------|
| Human-written | ~88% |
| PerplexityAI (retrieval-augmented) | 71.5% |
| GPT-4 (estimated) | ~65% |
| ChatGPT | 58.3% |
| InstructGPT | 42.5% |
| Vicuna 13B | ~40% |
| Alpaca variants | 25-35% |

**Human inter-annotator agreement**: 88-96% depending on model being evaluated.
**Automated estimator error**: <2% (best configs), demonstrating that LLM-based factuality checking CAN work well when combined with retrieval.

**Source**: [Min et al. 2023 — arXiv:2305.14251](https://arxiv.org/abs/2305.14251); [EMNLP 2023](https://aclanthology.org/2023.emnlp-main.741/)

### 4.4 SAFE: Search-Augmented Factuality Evaluator

**Google DeepMind 2024** (C1):
- SAFE agrees with crowdsourced human annotators 72% of the time
- On 100 disagreement cases, SAFE wins 76% of the time (humans were wrong more often)
- Cost: $0.19 per response (SAFE + GPT-3.5-Turbo + Serper API) vs $4.00 per response (human annotators)
- 20x cheaper than human annotation
- Larger models achieve better long-form factuality across Gemini, GPT, Claude, PaLM-2 families

**Source**: [Wei et al. 2024 — arXiv:2403.18802](https://arxiv.org/abs/2403.18802); [NeurIPS 2024](https://neurips.cc/virtual/2024/poster/96675)

**Key insight**: SAFE works precisely BECAUSE it uses external search, not self-evaluation. This aligns perfectly with Kamoi et al.'s finding that external feedback is the key bottleneck.

### 4.5 Hallucination Rates in Practice

**Current model hallucination rates** (C2):
- GPT-4 Turbo: ~3% hallucination rate in document summarization
- GPT-4o: ~1.5% hallucination rate
- GPT-3.5: ~39.6% hallucinated references in medical domain
- Bard: ~91.4% hallucinated references in medical domain

**Source**: [Chelli et al. 2024 cited via hallucination detection surveys](https://github.com/EdinburghNLP/awesome-hallucination-detection); [All About AI hallucination benchmark](https://www.allaboutai.com/resources/llm-hallucination/)

**Independence note**: The 3% GPT-4 figure comes from the Vectara hallucination leaderboard (document summarization task), while the 39.6% figure comes from Chelli et al. (medical reference generation). These measure different things and are not directly comparable.

---

## 5. Does the NUMBER of Verification Paths Matter?

### 5.1 Multi-Agent Verification Scaling (MAV)

**Key Results** (C1):

Performance at 256 candidate samples:
- Base accuracy: 52.7%
- Self-consistency plateau: ~61%
- Reward model plateau: ~61%
- BoN-MAV ceiling: 69.0%

**Scaling by verifier count**: Gains of up to 10% for large LLMs and up to 20% for small ones when expanding verifier quantity.

**Weak-to-strong generalization**:
- Gemini-1.5-Pro on MATH: 64.7% -> 72.7% (+8.0 pts using weaker verifiers)
- GPT-4o on MATH: 68.3% -> 76.3% (+8.0 pts using weaker verifiers)

**Critical caveat**: "Performance gains persist... however, the magnitude and pattern of improvement varies and, in some cases, accuracy initially decreases before improving with additional verifiers."

**Source**: [Multi-Agent Verification — arXiv:2502.20379](https://arxiv.org/abs/2502.20379)

### 5.2 The 3-Agent Sweet Spot

**Society of Minds / Du et al. evidence** (C1):
- Arithmetic accuracy: ~70% (1 agent) -> ~95% (3 agents, 2 rounds)
- Diminishing returns after 3 agents and 2 rounds

**Source**: [Du et al. 2023](https://composable-models.github.io/llm_debate/); [Truth Ensembles survey](https://gist.github.com/bigsnarfdude/21cbae2ef56c01e0f53c223b0e2ca0b1)

### 5.3 Production Evidence

**Iterative Consensus Ensemble** (C2):
- General accuracy gain: 7-15 points over best single model
- Medical subset: 72% -> 81% (+9 pts)
- GPQA-diamond: 46.9% -> 68.2% (+45% relative improvement)
- Consensus typically reached in 2-3 rounds

**OpenAI Safety Reasoner** (C2):
- Production accuracy: 52.2% on internal multi-policy benchmark
- Compute overhead: Up to 16% of total inference compute
- F1 scores: 82.9 (Moderation Dataset), 79.3-79.9 (ToxicChat)

**Source**: [Truth Ensembles survey](https://gist.github.com/bigsnarfdude/21cbae2ef56c01e0f53c223b0e2ca0b1)

### 5.4 Adversarial Vulnerabilities at Scale

**ColMAD (October 2024)** (C1):
- Error detection improvement from multi-agent: +4% vs single-agent
- But competitive debate showed **-15% performance decrease** ("debate hacking" problem)
- System accuracy drops up to 40% under adversarial attack
- Individual model accuracy decreases up to 30% when adversarial agents are present
- If a small subset of agents is compromised via prompt injection, majority voting can lead to complete system failure

**Source**: [MultiAgent Collaboration Attack — EMNLP 2024 Findings](https://aclanthology.org/2024.findings-emnlp.407/)

---

## 6. Binary vs. Scalar LLM Self-Evaluation

### 6.1 Core Finding

**Binary evaluations are more reliable than scalar ratings** (C1).

LLMs can be reliable judges for binary factual correctness, but as scoring scales become more detailed, LLMs produce more arbitrary scores, making judgments less reliable and more prone to randomness.

**Specific evidence**:
- Binary tasks with clear ground truth: reliability 0.989-0.990
- Complex MT-Bench tasks with scalar scoring: reliability 0.421-0.732
- Scale format dramatically affects results: same content scored 1.68 on a 1-5 numerical scale vs. 3.17 on an A-E categorical scale

**Source**: [Can You Trust LLM Judgments? — arXiv:2412.12509](https://arxiv.org/html/2412.12509v2); [Databricks RAG evaluation best practices](https://www.databricks.com/blog/LLM-auto-eval-best-practices-RAG)

### 6.2 Practical Recommendations

**Recommended scale**: Integer 0-3 or 0-4 (Likert-style) as compromise between binary simplicity and multi-level discrimination.

**Lower-precision scores** (0, 1, 2, 3) largely retain precision compared to 0-10.0 or 0-100.0 scales, while making rubric design significantly easier.

**Source**: [Databricks RAG evaluation](https://www.databricks.com/blog/LLM-auto-eval-best-practices-RAG); [Confident AI LLM-as-Judge guide](https://www.confident-ai.com/blog/why-llm-as-a-judge-is-the-best-llm-evaluation-method); [Evidently AI guide](https://www.evidentlyai.com/llm-guide/llm-as-a-judge)

---

## 7. Synthesis: What Actually Works

### 7.1 The Hierarchy of Verification Effectiveness

Based on the full evidence base, ranked by effectiveness:

1. **External tool-augmented verification** (search + code execution + symbolic reasoning): Most effective. SAFE achieves superhuman factuality evaluation. Kamoi et al. confirm external feedback is the key enabler.

2. **Multi-agent debate with diverse roles** (3 agents, 2-3 rounds): Genuine improvement when agents have different prompts/roles. ChatEval shows +2.5-6.2% over single-agent evaluation. Du et al. show +7.8-14.8 pts on factuality/reasoning. BUT Wang et al. 2024 shows this advantage mostly disappears with strong single-agent prompting.

3. **Self-consistency sampling** (5-10 paths, majority vote): Robust +6-18% improvement depending on task. Diminishing returns after ~10-15 paths. Best for tasks with clear correct answers.

4. **Single-agent with strong prompts**: Surprisingly competitive. Wang et al. 2024 (ACL) shows it matches 6-agent discussion when demonstrations are provided.

5. **Intrinsic self-correction** (ask the model to check itself): **DOES NOT WORK** for reasoning. Actively degrades performance (Huang et al. 2023). CommonSenseQA accuracy dropped from 75.8% to 38.1% after self-correction.

### 7.2 When Multi-Agent Beats Single-Agent

Multi-agent approaches genuinely outperform when:
- **No demonstrations/examples are provided** (Wang et al. 2024)
- **The task requires breaking out of a confidence trap** (Liang et al. 2023 DoT problem)
- **Diverse perspectives are needed** (ChatEval diverse roles requirement)
- **The judge is weaker than the debaters** (Khan et al. 2024 scalable oversight)
- **Verification involves binary True/False judgments** (MAV aspect verifiers)

Multi-agent approaches do NOT clearly outperform when:
- Strong prompts with demonstrations are available
- The task has a single clear correct answer that can be reached through sampling
- All agents use the same role/persona (ChatEval finding)
- The system is vulnerable to adversarial agents (ColMAD -15% finding)

### 7.3 Practical Recommendations for Pipeline Design

| Verification Goal | Best Approach | Expected Improvement | Compute Cost |
|---|---|---|---|
| Factual accuracy | External search + verification (SAFE-like) | Superhuman on factual claims | Moderate (API calls) |
| Reasoning correctness | Self-consistency, 5-10 paths | +6-18% absolute | Low-moderate |
| Quality evaluation | Binary judge with clear rubric | 0.989 reliability | Low |
| Error detection | 3 diverse agents, 2 rounds | +4-8% over single agent | 3-6x compute |
| Scalar quality rating | Avoid or use 0-3 scale max | Moderate reliability | Low |
| Self-correction | **Do not use** without external feedback | Negative (degrades performance) | Wasted |

### 7.4 The Cost-Effectiveness Question

- OpenAI Safety Reasoner: up to 16% of total inference compute for verification
- SAFE: 20x cheaper than human annotation ($0.19 vs $4.00 per response)
- Self-consistency with 40 paths: ~40x compute for +17.9% accuracy
- 3-agent debate: ~3-6x compute for +5-15% improvement
- Sweet spot: 3 agents, 2 rounds, binary verification, diverse roles

---

## 8. Confidence Assessment

| Claim | Confidence | Basis |
|-------|-----------|-------|
| Self-consistency improves accuracy by 6-18% | HIGH | Wang et al. 2022, peer-reviewed, widely replicated |
| Intrinsic self-correction degrades reasoning performance | HIGH | Huang et al. 2023 + Kamoi et al. 2024, two independent surveys |
| Multi-agent debate helps more without demonstrations | HIGH | Wang et al. 2024, ACL peer-reviewed, clear methodology |
| Binary LLM judgment more reliable than scalar | HIGH | Multiple sources, consistent finding |
| 3 agents is the sweet spot for debate | MEDIUM | Du et al. + MAV paper, but task-dependent |
| Multi-agent verification scales better than self-consistency at high N | MEDIUM | MAV paper (Feb 2025), not yet widely replicated |
| LLM judges have position/verbosity/self-preference bias | HIGH | Multiple independent studies, consistent results |
| External feedback is the key enabler for self-correction | HIGH | Kamoi et al. 2024 comprehensive survey, consistent with SAFE results |

---

## 9. Gaps and Limitations

1. **Direct apples-to-apples comparison is rare**: Most papers compare their method to baselines rather than to each other. Wang et al. 2024 is the exception and it shows the gap is smaller than assumed.

2. **Model generation effects**: Most evidence is from GPT-3.5/GPT-4 era. Modern reasoning models (o1, DeepSeek-R1) may change the calculus significantly.

3. **Task dependency**: Results vary dramatically by task type. Math reasoning shows different patterns than factual verification or open-ended evaluation.

4. **Adversarial robustness is under-studied**: The ColMAD finding (-15% from competitive debate hacking) suggests multi-agent systems have unexplored failure modes.

5. **Cost-controlled comparisons are missing**: Few papers compare methods at equal compute budget. Self-consistency with 10 paths might beat 3-agent debate at the same compute cost, or vice versa.

---

## 10. Source Catalog

| # | Source | Type | Quality | Key Finding |
|---|--------|------|---------|-------------|
| 1 | [Du et al. 2023](https://arxiv.org/abs/2305.14325) | ICML 2024 paper | A | Multi-agent debate +7.8-14.8 pts |
| 2 | [Liang et al. 2023](https://arxiv.org/abs/2305.19118) | EMNLP 2024 paper | A | DoT problem; MAD framework |
| 3 | [Wang et al. 2024](https://arxiv.org/abs/2402.18272) | ACL 2024 paper | A | Single agent matches multi-agent with demos |
| 4 | [Chan et al. 2023 (ChatEval)](https://arxiv.org/abs/2308.07201) | ICLR 2024 paper | A | +2.5-6.2% with diverse multi-agent evaluation |
| 5 | [Khan et al. 2024](https://arxiv.org/abs/2402.06782) | ICML 2024 Best Paper | A | Debate +28 pts; truth easier to argue for |
| 6 | [Wang et al. 2022](https://arxiv.org/abs/2203.11171) | arXiv/ICLR | A | Self-consistency +6-18% across benchmarks |
| 7 | [Huang et al. 2023](https://arxiv.org/abs/2310.01798) | ICLR 2024 paper | A | Self-correction degrades reasoning |
| 8 | [Kamoi et al. 2024](https://arxiv.org/abs/2406.01297) | TACL 2024 paper | A | External feedback is the bottleneck |
| 9 | [Min et al. 2023 (FActScore)](https://arxiv.org/abs/2305.14251) | EMNLP 2023 paper | A | ChatGPT 58.3% atomic fact accuracy |
| 10 | [Wei et al. 2024 (SAFE)](https://arxiv.org/abs/2403.18802) | NeurIPS 2024 paper | A | Beats human annotators at 1/20 cost |
| 11 | [MAV 2025](https://arxiv.org/abs/2502.20379) | arXiv preprint | B | BoN-MAV outscales self-consistency |
| 12 | [LLM Judge Reliability](https://arxiv.org/abs/2412.12509) | arXiv preprint | B | omega < 0.7 on complex tasks |
| 13 | [Bias Quantification](https://arxiv.org/html/2410.02736v1) | arXiv preprint | B | Position, verbosity, self-enhancement bias |
| 14 | [CIP Blog](https://www.cip.org/blog/llm-judges-are-unreliable) | Blog/analysis | C | Practical bias demonstrations |
| 15 | [Loo 2025](https://arxiv.org/abs/2511.00751) | arXiv preprint | B | Self-consistency plateau at 10-15 samples |
| 16 | [ColMAD / Adversarial Attacks](https://aclanthology.org/2024.findings-emnlp.407/) | EMNLP 2024 Findings | A | -15% from debate hacking; -40% under adversarial attack |
| 17 | [Truth Ensembles Survey](https://gist.github.com/bigsnarfdude/21cbae2ef56c01e0f53c223b0e2ca0b1) | Aggregated survey (GitHub Gist) | C | Comprehensive production data compilation |
| 18 | [Databricks RAG Best Practices](https://www.databricks.com/blog/LLM-auto-eval-best-practices-RAG) | Industry blog | C | Binary/low-precision scales recommended |
