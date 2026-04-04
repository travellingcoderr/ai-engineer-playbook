# Azure OpenAI Setup Guide

This guide ensures your Azure OpenAI infrastructure is correctly provisioned and connected to the **InsureDoc** platform.

---

## 1. Create the Azure OpenAI Resource
1. Sign in to the [Azure Portal](https://portal.azure.com/).
2. Search for **"Azure OpenAI"** and click **Create**.
3. Choose a **Name** (e.g., `insuredoc-ai-dev`). 💡 **This is your `AZURE_OPENAI_INSTANCE_NAME`**.
4. Select a region with `gpt-4o` support (e.g., `East US` or `Sweden Central`).
5. Complete creation.

---

## 2. Deploy the AI Model
1. In your resource, go to **Model deployments** -> **Manage Deployments**.
2. Create a new deployment for **`gpt-4o`**.
3. **Deployment Name**: Set this to `gpt-4o`. (Must match your `.env`).

---

## 3. Environment Mapping
Copy these values into your root **`.env`** file at `projects/insure-doc/.env`.

| Azure Portal Field | .env Variable | Example Value |
|:---|:---|:---|
| **Resource Name** | `AZURE_OPENAI_INSTANCE_NAME` | `insuredoc-ai-dev` |
| **KEY 1** | `AZURE_OPENAI_API_KEY` | `32-char-string` |
| **Deployment Name**| `AZURE_OPENAI_DEPLOYMENT` | `gpt-4o` |
| **N/A** | `AZURE_OPENAI_API_VERSION` | `2024-02-01` |

---

## Troubleshooting

### "Instance name not found"
- **Cause**: The `AZURE_OPENAI_INSTANCE_NAME` in your `.env` did not match the subdomain of your Azure endpoint.
- **Fix**: Ensure the instance name is **just the prefix** (e.g., `my-resource`), not the full URL.
