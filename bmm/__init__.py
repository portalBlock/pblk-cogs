from redbot.core.bot import Red

from .bmm import BMMCog


async def setup(bot: Red):
    await bot.add_cog(BMMCog(bot))
