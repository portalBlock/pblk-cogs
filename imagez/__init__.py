from redbot.core.bot import Red

from .imagez import ImagezCog


async def setup(bot: Red):
    await bot.add_cog(ImagezCog(bot))
