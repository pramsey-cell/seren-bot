# 🚀 Deploy to Railway — Beginner Checklist

Goal: get the bot running online 24/7 with no command line and no Docker
knowledge. Takes about 15 minutes. Tick each box as you go.

---

## Part 1 — Discord setup (do this once)

- [ ] Go to https://discord.com/developers/applications → **New Application**.
- [ ] Open the **Bot** tab → **Reset Token** → copy the token somewhere safe.
      This is your `DISCORD_TOKEN`. Treat it like a password — never share it.
- [ ] In your Discord server: **Server Settings → Roles**, create one role per
      feed (New Drops, Events, Deals, Brew Tips, Community).
- [ ] Turn on Developer Mode: **User Settings → Advanced → Developer Mode**.
- [ ] Right-click each role → **Copy Role ID**, and paste each ID into
      `config.py` (replace the `000000000000000000` placeholders).
- [ ] Drag the **bot's own role above all the feed roles** in the roles list,
      or it won't be allowed to assign them.
- [ ] Get your server ID: right-click the server icon → **Copy Server ID**.
      This is your `GUILD_ID`.
- [ ] Invite the bot: **OAuth2 → URL Generator** → check `bot` and
      `applications.commands`, then check **Manage Roles** + **Send Messages**.
      Open the generated link and add the bot to your server.

## Part 2 — Put the code on GitHub (all in the browser)

- [ ] Create a free account at https://github.com.
- [ ] Click **New repository**, give it a name, keep it **Private**, create it.
- [ ] On the new repo page, click **uploading an existing file**.
- [ ] Drag in every file from this folder **EXCEPT** your real `.env`.
      (The included `.gitignore` also protects you, but don't upload it anyway.)
- [ ] Click **Commit changes**.

> ⚠️ Never upload your real `.env` or your token. If you ever do by accident,
> go to the Discord Developer Portal and **Reset Token** immediately.

## Part 3 — Deploy on Railway

- [ ] Sign up at https://railway.app (log in with GitHub — easiest).
- [ ] Click **New Project → Deploy from GitHub repo** → pick your repo.
- [ ] Railway auto-detects the included `Dockerfile` and starts building.
- [ ] Open the **Variables** tab and add two variables:
        - `DISCORD_TOKEN` = your bot token
        - `GUILD_ID` = your server ID
- [ ] It redeploys automatically. Open the **Deploy Logs** and wait for
      `Logged in as ...` — that means it's live.

## Part 4 — Confirm it works

- [ ] In your server, type `/feeds-panel` in a channel (staff only).
- [ ] Tap **Manage my feeds** on the panel and pick a feed.
- [ ] Check that the matching role appears on your profile. 🎉

---

## If something's wrong

- **Commands don't appear:** make sure `GUILD_ID` is set correctly, then in
  Railway click **Redeploy**. Guild commands appear instantly.
- **"I couldn't change your roles":** the bot's role isn't above the feed roles,
  or it's missing **Manage Roles**. Fix in Server Settings → Roles.
- **Bot shows offline:** check Deploy Logs for an error. A bad/blank
  `DISCORD_TOKEN` is the usual cause.

## Cost note

Railway's trial includes about $5 of credit (~1 month). After that it's roughly
$5/month to stay online. If you'd rather not pay, ask about the free-but-more-
technical routes (e.g. Oracle Cloud) — they work but require managing a server.
