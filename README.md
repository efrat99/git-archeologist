Project Title: Semantic Git Archaeologist (MCP Server).

The Problem: Standard AI agents lack historical context and "intent" recognition in legacy codebases.

The Solution: A specialized MCP server that grants Claude "Historical Memory" using Gemini 2.5 Flash to analyze Git diffs, find bug patterns, and map code risk.

Key Features:

Semantic Analysis: Explaining the "Why" behind changes.

Bug Detective: Mining past fixes to prevent regressions.

Risk Mapping: Identifying fragile files and hotspots.




Tech Stack: Python, FastMCP, GitPython, Gemini API.



Project Title: Semantic Git Archaeologist (MCP Server)

A semantic code archaeology tool that analyzes Git history and uses Large Language Models (LLMs) to explain how and why code evolved over time.

This project is implemented as an MCP Server, enabling LLM clients (IDEs, agents, or chat systems) to reason about real repositories using structured Git data enriched with semantic analysis.

✨ What Problem Does This Solve?

Traditional tools like git log or git blame show what changed —
but they do not explain:

Why changes were made

Which files are fragile

Where architectural risk accumulates

What areas evolve fastest and why

This project bridges that gap by combining:

Git history analysis

Semantic reasoning via LLMs

MCP-based tool exposure

🧠 Key Capabilities

Analyze commit history of a repository

Detect code hotspots (frequently changed areas)

Identify fragile files and explain why they are fragile

Produce human-readable architectural explanations

Expose all functionality via MCP tools

🏗 Architecture Overview
LLM Client (IDE / Agent / Chat)
            ↓
        MCP Server
            ↓
   Git Repository + LLM Reasoning


The MCP server:

Extracts structured Git history

Enriches it with semantic analysis using an LLM

Returns concise, explainable insights

🔧 Available MCP Tools
Tool Name	Description
get_recent_commits	Retrieves recent commit metadata
analyze_file_evolution	Explains how a file’s logic evolved
analyze_code_hotspots	Identifies frequently changing areas
analyze_commit_semantics	Produces semantic interpretation of a commit
📌 Example: Code Hotspot Analysis (AgCloud)
MCP Tool Call
analyze_code_hotspots("AgCloud")

LLM Reasoning (Excerpt)

The sensor-related GUI modules exhibit high churn due to rapid feature expansion and UI-driven changes.
These files combine presentation logic, domain state, and asynchronous data flows, making them particularly fragile.

Why These Files Are Fragile

High change frequency

Mixed responsibilities (UI + domain logic)

Asynchronous sensor data handling

Limited isolation from core services

➡️ This combination increases regression risk and maintenance cost.

🧪 Testing

The project includes automated tests validating:

MCP tool behavior

Git history extraction logic

Error handling for missing repositories

📁 Documentation

Extended analyses and full LLM transcripts are available under:

docs/
├── agcloud-hotspot-analysis.md
├── agcloud-hotspot-analysis.pdf
└── prompts-and-responses.md


These documents contain:

Full hotspot analysis

Complete LLM explanations

Prompt / response examples for transparency

🚀 Future Work

Support multiple LLM providers

Cross-repository comparative analysis

IDE integrations (VSCode / Cursor MCP)

Cloud-based repository analysis (GitHub API)

Vector-based long-term architectural memory

⚙️ Setup
export REPO_PATH=/path/to/your/repo
export GEMINI_API_KEY=your_key
python main.py

🎯 Why MCP?

MCP enables composable, inspectable AI tooling:

Tools are explicit and auditable

Reasoning is transparent

Integrates naturally with agent-based workflows

This makes the system suitable for real-world developer tooling, not just demos.