---
description: Refine a vague research question then automatically launch deep research
allowed-tools: AskUserQuestion, WebSearch, WebFetch, Task, Read, Write, Glob, Grep, TodoWrite
argument-hint: [vague research topic]
---

# Research Question Refiner + Auto-Launch

Refine this vague question into a well-structured research prompt, then automatically launch deep research: $ARGUMENTS

## Step 1: Run the v2.0 refinement process

Follow the full `/dr-refine` process from `skills/deep-research/QUERY_REFINEMENT.md`:
1. **Phase 0**: Diagnose query type (Learning/Decision/Validation/Exploration/Due Diligence)
2. **Phase 1**: Surface the real question (action test, trigger, reframe)
3. **Phase 2**: Surface beliefs (reflective probe, confidence calibration, surprise elicitation)
4. **Phase 3**: Pre-mortem (structured assumption surfacing)
5. **Phase 4**: Generative expansion (sub-questions, adjacent questions, contrarian angles)
6. **Phase 5**: Stakes & constraints (conditional on query type)
7. **Phase 6**: Synthesize into a structured research contract

Use the adaptive matrix from QUERY_REFINEMENT.md to skip phases based on query type.

## Step 2: Automatically launch deep research

After the user confirms the refined research contract, immediately invoke the deep-research agent:

```
Task(subagent_type="deep-research", prompt="[refined research contract from Step 1]")
```

Do NOT ask for additional confirmation. The research contract confirmation IS the launch approval.
