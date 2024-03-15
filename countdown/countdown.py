from datetime import datetime

from redbot.core import commands, Config


class CountdownCog(commands.Cog):
    """Countdown Cog"""

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=1289862744207523841002)

    @commands.command("countdown")
    async def countdown(self, ctx: commands.Context):
        now = datetime.now()
        later = datetime(year=2024, month=3, day=14, hour=16, minute=30)
        diff = later - now
        hours, remainder = divmod(diff.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        await ctx.send(f"{hours} hours, {minutes} minutes, and {seconds} seconds left!!!")
