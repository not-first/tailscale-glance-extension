import logging
from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse
from src.config import config
from src.tailscale import get_devices
from src.widget import parse_widget_html

logging.basicConfig(format="%(levelname)s:    %(message)s", level=logging.INFO)
logger = logging.getLogger("tailscale-api")

app = FastAPI()


@app.get("/")
async def get_tailscale_devices(
    request: Request,
    show_updates: bool = Query(True, alias="show-updates"),
    show_user: bool = Query(True, alias="show-user")
):
    logger.info(f"Request received for Tailscale devices (show-updates: {show_updates}, show-user: {show_user})")

    if not config.TAILSCALE_API_KEY:
        error_msg = "TAILSCALE_API_KEY not configured"
        logger.error(error_msg)
        return HTMLResponse(
            content=f"<p class='color-negative'>Error: {error_msg}</p>",
            headers={"Widget-Title": "Tailscale Devices", "Widget-Content-Type": "html"}
        )

    devices_data = get_devices()
    if "error" in devices_data:
        return HTMLResponse(
            content=f"<p class='color-negative'>Error: {devices_data['error']}</p>",
            headers={"Widget-Title": "Tailscale Devices", "Widget-Content-Type": "html"}
        )

    display_options = {
        "show_updates": show_updates,
        "show_user": show_user
    }

    return HTMLResponse(
        content=parse_widget_html(devices_data, display_options),
        headers={"Widget-Title": "Tailscale Devices", "Widget-Content-Type": "html"}
    )