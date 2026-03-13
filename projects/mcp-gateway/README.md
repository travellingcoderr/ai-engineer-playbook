
# MCP Gateway Example

This example exposes tools to an AI model.

## Run

```
pip install -r requirements.txt
uvicorn main:app --reload
```

Endpoint example:

```
/query?sql=SELECT+1
```
