# Stream 5: LLM Self-Evaluation, Source Independence, and Verification Reliability

## Research Sub-Question
Can LLMs reliably assess source independence? Does source diversity actually improve research quality? What does the evidence say about LLM self-evaluation reliability for factual claims?

---

## 1. LLM Source Independence Assessment

### Can LLMs Determine Source Independence?

**Finding: No direct evidence exists that LLMs can reliably assess source independence.** [Source needed for direct studies]

The concept of "source independence" in the context of LLM-based research pipelines is an under-studied problem. Current research on automated provenance tracking focuses on data lineage in enterprise systems (tracking data transformations through pipelines), not on the epistemic question of whether two news articles or research papers derive from the same underlying investigation.

**What would be required:**
- Detecting shared funding sources, shared datasets, or citation chains
- Identifying when multiple articles paraphrase the same press release or wire report
- Tracing claims back to their originating study or dataset

**Current automated capabilities are limited to:**
- Data provenance tracking in enterprise contexts uses metadata, blockchain, and lineage tools to track data transformations, but these track *data flows*, not *epistemic independence* of conclusions [IBM, "What is Data Provenance?"]
- Citation network analysis can identify shared references, but shared citations do not necessarily mean shared conclusions

**Practical implication for LLM pipelines:** An LLM asked "are these two sources independent?" is performing a reasoning task that requires understanding provenance chains, funding structures, and methodological relationships. This falls squarely in the category of tasks where LLMs are known to hallucinate with high confidence. There is no evidence that LLMs can do this reliably without access to structured metadata about source provenance. The independence check in verification pipelines is likely to be **largely theatrical** unless supplemented with structured provenance data.

### C1 Claim: LLMs cannot reliably assess source independence without structured provenance metadata.
- **Evidence strength:** Indirect but strong. No studies demonstrate this capability; the theoretical limitations of LLM reasoning (Huang et al. 2023, Kamoi et al. 2024) apply directly.
- **Independence check:** Multiple independent research groups confirm LLM reasoning limitations.
- **Confidence:** HIGH (75-85%)

---

## 2. Source Diversity and Research Quality

### Does Diverse Source Triangulation Improve Research Quality?

**Finding: YES -- strong evidence from information science and research methodology that source diversity improves research quality, but with important caveats.**

**Evidence from research methodology literature:**

- **Triangulation** (using multiple data sources, methods, investigators, or theories) is a well-established methodological principle. "Synthesis and triangulation among multiple sources of information and multiple types of methods can strengthen the quality and credibility of the evidentiary support for findings and recommendations" [NCBI Bookshelf, "Analysis Through Triangulation and Synthesis"]
- Four types of triangulation are recognized: (a) method triangulation, (b) investigator triangulation, (c) theory triangulation, and (d) data source triangulation [Pubmed, "The use of triangulation in qualitative research"]
- "If data from multiple sources or investigators line up, you can be more certain of their credibility" [FCS6014, University of Florida EDIS]

**Evidence from team diversity research:**
- "Teams that include different kinds of thinkers outperform homogeneous groups on complex tasks, including improved problem solving, increased innovation, and more-accurate predictions" [ScienceDirect, "Diversity improves performance and outcomes"]

**Caveats and limitations:**
- Triangulation is most valuable for complex, judgment-dependent research (Type C/D in the GoT framework). For simple factual lookups (Type A), source diversity adds cost without proportional benefit.
- Source diversity does NOT automatically mean *independent* sources. Five different news outlets reprinting the same Reuters wire story are diverse in name but not in substance.
- The benefit is in *complementary perspectives*, not in mere numerical redundancy.

### C1 Claim: Source triangulation improves research quality for complex, judgment-dependent questions.
- **Source 1:** Established research methodology literature on triangulation (multiple independent textbooks and methodological guides)
- **Source 2:** Team cognition research showing diverse perspectives improve accuracy (ScienceDirect)
- **Independence check:** PASS -- research methodology literature and cognitive science literature are independent research traditions
- **Confidence:** HIGH (85-95%)

### C2 Claim: Source diversity without independence verification may create false confidence.
- **Evidence:** The distinction between diverse *labels* and diverse *origins* is well-documented in information science.

---

## 3. LLM Self-Evaluation Reliability

### 3.1 The Foundational Finding: Huang et al. 2023

**"Large Language Models Cannot Self-Correct Reasoning Yet"** (Huang et al., 2023, arXiv:2310.01798, Google DeepMind / UIUC)

**Core finding:** LLMs struggle to self-correct their responses without external feedback, and performance often *degrades* after self-correction attempts. The concept of "intrinsic self-correction" (correcting based solely on inherent capabilities) was shown to be unreliable for reasoning tasks.

**Key mechanism:** LLMs have trouble reliably evaluating the correctness of their own responses. They rarely identify flaws in their initial reasoning when given no external signal.

### 3.2 Has This Changed with Newer Models? The Kamoi et al. 2024 Critical Survey

**"When Can LLMs Actually Correct Their Own Mistakes?"** (Kamoi et al., 2024, TACL vol. 12, pp. 1417-1440)

This comprehensive survey extends and largely **confirms** the Huang et al. findings:

**Taxonomy of self-correction:**
- **Intrinsic self-correction** (no external feedback): "No prior work demonstrates successful self-correction with feedback from prompted LLMs, except for studies in tasks that are exceptionally suited for self-correction" [Kamoi et al. 2024, TACL]
- **External-feedback self-correction** (tools, search, knowledge bases): Effective when reliable external feedback exists
- **Fine-tuned self-correction** (100K+ training instances): Can work but requires massive training data

**Critical bottleneck:** "The bottleneck is in the feedback generation." LLMs struggle to generate accurate feedback about their own mistakes without external assistance. [Kamoi et al. 2024]

**Methodological critique:** Many prior positive results used unrealistic oracle information or unfairly weak initial prompts, overstating self-correction capabilities.

### 3.3 The 2025 Benchmark: Can LLMs Correct Themselves?

**"Can LLMs Correct Themselves? A Benchmark of Self-Correction in LLMs"** (2025, arXiv:2510.16062)

This benchmark tested LLaMA 3.1, Qwen 2.5, GPT-3.5, GPT-4o, Claude 3.5-Sonnet, DeepSeek-V3, and QWQ-32B across three correction paradigms:

| Paradigm | Method Examples | Key Result |
|----------|----------------|------------|
| S1: Intrinsic | RCI, Self-Refine, CoVe, Reflexion | Moderate gains on complex tasks, minimal on simple ones |
| S2: External | RARR, RATT, CRITIC | Greater stability through authoritative external resources |
| S3: Fine-tuned | DCoT, SCORE, SuperCorrect | Domain-specific improvements |

**Notable results:**
- GPQA improved by **+23.24%** with CoVe (a verification method)
- MATH improved by **+7.66%** with RARR (external retrieval)
- External methods generally outperformed intrinsic approaches
- Reasoning-focused LLMs (DeepSeek-V3) showed "only marginal gains" because they already embed sophisticated error-detection processes
- **Mixing methods increased computational overhead without proportional accuracy improvements**

### C1 Claim: LLMs cannot reliably self-correct reasoning without external feedback.
- **Source 1:** Huang et al. 2023 (Google DeepMind / UIUC) -- arXiv:2310.01798
- **Source 2:** Kamoi et al. 2024 (Penn State / UIUC) -- TACL vol. 12
- **Source 3:** 2025 self-correction benchmark -- arXiv:2510.16062
- **Independence check:** PASS -- Three independent research groups (DeepMind, Penn State, separate 2025 team) with independent experimental setups all converge on the same conclusion.
- **Confidence:** VERY HIGH (90-95%)

### 3.4 Does External Feedback Change the Picture?

**Finding: YES -- external feedback significantly improves self-correction, but does not eliminate errors.**

**Key evidence:**

**CRITIC Framework (ICLR 2024):** Interacts with appropriate tools (calculators, search, code executors) to evaluate text, then revises based on tool feedback. Showed improvements in free-form QA, mathematical program synthesis, and toxicity reduction.

**Self-RAG (ICLR 2024, Oral -- top 1%):** Trained a model to adaptively retrieve passages on-demand and generate reflection tokens. Results: 81% accuracy on fact checking, 80% factuality on biography generation vs. 71% for ChatGPT. [Asai et al. 2024]

**RARR (ACL 2023):** Automatically finds attribution for LLM outputs and post-edits unsupported content. Improved factual attribution while preserving over 90% of original content's intent. [Gao et al. 2023]

**Chain-of-Verification (CoVe) (ACL Findings 2024):** Model drafts response, plans verification questions, answers them independently, then generates verified response. Improved F1 score by 23% (from 0.39 to 0.48). [Dhuliawala et al. 2024]

**Multi-Agent Debate (ICML 2024):** Multiple LLM instances propose and debate responses over multiple rounds. "Improves the factual validity of generated content, reducing fallacious answers and hallucinations." Performance improves with more agents and more debate rounds. [Du et al. 2023/2024]

**Agentic Reasoning (2025):** Combining tools yielded synergistic effects -- "web search combined with coding provided greater improvements than individual gains." Best performance with all three: web search, Mind-Map, and coding.

### C1 Claim: External feedback (RAG, tool use, web search) materially improves LLM self-correction, but does not eliminate errors.
- **Source 1:** Self-RAG (ICLR 2024) -- 81% accuracy on fact checking
- **Source 2:** CoVe (ACL Findings 2024) -- 23% F1 improvement
- **Source 3:** CRITIC (ICLR 2024) -- improvements across multiple task types
- **Independence check:** PASS -- Independent research groups with different methods all show improvement with external feedback.
- **Confidence:** VERY HIGH (90-95%)

---

## 4. Verification Theater: When Does Verification Actually Work?

### The Theoretical Case for Inevitability of Errors

**"LLMs Will Always Hallucinate, and We Need to Live With This"** (Banerjee et al., 2024, arXiv:2409.05746)

This paper uses computational theory (Turing computability, Gödel's Incompleteness Theorem, the Halting Problem) to argue that hallucination is a **structural, not accidental** property of LLMs:

Five core arguments:
1. No training dataset can contain all true facts
2. Accurate retrieval is mathematically undecidable
3. Understanding user intent is undecidable
4. The halting problem prevents predictable generation
5. **"No amount of fact-checking can remove hallucination with 100% accuracy"** because fact-checkers themselves face the same undecidable problems

**"Hallucination is Inevitable: An Innate Limitation of Large Language Models"** (Xu et al., 2024, arXiv:2401.11817) formalizes this further, showing LLMs "cannot learn all computable functions and will therefore inevitably hallucinate."

### When Verification Works vs. When It's Theater

**Verification WORKS when:**
1. **External ground truth is available:** Code execution, calculator verification, database lookups -- these provide objective feedback the model cannot self-generate [CRITIC, Self-RAG]
2. **The verification task is decomposable:** Breaking claims into atomic facts and checking each against a knowledge source works reasonably well. FActScore achieved less than 2% error rate for automated factuality evaluation against Wikipedia. [Min et al., EMNLP 2023]
3. **Multiple independent models debate:** Multi-agent debate reduces hallucinations by creating adversarial pressure [Du et al., ICML 2024]
4. **Pairwise comparison rather than absolute scoring:** LLM judges show better alignment with humans on pairwise comparisons than absolute scores [Survey on LLM-as-a-Judge, 2024]

**Verification is THEATER when:**
1. **The same model (or same-family model) verifies its own output:** Self-preference bias means models rate their own outputs higher. GPT-4 showed a 0.520 bias score (52-percentage-point difference in rating own outputs) [Self-Preference Bias, 2024]. The root cause is perplexity: LLMs favor text with lower perplexity (more familiar), and their own outputs inherently have lower perplexity.
2. **Intrinsic self-correction without external tools:** The model is essentially asked "is your answer right?" and it says "yes" -- or worse, "corrects" a right answer to a wrong one. [Huang et al. 2023, Kamoi et al. 2024]
3. **Elaborate multi-step verification using only the model's internal knowledge:** Adding more steps of self-reflection does not compensate for the lack of external ground truth. "Mixing methods increased computational overhead without proportional accuracy improvements." [2025 Benchmark]
4. **Confidence-based filtering without calibration:** Models are systematically overconfident (see Section 6), so filtering by stated confidence is unreliable.
5. **Expert domain verification:** In specialized domains like dietetics and mental health, "agreement rates between LLM judges and human subject matter experts range from 60-68%" [Collective Intelligence Project, 2024]

### C1 Claim: LLM verification of own outputs without external ground truth is substantially theatrical.
- **Source 1:** Huang et al. 2023 -- intrinsic self-correction fails
- **Source 2:** Kamoi et al. 2024 -- survey confirms bottleneck is feedback generation
- **Source 3:** Panickssery et al. NeurIPS 2024 -- causal link between self-recognition and self-preference bias
- **Independence check:** PASS -- Three independent research programs converge.
- **Confidence:** HIGH (80-90%)

### C1 Claim: Verification with external tools (search, execution, knowledge bases) provides genuine quality improvement.
- **Source 1:** Self-RAG (ICLR 2024) -- 81% fact-checking accuracy
- **Source 2:** CoVe (ACL Findings 2024) -- 23% F1 improvement
- **Source 3:** FActScore (EMNLP 2023) -- <2% error automated factuality scoring
- **Independence check:** PASS
- **Confidence:** VERY HIGH (90-95%)

---

## 5. Binary vs. Scalar Assessment Reliability

### Finding: Pairwise/comparative assessment outperforms absolute scoring; binary may outperform fine-grained scales.

**Evidence from LLM-as-a-Judge research:**

"LLM and human evaluations are more aligned in the context of pairwise comparisons compared to score-based assessments." Pairwise comparative assessments demonstrate "superior positional consistency and better alignment with human judgment than direct scoring methods." [Survey on LLM-as-a-Judge, arXiv:2411.15594]

**Scale format significantly impacts results:**
- A 1-5 numerical scale for content detection yielded average scores of 1.68, while the identical item on an A-E categorical scale scored 3.17 -- nearly double. [Collective Intelligence Project, 2024]
- LLMs show classification instability: "for ambiguous content, models change classifications substantially when prompt templates or category ordering shifts, with some models showing 100% sensitivity to these variations." [CIP 2024]

**Raw confidence scores are poorly calibrated:**
- "Raw confidence estimates from GPT methods are not well calibrated, with calibration error around 45%, which is 4x that of Logistic Regression baseline (11%)" [Amazon Science, 2024]
- "Vanilla verbalized confidence exhibits significant overconfidence and poor failure prediction, casting doubts on its reliability" [Various, 2024]

**Practical implication:** For LLM research pipelines, a three-category classification (SUPPORTED / CONTRADICTED / UNCERTAIN) is likely more reliable than asking for confidence scores on a 0-1.0 scale. Pairwise comparison ("which of these two sources is more authoritative?") is more reliable than absolute scoring ("rate this source 1-10").

### C2 Claim: Binary or ternary classifications are likely more reliable than fine-grained scalar confidence scores when LLMs evaluate claims.
- **Evidence:** Convergent findings from LLM-as-a-Judge surveys, calibration research, and scale-format studies.
- **Confidence:** MEDIUM-HIGH (70-80%) -- Direct comparative studies of binary vs. scalar for claim verification specifically are limited.

---

## 6. Calibration of LLM Confidence Estimates

### Finding: LLM confidence estimates are systematically miscalibrated, predominantly overconfident.

**Key quantitative findings:**

**Overconfidence prevalence:**
- "In the vast majority of scenarios (84.3%), LLMs are overconfident" [NAACL 2024 Survey on Confidence Calibration]
- GPT-3.5 on math word problems: ECE of 74.8%, NCE of -74.8% (extreme overconfidence) -- "All models reported 90-100% confidence despite much lower actual accuracy" [Groot & Valdenegro-Toro, 2024, arXiv:2405.02917]

**Calibration Error magnitudes:**
- GPT-4o on SimpleQA: ECE of 0.450 (45% calibration error) in free-generation [Mind the Confidence Gap, 2025]
- GPT-4o assigned 93% confidence to an incorrect answer [Mind the Confidence Gap, 2025]
- Clinical domain: "Mean difference in confidence between correct and incorrect responses ranged from 0.6% to 5.4%" -- essentially no meaningful discrimination [JMIR Medical Informatics, 2025]

**Model-specific patterns:**
- GPT-4 variants show best calibration but still significantly overconfident
- Smaller models (8B parameters) show dramatic accuracy jumps with scale but retain poor calibration
- RLHF-trained models tend to exhibit overconfidence "potentially due to sharpened output distributions" [2024]
- "Noisy retrieved contexts" (as in RAG) tend to "inflate the model's false certainty, leading to severe overconfidence" [NAACL 2025]

**Task-dependency:**
- Math: Extreme overconfidence (74.8% ECE)
- Named Entity Recognition: Moderate overconfidence (2.5-12.7% NCE)
- Sentiment Analysis: Slight underconfidence in some models

**Hallucination detection via confidence:**
- Semantic entropy (computing uncertainty at meaning level) shows promise: "At above 80% of questions being answered, semantic entropy has the highest accuracy" for hallucination detection [Nature, 2024, Farquhar et al.]
- Semantic entropy requires ~10x compute (sampling multiple answers and comparing meanings)
- Limitation: Cannot detect cases where the model has been "trained into an incorrect style of reasoning or set of facts"

**Fact-level calibration:**
- ConFix (2024) operated at fact-level granularity: GPT-3.5-turbo achieved 83.29% error detection accuracy, but low recall (0.15-30.62%)
- Poorly calibrated models actually regress with self-correction: LLaMA-2-7B worsened 80.68% of revisions [Fact-Level Confidence Calibration, 2024]

### C1 Claim: LLM confidence estimates are systematically overconfident and poorly calibrated, with Expected Calibration Error (ECE) ranging from 11% to 75% depending on task and model.
- **Source 1:** NAACL 2024 Survey on Confidence Calibration -- "84.3% overconfident"
- **Source 2:** Groot & Valdenegro-Toro 2024 -- ECE up to 74.8% on math
- **Source 3:** Mind the Confidence Gap (2025) -- ECE of 0.450 for GPT-4o
- **Independence check:** PASS -- Three independent research groups with different experimental designs.
- **Confidence:** VERY HIGH (95%)

### C1 Claim: Semantic entropy is the most promising approach to hallucination detection via confidence, but requires ~10x compute overhead.
- **Source 1:** Farquhar et al. 2024, Nature -- outperforms baselines
- **Source 2:** Semantic Entropy Probes (2024) -- confirmatory approach
- **Independence check:** Source 2 builds on Source 1 (same research group, Oxford OATML). Mark as PARTIAL independence.
- **Confidence:** MEDIUM-HIGH (70-80%)

---

## 7. LLM-as-Judge: Systematic Biases

### The 12 Identified Biases (CALM Framework)

The "Justice or Prejudice?" paper (NeurIPS 2024) identified and quantified 12 bias types using the CALM framework:

**Task-Agnostic Biases:**
- Position bias (favoring certain response positions -- B preferred ~60-69% of the time)
- Length/verbosity bias (preferring longer responses)
- Self-enhancement bias (favoring outputs from the evaluating model)
- Bandwagon effect

**Judgment-Specific Biases:**
- Concreteness bias (overweighting stylistic qualities)
- Fallacy oversight (ignoring logical errors in reasoning)
- Sentiment bias
- Authority bias

**Critical finding:** "While advanced models like GPT-4o show strong performance in certain biases (e.g., verbosity, bandwagon-effect), **no single model consistently outperforms others across all 12 bias types**."

### Self-Preference Bias: A Causal Mechanism

**Panickssery et al. (NeurIPS 2024):** Established a **causal link** between self-recognition and self-preference bias:
- GPT-4 and Llama 2 have "non-trivial accuracy at distinguishing themselves from other LLMs and humans"
- Fine-tuning revealed "a linear correlation between self-recognition capability and the strength of self-preference bias"
- GPT-4 showed strongest self-preference (0.520 bias score)
- Root cause: LLMs favor lower-perplexity text, and their own outputs inherently have lower perplexity

**Practical implication for verification pipelines:** Using the same model family to both generate and verify content is structurally biased. The verifier will tend to approve the generator's output because it finds it linguistically familiar, not because it has verified the claims.

### C1 Claim: LLMs used as judges exhibit systematic, quantifiable biases including position bias, verbosity bias, and self-preference bias.
- **Source 1:** "Justice or Prejudice?" NeurIPS 2024 -- 12 biases quantified via CALM
- **Source 2:** Panickssery et al. NeurIPS 2024 -- causal link established
- **Source 3:** Survey on LLM-as-a-Judge (arXiv:2411.15594) -- comprehensive review
- **Independence check:** PASS -- Three independent research groups.
- **Confidence:** VERY HIGH (95%)

---

## 8. Synthesis: Implications for LLM Research Pipeline Design

### What Actually Works for Verification

| Approach | Evidence of Effectiveness | Recommended? |
|----------|--------------------------|-------------|
| External tool verification (code exec, search, KB) | Strong (Self-RAG 81%, CoVe +23% F1) | YES |
| Multi-agent debate (different models) | Moderate-strong (Du et al. ICML 2024) | YES, for high-stakes claims |
| Atomic fact decomposition + retrieval | Strong (FActScore <2% error) | YES |
| Semantic entropy for uncertainty detection | Promising (Nature 2024) | YES, if compute budget allows |
| Pairwise comparison over absolute scoring | Moderate (better human alignment) | YES |
| Same-model self-reflection without tools | Weak to negative (Huang 2023, Kamoi 2024) | NO |
| Confidence score filtering (unexcalibrated) | Weak (84.3% overconfident) | NO |
| Elaborate multi-step intrinsic verification | Weak (overhead without proportional gain) | NO |

### Design Recommendations for the GoT Pipeline

1. **Replace intrinsic verification with tool-grounded verification.** Instead of asking the LLM "is this claim correct?", have it search for contradicting evidence, check citations against actual source text, and verify numbers against authoritative databases.

2. **Use binary/ternary claim classifications, not scalar confidence.** SUPPORTED / CONTRADICTED / UNCERTAIN is more reliable than 0.78 confidence.

3. **Do not use the same model to generate and verify.** Self-preference bias is structural. Use different model families or, better, external tools.

4. **Source independence assessment requires structured approach.** Don't ask the LLM "are these independent?" Instead, check for: shared URLs/domains, shared authors, shared publication dates suggesting same event, shared unique data points suggesting same underlying source.

5. **Calibrate expectations about verification depth.** The theoretical impossibility results (Banerjee et al. 2024) mean verification reduces error probability but cannot eliminate it. Design for graceful uncertainty rather than false certainty.

6. **Focus verification budget on C1 claims.** External verification is expensive (~10x compute for semantic entropy, significant latency for web search). Reserve thorough verification for critical claims.

7. **Treat elaborate internal verification skeptically.** Multi-step self-reflection without external grounding is likely verification theater. The research is clear: the bottleneck is feedback quality, not feedback quantity.

---

## 9. Gaps and Limitations in This Analysis

### What We Could Not Find

1. **Direct studies on LLM source independence assessment** -- No published research directly tests whether LLMs can determine if two sources are truly independent. This is a gap in the literature.

2. **Controlled experiments comparing binary vs. scalar evaluation for claim verification specifically** -- The evidence for binary superiority comes from adjacent domains (LLM-as-judge, classification tasks) rather than from claim verification directly.

3. **Long-term reliability studies** -- Most benchmarks are cross-sectional. We lack evidence on whether verification quality degrades over repeated use or with evolving knowledge.

4. **Cost-benefit analysis of verification depth** -- No studies directly measure the ROI of various verification strategies in LLM research pipelines.

### Unresolved Contradictions

- The 2025 self-correction benchmark showed +23.24% GPQA improvement with CoVe, while Kamoi et al. 2024 found intrinsic self-correction generally fails. Resolution: CoVe involves structured decomposition (essentially turning a hard problem into easier sub-problems), which is the exception Kamoi et al. identify -- tasks where verification is substantially easier than generation.

- Semantic entropy shows promise for hallucination detection, but RLHF-trained models (which most production models are) have "sharpened output distributions" that may reduce the signal semantic entropy relies on. This needs further investigation.

---

## 10. Source Catalog

### Grade A Sources (Systematic reviews, peer-reviewed at top venues)
| Source | Citation | Used For |
|--------|----------|----------|
| Kamoi et al. 2024 | "When Can LLMs Actually Correct Their Own Mistakes?" TACL vol. 12, pp. 1417-1440 | Self-correction taxonomy, meta-analysis |
| Survey on LLM-as-a-Judge 2024 | arXiv:2411.15594 | Comprehensive bias analysis |
| Farquhar et al. 2024 | "Detecting hallucinations using semantic entropy" Nature vol. 630, pp. 625-630 | Hallucination detection |
| NAACL 2024 Survey | "A Survey of Confidence Estimation and Calibration in LLMs" | Calibration overview |

### Grade B Sources (Published at top venues, single study)
| Source | Citation | Used For |
|--------|----------|----------|
| Huang et al. 2023 | "Large Language Models Cannot Self-Correct Reasoning Yet" arXiv:2310.01798 | Foundational self-correction finding |
| Du et al. 2024 | "Improving Factuality through Multiagent Debate" ICML 2024 | Multi-agent verification |
| Panickssery et al. 2024 | "LLM Evaluators Recognize and Favor Their Own Generations" NeurIPS 2024 | Self-preference bias |
| Asai et al. 2024 | "Self-RAG" ICLR 2024 (Oral) | External-feedback self-correction |
| Min et al. 2023 | "FActScore" EMNLP 2023 | Atomic fact evaluation |
| Dhuliawala et al. 2024 | "Chain-of-Verification" ACL Findings 2024 | Verification method |
| Gao et al. 2023 | "RARR" ACL 2023 | Attribution verification |
| "Justice or Prejudice?" 2024 | NeurIPS 2024 | 12 LLM judge biases |
| Groot & Valdenegro-Toro 2024 | "Overconfidence is Key" arXiv:2405.02917 | Calibration measurements |
| 2025 Self-Correction Benchmark | arXiv:2510.16062 | Updated benchmark results |

### Grade C Sources (Preprints, technical reports, blog posts)
| Source | Citation | Used For |
|--------|----------|----------|
| Banerjee et al. 2024 | "LLMs Will Always Hallucinate" arXiv:2409.05746 | Theoretical impossibility argument |
| Xu et al. 2024 | "Hallucination is Inevitable" arXiv:2401.11817 | Formal impossibility proof |
| Mind the Confidence Gap 2025 | arXiv:2502.11028 | GPT-4o calibration measurements |
| Fact-Level Confidence 2024 | arXiv:2411.13343 | ConFix results |
| CIP 2024 | "LLM Judges Are Unreliable" Blog post | Scale format effects |
| OATML Oxford Blog 2024 | Semantic entropy blog | Implementation details |

---

## Key Findings Summary

1. **LLMs cannot reliably assess source independence** -- no evidence supports this capability, and theoretical limitations of LLM reasoning make it implausible without structured provenance data.

2. **Source diversity genuinely improves research quality** -- well-established in research methodology (triangulation), but diversity must mean genuine independence, not just different labels on the same underlying source.

3. **LLM self-correction without external feedback is unreliable** -- confirmed by Huang 2023, Kamoi 2024 survey, and 2025 benchmark. This finding has held up across model generations. The bottleneck is feedback quality, not quantity.

4. **External feedback (RAG, tools, search) materially helps** -- Self-RAG (81% fact-checking), CoVe (+23% F1), CRITIC all show genuine improvement. This is the primary lever for quality.

5. **Verification without external grounding is largely theater** -- Same-model self-reflection, confidence-based filtering, and elaborate multi-step intrinsic verification create an appearance of rigor without the substance. The self-preference bias (GPT-4 = 0.520 bias score) means the verifier is structurally inclined to approve.

6. **LLM confidence is systematically overconfident** -- 84.3% overconfident across scenarios, ECE up to 74.8%. Binary/ternary classifications are more reliable than scalar scores.

7. **Multi-agent debate provides genuine improvement** -- but at significant computational cost. Best reserved for high-stakes claims.

8. **Hallucination is theoretically irreducible** -- formal proofs show it cannot be fully eliminated, only reduced. Design for graceful uncertainty.
