from datetime import date
import random

from redbot.core import commands, Config


class BMMCog(commands.Cog):
    """BMM Cog"""

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=1289862744207523841004)

    @commands.command("bmm")
    async def countdown(self, ctx: commands.Context):
        if date.today().weekday() == 0:
            if bool(random.getrandbits(1)):
                await ctx.send("Ya best be gettin' it!")
            else:
                await ctx.send("Nope, no juicy chicken today.")
        else:
            await ctx.send("It's not Monday :(")
