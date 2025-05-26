from typing import Any, Dict
import re

def validate_email(email: str) -> bool:
    """בדיקה בסיסית של פורמט אימייל"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def clean_string(text: str) -> str:
    """ניקוי מחרוזת מרווחים מיותרים"""
    return text.strip() if text else ""

def format_response(data: Any, message: str = "Success") -> Dict[str, Any]:
    """פורמט סטנדרטי לתגובות API"""
    return {
        "success": True,
        "message": message,
        "data": data
    }