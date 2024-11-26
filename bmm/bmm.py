import zoneinfo
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import random

from redbot.core import commands, Config, checks


class BMMCog(commands.Cog):
    """BMM Cog"""

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=1289862744207523841004)

        guild_default_config = {
            "timezone": "UTC"
        }

        self.config.register_guild(**guild_default_config)

    @commands.group(name="bmm", pass_context=True, invoke_without_command=True)
    async def _bmm(self, ctx: commands.Context):
        now = datetime.utcnow().replace(tzinfo=timezone.utc)
        localized = now.astimezone(ZoneInfo(await self.config.guild(ctx.guild).timezone()))
        if localized.weekday() == 0:
            if bool(random.getrandbits(1)):
                await ctx.send("Ya best be gettin' it!")
            else:
                await ctx.send("Nope, no juicy chicken today.")
        else:
            await ctx.send("It's not Monday :(")

    @commands.guild_only()
    @checks.mod()
    @_bmm.command(name="timezone", aliases=["tz"])
    async def _bmm_timezone(self, ctx: commands.Context, timezone: str):
        """Sets the timezone to handle days across the Earth."""
        if timezone not in zoneinfo.available_timezones():
            await ctx.send("That's not a valid timezone!")
            return
        await self.config.guild(ctx.guild).timezone.set(timezone)
        await ctx.send("Timezone updated!")
