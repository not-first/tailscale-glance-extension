from src.config import config
from datetime import datetime, timezone
import humanize

def parse_widget_html(data, display_options=None):
    if display_options is None:
        display_options = {
            "show_updates": True,
            "show_user": True
        }

    show_updates = display_options.get("show_updates", True)
    show_user = display_options.get("show_user", True)

    if "error" in data:
        return f"<p class='color-negative'>Error: {data['error']}</p>"

    devices = data.get("devices", [])

    if not devices:
        return "<p>No devices found</p>"

    css = """
    <style>
        .device-info-container {
            position: relative;
            overflow: hidden;
            height: 1.5em;
        }

        .device-info {
            display: flex;
            transition: transform 0.3s ease, opacity 0.3s ease;
        }

        .device-ip {
            position: absolute;
            top: 0;
            left: 0;
            transform: translateY(-100%);
            opacity: 0;
            transition: transform 0.3s ease, opacity 0.3s ease;
        }

        .device-info-container:hover .device-info {
            transform: translateY(100%);
            opacity: 0;
        }

        .device-info-container:hover .device-ip {
            transform: translateY(0);
            opacity: 1;
        }

        .update-indicator {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background-color: var(--color-primary);
            display: inline-block;
            margin-left: 4px;
            vertical-align: middle;
        }

        .offline-indicator {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background-color: var(--color-negative);
            display: inline-block;
            margin-left: 4px;
            vertical-align: middle;
        }

        .device-name-container {
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .indicators-container {
            display: flex;
            align-items: center;
            gap: 4px;
        }
    </style>
    """

    device_items = []
    current_time = datetime.now(timezone.utc)

    for device in devices:
        # Get name up to the first period instead of hostname
        full_name = device.get("name", "Unknown")
        name = full_name.split('.')[0] if '.' in full_name else full_name

        ip_address = device.get("addresses", [""])[0] if device.get("addresses") else "No IP"
        os = device.get("os", "Unknown")
        user = device.get("user", "Unknown")
        update_available = device.get("updateAvailable", False)

        # Check if device is offline (last seen > 10 seconds ago)
        last_seen_str = device.get("lastSeen")
        offline = False
        last_seen_human = "Unknown"

        if last_seen_str:
            try:
                last_seen_time = datetime.fromisoformat(last_seen_str.replace('Z', '+00:00'))
                time_diff = (current_time - last_seen_time).total_seconds()
                offline = time_diff > 10
                last_seen_human = humanize.naturaltime(current_time - last_seen_time)
            except (ValueError, TypeError):
                pass

        indicators = []

        if show_updates and update_available:
            indicators.append("""
            <span class="update-indicator" data-popover-type="text" data-popover-text="Update Available"></span>
            """)

        if offline:
            indicators.append(f"""
            <span class="offline-indicator" data-popover-type="text" data-popover-text="Offline - Last seen {last_seen_human}"></span>
            """)

        indicators_html = "".join(indicators)

        info_items = [f"<li>{os}</li>"]
        if show_user:
            info_items.append(f"<li>{user}</li>")

        info_html = "".join(info_items)

        animated_info = f"""
        <div class="device-info-container">
            <ul class="list-horizontal-text device-info">
                {info_html}
            </ul>
            <div class="device-ip">
                {ip_address}
            </div>
        </div>
        """

        device_html = f"""
        <li>
            <div class="flex items-center gap-10">
                <div class="device-name-container grow">
                    <span class="size-h4 block text-truncate color-primary">
                        {name}
                    </span>
                    <div class="indicators-container">
                        {indicators_html}
                    </div>
                </div>
            </div>
            {animated_info}
        </li>
        """
        device_items.append(device_html)

    devices_html = "\n".join(device_items)

    return f"""
    {css}
    <ul class="list list-gap-10 collapsible-container" data-collapse-after="4">
        {devices_html}
    </ul>
    """
