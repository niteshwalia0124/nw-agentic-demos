# 🏗️ Architecture

This document describes the system-level architecture of the NW Agentic Demos repository, including component design, data flow, and the reasoning behind key design decisions.

---

## Table of Contents

- [Repository Philosophy](#repository-philosophy)
- [Shared Infrastructure](#shared-infrastructure)
- [Agent Taxonomy](#agent-taxonomy)
- [Component Diagrams](#component-diagrams)
  - [Core Agent Loop](#core-agent-loop)
  - [Multi-Agent Communication](#multi-agent-communication)
  - [RAG Pipeline](#rag-pipeline)
  - [Tool Execution Flow](#tool-execution-flow)
  - [Autonomous Research Pipeline](#autonomous-research-pipeline)
- [Data Flow](#data-flow)
- [LLM Provider Abstraction](#llm-provider-abstraction)
- [Memory & State Management](#memory--state-management)
- [Security Considerations](#security-considerations)

---

## Repository Philosophy

Each demo in this repository is designed around three core properties:

1. **Isolation** — Every demo is a standalone project with its own virtual environment, dependencies, and entry point. You can understand and run any demo without reading the others.
2. **Transparency** — Agents log every reasoning step, tool call, and intermediate result so you can follow the agent's "thought process" from input to output.
3. **Composability** — The patterns demonstrated can be combined. The multi-agent orchestration demo, for example, internally uses the RAG agent and the tool-using agent as specialist sub-agents.

---

## Shared Infrastructure

Although demos are self-contained, they share a conceptual infrastructure that maps to this ADK-based stack:

```
┌─────────────────────────────────────────────────────────────────────┐
│                        Shared Concepts                              │
│                                                                     │
│  ┌───────────────┐  ┌───────────────┐  ┌────────────────────────┐  │
│  │  LLM Provider │  │  Tool Library │  │  Session / Memory Mgr  │  │
│  │  Abstraction  │  │  (ADK Built-  │  │  (In-memory + optional │  │
│  │  (swap easily)│  │   in + custom)│  │   persistent store)    │  │
│  └───────────────┘  └───────────────┘  └────────────────────────┘  │
│                                                                     │
│  ┌───────────────┐  ┌───────────────┐  ┌────────────────────────┐  │
│  │  Logging &    │  │  .env Config  │  │  Evaluation Harness    │  │
│  │  Tracing      │  │  Management   │  │  (ADK evals)           │  │
│  └───────────────┘  └───────────────┘  └────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Agent Taxonomy

```mermaid
graph TD
    A["Agent Types in this Repo"]

    A --> B["Single Agents"]
    A --> C["Multi-Agent Systems"]

    B --> B1["Conversational Agent\n(Demo 04)"]
    B --> B2["Tool-Using Agent\n(Demo 03)"]
    B --> B3["RAG Agent\n(Demo 02)"]

    C --> C1["Hierarchical\n(Orchestrator + Specialists)\nDemo 01"]
    C --> C2["Sequential Pipeline\n(Plan → Search → Write)\nDemo 05"]

    style A fill:#fef3c7,stroke:#f59e0b
    style B fill:#dbeafe,stroke:#3b82f6
    style C fill:#d1fae5,stroke:#10b981
```

---

## Component Diagrams

### Core Agent Loop

All agents in this repo follow the standard ReAct (Reasoning + Acting) loop:

```mermaid
sequenceDiagram
    participant U as User
    participant A as Agent
    participant L as LLM
    participant T as Tools

    U->>A: Input / Query
    loop ReAct Loop
        A->>L: Prompt (system + history + query)
        L-->>A: Thought + Action
        alt Action = tool call
            A->>T: Execute tool
            T-->>A: Tool result (Observation)
            A->>L: Append observation, continue
        else Action = final answer
            A-->>U: Final Response
        end
    end
```

---

### Multi-Agent Communication

Demo 01 uses a **hub-and-spoke** topology where the orchestrator delegates to specialist agents:

```mermaid
sequenceDiagram
    participant U as User
    participant O as Orchestrator
    participant R as Research Agent
    participant C as Code Agent
    participant W as Writer Agent

    U->>O: Complex task
    O->>O: Break task into sub-tasks
    O->>R: Sub-task: research topic X
    R-->>O: Research findings
    O->>C: Sub-task: generate code for Y
    C-->>O: Code snippet
    O->>W: Sub-task: write summary using findings + code
    W-->>O: Draft report
    O->>O: Aggregate & review
    O-->>U: Final result
```

---

### RAG Pipeline

Demo 02 follows a standard RAG architecture with an ingest phase and a query phase:

```mermaid
flowchart LR
    subgraph Ingest["📥 Ingest Phase (one-time)"]
        Docs["📄 Source Documents\n(PDF, HTML, TXT)"]
        Chunk["✂️ Chunker"]
        Embed["🔢 Embedder\n(text-embedding-004)"]
        Store["🗄️ Vector Store\n(ChromaDB)"]
        Docs --> Chunk --> Embed --> Store
    end

    subgraph Query["🔍 Query Phase (per request)"]
        Q["❓ User Query"]
        QEmbed["🔢 Query Embedder"]
        Retrieve["🔎 Semantic Retrieval\n(top-k chunks)"]
        Context["📋 Context Builder"]
        LLM["🤖 LLM\n(Gemini / GPT-4)"]
        Ans["✅ Grounded Answer\n+ Citations"]

        Q --> QEmbed --> Retrieve --> Context --> LLM --> Ans
        Store -.->|"retrieve top-k"| Retrieve
    end

    style Ingest fill:#dbeafe,stroke:#3b82f6
    style Query fill:#d1fae5,stroke:#10b981
```

---

### Tool Execution Flow

Demo 03 demonstrates how the agent selects and executes tools safely:

```mermaid
flowchart TD
    Input["User Input"]
    Planner["🧠 LLM Planner\n(select tool & args)"]
    Validator["🛡️ Arg Validator"]
    Executor["⚙️ Tool Executor"]
    Result["📤 Tool Result"]
    NextStep{"More steps?"}
    FinalAnswer["✅ Final Answer"]
    Error["⚠️ Error Handler\n(retry / fallback)"]

    Input --> Planner
    Planner --> Validator
    Validator -->|"valid"| Executor
    Validator -->|"invalid"| Error
    Executor -->|"success"| Result
    Executor -->|"failure"| Error
    Error -->|"retry"| Planner
    Result --> NextStep
    NextStep -->|"yes"| Planner
    NextStep -->|"no"| FinalAnswer

    style Error fill:#fee2e2,stroke:#ef4444
    style FinalAnswer fill:#d1fae5,stroke:#10b981
```

---

### Autonomous Research Pipeline

Demo 05 is the most complex — a fully autonomous multi-stage pipeline:

```mermaid
flowchart TD
    Q["❓ Research Question"]

    subgraph Plan["Stage 1: Planning"]
        Planner["🧠 Planner Agent\nDecompose into sub-queries"]
    end

    subgraph Search["Stage 2: Retrieval"]
        Web["🌐 Web Search\n(per sub-query)"]
        Scrape["📄 Content Scraper"]
        Rank["📊 Relevance Ranker"]
    end

    subgraph Synthesize["Stage 3: Synthesis"]
        Extract["🔍 Key Fact Extractor"]
        Draft["✍️ Report Drafter"]
        Review["🔎 Self-Review Agent\n(fact-check + gaps)"]
    end

    subgraph Output["Stage 4: Output"]
        Report["📑 Structured Markdown Report\n(with citations)"]
    end

    Q --> Planner
    Planner -->|"sub-queries"| Web
    Web --> Scrape --> Rank --> Extract
    Extract --> Draft --> Review
    Review -->|"revision needed"| Draft
    Review -->|"approved"| Report

    style Plan fill:#dbeafe,stroke:#3b82f6
    style Search fill:#fef3c7,stroke:#f59e0b
    style Synthesize fill:#ede9fe,stroke:#8b5cf6
    style Output fill:#d1fae5,stroke:#10b981
```

---

## Data Flow

```mermaid
flowchart LR
    User("👤 User")
    Session("🗂️ Session Store\n(context window)")
    Agent("🤖 Agent")
    Memory("🧠 Long-term Memory\n(vector store)")
    Tools("🛠️ Tools")
    LLM("💬 LLM")

    User -->|"message"| Session
    Session -->|"history + message"| Agent
    Agent -->|"relevant memories"| Memory
    Memory -->|"retrieved context"| Agent
    Agent -->|"prompt"| LLM
    LLM -->|"thought + action"| Agent
    Agent -->|"tool call"| Tools
    Tools -->|"observation"| Agent
    Agent -->|"response"| Session
    Session -->|"response"| User

    style User fill:#fef3c7,stroke:#f59e0b
    style LLM fill:#fee2e2,stroke:#ef4444
    style Memory fill:#ede9fe,stroke:#8b5cf6
```

---

## LLM Provider Abstraction

All demos use ADK's model abstraction, allowing you to swap providers by changing a single config value:

```python
# Gemini (default)
agent = Agent(model="gemini-2.5-flash")

# OpenAI
agent = Agent(model="openai/gpt-4o")

# Anthropic
agent = Agent(model="anthropic/claude-3-5-sonnet")
```

The abstraction layer normalizes:
- Message formatting (system, user, assistant roles)
- Tool/function calling schemas
- Streaming response handling
- Token counting & context window management

---

## Memory & State Management

```
┌─────────────────────────────────────────────────────────┐
│                   Memory Hierarchy                      │
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │  In-Context Memory (shortest-lived)             │   │
│  │  Current conversation turns in the prompt       │   │
│  └─────────────────────────────────────────────────┘   │
│                          ▼                              │
│  ┌─────────────────────────────────────────────────┐   │
│  │  Session Memory (session-scoped)                │   │
│  │  ADK session store — persists across turns      │   │
│  └─────────────────────────────────────────────────┘   │
│                          ▼                              │
│  ┌─────────────────────────────────────────────────┐   │
│  │  Long-term Memory (persistent)                  │   │
│  │  Vector DB — semantic retrieval across sessions │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

---

## Security Considerations

| Concern | Mitigation |
|---------|-----------|
| Prompt injection | Input sanitisation + system prompt hardening |
| Tool misuse | Argument validation before every tool call |
| Code execution | Sandboxed executor (Docker / restricted subprocess) |
| API key exposure | Keys loaded from `.env` only, never hardcoded |
| Excessive LLM calls | Max iteration limits on all ReAct loops |
| Data leakage | No PII stored in vector DBs in demos |

---

> 📌 For implementation details, read the README in each demo directory.
