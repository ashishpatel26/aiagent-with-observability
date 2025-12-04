# AI Agent with Observability

[![Python Version](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://python.org) [![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT) [![LangGraph](https://img.shields.io/badge/LangGraph-1.0+-orange.svg)](https://langchain-ai.github.io/langgraph/) [![LangChain](https://img.shields.io/badge/LangChain-0.1+-red.svg)](https://python.langchain.com/) [![CrewAI](https://img.shields.io/badge/CrewAI-1.6+-purple.svg)](https://www.crewai.com/)

A comprehensive AI agent implementation using **LangGraph, CrewAI, OpenRouter, and Langfuse** for intelligent conversations and observability.

[Quick Start](#setup) • [Features](#features) • [Installation](#installation) • [Usage](#usage) • [Documentation](#architecture)

</div>

## Features

- **LangGraph Chatbot**: Interactive conversational AI using LangGraph state management
- **CrewAI Agent**: Task-oriented AI agent for complex operations
- **OpenRouter Integration**: Access to multiple LLM providers through OpenRouter API
- **Langfuse Observability**: Full tracing and monitoring of AI interactions
- **Local Langfuse**: Self-hosted observability platform

### Key Capabilities

- Intelligent conversational AI with context awareness
- Persistent conversation states using LangGraph
- Multi-agent collaboration systems
- End-to-end observability and monitoring
- Easy integration with Docker and modern Python tooling
- High-performance AI processing

## Setup

### Prerequisites

- Python 3.12 or higher
- uv package manager
- Docker (for Langfuse)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/ashishpatel26/aiagent-with-observability.git
   cd aiagent-with-observability
   ```
2. Install dependencies:

   ```bash
   uv sync
   ```
3. Set up environment variables:

   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```
4. Install and start Langfuse locally:

   **Option 1: Using the included Langfuse setup**

   ```bash
   cd langfuse
   docker-compose up -d
   ```

   **Option 2: Full installation from scratch**

   a. Install Docker and Docker Compose on your system.

   b. Clone the Langfuse repository:

   ```bash
   git clone https://github.com/langfuse/langfuse.git
   cd langfuse
   ```

   c. Create environment file:

   ```bash
   cp .env.example .env
   # Edit .env with your configuration (database URLs, etc.)
   ```

   d. Start the services:

   ```bash
   docker-compose up -d
   ```

   e. Wait for services to be ready (check logs with `docker-compose logs`).

   f. Access Langfuse at http://localhost:3000

   g. Create an account and note down the API keys from the dashboard.

### Installation Sequence

```mermaid
sequenceDiagram
   participant User
   participant Git
   participant uv
   participant Docker
   participant Langfuse

   User->>Git: git clone https://github.com/ashishpatel26/aiagent-with-observability.git
   User->>uv: uv sync
   User->>User: cp .env.example .env
   User->>User: Edit .env with API keys
   User->>Docker: docker-compose up -d (in langfuse/)
   Docker->>Langfuse: Start Langfuse services
   Langfuse->>User: Langfuse ready at localhost:3000
   User->>Langfuse: Create account & get API keys
   User->>User: Update .env with Langfuse keys
```

**Expected Output:**

- `uv sync` should complete without errors, installing all dependencies
- Docker containers should start successfully
- Langfuse dashboard accessible at http://localhost:3000

### 🔑 Langfuse API Key Setup

After starting Langfuse, you need to generate API keys for observability integration:

1. **Access Langfuse Dashboard**
   ```bash
   # Open your browser and go to:
   http://localhost:3000
   ```

2. **Create an Account**
   - Click "Sign Up" or "Create Account"
   - Fill in your details (email, password)
   - Verify your email if required

3. **Generate API Keys**
   - Go to **Settings** → **API Keys** (or **Project Settings**)
   - Click **"Create new API key"** or **"Generate Keys"**
   - You'll see two keys:
     - **Public Key** (starts with `pk-`)
     - **Secret Key** (starts with `sk-`)

4. **Configure Environment Variables**
   ```bash
   # Edit your .env file with the generated keys:
   LANGFUSE_PUBLIC_KEY=pk-your-public-key-here
   LANGFUSE_SECRET_KEY=sk-your-secret-key-here
   LANGFUSE_BASE_URL=http://localhost:3000
   ```

5. **Verify Configuration**
   ```bash
   # Test that keys work by running the agent:
   uv run scripts/run_agent.py
   ```

**🔒 Security Notes:**
- Keep your `SECRET_KEY` secure and never commit it to version control
- The `PUBLIC_KEY` is safe to share in client-side code
- Use different keys for development/production environments

## Usage

### Interactive Chatbot

Run the LangGraph-based chatbot:

```bash
uv run scripts/run_chatbot.py
```

**Expected Output:**

```bash
2024-01-01 12:00:00,000 - aiagent.core.chatbot - INFO - Starting AI agent chatbot
Chat with the AI agent! Type 'exit' or 'quit' to end.
You: Hello, how are you?
2024-01-01 12:00:01,000 - aiagent.core.chatbot - INFO - Processing user message: Hello, how are you?...
AI: Hello! I'm doing well, thank you for asking. How can I help you today?
You: exit
2024-01-01 12:00:02,000 - aiagent.core.chatbot - INFO - User ended the chat session
Goodbye!
```

This starts an interactive chat session where you can converse with the AI agent. All interactions are traced in Langfuse.

### Task-Oriented Agent

Run the CrewAI-based agent:

```bash
uv run scripts/run_agent.py
```

**Expected Output:**

```bash
LiteLLM completion() model= z-ai/glm-4.5-air:free; provider = openrouter
14:46:20 - LiteLLM:INFO: utils.py:1308 - Wrapper: Completed Call, calling success_handler
2025-12-04 14:46:20,021 - LiteLLM - INFO - Wrapper: Completed Call, calling success_handler
Agent Result: Langfuse is like a special dashboard or notebook that helps developers keep track of their AI applications. When developers build applications that use AI (like chatbots, content generators, or recommendation systems), Langfuse helps them see what's happening "under the hood."

Think of it like a flight recorder for airplanes - it records everything that happens when the AI is working:
- What questions users are asking
- What information the AI is looking at
- What decisions the AI is making
- What answers the AI is giving back

This helps developers when something goes wrong. If an AI gives a strange or incorrect answer, developers can look at Langfuse to see exactly what happened and fix the problem. It's also useful for improving the AI over time by seeing what kinds of questions it handles well and where it struggles.

Langfuse is particularly helpful for teams building complex AI systems because it provides a centralized place to monitor and understand how their AI is performing across many different situations.
2025-12-04 14:46:20,038 - aiagent.core.agent - INFO - Task completed successfully
Task: ╭───────────────────────────────────────────────────────────── Trace Batch Finalization ─────────────────────────────────────────────────────────────╮
│ ✅ Trace batch finalized with session ID: a2ce2f20-70dd-4300-a6c1-c3fb97bf6413                                                                     │
│                                                                                                                                                    │
│ 🔗 View here: https://app.crewai.com/crewai_plus/ephemeral_trace_batches/a2ce2f20-70dd-4300-a6c1-c3fb97bf6413?access_code=TRACE-9e144713e1         │
│ 🔑 Access Code: TRACE-9e144713e1                                                                                                                   │
```

*See [assets/agent_output_example.txt](assets/agent_output_example.txt) for the complete output.*

This executes a predefined task using the CrewAI framework with full observability enabled. The agent automatically synchronizes with CrewAI Plus for trace batch management, providing detailed execution insights and performance monitoring.

## 📸 Screenshots & Observability Demos

### 🔍 Langfuse Observability Dashboard

<div align="center">
<img src="assets/langfuse_observability_trace.jpg" alt="Langfuse Observability Trace" width="800">
<p><em>Langfuse dashboard showing comprehensive AI agent observability traces</em></p>
</div>

### 🤖 CrewAI Agent Execution Flow

<div align="center">

#### 1. Agent Input Processing
<img src="assets/1_CrewAI_Input.jpg" alt="CrewAI Input Processing" width="800">
<p><em>CrewAI agent receiving and processing input tasks</em></p>

#### 2. LLM Call & Response
<img src="assets/2_CrewAI_LLM_Call_Response.jpg" alt="CrewAI LLM Response" width="800">
<p><em>CrewAI orchestrating LLM calls and processing responses</em></p>

#### 3. Final Agent Response
<img src="assets/3_Agent_Response.jpg" alt="CrewAI Final Response" width="800">
<p><em>Complete agent execution with final results and trace finalization</em></p>

</div>

### 📊 Key Observability Features Demonstrated

- **🔄 Real-time Tracing**: Live monitoring of agent interactions
- **🧠 LLM Call Tracking**: Detailed view of language model interactions
- **📈 Performance Metrics**: Response times and execution analytics
- **🔗 Trace Linking**: Connected workflows across multiple agents
- **📋 Session Management**: Organized trace batches with access codes

## Configuration

### Environment Variables

|        Variable        |      Description      |            Required            |
| :---------------------: | :--------------------: | :-----------------------------: |
| `LANGFUSE_SECRET_KEY` |  Langfuse secret key  |               Yes               |
| `LANGFUSE_PUBLIC_KEY` |  Langfuse public key  |               Yes               |
|  `LANGFUSE_BASE_URL`  |  Langfuse server URL  | No (defaults to localhost:3000) |
| `OPENROUTER_API_KEY` |   OpenRouter API key   |               Yes               |
|    `YOUR_SITE_URL`    | Site URL for rankings |            Optional            |
|   `YOUR_SITE_NAME`   | Site name for rankings |            Optional            |

### CrewAI Plus Integration

The agent integrates with **CrewAI Plus** for enhanced observability and trace management. When running agents, you'll see trace batch finalization with session IDs and access codes.

**Features:**
- **Trace Batch Management**: Automatic session tracking and finalization
- **Access Codes**: Secure links to view detailed execution traces
- **Multi-Agent Coordination**: Synchronized agent collaboration with full observability

**Trace Access:**
- Use the provided access code to view detailed execution traces
- Traces include agent interactions, decision-making processes, and performance metrics
- Access via: `https://app.crewai.com/crewai_plus/ephemeral_trace_batches/{session_id}?access_code={code}`

### Langfuse Dashboard

Access the Langfuse dashboard at http://localhost:3000 to view traces, metrics, and analytics of your AI agent interactions.

## Architecture

```mermaid
graph TB
     A[scripts/run_chatbot.py] --> B[aiagent.core.chatbot.run_chatbot]
     C[scripts/run_agent.py] --> D[aiagent.core.agent.run_crew_agent]

     B --> E[aiagent.core.chatbot.create_chatbot_graph]
     D --> F[aiagent.core.agent.create_crew_agent]

     E --> G[LangGraph StateGraph]
     F --> H[CrewAI Agent & Task]

     G --> I[ChatOpenAI LLM]
     H --> I

     I --> J[OpenRouter API]
     J --> K[Various LLM Models]

     B --> L[Langfuse CallbackHandler]
     D --> M[CrewAIInstrumentor]

     L --> N[Langfuse Tracing]
     M --> O[CrewAI Plus Sync]

     O --> P[Trace Batch Management]
     P --> Q[Session IDs & Access Codes]

     N --> R[Langfuse Dashboard]
     Q --> R

     S[aiagent.config.settings] --> T[Environment Variables]
     T --> U[.env File]

     G --> V[User Input/Output]
     H --> W[Task Results]

     R --> X[Unified Observability]
     X --> Y[Traces & Analytics]
```

### Components

- **Scripts**: Entry points for running chatbot and agent
- **Core Modules**: Main business logic for AI interactions
- **Configuration**: Settings management via Pydantic
- **External Services**: OpenRouter for LLMs, Langfuse for observability
- **Data Flow**: User input → Processing → LLM → Response → Tracing

## Development

### Code Structure

```
aiagent-with-observability/
├── aiagent/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── chatbot.py          # LangGraph chatbot implementation
│   │   └── agent.py            # CrewAI agent implementation
│   └── config/
│       ├── __init__.py
│       └── settings.py         # Configuration management
├── scripts/
│   ├── run_chatbot.py          # Chatbot runner script
│   └── run_agent.py            # Agent runner script
├── tests/                      # Test directory
├── docs/                       # Documentation
├── .env                        # Environment configuration
├── .gitignore                  # Git ignore rules
├── pyproject.toml              # Project dependencies
├── README.md                   # This file
└── main.py                     # Legacy CrewAI implementation
```

### Adding New Features

1. Implement new agent logic in respective files
2. Ensure proper error handling and logging
3. Update environment variables as needed
4. Test with Langfuse tracing enabled

## Contributing

1. Follow the existing code style and structure
2. Add comprehensive docstrings
3. Ensure all interactions are properly traced
4. Test thoroughly with different scenarios

## License

MIT License - See LICENSE file for details.
