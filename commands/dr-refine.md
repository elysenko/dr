---
description: Refine a vague research question before deep research (optional - /dr now auto-refines)
allowed-tools: AskUserQuestion
argument-hint: [vague research topic]
---

# Research Question Refiner (v2.0)

**Note:** This skill is optional. `/dr` automatically detects vague queries and triggers refinement. Use `/dr-refine` if you want to refine a question WITHOUT starting research, or to explore what you need before committing.

Before launching deep research, refine this question: $ARGUMENTS

---

## Refinement Philosophy

Good refinement doesn't capture what users think they know—it helps them discover what they didn't know they needed. The research consistently shows:

1. **Users cannot articulate tacit knowledge** - Asking "what do you need?" fails for complex questions
2. **"Why" questions invite rationalization** - Timeline questions ("what triggered this?") reveal more
3. **Assumptions are invisible to holders** - Structured techniques (pre-mortem) surface them better than direct questions
4. **Query types differ fundamentally** - Learning, deciding, and validating need different approaches

This skill generates insight, not just captures it.

---

## Phase 0: Query Type Diagnosis (Always First)

Before any substantive questions, classify the query type. This determines which phases to use and how deep to go.

### Ask or Infer

**If type is unclear from the query, ask:**
```
Before we refine this, help me understand what kind of question this is:

□ LEARNING - "I want to understand something new"
□ DECISION - "I need to choose between options"
□ VALIDATION - "I think X is true and want to verify"
□ EXPLORATION - "I'm not sure what I'm even asking yet"
□ DUE DILIGENCE - "I need to understand what could go wrong"
```

**If type seems clear, confirm:**
```
This sounds like a [DECISION] question—you're trying to choose between approaches. Is that right, or is it more about [learning/validation/etc.]?
```

### Type Determines Path

| Type | Real Question | Beliefs | Pre-Mortem | Generative | Stakes |
|------|--------------|---------|------------|------------|--------|
| Learning | Action test only | Abbreviated | Skip | Full | Depth only |
| Decision | Full | Full | Full | Full | Full |
| Validation | Action + doubt source | Full | Full | Contrarian only | Cost of wrong |
| Exploration | Action + gap | Abbreviated | Abbreviated | Full | Skip |
| Due Diligence | Full | Full | Full | Risk-focused | Full |

---

## Phase 1: The Real Question

The goal is to surface what they actually need—not what they think they're asking.

### 1.1 The Action Test (Always Start Here)

This single question cuts through vague framing faster than anything else:

```
If you had a perfect answer right now, what would you DO with it?
```

**Why this works:** It forces specificity. "I'd decide whether to..." vs "I'd understand..." vs "Nothing, just curious" completely changes what research is needed.

**Follow the thread:** Whatever they say, probe once more:
- "Decide whether to..." → "What's making that decision hard?"
- "Convince someone..." → "What would change their mind?"
- "Understand..." → "What specifically is unclear?"

### 1.2 The Trigger (Only If Action-Oriented)

**Skip this for pure learning queries.** Only ask when the action test revealed a decision or deadline:

```
What changed that made this urgent now?
```

Don't ask generically. Ask specifically based on what they said:
- If they mentioned a decision: "What forced this decision onto your plate?"
- If they mentioned a problem: "When did this start being a problem?"
- If they mentioned a deadline: "What happens if you don't have an answer by then?"

### 1.3 The Gap (Only If They've Already Searched)

**Skip if they're starting fresh.** Only ask if they indicate prior research:

```
What have you found that almost answered this but didn't quite?
```

This is gold when it applies—reveals exactly what "good enough" looks like for them. But asking someone who hasn't searched yet wastes time.

### 1.4 The Reframe (Always Offer)

After hearing their answers, reflect back what you think they're actually asking:

```
So it sounds like the real question is: [your reframing]

Is that right, or am I missing something?
```

**This is where you add value.** Don't just parrot back—synthesize. If they asked "What's the best database?" but revealed they're trying to handle 10x traffic growth, the real question might be "How do we scale our data layer for 10x growth?"

### When to Skip Phase 1 Entirely

If the query is already specific and action-oriented, don't belabor it:
- "Compare PostgreSQL vs MySQL for our write-heavy workload" → Skip to Phase 2
- "What are the risks of using JWT for session management?" → Skip to Phase 2
- "Help me understand how Kubernetes networking works" → Just confirm depth preference

**The test:** Can you already write a clear research question from what they said? If yes, confirm it and move on.

---

## Phase 2: Belief Surfacing (Evocative, Not Extractive)

Direct questions about beliefs get rehearsed answers. These techniques surface beliefs indirectly.

### 2.1 Reflective Probe
After hearing their question, reflect back with interpretation:
```
So it sounds like you believe [your interpretation of their underlying belief]. Is that right, or am I missing something important?
```

Example: "So it sounds like you believe switching to TypeScript will slow down the team initially but pay off long-term. Is that the core assumption we're testing?"

### 2.2 Confidence Calibration
```
What's your gut feeling about the answer right now?
- If you had to bet money, what would you bet is probably true?
- How confident are you in that? (20%? 60%? 90%?)
- Where did that belief come from?
```

### 2.3 Surprise Elicitation
```
What would genuinely SURPRISE you if the research revealed it?

Not what you'd find interesting—what would make you say "Wow, I really didn't expect that"?
```

The surprise test reveals beliefs by their negation.

### 2.4 Contrarian Probe
```
What's the strongest argument AGAINST your current thinking?

If someone smart and well-informed disagreed with you, what would they say?
```

---

## Phase 3: Pre-Mortem (Structured Assumption Surfacing)

Research shows prospective hindsight improves failure identification by 30%. This phase imagines research failure to surface hidden assumptions.

### 3.1 The Core Pre-Mortem
```
Let's imagine: The research is complete. You read it and think "This completely missed the mark—it didn't answer what I actually needed."

What happened? Why did it miss?
```

### 3.2 Follow-Up Probes
```
What would make you say "This answered a different question than I had"?

What's the most important thing this research could get WRONG that would make it useless?

What assumptions might the research make that don't apply to your specific situation?
```

### 3.3 Alternative Framing (If Pre-Mortem Feels Uncomfortable)
```
To make sure the research hits the mark:
- What would definitely NOT answer your question?
- What scope would be too narrow or too broad?
- What angle would be the wrong angle?
```

---

## Phase 4: Generative Expansion (The Skill Generates, User Confirms)

Instead of asking users to articulate all their needs, generate questions they might not have considered.

### 4.1 Sub-Question Generation
Based on the query and conversation, generate 4-6 sub-questions:
```
To properly answer your question, research might need to address these sub-questions:

1. [Generated sub-question addressing a potential blind spot]
2. [Generated sub-question covering an alternative angle]
3. [Generated sub-question about constraints or tradeoffs]
4. [Generated sub-question about implementation/application]
5. [Generated sub-question about risks or failure modes]

Which of these matter to you? Any that are irrelevant? Any important ones missing?
```

### 4.2 Adjacent Questions
```
Related questions that might also matter:
- [Adjacent question 1 - related topic they might not have connected]
- [Adjacent question 2 - prerequisite knowledge they might be missing]

Should research touch on any of these, or stay focused on your core question?
```

### 4.3 Contrarian Angle Offer
```
Research could also explore the opposite view:
"[Contrarian framing of their assumption]"

Worth including as a counter-perspective, or definitely out of scope?
```

---

## Phase 5: Stakes & Constraints (Conditional on Query Type)

Only ask what's relevant to this query type. Skip irrelevant logistics.

### For DECISION Queries
```
Decision-specific questions:
- What alternatives are you actually comparing?
- What's the default if you do nothing?
- Who else needs to be convinced, and what would change their mind?
- What timeline are you working with?
- What constraints are non-negotiable vs. preferences?
```

### For VALIDATION Queries
```
Validation-specific questions:
- What evidence would actually change your mind?
- What's the strongest source that might disagree with your current view?
- What's the cost of being wrong in either direction?
```

### For LEARNING Queries
```
Learning-specific questions:
- How deep do you need to go—survey level or expert level?
- Is this for your own understanding or to explain to others?
- Any areas you specifically want to avoid or definitely want included?
```

### For EXPLORATION Queries
```
Exploration-specific questions:
- What would a successful exploration look like? (Map of options? Key questions identified? Promising directions flagged?)
- Any areas to definitely avoid or definitely include?
```

### For DUE DILIGENCE Queries
```
Due diligence-specific questions:
- What's the worst-case scenario you need to understand?
- What risk level is acceptable vs. unacceptable?
- Who are the stakeholders who would be affected by failure?
- What's the cost of NOT knowing something important?
```

### Skip for Most Types
Unless specifically relevant, don't ask about:
- Geographic scope
- Format preferences
- Source type preferences
- Precise depth preferences (infer from stakes)

---

## Phase 6: Synthesis & Confirmation

### Output Structured Research Contract

Present the refined understanding:

```
### RESEARCH QUESTION
[Reframed based on conversation—often different from original]

### QUERY TYPE
[Learning / Decision / Validation / Exploration / Due Diligence]

### WHAT THEY'LL DO WITH IT
[The action or decision this enables—from the action test]

### CURRENT BELIEF
[What they think is probably true]
- Confidence level: [X%]
- Source of belief: [where this came from]
→ Research should: [confirm / challenge / expand / test] this view

### KEY UNCERTAINTIES
[2-4 specific things that, if answered, would most change their thinking]

### WHAT WOULD CHANGE THEIR MIND
[Evidence or findings that would shift their view]

### PRE-MORTEM INSIGHTS
[How research could miss the mark; assumptions to watch]

### SUB-QUESTIONS TO ADDRESS
[Generated and confirmed sub-questions]

### SCOPE BOUNDARIES
- Focus areas: [where to go deep]
- Exclusions: [what to skip or cover lightly]
- [Type-specific constraints from Phase 5]

### SUCCESS CRITERIA
[What would make this research actually valuable to them]
```

### Confirm
```
Does this capture what you actually need?

Anything important I'm missing or getting wrong?
```

Then offer to run `/dr` with the refined question.

---

## Quick Reference: Question Selection by Type

### LEARNING Queries (Shortest Path)
1. ✓ Type diagnosis (or skip if obvious)
2. ~ Real Question: Action test only ("what will you do with this?"), skip trigger
3. ~ Beliefs: Just surprise elicitation
4. ✗ Pre-mortem: Skip
5. ✓ Generative: Sub-questions to expand thinking
6. ~ Stakes: Just depth preference
7. ✓ Synthesis

### DECISION Queries (Full Path)
1. ✓ Type diagnosis
2. ✓ Real Question: Full—action test, trigger, reframe
3. ✓ Beliefs: Full—especially contrarian probe
4. ✓ Pre-mortem: Full
5. ✓ Generative: Full
6. ✓ Stakes: Alternatives, constraints, stakeholders
7. ✓ Synthesis

### VALIDATION Queries
1. ✓ Type diagnosis
2. ~ Real Question: Action test + what's making you doubt?
3. ✓ Beliefs: Full—especially source of belief
4. ✓ Pre-mortem: What would prove you wrong?
5. ~ Generative: Contrarian angles mainly
6. ✓ Stakes: Cost of being wrong
7. ✓ Synthesis

### EXPLORATION Queries
1. ~ Type diagnosis (usually obvious)
2. ✓ Real Question: Action test ("what would you do?") + the gap if they've searched
3. ~ Beliefs: Just surprise elicitation
4. ~ Pre-mortem: Abbreviated—what would miss the mark?
5. ✓ Generative: Full—essential for exploration
6. ✗ Stakes: Skip—exploration is open-ended
7. ✓ Synthesis

### DUE DILIGENCE Queries
1. ✓ Type diagnosis
2. ✓ Real Question: Full—what's at stake if you miss something?
3. ✓ Beliefs: Full—especially hidden assumptions
4. ✓ Pre-mortem: Full—essential for risk assessment
5. ✓ Generative (risk-focused sub-questions)
6. ✓ Stakes (full—especially worst case and cost of not knowing)
7. ✓ Synthesis

---

## Anti-Patterns to Avoid

1. **Don't ask "why"** - It invites rationalization. Ask "what happened" instead.

2. **Don't ask about format early** - Substance before logistics. Format questions can wait until synthesis or be skipped entirely.

3. **Don't accept the first framing** - The stated question rarely reflects the real need. Use timeline and belief probes to discover the actual question.

4. **Don't ask directly about assumptions** - "What are you assuming?" doesn't work. Use pre-mortem and reflective probing instead.

5. **Don't treat all queries the same** - Learning and Decision queries need fundamentally different refinement.

6. **Don't just capture—generate** - Show users questions they didn't think to ask. The skill should expand their thinking, not just record it.

7. **Don't skip follow-ups** - Initial answers are often rehearsed. Depth comes from "tell me more about that."

8. **Don't overwhelm with questions** - Use the adaptive matrix. Skip phases that don't apply to this query type.
