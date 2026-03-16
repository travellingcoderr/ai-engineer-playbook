from __future__ import annotations
from pathlib import Path
from app.policy_engine import policy_engine

BASE_ALLOWED_DIR = Path(__file__).resolve().parents[2]

def health_check(_: dict) -> dict:
    return {"status": "ok"}

def query_readonly_sql(arguments: dict) -> dict:
    sql = str(arguments.get("sql", "")).strip().lower()
    if not sql:
        raise ValueError("sql is required")
    banned = ["delete ", "update ", "insert ", "drop ", "alter ", "truncate "]
    if any(word in sql for word in banned):
        raise ValueError("Only read-only SQL is allowed")
    if not sql.startswith("select"):
        raise ValueError("Only SELECT queries are allowed")

    # demo stub result
    return {
        "executed": False,
        "message": "Stub only. Replace with a real read-only adapter.",
        "sql": sql,
    }


def read_repo_file(arguments: dict) -> dict:
    relative_path = str(arguments.get("path", "")).strip()
    if not relative_path:
        raise ValueError("path is required")

    full_path = (BASE_ALLOWED_DIR / relative_path).resolve()
    if BASE_ALLOWED_DIR not in full_path.parents and full_path != BASE_ALLOWED_DIR:
        raise ValueError("Path is outside allowed directory")
    if not full_path.exists() or not full_path.is_file():
        raise FileNotFoundError("File not found")

    content = full_path.read_text(encoding="utf-8")
    return {
        "path": str(full_path.relative_to(BASE_ALLOWED_DIR)),
        "preview": content[:2000],
    }


def list_files(arguments: dict) -> dict:
    relative_path = str(arguments.get("path", ".")).strip()
    full_path = (BASE_ALLOWED_DIR / relative_path).resolve()

    if BASE_ALLOWED_DIR not in full_path.parents and full_path != BASE_ALLOWED_DIR:
        raise ValueError("Path is outside allowed directory")
    if not full_path.exists() or not full_path.is_dir():
        raise FileNotFoundError("Directory not found")

    items = []
    for item in full_path.iterdir():
        items.append({
            "name": item.name,
            "type": "directory" if item.is_dir() else "file",
            "size": item.stat().st_size if item.is_file() else None
        })

    return {
        "path": str(full_path.relative_to(BASE_ALLOWED_DIR)),
        "items": items
    }


TOOL_REGISTRY = {
    "health_check": health_check,
    "query_readonly_sql": query_readonly_sql,
    "read_repo_file": read_repo_file,
    "list_files": list_files,
}


def invoke_tool(role: str, tool_name: str, arguments: dict) -> dict:
    policy_engine.validate_access(role, tool_name, arguments)
    tool_fn = TOOL_REGISTRY.get(tool_name)
    if not tool_fn:
        raise ValueError(f"Unknown tool: {tool_name}")
    return tool_fn(arguments)
