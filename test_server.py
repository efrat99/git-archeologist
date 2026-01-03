import pytest
from unittest.mock import MagicMock, patch
from git import Repo, Actor
from server import get_recent_history, semantic_archeology_analyze, detective_bug_miner

# ==========================================
#              TEST FIXTURES
# ==========================================

@pytest.fixture
def mock_repo_path(tmp_path, monkeypatch):
    """
    Creates a temporary dummy git repository using GitPython.
    Isolates tests from the actual file system.
    """
    # 1. Create a folder for the repo
    git_dir = tmp_path / "test_repo"
    git_dir.mkdir()
    
    # 2. Initialize repo
    repo = Repo.init(git_dir)
    
    # 3. Create a dummy file
    file_path = git_dir / "file.txt"
    file_path.write_text("test content", encoding="utf-8")
    
    # 4. Add and Commit with a dummy author
    author = Actor("Test User", "test@example.com")
    repo.index.add([str(file_path)])
    repo.index.commit("Initial commit", author=author, committer=author)
    
    # 5. Inject this path into server.REPO_PATH
    monkeypatch.setattr("server.REPO_PATH", str(git_dir))
    return str(git_dir)

@pytest.fixture
def mock_gemini():
    """
    Mocks the Google GenAI client to avoid real API calls.
    """
    with patch("server.client") as mock_client:
        mock_response = MagicMock()
        mock_response.text = "AI Analysis: This is a mocked response."
        mock_client.models.generate_content.return_value = mock_response
        yield mock_client

# ==========================================
#              HISTORY TOOL TESTS
# ==========================================

def test_get_recent_history_valid_repo(mock_repo_path):
    """Ensures valid history is returned from a configured repo."""
    result = get_recent_history(limit=1)
    
    assert "Error" not in result
    assert "Recent History" in result
    assert "ID:" in result
    assert "Initial commit" in result

def test_get_recent_history_invalid_path(monkeypatch):
    """Ensures graceful error handling for bad paths."""
    monkeypatch.setattr("server.REPO_PATH", "C:/non/existent/path")
    result = get_recent_history(limit=1)
    
    assert "Error" in result 
    assert "Error reading Git history" in result or "Could not read Git history" in result

@pytest.mark.parametrize("limit", [1, 5, 0, 100])
def test_get_recent_history_limits(limit, mock_repo_path):
    """Verifies limit handling (boundary testing)."""
    result = get_recent_history(limit=limit)
    
    if limit == 0:
        assert "ID:" not in result
    else:
        assert "ID:" in result

# ==========================================
#              AI ANALYSIS TESTS
# ==========================================

def test_semantic_archeology_analyze_mocked(mock_repo_path, mock_gemini):
    """Tests semantic analysis integration (Mocked AI)."""
    result = semantic_archeology_analyze()
    
    assert "Archeological Analysis" in result
    assert "AI Analysis: This is a mocked response" in result
    mock_gemini.models.generate_content.assert_called_once()

def test_detective_bug_miner_no_results(mock_repo_path):
    """Tests bug miner when no matches are found."""
    result = detective_bug_miner(query="non_existent_bug")
    
    assert "No past fixes found" in result