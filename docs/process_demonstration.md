<!-- # 🧠 Anatomy of an AI Investigation

This document demonstrates the **internal reasoning process** of the Semantic Git Archaeologist.  
It shows how a vague user request like _"brief me on risks"_ is transformed into a structured, evidence-based report.

---

## 🎯 The Challenge

**User Prompt:**
> "I'm about to make a change in the sensor logic. Give me a full briefing: what are the risks, what should I learn from past fixes, and what is the current logic's intent?"

---

## 🕵️‍♂️ Step 1: Agent's Thought Process

Before executing any code, the Agent (Gemini 2.5) analyzes the request and formulates a plan.

> **🤖 Internal Monologue:**
> "The user wants a **risk assessment** on a critical module ('sensor logic').  
> To answer 'what are the risks', I need historical failure patterns, not just the code."
>
> **Plan:**
> 1. Identify recent changes to understand the *current* state.
> 2. Use `detective_bug_miner` to find past fixes (commits starting with 'fix', 'bug', 'patch') in this module.
> 3. Check for files that are frequently changed together (coupling analysis).

---

## 🛠️ Step 2: Tool Execution

The Agent calls two MCP Server tools autonomously.

**Tool Call #1: Mapping the Territory**
```python
get_recent_history(limit=10, search_term="sensor")
```

**Tool Call #2: Hunting for Bugs**
```python
detective_bug_miner(topic="sensors", lookback_days=90)
```

---

## ⚡ Step 3: Raw Findings

The MCP server returns raw data. Most tools stop here, but the Archaeologist analyzes it.

<details open>
<summary><strong>🔍 Click to inspect Raw Tool Output</strong></summary>

```json
{
  "bug_patterns_found": [
    {
      "pattern": "Rushed Deployment",
      "evidence": [
        "Commit 0a6a: 'Add sensors gui' (12:58 PM)",
        "Commit 496d: 'Fix onclick syntax' (13:05 PM) - 7 minutes later"
      ]
    },
    {
      "pattern": "Incomplete Implementation",
      "evidence": "File 'sensorsMapView.py' accessed 'self.t' (undefined attribute) in production."
    },
    {
      "pattern": "Integration Instability",
      "evidence": "Multiple commits labeled 'connect GUI to db' followed by 'revert' or 'fix'."
    }
  ]
}
```
</details>

---

## 🧠 Step 4: Synthesis ("Aha!" Moment)

The Agent connects the dots between the raw logs and the user's question.

> **🤖 Agent Reasoning:**  
> - The code shows premature merging and rushed deployments.  
> - The 'onclick' error proves insufficient local testing.  
> - The `self.t` undefined attribute shows incomplete refactoring.  
>
> **Conclusion:**  
> The primary risk is **process-related**, not purely logic-related. Extra attention must be given to integration layer testing.

---

## 📄 Step 5: Final Artifact

Based on this reasoning, the Agent generates a structured briefing.

👉 **[View the Final Generated Report: Sensor Logic Briefing](artifacts/sensor_logic_briefing.md)**

*(Note how the final report explicitly warns about "Rushed Deployment" based on the timestamp evidence found in Step 3)*

> Note: The final report explicitly warns about "Rushed Deployment" with supporting timestamp evidence.

---

## ✅ Summary

This README shows how the Semantic Git Archaeologist:

1. Analyzes vague user prompts.
2. Collects relevant historical commit data.
3. Detects patterns and synthesizes actionable insights.
4. Produces a final artifact that guides risk-aware development. -->


# 🧠 Anatomy of an AI Investigation

This document demonstrates the **end-to-end reasoning workflow** of the *Semantic Git Archaeologist* MCP server.

It shows how a vague user request like _“brief me on risks”_ is transformed into a **structured, evidence-based engineering report** — grounded in real Git history.

---

## 🎯 The Challenge

**User Prompt:**
> _"I'm about to make a change in the sensor logic. Give me a full briefing:  
> what are the risks, what should I learn from past fixes, and what is the current logic's intent?"_

This type of question cannot be answered by static code inspection alone — it requires **historical context and semantic reasoning**.

---

## 🕵️ Step 1: Strategic Reasoning

Before executing any tool, the AI agent analyzes the request and forms an investigation plan.

> **Agent reasoning (simplified):**
>
> - The user is asking for **risk**, not syntax.
> - Risks emerge from **past failures**, not just current code.
> - Git history must be queried semantically, not line-by-line.

**Planned actions:**
1. Inspect recent commits to understand the current state.
2. Mine historical bug-fix patterns related to the module.
3. Detect instability signals such as rushed fixes or rewrites.

---

## 🛠️ Step 2: Tool Execution (via MCP)

The agent invokes MCP tools autonomously:

### Mapping Recent Activity
```python
get_recent_history(limit=10, search_term="sensor")
```

### Mining Historical Bug Patterns
```python
detective_bug_miner(topic="sensors", lookback_days=90)
```

---

## ⚡ Step 3: Raw Findings (Unfiltered)

The MCP server returns structured data directly from Git history.

<details open>
<summary><strong>🔍 Inspect Raw Tool Output</strong></summary>

```json
{
  "bug_patterns_found": [
    {
      "pattern": "Rushed Deployment",
      "evidence": [
        "Commit 0a6a: 'Add sensors gui' (12:58 PM)",
        "Commit 496d: 'Fix onclick syntax' (13:05 PM)"
      ]
    },
    {
      "pattern": "Incomplete Implementation",
      "evidence": "File 'sensorsMapView.py' accessed undefined attribute 'self.t'"
    },
    {
      "pattern": "Integration Instability",
      "evidence": "Repeated 'connect GUI to db' commits followed by fixes and reverts"
    }
  ]
}
```
</details>

---

## 🧠 Step 4: Synthesis & Insight

The agent correlates timing, intent, and failure patterns.

**Key conclusions:**
- The dominant risk is **process-related**, not algorithmic.
- Multiple bugs stem from **rushed merges and insufficient integration testing**.
- Certain files show signs of architectural instability and refactoring debt.

---

## 📄 Step 5: Final Generated Artifacts

👉 **[View the Final Generated Report: Sensor Logic Briefing](artifacts/sensor_logic_briefing.md)**  
👉 **[View the Semantic Evolution Analysis](artifacts/sensor_gui_evolution.md)**

---

## ✅ Summary

This README demonstrates how the **Semantic Git Archaeologist MCP** enables AI agents to turn Git history into engineering intelligence.
