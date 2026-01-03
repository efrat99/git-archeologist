# 🏛️ Semantic Git Archaeologist (MCP Server)

> **Grant your AI agents "Historical Memory" and Intent Recognition.**

**Semantic Git Archaeologist** is a specialized Model Context Protocol (MCP) server that enables LLMs to analyze not just *what* code changed, but *why*. By combining `GitPython` with the reasoning capabilities of **Gemini 2.5 Flash**, it maps code risks, explains legacy decisions, and detects bug patterns rooted in history.

---

## 📉 The Problem
Standard AI coding agents operate in the "now." They see the current state of the code but lack context. Tools like `git blame` tell you *who* changed a line, but they don't explain:
* **Why** a weird logic fix was introduced 3 years ago.
* **Where** the architectural hotspots and fragile files are.
* **How** functionality has evolved over time.

## ✨ The Solution
This tool bridges the gap between raw Git history and semantic reasoning. It acts as an **archaeologist**, digging through commit diffs to surface:
1.  **Semantic Analysis:** The "Intent" behind changes.
2.  **Bug Detective:** Patterns of past fixes to prevent regressions.
3.  **Risk Mapping:** Identification of high-churn, fragile modules.

---

## 🏗️ Architecture

This project exposes Git history to LLM clients (like Cursor, Claude Desktop, or Windsurf) via the MCP protocol.

```mermaid
graph LR
    Client[🖥️ LLM Client] -->|MCP Protocol| Server[⚙️ MCP Server]
    Server -->|GitPython| Repo[(📂 Git Repository)]
    Server -->|Reasoning| Gemini[✨ Gemini 2.5 Flash]
    Gemini -.->|Semantic Insights| Server
    Server -.->|Structured Context| Client
🚀 Key Features🕵️‍♂️ Semantic Analysis: Translates complex diffs into human-readable narratives explaining the "Why".🔥 Hotspot Detection: Identifies files with high churn and mixed responsibilities.🧱 Fragility Assessment: Explains why specific files are prone to breaking (e.g., tight coupling, async complexity).🧠 Architectural Memory: Provides context that standard generic LLMs miss.🛠️ Tech StackCore: Python 3.10+Protocol: FastMCP (Model Context Protocol)Git Engine: GitPythonAI Engine: Google Gemini 2.5 Flash API📦 Available ToolsWhen connected to an MCP client, the following tools become available:Tool NameDescriptionget_recent_commitsRetrieves structured metadata for recent commits.analyze_file_evolutionTraces how a specific file's logic has changed over time.analyze_code_hotspotsIdentifies frequently changing areas and calculates risk scores.analyze_commit_semanticsGenerates a semantic explanation of a specific commit diff.📌 Example: Code Hotspot AnalysisInput (MCP Tool Call):analyze_code_hotspots("AgCloud")Output (LLM Reasoning Excerpt):"The sensor-related GUI modules exhibit high churn due to rapid feature expansion. These files combine presentation logic, domain state, and asynchronous data flows."Identified Risks:🔴 High Change Frequency: Top 5% of modified files.⚠️ Mixed Responsibilities: UI + Domain Logic coupling.🔄 Async Complexity: Race conditions detected in past fixes.⚙️ Setup & Usage1. PrerequisitesPython 3.10 or higherA Google Gemini API Key2. InstallationBash# Clone the repository
git clone [https://github.com/yourusername/semantic-git-archaeologist.git](https://github.com/yourusername/semantic-git-archaeologist.git)
cd semantic-git-archaeologist

# Install dependencies
pip install -r requirements.txt
# OR if using uv
uv pip install -r requirements.txt
3. Running the ServerSet your environment variables and start the server:Bashexport REPO_PATH=/path/to/target/repo
export GEMINI_API_KEY=your_gemini_key

# Run the MCP server
python main.py
📁 DocumentationFull analyses and detailed transcripts are available in the docs/ directory.📄 AgCloud Hotspot Analysis - A complete case study of a legacy system.📄 Prompts & Responses - Transparency logs of LLM interactions.📄 Architecture Deep Dive - Internal design decisions.🔮 Future Work[ ] Support for multiple LLM providers (OpenAI, Anthropic).[ ] Cross-repository comparative analysis.[ ] Vector-based long-term architectural memory (RAG).[ ] Direct GitHub API integration for cloud analysis.