# 🚀 Getting Started

This guide walks you through everything you need to set up your environment and run the demos in this repository.

---

## Table of Contents

- [System Requirements](#system-requirements)
- [Installation](#installation)
  - [1. Clone the Repository](#1-clone-the-repository)
  - [2. Python Environment](#2-python-environment)
  - [3. Install Google ADK](#3-install-google-adk)
  - [4. API Keys](#4-api-keys)
- [Running Your First Demo](#running-your-first-demo)
- [Environment Configuration Reference](#environment-configuration-reference)
- [Troubleshooting](#troubleshooting)

---

## System Requirements

| Dependency | Minimum Version | Notes |
|-----------|----------------|-------|
| Python | 3.10 | 3.11 or 3.12 recommended |
| pip | 23.0 | `pip install --upgrade pip` |
| Git | 2.30 | |
| Google ADK | latest | `pip install google-adk` |
| Gemini API Key | — | Free tier available at [aistudio.google.com](https://aistudio.google.com) |

Optional (required by some demos):

| Dependency | Required by | Notes |
|-----------|------------|-------|
| OpenAI API Key | Demo 03, 05 | `pip install openai` |
| Docker | Demo 03 | Sandboxed code execution |
| ChromaDB | Demo 02 | `pip install chromadb` |

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/niteshwalia0124/nw-agentic-demos.git
cd nw-agentic-demos
```

### 2. Python Environment

It is strongly recommended to use a virtual environment to avoid dependency conflicts between demos.

**Using `venv` (built-in):**

```bash
python -m venv .venv

# Activate on macOS / Linux:
source .venv/bin/activate

# Activate on Windows (PowerShell):
.venv\Scripts\Activate.ps1

# Activate on Windows (CMD):
.venv\Scripts\activate.bat
```

**Using `conda`:**

```bash
conda create -n agentic-demos python=3.12
conda activate agentic-demos
```

### 3. Install Google ADK

```bash
pip install google-adk
```

To verify the installation:

```bash
adk --version
```

### 4. API Keys

Each demo requires at minimum a **Google Gemini API key**. Some demos optionally support OpenAI or Anthropic models.

#### Get a Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click **Create API key**
3. Copy the key

#### Set Environment Variables

**Option A: Export directly (temporary, current session only)**

```bash
export GOOGLE_API_KEY="your-gemini-api-key-here"
```

**Option B: `.env` file (recommended, persists across sessions)**

Each demo directory contains a `.env.example` file. Copy it to `.env` and fill in your keys:

```bash
cd demos/01-multi-agent-orchestration
cp .env.example .env
# Edit .env with your favorite editor
```

`.env` files are listed in `.gitignore` and will never be committed to the repository.

---

## Running Your First Demo

We recommend starting with **Demo 04 — Conversational Agent** as it has the fewest dependencies.

```bash
# From the repo root
cd demos/04-conversational-agent

# Install demo-specific dependencies
pip install -r requirements.txt

# Run with ADK
adk run agent.py
```

You should see the ADK UI open in your browser at `http://localhost:8000` where you can chat with the agent.

**Alternatively, run in terminal mode:**

```bash
adk run --no-ui agent.py
```

---

## Environment Configuration Reference

The following environment variables are used across demos. Set those relevant to the demos you want to run.

| Variable | Required | Description | Used by |
|----------|----------|-------------|---------|
| `GOOGLE_API_KEY` | ✅ Yes | Gemini API key | All demos |
| `OPENAI_API_KEY` | Optional | OpenAI GPT-4 key | Demo 03, 05 |
| `ANTHROPIC_API_KEY` | Optional | Anthropic Claude key | Demo 03 |
| `CHROMA_PERSIST_DIR` | Optional | ChromaDB storage path | Demo 02 |
| `SERPAPI_KEY` | Optional | Web search via SerpAPI | Demo 03, 05 |
| `MAX_ITERATIONS` | Optional | ReAct loop limit (default: 10) | All demos |
| `LOG_LEVEL` | Optional | Logging verbosity (`DEBUG`, `INFO`) | All demos |

---

## Demo-Specific Setup

Quick links to each demo's own setup instructions:

| Demo | Setup Guide |
|------|------------|
| 01 — Multi-Agent Orchestration | [demos/01-multi-agent-orchestration/README.md](../demos/01-multi-agent-orchestration/README.md) |
| 02 — RAG Agent | [demos/02-rag-agent/README.md](../demos/02-rag-agent/README.md) |
| 03 — Tool-Using Agent | [demos/03-tool-using-agent/README.md](../demos/03-tool-using-agent/README.md) |
| 04 — Conversational Agent | [demos/04-conversational-agent/README.md](../demos/04-conversational-agent/README.md) |
| 05 — Autonomous Research Agent | [demos/05-autonomous-research-agent/README.md](../demos/05-autonomous-research-agent/README.md) |

---

## Troubleshooting

### `adk: command not found`

The ADK CLI isn't on your `PATH`. Try:

```bash
pip install google-adk --upgrade
# Then restart your terminal, or run:
python -m adk --version
```

### `GOOGLE_API_KEY not set` error

Ensure you've exported the variable in your current shell session, or that your `.env` file is present and correctly formatted. ADK loads `.env` automatically if [python-dotenv](https://pypi.org/project/python-dotenv/) is installed:

```bash
pip install python-dotenv
```


### `ModuleNotFoundError`

Install the demo's dependencies first:

```bash
pip install -r requirements.txt
```

### Rate limit / quota errors

Gemini's free tier has per-minute rate limits. If you hit them, add a short `time.sleep(1)` between agent calls, or upgrade to a paid tier.

### Port 8000 already in use

Run the ADK server on a different port:

```bash
adk run --port 8080 agent.py
```

---

> 💡 **Tip:** Run `adk --help` at any time to see all available CLI commands and options.
