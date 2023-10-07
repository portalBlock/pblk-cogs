import random

import discord
from redbot.core import commands, Config, checks


class UnflipperCog(commands.Cog):
    """Unflipper Cog"""

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=1289862744207523841001)

        guild_default_config = {
            "enabled": False,
            "random": True,
            "random_percent": 0.25
        }

        self.config.register_guild(**guild_default_config)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot or not message.guild:
            return
        if not await self.config.guild(message.guild).enabled():
            return
        if "(╯°□°)╯︵ ┻━┻" in message.content or "(ノಠ益ಠ)ノ彡┻━┻" in message.content:
            if await self.config.guild(message.guild).random():
                conf_percent = await self.config.guild(message.guild).random_percent()
                percentage_chance = 1 - conf_percent
                if random.random() < percentage_chance:
                    return
            await message.channel.send(content="┬─┬ノ( º _ ºノ)")

    @commands.guild_only()
    @checks.mod()
    @commands.group(name="unflipper")
    async def _unflipper(self, ctx: commands.Context):
        pass

    @_unflipper.command("enable")
    async def unflipper_enable(self, ctx: commands.Context, enable: bool):
        """Enables or disables the cog for the guild. [p]unflipper enable <true|false>"""
        await self.config.guild(ctx.guild).enabled.set(enable)
        await ctx.channel.send(f"Unflipper enabled: {enable}!")

    @_unflipper.group(name="random")
    async def _unflipper_random(self, ctx: commands.Context):
        pass

    @_unflipper_random.command("enable")
    async def unflipper_random_enable(self, ctx: commands.Context, enable: bool):
        """Enables or disables random unflipping for the guild. [p]unflipper random enable <true|false>"""
        await self.config.guild(ctx.guild).random.set(enable)
        await ctx.channel.send(f"Unflipper random enabled: {enable}!")

    @_unflipper_random.command("percent")
    async def unflipper_random_percent(self, ctx: commands.Context, percent: int):
        """Enables or disables the cog for the guild. [p]unflipper random percent <percent as integer>"""
        await self.config.guild(ctx.guild).random_percent.set(percent / 100)
        await ctx.channel.send(f"Unflipper random percent: {percent}%")
