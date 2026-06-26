# Define your community's feeds here.
#
# 1. In your Discord server, create one ROLE per feed (Server Settings > Roles).
# 2. Enable Developer Mode (User Settings > Advanced), then right-click each
#    role > Copy Role ID and paste it below as an integer (no quotes).
#
# "value" just needs to be unique per feed. "roleId" is the role that actually
# gets added/removed from the member.

FEEDS = [
    {
        "label": "New Drops",
        "value": "feed_new_drops",
        "roleId": 1520149266725605587,
        "emoji": "☕",
        "description": "New beans, roasts, and seasonal menu items",
    },
    {
        "label": "Events & Tastings",
        "value": "feed_events",
        "roleId": 000000000000000000,
        "emoji": "📅",
        "description": "Cuppings, tastings, and community meetups",
    },
    {
        "label": "Deals & Promos",
        "value": "feed_deals",
        "roleId": 000000000000000000,
        "emoji": "🔥",
        "description": "Discounts and limited-time offers",
    },
    {
        "label": "Brew Tips",
        "value": "feed_brew",
        "roleId": 000000000000000000,
        "emoji": "📚",
        "description": "Recipes, ratios, and brewing guides",
    },
    {
        "label": "Community",
        "value": "feed_community",
        "roleId": 000000000000000000,
        "emoji": "💬",
        "description": "General announcements and chat pings",
    },
]
