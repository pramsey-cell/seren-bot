# ☕ Coffee Feeds Bot (Python / discord.py)

Lets community members customize their feed — they pick which categories of
updates they want (New Drops, Events, Deals, Brew Tips, Community) and the bot
manages the matching roles. Ping a feed's role when you post, and only the
people who opted in get notified.

- `/feeds` — any member opens a private menu and toggles the feeds they want.
- `/feeds-panel` — staff post a permanent panel with a **Manage my feeds** button
  (works forever, even after the bot restarts).

## One-time Discord setup

1. **Create the bot:** https://discord.com/developers/applications → New Application
   → **Bot** tab → Reset Token → copy it (`DISCORD_TOKEN`).
2. **Make a role per feed** (Server Settings → Roles). Enable Developer Mode,
   right-click each role → Copy Role ID, and paste the IDs into `config.py`.
   Then **drag the bot's role above the feed roles**.
3. **Invite it:** OAuth2 → URL Generator → scopes `bot` + `applications.commands`;
   permissions **Manage Roles** + **Send Messages**. Open the URL, add to server.
4. Grab your **Server ID** (right-click server icon → Copy Server ID) for `GUILD_ID`.

## Deploy — pick one

### A) Local / any VPS
```bash
pip install -r requirements.txt
cp .env.example .env        # fill in DISCORD_TOKEN and GUILD_ID
python bot.py
```

### B) Docker (one command)
```bash
docker build -t coffee-feeds-bot .
docker run --env-file .env coffee-feeds-bot
```

### C) Railway / Render (no server to manage)
1. Push this folder to a GitHub repo.
2. Create a new project from the repo. The included **Dockerfile** (or
   **Procfile** → run as a *Worker*, not a Web service) is detected automatically.
3. Add environment variables `DISCORD_TOKEN` and `GUILD_ID` in the dashboard.
4. Deploy. That's it — the bot stays online.

> Run `/feeds-panel` once in a channel and you're live.

## Customizing feeds
Edit `config.py` only — add, remove, or rename feeds. Each needs a unique
`value` and its role's `roleId`. No other code changes required.

---
Built with discord.py v2.
