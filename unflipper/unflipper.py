import random

import discord
from redbot.core import commands, Config, checks

flips = [
    "(╯°□°)╯︵ ┻━┻",
    "(ノಠ益ಠ)ノ彡┻━┻",
    "(┛ಠ_ಠ)┛彡┻━┻"
]


class UnflipperCog(commands.Cog):
    """Unflipper Cog"""

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=1289862744207523841001)

        guild_default_config = {
            "enabled": False,
            "random": True,
            "random_percent": 0.25,
            "enhanced_users": []
        }

        self.config.register_guild(**guild_default_config)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot or not message.guild:
            return
        if not await self.config.guild(message.guild).enabled():
            return
        unflip = False
        async with self.config.guild(message.guild).enhanced_users() as users:
            notascii = 0
            if message.author.id in users:
                for c in message.content:
                    if ord(c) > 127:
                        notascii += 1
                if notascii / len(message.content) > 0.5:
                    unflip = True
            else:
                for flip in flips:
                    if flip in message.content:
                        unflip = True
            if unflip:
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

    @_unflipper.group(name="enhanced")
    async def _unflipper_enhanced(self, ctx: commands.Context):
        pass

    @_unflipper_enhanced.command("add")
    async def _unflipper_enhanced_add(self, ctx: commands.Context, user: discord.Member):
        """Adds a user to the enhanced detection list for the guild."""
        async with self.config.guild(ctx.guild).enhanced_users() as users:
            if user.id not in users:
                users.append(user.id)
                await ctx.send("User added to enhanced detection!")
            else:
                await ctx.send("User already in enhanced detection list.")

    @_unflipper_enhanced.command("delete")
    async def _unflipper_enhanced_delete(self, ctx: commands.Context, user: discord.Member):
        """Deletes a user from the enhanced detection list for the guild."""
        async with self.config.guild(ctx.guild).enhanced_users() as users:
            users.remove(user.id)
        await ctx.send("User removed from enhanced detection!")
