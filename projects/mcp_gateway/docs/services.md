# MCP Gateway API Services

This document outlines the endpoints provided by the MCP-Style Gateway.

## 1. POST `/login`
- **Description**: Authenticates a user and returns a Bearer JWT.
- **Request Body**:
  ```json
  {
    "username": "admin"
  }
  ```
  *(Supported usernames for demo: `admin`, `analyst`, `engineer`)*
- **Response**:
  - `access_token`: The JWT to be used in subsequent requests.
  - `token_type`: Always "bearer".

## 2. POST `/tools/invoke`
- **Description**: Invokes a specific tool if authorized.
- **Authorization**: Required (Bearer Token).
- **Request Body** (`ToolRequest`):
  ```json
  {
    "tool_name": "list_files",
    "arguments": {
      "path": "."
    }
  }
  ```
- **Response** (`ToolResponse`):
  - `ok`: Boolean (True if execution succeeded).
  - `tool_name`: Name of the tool called.
  - `result`: The output of the tool.

## 3. GET `/health`
- **Description**: Returns the status of the gateway service.
- **Response**: `{"status": "ok"}`

---

## Interactive Documentation

While the gateway is running (usually on `http://localhost:8001`), you can access:
- **Swagger UI**: `/docs`
- **ReDoc**: `/redoc`

> [!IMPORTANT]
> **If you see "Unprocessable Entity" in Swagger**, please **refresh the page**. The API schema was updated to support the "Authorize" button flow.

### How to use the "Authorize" button:
1. Click **"Authorize"** at the top right.
2. Enter one of the following in the **`username`** field:
   - `admin` (Full access)
   - `analyst` (File listing, SQL queries)
   - `engineer` (File reading)
3. Enter *any* value in the **`password`** field (it is not checked for this demo).
4. Leave **`client_id`** and **`client_secret`** blank.
5. Click **"Authorize"** then **"Close"**.
