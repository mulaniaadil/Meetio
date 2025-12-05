🌟 Meetio: The RAG-Enhanced AI Tooling Agent

Repository Tag: murf-ai

[Image: Meetio AI Logo]

A Real-Time Conversational Agent Powered by Murf Falcon, Groq, and LiveKit for Tool-Use Orchestration.

📌 Project Overview

Meetio is a sophisticated AI voice agent built on the LiveKit Agents framework. It is designed to act as a real-time productivity assistant capable of performing complex, data-driven tasks via voice command. Meetio integrates high-speed ASR, ultra-low-latency TTS, and advanced LLM function-calling capabilities.

The primary innovation is the seamless integration of external knowledge sources: Supabase for internal data querying and Firecrawl for real-time web searches, effectively demonstrating a RAG-like capability to retrieve precise information and execute functions instantly.

💻 Workflow

The agent operates on a robust, real-time pipeline to ensure fluid conversation and immediate action.

[Image: Meetio: Real-Time Conversational AI Workflow Diagram]

✨ Core Features

Real-Time Voice (TTS): Utilizes the Murf Falcon TTS API (via livekit-plugins-murf) to deliver spoken responses with industry-leading low latency, ensuring a fluid, natural conversation flow.

ASR & VAD: Integrates Deepgram/AssemblyAI for accurate Speech-to-Text (stt) and Silero for reliable Voice Activity Detection (vad) to handle conversational turn-taking effectively.

Intelligent Tool Orchestration: Leverages the LLM (Groq/OpenAI) to automatically decide which tool to use based on the user's intent.

Supabase MCP: Queries and manages data in a connected Supabase database.

Firecrawl: Performs live web searches and crawls external URLs to gather fresh, external information.

Modular Architecture: Built using the best-of-breed LiveKit plugins, demonstrating a scalable, production-ready voice pipeline.

⚙️ Tech Stack & Dependencies

Meetio is a Python application requiring several key libraries and plugins for its real-time functionality.

Component

Technology

Role

TTS (Vocalization)

Murf Falcon (livekit-plugins-murf)

Ultra-low latency voice output.

LLM (Reasoning)

Groq/OpenAI (livekit-plugins-groq, openai)

Function calling, complex reasoning, and response generation.

STT (Transcription)

Deepgram/AssemblyAI

Accurate Speech-to-Text conversion.

Tooling/Data (RAG)

Supabase MCP, Firecrawl

Database query and real-time web retrieval.

Framework

LiveKit Agents

Orchestration, room connection, and real-time audio pipeline.

The full list of dependencies is located in requirements.txt:

livekit-agents
livekit-plugins-assemblyai
livekit-plugins-groq
livekit-plugins-deepgram 
livekit-plugins-murf
livekit-plugins-silero
python-dotenv
pydantic-ai-slim[openai,mcp]
firecrawl


🚀 Setup and Configuration

1. Prerequisites

Python 3.9+ installed.

API keys for LiveKit, Murf AI, Deepgram/AssemblyAI, Groq/OpenAI, Supabase, and Firecrawl.

2. Installation

Navigate to the project root and install the dependencies:

pip install -r requirements.txt


3. Environment Variables

Create a file named .env in the root directory and populate it with your API keys. Meetio uses these environment variables for secure credential management:

# LiveKit Agent Configuration
LIVEKIT_URL="wss://<your-livekit-server-url>"
LIVEKIT_API_KEY="AP... "
LIVEKIT_API_SECRET="Xr..."

# Core AI Service Keys
MURF_API_KEY="ap2_..."             # Murf Falcon TTS
DEEPGRAM_API_KEY="dg_..."          # Deepgram or AssemblyAI for STT
GROQ_API_KEY="gsk_..."             # Groq LLM for speed

# Tooling Keys
SUPABASE_ACCESS_TOKEN="sbp_..."    # For Supabase MCP tool access
FIRECRAWL_API_KEY="fc_..."         # For real-time web searching


4. Running the Agent

You can run the agent locally using the LiveKit CLI (if installed) or directly with Python for basic testing:

To run the core agent:

python myagent.py
# This runs the simple conversational agent using Murf, Groq, and Deepgram.


To run the advanced tool-use agent:

python agent.py
# This runs the agent with Supabase and Firecrawl tool integration.


🏆 Hackathon Notes

Integrates Murf Falcon: Successfully demonstrates the required use of the Murf Falcon TTS API for conversational, low-latency voice responses.

Conversational AI: Provides a full-duplex conversational experience, integrating ASR, LLM, and TTS.

Secure API Handling: Utilizes python-dotenv for secure management of all required API keys.
