# Insurance Advisor Voice Bot

A professional, premium Voice AI insurance advisor platform with a React frontend and a Python backend powered by Google's ADK (Agent Development Kit) and Gemini Live.

## System Architecture

The system is a real-time, bidirectional voice AI assistant. It allows users to interact with an AI insurance advisor using voice, with support for complex tool execution via Model Context Protocol (MCP) servers.

### Architecture Diagram

```mermaid
graph TD
    User((User)) <-->|Audio & Events| Frontend[React Frontend]
    
    subgraph Frontend (Browser)
        Frontend -->|16kHz PCM| Recorder[Audio Recorder]
        Player[PCM Player Worklet] -->|Audio Out| Frontend
        UI[Chat UI] -->|Loading State| Frontend
    end

    Frontend <-->|WebSocket| Backend[FastAPI Backend]

    subgraph Backend (Cloud Run)
        Backend -->|Upstream Task| Queue[LiveRequestQueue]
        Backend -->|Downstream Task| WS_Out[WebSocket Send]
        Backend -->|Keep-Alive Task| WS_Ping[WebSocket Ping]
    end

    Queue --> ADK[ADK Runner.run_live]
    ADK --> WS_Out

    subgraph Agent & Model
        ADK <-->|BIDI Stream| Model((Gemini 3.1 Flash Live))
        ADK -->|Tool Calls| MCP_Toolsets[MCP Toolsets]
    end

    subgraph Remote Tools (Cloud Run)
        MCP_Toolsets -->|HTTP POST /mcp| Claims[Claims MCP Server]
        MCP_Toolsets -->|HTTP POST /mcp| Policy[Policy MCP Server]
        MCP_Toolsets -->|HTTP POST /mcp| Risk[Risk Premium MCP Server]
        MCP_Toolsets -->|HTTP POST /mcp| RAG[Knowledge RAG MCP Server]
    end
```

### Key Components

*   **`frontend/`**: A React/Vite application handling audio recording, playback (PCM player worklet), and WebSocket communication.
*   **`agent/`**: The core Python agent logic using ADK. It acts as an orchestrator and delegates tasks to specialized MCP servers.
*   **`tools/`**: Model Context Protocol (MCP) servers that provide specialized knowledge and capabilities (Claims, Compliance, Policy, Risk, Knowledge RAG).

## Design Principles & Features

*   **Bidirectional Voice Streaming**: Real-time conversation with Gemini Live.
*   **Barge-in Support**: Users can interrupt the AI while it is speaking.
*   **Visual Feedback**: UI shows "thinking" state during slow tool executions.
*   **Filler Phrases**: AI naturally narrates actions before fetching information.
*   **Luxury Aesthetics**: Curated color palette and smooth transitions in the frontend.

## How to Build and Run

### Prerequisites

*   Node.js (v20 or higher)
*   Python (v3.11 or higher)
*   Google Cloud SDK (gcloud)

### Backend Setup

1.  Navigate to the `agent` directory:
    ```bash
    cd agent
    ```
2.  Install dependencies:
    ```bash
    uv sync
    ```
3.  Run the voice backend:
    ```bash
    make local-backend
    ```

### Frontend Setup

1.  Navigate to the `frontend` directory:
    ```bash
    cd frontend
    ```
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  Run the development server:
    ```bash
    npm run dev
    ```

### Deployment

Refer to the `Makefile` for deployment commands to Google Cloud Run.
```bash
make deploy
```
Make sure to set the correct environment variables for MCP servers (e.g., `POLICY_MCP_URL`) in the deployment command or Cloud Run configuration.
