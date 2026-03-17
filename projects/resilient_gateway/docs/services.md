# Resilient Gateway Services

## Endpoint: POST `/v1/complete`
The primary endpoint for generating LLM completions.

### Request Body
```json
{
  "prompt": "Explain Quantum Computing",
  "model": "gpt-4o",
  "temperature": 0.7
}
```

### Response Body
```json
{
  "id": "res-12345",
  "text": "...response...",
  "model": "gpt-4o",
  "usage": {
    "total_tokens": 30
  },
  "provider": "Azure",
  "region": "westus",
  "cached": false
}
```

## Endpoint: GET `/health`
Returns the status of the gateway and its current operational mode (Simulation/Production).

## Middleware
- **AuditLogMiddleware**: Logs all incoming HTTP requests to stdout for traceability.
- **Observability**: Exports metrics to the centralized observability service.
