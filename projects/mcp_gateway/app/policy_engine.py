from typing import Any

class PolicyEngine:
    def __init__(self):
        # In production, these could be loaded from a DB or YAML
        self.role_tools = {
            "analyst": {"health_check", "query_readonly_sql", "list_files"},
            "engineer": {"health_check", "read_repo_file"},
            "admin": {"health_check", "query_readonly_sql", "read_repo_file", "list_files"},
        }

    def validate_access(self, role: str, tool_name: str, arguments: dict[str, Any]) -> None:
        if tool_name not in self.role_tools.get(role, set()):
            raise PermissionError(f"Role '{role}' cannot use tool '{tool_name}'")
        
        # Attribute-based access control (ABAC) example
        if tool_name == "list_files":
            path = str(arguments.get("path", "."))
            if ".." in path or path.startswith("/"):
                raise PermissionError("Path traversal or absolute paths are forbidden")
            
            # Analysts can only see 'projects' and 'packages'
            if role == "analyst" and not any(p in path for p in ["projects", "packages", "."]):
                raise PermissionError("Analysts can only list project or package directories")

policy_engine = PolicyEngine()
