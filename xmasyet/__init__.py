from redbot.core.bot import Red

from .xmasyet import XMASYetCog


async def setup(bot: Red):
    await bot.add_cog(XMASYetCog(bot))
