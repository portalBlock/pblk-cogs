import zoneinfo
import datetime

from discord.ext import tasks
from redbot.core import commands, Config, checks


class NotifiCog(commands.Cog):
    """Notifi Cog"""

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=1289862744207523841006)

        guild_default_config = {
            "timezone": "UTC",
            "messages": {
                "0": {
                    "0": [
                        {
                            "channel_id": "123",
                            "name": "",
                            "message": "Default message!"
                        }
                    ]
                }
            }
        }

        self.config.register_guild(**guild_default_config)

        self.notifi_task.start()

    def cog_unload(self) -> None:
        self.notifi_task.cancel()

    @tasks.loop(time=datetime.time(minute=1, tzinfo=datetime.timezone.utc))
    async def notifi_task(self):
        await self.run_tasker()

    async def run_tasker(self):
        now = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
        for gid, gconfig in (await self.config.all_guilds()).items():
            localized = now.astimezone(zoneinfo.ZoneInfo(gconfig['timezone']))
            for hour, hfig in gconfig['messages'].items():
                if localized.hour == int(hour):
                    for minute, mfig in hfig.items():
                        if localized.minute == int(minute):
                            for message in mfig:
                                c = self.bot.get_channel(int(message['channel_id']))
                                if c is not None:
                                    await c.send(message['message'])

    @commands.guild_only()
    @checks.mod()
    @commands.group(name="notifi", pass_context=True)
    async def _notifi(self, ctx: commands.Context):
        pass

    @_notifi.command(name="add")
    async def _notifi_add(self, ctx: commands.Context, hour: int, minute: int, name: str, *, message: str):
        """Add a scheduled notification."""
        async with self.config.guild(ctx.guild).messages() as conf:
            if str(hour) not in conf:
                conf[str(hour)] = {}
            if str(minute) not in conf[str(hour)]:
                conf[str(hour)][str(minute)] = []
            conf[str(hour)][str(minute)].append({"name": name, "channel_id": str(ctx.channel.id), "message": message})
        await ctx.send("")

    @_notifi.command(name="timezone", aliases=["tz"])
    async def _notifi_timezone(self, ctx: commands.Context, timezone: str):
        """Sets the timezone to handle time across the Earth."""
        if timezone not in zoneinfo.available_timezones():
            await ctx.send("That's not a valid timezone!")
            return
        await self.config.guild(ctx.guild).timezone.set(timezone)
        await ctx.send("Timezone updated!")
