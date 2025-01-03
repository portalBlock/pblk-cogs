import zoneinfo
import datetime

from discord.ext import tasks
from redbot.core import commands, Config, checks
from redbot.core.bot import Red


class NotifiCog(commands.Cog):
    """Notifi Cog"""

    def __init__(self, bot: Red):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=1289862744207523841006)

        guild_default_config = {
            "timezone": "UTC",
            "messages": {}
        }

        self.config.register_guild(**guild_default_config)

        self.notifi_task.start()

    def cog_unload(self) -> None:
        self.notifi_task.cancel()

    @tasks.loop(minutes=1)
    async def notifi_task(self):
        await self.run_tasker()

    async def run_tasker(self):
        now = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
        for guild in self.bot.guilds:
            messages = await self.config.guild(guild).messages()
            timezone = await self.config.guild(guild).timezone()
            localized = now.astimezone(zoneinfo.ZoneInfo(timezone))
            day = str(localized.weekday())
            hour = str(localized.hour)
            minute = str(localized.minute)
            if day in messages and hour in messages[day] and minute in messages[day][hour]:
                for msg in messages[day][hour][minute]:
                    cid = msg['channel_id']
                    c = self.bot.get_channel(int(cid))
                    if c is not None:
                        await c.send(msg['message'])

    @commands.guild_only()
    @checks.mod()
    @commands.group(name="notifi", pass_context=True)
    async def _notifi(self, ctx: commands.Context):
        pass

    @_notifi.command(name="add")
    async def _notifi_add(self, ctx: commands.Context, day: str, hour: str, minute: str, name: str, *, message: str):
        """Add a scheduled notification."""
        async with self.config.guild(ctx.guild).messages() as messages:
            new = {"name": name, "channel_id": ctx.channel.id, "message": message}
            if day not in message:
                messages[day] = {}
            if hour not in messages[day]:
                messages[day][hour] = {}
            if minute not in messages[day][hour]:
                messages[day][hour][minute] = []
            messages[day][hour][minute].append(new)
        await ctx.send("Scheduled message added!")

    @_notifi.command(name="timezone", aliases=["tz"])
    async def _notifi_timezone(self, ctx: commands.Context, timezone: str):
        """Sets the timezone to handle time across the Earth."""
        if timezone not in zoneinfo.available_timezones():
            await ctx.send("That's not a valid timezone!")
            return
        await self.config.guild(ctx.guild).timezone.set(timezone)
        await ctx.send("Timezone updated!")

    @_notifi.command(name="fire")
    async def _notifi_fire(self, ctx: commands.Context):
        """Sets the timezone to handle time across the Earth."""
        await ctx.send("Manually firing!")
        await self.run_tasker()
