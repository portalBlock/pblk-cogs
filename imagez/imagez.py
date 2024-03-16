from redbot.core import commands, Config
from redbot.core.data_manager import cog_data_path

from imagez.utils import ImagezConfigHelper


# This is a trial for some Labbot thing, I'm just doing a trial here.


class ImagezCog(commands.Cog):
    """Imagez Cog"""

    def __init__(self, bot, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot = bot
        self._base_path = cog_data_path(self)

        self.config = ImagezConfigHelper(self._base_path)

    @commands.group("imagez", pass_context=True)
    def _imagez(self, ctx: commands.Context):
        """Manages the imagez data"""
        pass

    @_imagez.group("font")
    def _imagez_font(self):
        """Manages imagez fonts."""
        pass

    @_imagez_font.command("download")
    def _imagez_font_download(self, ctx: commands.Context, name: str, link: str):
        """Downloads a font for use in images."""
        if not link.startswith("https://") or not link.endswith(".ttf"):
            await ctx.send("Error! You need to specify an HTTPS link ending with `.ttf`.")
            return
        wrapper = await self.config.download_file(ctx, "font", link, name, ctx.author)
        await ctx.send(f"Downloaded `{wrapper.name}` as `{wrapper.guid}`.")

    @_imagez_font.command("delete")
    def _imagez_font_delete(self, ctx: commands.Context, name: str):
        """Deletes a font from the system."""
        pass
