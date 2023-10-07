from redbot.core.bot import Red

from .unflipper import UnflipperCog


async def setup(bot: Red):
    await bot.add_cog(UnflipperCog(bot))
