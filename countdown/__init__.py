from redbot.core.bot import Red

from .countdown import CountdownCog


async def setup(bot: Red):
    await bot.add_cog(CountdownCog(bot))
