# 🛡️ Demo Insurance AI Assistant Chatbot

A premium, enterprise-grade multi-agent AI insurance advisory platform built using **Google's Agent Development Kit (ADK)**. It orchestrates multiple specialist sub-agents via the **Google Cloud Agent Platform (Agent Runtime)** and accesses real-time data tools using custom **Model Context Protocol (MCP)** servers over the **Agent Registry**.

---

## 📊 Architecture

The Insurance Advisor leverages a decoupled, modular architecture where the core **Orchestration Agent** manages user conversations and delegates specialized tasks to specific **Specialist Agents** using the Agent Gateway.

```text
┌────────────────────────────────────────────────────────┐
│        AGENT PLATFORM / AGENT RUNTIME (VERTEX AI)      │
│                                                        │
│                ┌─────────────────────┐                 │
│                │ Orchestration Agent │                 │
│                └──────────┬──────────┘                 │
│       ┌───────────────────┼───────────────────┐        │
│       ▼                   ▼                   ▼        │
│┌────────────┐      ┌─────────────┐     ┌──────────────┐│
││Policy Agent│      │Claims Agent │     │ Risk Agent   ││
│└──────┬─────┘      └──────┬──────┘     └──────┬───────┘│
└───────┼───────────────────┼───────────────────┼────────┘
        │ (Agent Registry)  │                   │
        ▼                   ▼                   ▼
┌──────────────┐     ┌──────────────┐    ┌───────────────┐
│ Customer/RAG │     │ Claims MCP   │    │ Risk & Premium│
│ MCP Service  │     │ Service      │    │ MCP Service   │
└──────┬───────┘     └──────┬───────┘    └──────┬────────┘
       ▼                    ▼                   ▼
┌──────────────┐     ┌──────────────┐    ┌───────────────┐
│  Firestore   │     │  Cloud SQL   │    │   BigQuery    │
└──────────────┘     └──────────────┘    └───────────────┘
```

---

## 🚀 Key Features

* **Intelligent Orchestration**: The root orchestrator seamlessly evaluates user queries and routes them to specific specialists without exposing internal tool mechanics to the user.
* **Zero-Friction Form Collection**: Detects when the user has already provided details (e.g., Name, City, Vehicle) and skips conversational form collection to provide proactive quote tables upfront.
* **Zero-Step Product Comparisons & Cross-selling**: Proactively flags expired plans, calculates exact renewal premiums, and identifies coverage gaps (e.g., missing Life or Health plans) in a single Unified Dashboard table.
* **Empathetic Claim Handling**: Proactively surfaces estimated processing timelines and required next steps for all active claims.

---

## 🛠️ Google Cloud Infrastructure

The platform runs entirely serverless on Google Cloud using the following services:

1. **Agent Runtime (Vertex AI Reasoning Engine)**: Hosts the Python-based ADK root orchestrator and specialist subagents.
2. **Agent Registry**: Governs, tests, and shares the MCP Toolsets natively across the Agent Runtime.
3. **Cloud Run**: Hosts the 5 custom microservices implementing the **Model Context Protocol (MCP)**.
4. **Cloud Firestore**: Stores customer profiles, tiers, and active policy catalogs.
5. **Cloud SQL (PostgreSQL)**: Manages the transaction history, status tracking, and processing logs for all claims.
6. **BigQuery**: Performs regulatory compliance checks against per-state rules, rate-increase caps, and federal guidelines.

---

## 💻 Setup & Deployment

### 1. Prerequisites
* Python 3.11 or Python 3.12
* [uv](https://docs.astral.sh/uv/getting-started/installation/) installed for dependency management
* Google Cloud CLI (`gcloud`) authenticated to your GCP project

### 2. Setup Environment
Create an active environment file in the `agent/` directory using the provided template:
```bash
cd agent
cp .env.example .env
```

Update your **`GOOGLE_API_KEY`** and the registered **`mcpServers` resource names** inside the agent files to match your Google Cloud Console deployment.

---

## 📦 How to Deploy

### Step 1: Register the MCP Servers to the Agent Registry
For each of the 5 custom MCP servers (Claims, Compliance, Customer Policy, Knowledge RAG, Risk), deploy the server to **Cloud Run** and add its tools metadata to the **Agent Registry**. 

The expected tool specifications can be generated via the scripts provided in the `tools/` folder and wrapped inside a `tools` field:

```json
{
  "tools": [
    {
      "name": "example_tool",
      "description": "Detailed tool description here",
      "inputSchema": { ... }
    }
  ]
}
```

### Step 2: Deploy the Agent to Agent Runtime
Use the new unified **`agents-cli`** to build, package, and host your agent on the platform:

```bash
# Install the unified CLI
uv tool install google-agents-cli

# Deploy the agent
uv run agents-cli deploy \
  --deployment-target agent_runtime \
  --project YOUR_PROJECT_ID \
  --region us-central1
```

### Step 3: Test Interactively
Once deployed, open the live **Agent Playground** in the Google Cloud Console:
```bash
agents-cli deploy --status
```
The CLI will return the direct link to test the live agent in the Google Cloud Console!
