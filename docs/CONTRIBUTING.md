# 🤝 Contributing

Thank you for your interest in contributing to **NW Agentic Demos**! Contributions of all kinds are welcome — new demos, bug fixes, documentation improvements, or just opening an issue with an idea.

---

## Table of Contents

- [Ways to Contribute](#ways-to-contribute)
- [Development Setup](#development-setup)
- [Adding a New Demo](#adding-a-new-demo)
  - [Demo Structure](#demo-structure)
  - [README Template](#readme-template)
  - [Checklist Before Submitting](#checklist-before-submitting)
- [Improving Existing Demos](#improving-existing-demos)
- [Documentation Changes](#documentation-changes)
- [Pull Request Guidelines](#pull-request-guidelines)
- [Code Style](#code-style)
- [Commit Convention](#commit-convention)

---

## Ways to Contribute

| Contribution type | Notes |
|-------------------|-------|
| 🆕 New demo | Follow the [Adding a New Demo](#adding-a-new-demo) guide |
| 🐛 Bug fix | Open an issue first if the fix is non-trivial |
| 📖 Docs improvement | PRs for typos, clarity, or missing info are always welcome |
| 💡 Feature request | Open an issue with the `enhancement` label |
| 🔧 Dependency update | Include a reason and test confirmation |

---

## Development Setup

```bash
git clone https://github.com/niteshwalia0124/nw-agentic-demos.git
cd nw-agentic-demos

python -m venv .venv
source .venv/bin/activate

pip install google-adk
```

---

## Adding a New Demo

### Demo Structure

Create a new directory under `demos/` with the next available number prefix:

```
demos/
└── 06-my-new-demo/
    ├── README.md          ← required — use the template below
    ├── agent.py           ← required — the ADK agent entry point
    ├── requirements.txt   ← required — pinned dependencies
    ├── .env.example       ← required — list all required env vars (no values)
    ├── tools/             ← optional — custom tool implementations
    │   └── my_tool.py
    ├── tests/             ← optional but encouraged
    │   └── test_agent.py
    └── assets/            ← optional — screenshots, diagrams
        └── architecture.png
```

### README Template

Every demo README should follow this structure (copy and adapt):

```markdown
# Demo NN — [Demo Title]

> One-line tagline describing what this demo does.

## Overview

Brief description (2–3 sentences).

## Architecture

[Mermaid diagram or image]

## What You'll Learn

- Bullet 1
- Bullet 2
- Bullet 3

## Prerequisites

- Google ADK (see [Getting Started](../../docs/GETTING_STARTED.md))
- `GOOGLE_API_KEY` environment variable
- Any other requirements

## Setup

```bash
cd demos/NN-my-demo
pip install -r requirements.txt
cp .env.example .env  # fill in your API keys
```

## Running the Demo

```bash
adk run agent.py
```

## Example Output

Paste a sample run here.

## Key Concepts

| Concept | Where to find it |
|---------|-----------------|
| ...     | `agent.py:42`   |

## Extending This Demo

Ideas for how contributors or readers can build on this demo.
```

### Checklist Before Submitting

- [ ] Demo directory follows the naming convention `NN-descriptive-name/`
- [ ] `README.md` is complete (uses the template above)
- [ ] `requirements.txt` includes all dependencies with pinned versions
- [ ] `.env.example` lists all required environment variables (values redacted)
- [ ] `agent.py` runs successfully with `adk run agent.py`
- [ ] Demo is added to the table in the root `README.md`
- [ ] Demo is linked in `docs/GETTING_STARTED.md` demo-specific setup table
- [ ] No API keys or secrets committed

---

## Improving Existing Demos

1. **Fork** the repository and create a feature branch:
   ```bash
   git checkout -b fix/demo-02-embedding-model
   ```
2. Make your changes.
3. Test the affected demo end-to-end with `adk run agent.py`.
4. Open a Pull Request with a clear description of the change and why it's an improvement.

---

## Documentation Changes

Documentation lives in:
- `README.md` — root overview
- `docs/ARCHITECTURE.md` — technical design
- `docs/GETTING_STARTED.md` — setup guide
- `docs/CONTRIBUTING.md` — this file
- `demos/*/README.md` — per-demo docs

For Mermaid diagrams, test them in the [Mermaid Live Editor](https://mermaid.live) before committing.

---

## Pull Request Guidelines

- **One change per PR** — keep PRs focused. Large PRs are hard to review.
- **Descriptive title** — use the commit convention format (see below).
- **Fill in the PR template** — describe what changed and why.
- **Link related issues** — use `Closes #NN` or `Relates to #NN`.
- **No merge commits** — rebase on `main` before opening a PR if your branch is behind.

---

## Code Style

All Python code should follow [PEP 8](https://peps.python.org/pep-0008/) and be formatted with [black](https://black.readthedocs.io/):

```bash
pip install black
black demos/your-demo/
```

Type hints are encouraged where they improve readability.

---

## Commit Convention

This repo follows [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <short description>
```

| Type | When to use |
|------|------------|
| `feat` | New demo or new feature in an existing demo |
| `fix` | Bug fix |
| `docs` | Documentation only change |
| `refactor` | Code change that doesn't fix a bug or add a feature |
| `chore` | Dependency updates, config changes |

**Examples:**

```
feat(demo-06): add autonomous coding agent
fix(demo-02): correct ChromaDB collection initialization
docs(architecture): add tool execution flow diagram
```

---

> Questions? Open an issue with the `question` label or start a [Discussion](https://github.com/niteshwalia0124/nw-agentic-demos/discussions).
