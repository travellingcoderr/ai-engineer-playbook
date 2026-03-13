from __future__ import annotations

from pathlib import Path

BASE_ALLOWED_DIR = Path(__file__).resolve().parents[2]
ALLOWED_TOOLS = {
    "analyst": {"health_check", "query_readonly_sql"},
    "engineer": {"health_check", "read_repo_file"},
    "admin": {"health_check", "query_readonly_sql", "read_repo_file"},
}


def _assert_tool_allowed(role: str, tool_name: str) -> None:
    if tool_name not in ALLOWED_TOOLS.get(role, set()):
        raise PermissionError(f"Role '{role}' cannot use tool '{tool_name}'")


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


TOOL_REGISTRY = {
    "health_check": health_check,
    "query_readonly_sql": query_readonly_sql,
    "read_repo_file": read_repo_file,
}


def invoke_tool(role: str, tool_name: str, arguments: dict) -> dict:
    _assert_tool_allowed(role, tool_name)
    tool_fn = TOOL_REGISTRY.get(tool_name)
    if not tool_fn:
        raise ValueError(f"Unknown tool: {tool_name}")
    return tool_fn(arguments)
