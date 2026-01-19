# /dr - Deep Research Skill for Claude Code

A comprehensive deep research implementation using **Graph of Thoughts (GoT)** methodology.

## Overview

The `/dr` skill enables multi-phase research with:
- Automatic query refinement for vague inputs
- Perspective discovery (STORM methodology)
- Evidence indexing and retrieval
- Reflexion-based QA with cross-project learning
- Domain overlays (Healthcare, Financial, Legal, Market)

## Usage

```
/dr [topic]
```

Or invoke directly:
```
Deep research [topic]
```

## Structure

```
agents/
  deep-research.md       # Main agent definition (GoT implementation)

commands/
  dr.md                  # Skill entry point
  dr-refine.md           # Optional standalone refinement

skills/deep-research/
  ADVANCED_RETRIEVAL.md  # HyDE + Evidence indexing
  PERSPECTIVE_DISCOVERY.md # STORM-inspired perspective mining
  QUERY_REFINEMENT.md    # Adaptive query refinement
  REFLEXION_QA.md        # Self-correction with failure taxonomy
  HEALTHCARE.md          # Domain overlay
  FINANCIAL.md           # Domain overlay
  LEGAL.md               # Domain overlay
  MARKET.md              # Domain overlay

reflection_memory.json   # Cross-project learning bootstrap
```

## Installation

Copy or symlink to your `~/.claude/` directory:

```bash
# Symlink approach (recommended)
ln -s /path/to/dr/agents/deep-research.md ~/.claude/agents/
ln -s /path/to/dr/commands/dr.md ~/.claude/commands/
ln -s /path/to/dr/commands/dr-refine.md ~/.claude/commands/
ln -s /path/to/dr/skills/deep-research ~/.claude/skills/
```

## 7-Phase Methodology

1. **Phase 0**: Question complexity classification
2. **Phase 1**: Scope refinement (adaptive questioning)
3. **Phase 1.5-1.6**: Hypothesis formation + Perspective discovery
4. **Phase 2**: Retrieval planning
5. **Phase 3**: Iterative querying (GoT Generate)
6. **Phase 4**: Source triangulation (GoT Score)
7. **Phase 5**: Knowledge synthesis (GoT Aggregate)
8. **Phase 6**: Quality assurance (Reflexion)
9. **Phase 7**: Output packaging

## Version History

- **v1.0**: Initial release with GoT, adaptive refinement, perspectives, HyDE, Reflexion
