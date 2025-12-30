import pytest
from server import get_recent_history
import os

def test_get_recent_history_valid_repo():
    """בדיקה שהכלי מחזיר היסטוריה עבור נתיב תקין"""
    # קריאה לכלי שבנית
    result = get_recent_history(limit=1)
    
    # בדיקה שהתוצאה מכילה את המילים המצופות
    assert "Recent History" in result
    assert "ID:" in result
    assert "Author:" in result

def test_get_recent_history_invalid_path(monkeypatch):
    """בדיקה שהכלי מטפל בשגיאות כשנתיב התיקייה שגוי"""
    # "נדרוס" זמנית את הנתיב לנתיב לא קיים
    monkeypatch.setattr("server.REPO_PATH", "C:/non/existent/path")
    
    result = get_recent_history(limit=1)
    assert "Error" in result # מוודא שהחזרנו הודעת שגיאה מסודרת