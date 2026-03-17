import httpx
import logging
import os
from typing import Any, Dict

logger = logging.getLogger("webhook-service")

class WebhookService:
    """
    Utility service to fire webhooks to n8n or other external orchestrators.
    """
    def __init__(self):
        self.webhook_url = os.getenv("N8N_WEBHOOK_URL", "http://localhost:5678/webhook/enrich-ai")

    async def fire_event(self, event_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sends an event to the configured webhook URL and returns the response.
        """
        payload = {
            "event": event_type,
            "data": data
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(self.webhook_url, json=payload, timeout=5.0)
                if response.status_code >= 400:
                    logger.warning(f"Webhook failed with status {response.status_code}: {response.text}")
                    return {}
                
                logger.info(f"Successfully fired webhook event: {event_type}")
                try:
                    return response.json()
                except:
                    return {}
        except Exception as e:
            logger.error(f"Failed to fire webhook: {str(e)}")
            return {}
        
        return {}
