import os

import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

from config import FEEDS

load_dotenv()
TOKEN = os.environ["DISCORD_TOKEN"]
GUILD_ID = os.environ.get("GUILD_ID")  # optional: instant command sync to one server

# Only default intents are needed. We add/remove roles on the member attached to
# each interaction, so no privileged intents are required.
intents = discord.Intents.default()


def build_options(current_role_ids):
    """Build the select options, pre-checking feeds the user already follows."""
    options = []
    for f in FEEDS:
        desc = (f.get("description") or "")[:100] or None
        options.append(
            discord.SelectOption(
                label=f["label"],
                value=f["value"],
                description=desc,
                emoji=f.get("emoji"),
                default=f["roleId"] in current_role_ids,
            )
        )
    return options


async def handle_selection(interaction: discord.Interaction, selected_values):
    """Reconcile the member's roles to exactly what they selected."""
    member = interaction.user
    selected = set(selected_values)
    added, removed = [], []

    try:
        for f in FEEDS:
            role = interaction.guild.get_role(f["roleId"])
            if role is None:
                continue
            wants = f["value"] in selected
            has = role in member.roles
            if wants and not has:
                await member.add_roles(role)
                added.append(f["label"])
            elif not wants and has:
                await member.remove_roles(role)
                removed.append(f["label"])
    except discord.Forbidden:
        await interaction.response.edit_message(
            content=(
                "I couldn't change your roles. Ask an admin to give me the "
                '"Manage Roles" permission and drag my role above the feed roles.'
            ),
            view=None,
        )
        return

    lines = []
    if added:
        lines.append(f"✅ **Subscribed:** {', '.join(added)}")
    if removed:
        lines.append(f"🔕 **Unsubscribed:** {', '.join(removed)}")
    if not lines:
        lines.append("No changes — your feeds are already set that way.")

    await interaction.response.edit_message(content="\n".join(lines), view=None)


class FeedSelect(discord.ui.Select):
    def __init__(self, current_role_ids):
        super().__init__(
            placeholder="Choose the feeds you want to follow",
            min_values=0,
            max_values=len(FEEDS),
            options=build_options(current_role_ids),
        )

    async def callback(self, interaction: discord.Interaction):
        await handle_selection(interaction, self.values)


class FeedSelectView(discord.ui.View):
    """Short-lived, per-user picker shown ephemerally."""

    def __init__(self, current_role_ids):
        super().__init__(timeout=120)
        self.add_item(FeedSelect(current_role_ids))


async def send_picker(interaction: discord.Interaction):
    if interaction.guild is None:
        await interaction.response.send_message(
            "Use this inside the server, not in DMs.", ephemeral=True
        )
        return
    current = [r.id for r in interaction.user.roles]
    await interaction.response.send_message(
        "Pick the feeds you want — whatever you select becomes your full "
        "subscription list. Deselect anything to unsubscribe.",
        view=FeedSelectView(current),
        ephemeral=True,
    )


class FeedPanelView(discord.ui.View):
    """Persistent panel. The button keeps working after the bot restarts."""

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Manage my feeds",
        emoji="🔔",
        style=discord.ButtonStyle.primary,
        custom_id="feed_open",
    )
    async def open_feeds(self, interaction: discord.Interaction, button: discord.ui.Button):
        await send_picker(interaction)


class FeedBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # Re-register the persistent panel so its button survives restarts.
        self.add_view(FeedPanelView())
        # Sync slash commands. Guild-scoped = instant; global can take up to 1h.
        if GUILD_ID:
            guild = discord.Object(id=int(GUILD_ID))
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
        else:
            await self.tree.sync()


bot = FeedBot()


@bot.tree.command(
    name="feeds", description="Choose which coffee shop feeds you want to follow"
)
async def feeds(interaction: discord.Interaction):
    await send_picker(interaction)


@bot.tree.command(
    name="feeds-panel", description="Post a public feed-selection panel (staff only)"
)
@app_commands.default_permissions(manage_guild=True)
async def feeds_panel(interaction: discord.Interaction):
    embed = discord.Embed(
        title="☕ What can we pour you?",
        description=(
            "Tap below to build your tab — pick the updates you actually want,"
            "and we'll only ping you about those. Change it anytime."
        ),
        color=0x6F4E37,
    )
    await interaction.channel.send(embed=embed, view=FeedPanelView())
    await interaction.response.send_message("Feed panel posted ✅", ephemeral=True)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


bot.run(TOKEN)
