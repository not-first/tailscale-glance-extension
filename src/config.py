import os

class Config:
    TAILSCALE_API_KEY = os.getenv("TAILSCALE_API_KEY", "")

config = Config()
