from fastapi import Header, HTTPException


TOKEN_ROLE_MAP = {
    "demo-analyst-token": "analyst",
    "demo-engineer-token": "engineer",
    "demo-admin-token": "admin",
}


def get_role_from_auth_header(authorization: str | None = Header(default=None)) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid bearer token")

    token = authorization.removeprefix("Bearer ").strip()
    role = TOKEN_ROLE_MAP.get(token)
    if not role:
        raise HTTPException(status_code=403, detail="Unknown token")

    return role
