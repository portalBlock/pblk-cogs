from redbot.core.bot import Red

from .notifi import NotifiCog


async def setup(bot: Red):
    await bot.add_cog(NotifiCog(bot))
