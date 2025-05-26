from typing import Any, Optional

def success_response(data: Any, message: str = "Success", status: int = 200):
    return {
        "status": status,
        "message": message,
        "data": data
    }

def error_response(message: str, status: int = 400, data: Any = None):
    return {
        "status": status,
        "message": message,
        "data": data
    }