---
description: Refine a vague research question then automatically launch deep research
allowed-tools: AskUserQuestion, WebSearch, WebFetch, Task, Read, Write, Glob, Grep, TodoWrite
argument-hint: [vague research topic]
---

# Research Question Refiner + Auto-Launch

Refine this vague question into a well-structured research prompt, then automatically launch deep research: $ARGUMENTS

## Step 1: Ask clarifying questions to capture:

1. **Core Question**: What is the one-sentence research question?
2. **Decision/Use-case**: What will this research inform? (investment, strategy, learning, etc.)
3. **Audience**: Who will consume this? (Executive, Technical, Mixed)
4. **Scope**:
   - Geographic focus (Global, US, EU, specific country?)
   - Timeframe (Historical? Current state? Future projections?)
   - What to include/exclude?
5. **Constraints**:
   - Required sources (academic only? include news?)
   - Banned sources (avoid vendor content? exclude specific outlets?)
   - Budget/depth preference (Quick overview vs exhaustive analysis)
6. **Output Format**: Report, bullet summary, data pack, slides outline?
7. **Citation Strictness**: Full academic citations vs light sourcing?
8. **Definition of Done**: What would make this research "complete"?

## Step 2: After gathering answers, construct the refined prompt:

```
### RESEARCH QUESTION
[One clear sentence]

### CONTEXT
[What this informs, who will use it]

### SCOPE
- Geography: [X]
- Timeframe: [X]
- Include: [X]
- Exclude: [X]

### CONSTRAINTS
- Required sources: [X]
- Avoid: [X]
- Depth: [Quick/Standard/Deep/Exhaustive]

### OUTPUT FORMAT
[What deliverable looks like]

### SUCCESS CRITERIA
[How we know we're done]
```

## Step 3: Automatically launch deep research

Do NOT ask for confirmation. Immediately invoke the deep-research agent with the refined prompt using the Task tool:

```
Task(subagent_type="deep-research", prompt="[refined research prompt from Step 2]")
```

The research will proceed through all phases automatically.
