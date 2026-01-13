# RLM - Recursive Language Model Plugin

A Claude Code plugin that implements state-of-the-art recursive reasoning techniques for iterative solution refinement.

## Features

- **Self-Refine**: Generate → Critique → Refine loop (~20% improvement)
- **Reflexion**: Maintain memory buffer across iterations
- **Tree of Thoughts**: Multi-branch exploration with backtracking
- **Self-Consistency**: Sample diverse paths, select consensus
- **Constitutional AI**: Principle-guided self-critique
- **Least-to-Most**: Problem decomposition into subproblems

## Installation

### Option 1: Local Development

```bash
claude --plugin-dir /path/to/rlm-skill
```

### Option 2: From GitHub

First, add the marketplace:

```bash
/plugin marketplace add lollipopkit/rlm-skill
```

Then install the plugin:

```bash
/plugin install rlm
```

### Option 3: Direct Git Install

```bash
/plugin install github:lollipopkit/rlm-skill
```

## Usage

### Trigger Phrases

The RLM skill activates automatically when you use phrases like:

- "Use RLM to solve this"
- "Think recursively about..."
- "Refine this iteratively"
- "Deep think mode"
- "Multi-pass reasoning"
- "Self-refine this solution"

### Example

```text
User: Use RLM to design a rate limiter algorithm

Claude: [Applies RLM workflow]
- Phase 1: Decompose problem
- Phase 2: Generate initial solution
- Phase 3: Self-critique against principles
- Phase 4: Explore alternative branches
- Phase 5: Refine and iterate
- Phase 6: Verify consistency
- Final: Synthesized answer with evolution summary
```

## Plugin Structure

```text
rlm-skill/
├── .claude-plugin/
│   ├── plugin.json         # Plugin manifest
│   └── marketplace.json    # Marketplace definition
├── skills/
│   └── rlm/
│       ├── SKILL.md              # Main skill definition
│       ├── advanced-techniques.md # Detailed methodology
│       └── examples.md           # Example workflows
└── README.md
```

## Mode Selection

| Problem Type | Mode | Iterations |
| -------------- | ------ | ------------ |
| Simple bug fix | Light RLM | 2 |
| Algorithm design | Full RLM | 3-4 |
| Architecture decision | Full RLM + ToT | 4-5 |
| Creative/open-ended | Full RLM + Branching | 5+ |
| Mission-critical code | Full RLM + Consistency | 5+ |

## Research References

| Technique | Paper | Venue/Year |
| ----------- | ------- | ----------- |
| PRefLexOR | Preference-Based Recursive Language Models | Nature 2025 |
| SSR | Socratic Self-Refine for LLM Reasoning | arXiv 2025 |
| Self-Refinement | Learning to Refine: Parallel Reasoning in LLMs | OpenReview 2025 |
| Self-Reflection | Self-reflection enhances LLMs (Dual-loop) | Nature 2025 |
| Recursive Reasoning | Tiny Recursive Models (Samsung TRM) | arXiv 2025 |
| Self-Evolving Agents | Reframing Self-Evolving LLM Agents | arXiv 2026 |
| Survey | A Comprehensive Survey on Latent Chain-of-Thought | arXiv 2025 |
| Survey | A Survey of Reasoning Large Language Models | arXiv 2025 |
| Survey | Empowering LLMs with Logical Reasoning | IJCAI 2025 |
| Survey | A Survey of Chain-of-X Paradigms | COLING 2025 |

## License

MIT
