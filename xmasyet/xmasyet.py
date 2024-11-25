from datetime import time

from discord.ext import tasks
from redbot.core import commands, Config, checks
from redbot.core.bot import Red


class XMASYetCog(commands.Cog):
    """XMASYet Cog"""

    async def debug(self, message: str):
        out = self.bot.get_channel(int(await self.config.debug()))
        if out is not None:
            await out.send(message)

    @tasks.loop(time=time(hour=11, minute=59))
    async def ask_xmasyet(self):
        await self.debug(f'[XMASYet] Firing!')
        async with self.config.channels() as channels:
            for cid, val in channels.items():
                if val:
                    c = self.bot.get_channel(int(cid))
                    if c is not None:
                        await c.send("Is it Christmas yet?")
                    else:
                        await self.debug(f'[XMASYet] None channel: {cid}')
                else:
                    await self.debug(f'[XMASYet] Disabled channel: {cid}')

    def __init__(self, bot: Red):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=1289862744207523841005)

        global_default_config = {
            "debug": "",
            "channels": {}
        }

        self.config.register_global(**global_default_config)

        self.debug(f'[XMASYet] Loading timed task!')
        self.ask_xmasyet.start()

    @commands.guild_only()
    @checks.mod()
    @commands.group(name="xmasyet")
    async def _xmasyet(self, ctx: commands.Context):
        pass

    @_xmasyet.command("enable")
    async def _xmasyet_enable(self, ctx: commands.Context, enable: bool):
        """Enables or disables the cog for the channel. [p]xmasyet enable <true|false>"""
        async with self.config.channels() as channels:
            channels[str(ctx.channel.id)] = enable
        await ctx.channel.send(f"XMASYet enabled: {enable}!")

    @checks.is_owner()
    @_xmasyet.command("debug")
    async def _xmasyet_debug(self, ctx: commands.Context):
        """Sets the global debug output channel. [p]xmasyet debug"""
        await self.config.debug.set(str(ctx.channel.id))
        await ctx.channel.send(f"XMASYet debug output set to this channel!")

    @checks.is_owner()
    @_xmasyet.command("set")
    async def _xmasyet_set(self, ctx: commands.Context, hour: int, minute: int):
        """Updates the daily run time. [p]xmasyet set <hours> <minutes>"""
        self.ask_xmasyet.change_interval(time=time(hour=hour, minute=minute))
        await ctx.channel.send(f"XMASYet run time updated!")
