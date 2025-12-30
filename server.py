import os
from mcp.server.fastmcp import FastMCP
from git import Repo
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

mcp = FastMCP("Git-Archeologist")

REPO_PATH = "C:\\Users\\משתמש\\Desktop\\vectordb_efrat\\AgCloud"

@mcp.tool()
def get_recent_history(limit: int = 5) -> str:
    """
    Retrieves the recent git commit history with messages and authors.
    This helps the AI understand the latest changes in the project.
    """
    try:
        repo = Repo(REPO_PATH)
        commits = list(repo.iter_commits(max_count=limit))
        
        output = f"--- Recent History for {os.path.basename(REPO_PATH)} ---\n"
        for commit in commits:
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
        # אם לא נבחר האש ספציפי, ניקח את האחרון
        target = commit_hash if commit_hash else "HEAD"
        commit = repo.commit(target)
        
        # שליפת ה-Diff (השינוי עצמו)
        diff = repo.git.show(target)

        # יצירת הפרומפט עבור הארכיאולוג הסמנטי
        archeologist_prompt = f"""
        You are a Senior Software Archeologist. Analyze this git diff and explain:
        1. The main purpose of this change.
        2. The logic behind the implementation.
        3. Potential side effects.

        Git Diff:
        {diff[:8000]}  # הגדלה של כמות הטקסט לניתוח עמוק יותר
        """
        
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
        # חיפוש קומיטים שהודעתם מכילה את המילה המבוקשת
        matching_commits = list(repo.iter_commits(max_count=10, grep=query))
        
        if not matching_commits:
            return f"No past fixes found for '{query}'."

        summary = "--- Found Past Fixes ---\n"
        for c in matching_commits:
            summary += f"ID: {c.hexsha[:8]} | Message: {c.message.strip()}\n"
            
        # שימוש ב-Gemini 2.5 לניתוח הדפוס
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"Analyze these past fixes for '{query}' and summarize the common patterns: {summary}"
        )
        return f"--- 🔍 Detective Insights ---\n{response.text}"
    except Exception as e:
        return f"Detective failed: {e}"
    

@mcp.tool()
def analyze_code_hotspots() -> str:
    """Identifies 'fragile' files that change frequently (Risk Map)."""
    try:
        repo = Repo(REPO_PATH)
        # ספירת קבצים שהשתנו ב-50 הקומיטים האחרונים
        file_counts = Counter()
        for commit in repo.iter_commits(max_count=50):
            file_counts.update(commit.stats.files.keys())
        
        hotspots = file_counts.most_common(5)
        hotspot_str = "\n".join([f"{file}: {count} changes" for file, count in hotspots])
        
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"Analyze these code hotspots and explain why they might be risky: {hotspot_str}"
        )
        return f"--- ⚠️ Risk Map (Top Hotspots) ---\n{response.text}"
    except Exception as e:
        return f"Hotspot analysis failed: {e}"

@mcp.tool()
def get_file_evolution(file_path: str) -> str:
    """Traces how a specific file's logic has evolved over time."""
    try:
        repo = Repo(REPO_PATH)
        commits = list(repo.iter_commits(paths=file_path, max_count=5))
        evolution = "\n".join([f"ID: {c.hexsha[:8]} | Message: {c.message.strip()}" for c in commits])
        
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"Explain the evolution of the logic in {file_path} based on these updates: {evolution}"
        )
        return f"--- 🧬 Evolution of {file_path} ---\n{response.text}"
    except Exception as e:
        return f"Evolution trace failed: {e}"

if __name__ == "__main__":
    mcp.run()

