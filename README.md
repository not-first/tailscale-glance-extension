# Tailscale Glance Extension
_An extension widget API for the [Glance](https://github.com/glanceapp/glance) dashboard._

A widget that displays the devices on your [Tailscale](https://tailscale.com/) tailnet, as well as their online status and availability of updates.

## Setup
### Docker Compose
Add the following to your existing glance docker compose
```yml
services:
  glance:
    image: glanceapp/glance
    # ...

  tailscale-extension:
    image: ghcr.io/not-first/tailscale-glance-extension
    ports:
      - '8677:8677'
    restart: unless-stopped
    env_file: .env
```
#### Environment Variables
This widget must be set up by providing an environment variable, which can be added to your existing glance .env file:
```env
TAILSCALE_API_KEY=tskey-api-xxxxxxxxxxxxxxxxxxxxxxxxx
```

### Glance Config
Next, add the extension widget into your glance page by adding this to your `glance.yml`.
```yml
- type: extension
  title: Uptime Status
  url: http://tailscale-extension:8677/
  cache: 10m
  allow-potentially-dangerous-html: true
```

---

