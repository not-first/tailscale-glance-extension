import requests
import logging
from src.config import config

logger = logging.getLogger("tailscale-api")

def get_devices():
    """Get all devices in the tailnet from Tailscale API"""
    try:
        if not config.TAILSCALE_API_KEY:
            logger.error("TAILSCALE_API_KEY not configured")
            return {"error": "TAILSCALE_API_KEY not configured"}

        headers = {
            "Authorization": f"Bearer {config.TAILSCALE_API_KEY}"
        }

        response = requests.get(
            "https://api.tailscale.com/api/v2/tailnet/-/devices",
            headers=headers
        )
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching devices from Tailscale API: {e}")
        return {"error": str(e)}
