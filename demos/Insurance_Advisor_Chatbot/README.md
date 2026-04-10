# Insurance Advisor Chatbot

A professional, premium AI insurance advisor platform with a React frontend and a Python backend powered by Google's ADK (Agent Development Kit).

## Architecture

The project is organized into the following modular components:

*   **`frontend/`**: A React/Vite application providing a luxury chat interface with dynamic loading states and form-based data collection.
*   **`agent/`**: The core Python agent logic using ADK. It acts as an orchestrator and delegates tasks to specialized MCP servers.
*   **`tools/`**: Model Context Protocol (MCP) servers that provide specialized knowledge and capabilities (Claims, Compliance, Policy, Risk, Knowledge RAG).
*   **`deployment/`**: Configuration files and scripts for deploying to Google Cloud Run.
*   **`data/`**: Data files used by the project.

## Design Principles

*   **Luxury Aesthetics**: Curated color palette, smooth transitions, and modern typography (Playfair Display and Inter).
*   **Structured Data Collection**: Uses special `[FORM: ...]` tags to prompt the frontend to render native input fields, ensuring clean data collection.
*   **Concise & Professional Tone**: The agent is trained to be direct, professional, and avoid unnecessary fluff.

## How to Build and Run

### Prerequisites

*   Node.js (v20 or higher)
*   Python (v3.11 or higher)
*   Google Cloud SDK (gcloud)
*   Docker (optional, for local container builds)

### Backend Setup

1.  Navigate to the `agent` directory:
    ```bash
    cd agent
    ```
2.  Install dependencies (using `uv` or `pip`):
    ```bash
    uv sync
    ```
3.  Set up environment variables in a `.env` file (copy from `.env.example` in root).
4.  Run the agent locally:
    ```bash
    adk web .
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
3.  Update the API URL in `src/App.jsx` or use an environment variable if configured.
4.  Run the development server:
    ```bash
    npm run dev
    ```

### Deployment to Cloud Run

Refer to the `deployment/` directory and the `Makefile` in the original repository for deployment commands.
Typically:
```bash
make deploy
```
(Note: You may need to update the project ID and region in the Makefile).
