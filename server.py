import os
from collections import Counter
from mcp.server.fastmcp import FastMCP
from git import Repo
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

mcp = FastMCP("Git-Archeologist")

REPO_PATH = os.getenv("REPO_PATH")
if not REPO_PATH:
    raise RuntimeError("REPO_PATH must be set")


@mcp.tool()
def get_recent_history(limit: int = 5) -> str:
    """
    Retrieves the recent git commit history with messages and authors.
    This helps the AI understand the latest changes in the project.
    """
    try:
        # Create a Repo object pointing to the target repository
        repo = Repo(REPO_PATH)
        commits = list(repo.iter_commits(max_count=limit))
        
        output = f"--- Recent History for {os.path.basename(REPO_PATH)} ---\n"
        for commit in commits:
            # hexsha[:8] gives the short commit hash (e.g., a1b2c3d4)
            output += f"ID: {commit.hexsha[:8]} | Author: {commit.author} | Date: {commit.authored_datetime}\n"
            output += f"Message: {commit.message.strip()}\n"
            output += "-" * 20 + "\n"
        return output
    except Exception as e:
        return f"Error: Could not read Git history. Make sure this is a Git repository. Details: {e}"
    

@mcp.tool()
def semantic_archeology_analyze(commit_hash: str = None) -> str:
    """
    Analyzes a specific commit or the latest change using Gemini.
    It explains the logic and intent behind the code changes, not just what changed.
    """
    try:
        repo = Repo(REPO_PATH)
        # Use the provided commit hash, or default to "HEAD" (latest commit)
        target = commit_hash if commit_hash else "HEAD"
        commit = repo.commit(target)
        
        # Retrieve the Git Diff (the actual code changes)
        diff = repo.git.show(target)

        # Prepare the prompt for the AI Semantic Archeologist
        archeologist_prompt = f"""
        You are a Senior Software Archeologist. Analyze this git diff and explain:
        1. The main purpose of this change.
        2. The logic behind the implementation.
        3. Potential side effects.

        Git Diff:
        {diff[:8000]}  # Truncated to avoid token limits
        """
        
        # Call Gemini API
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=archeologist_prompt
        )
        
        return f"--- Archeological Analysis of Commit {commit.hexsha[:8]} ---\n{response.text}"
    
    except Exception as e:
        return f"Error in semantic analysis: {str(e)}"
    

@mcp.tool()
def detective_bug_miner(query: str = "fix") -> str:
    """
    Searches the Git history for bug fixes related to a query.
    Helps learn from past solutions to solve current issues.
    """
    try:
        repo = Repo(REPO_PATH)
        # Search for commits containing the query string in their message
        matching_commits = list(repo.iter_commits(max_count=10, grep=query))
        
        if not matching_commits:
            return f"No past fixes found for '{query}'."

        summary = "--- Found Past Fixes ---\n"
        for c in matching_commits:
            summary += f"ID: {c.hexsha[:8]} | Message: {c.message.strip()}\n"
            
        # Use Gemini to analyze patterns in the fixes
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"Analyze these past fixes for '{query}' and summarize the common patterns: {summary}"
        )
        return f"--- Detective Insights ---\n{response.text}"
    except Exception as e:
        return f"Detective failed: {e}"
    

@mcp.tool()
def analyze_code_hotspots() -> str:
    """Identifies 'fragile' files that change frequently (Risk Map)."""
    try:
        repo = Repo(REPO_PATH)
        # Count changed files in the last 50 commits
        file_counts = Counter()
        for commit in repo.iter_commits(max_count=50):
            file_counts.update(commit.stats.files.keys())
        
        # Get the top 5 most modified files
        hotspots = file_counts.most_common(5)
        hotspot_str = "\n".join([f"{file}: {count} changes" for file, count in hotspots])
        
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"Analyze these code hotspots and explain why they might be risky: {hotspot_str}"
        )
        return f"--- Risk Map (Top Hotspots) ---\n{response.text}"
    except Exception as e:
        return f"Hotspot analysis failed: {e}"

@mcp.tool()
def get_file_evolution(file_path: str) -> str:
    """Traces how a specific file's logic has evolved over time."""
    try:
        repo = Repo(REPO_PATH)

        # Get history specifically for this file path
        commits = list(repo.iter_commits(paths=file_path, max_count=5))
        evolution = "\n".join([f"ID: {c.hexsha[:8]} | Message: {c.message.strip()}" for c in commits])
        
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"Explain the evolution of the logic in {file_path} based on these updates: {evolution}"
        )
        return f"--- Evolution of {file_path} ---\n{response.text}"
    except Exception as e:
        return f"Evolution trace failed: {e}"

if __name__ == "__main__":
    mcp.run()

