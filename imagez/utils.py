import urllib.request
import uuid
from datetime import datetime
from pathlib import Path

import discord
from redbot.core import commands, Config

from imagez.abstracts import FileWrapperABC, ImagezConfigHelperABC


class FileWrapper(FileWrapperABC):

    @classmethod
    def new(cls, ctx: commands.Context, guid: str, name: str, installer: int, installed: int):
        return cls(
            guid=guid,
            name=name,
            installer=installer,
            installed=installed
        )

    @classmethod
    def from_storage(cls, ctx: commands.Context, data: dict):
        return cls(
            guid=data['guid'],
            name=data['name'],
            installer=data['installer'],
            installed=data['installed']
        )

    def to_dict(self):
        return {
            "guid": self.guid,
            "name": self.name,
            "installer": self.installer,
            "installed": self.installed
        }


class ImagezConfigHelper(ImagezConfigHelperABC):

    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.config = Config.get_conf(self, identifier=1289862744207523841003, cog_name="ImagezCog")
        self.config.register_guild(fonts={}, images={})

        self.fonts_path = self.base_path / "fonts/"
        if not self.fonts_path.exists():
            self.fonts_path.mkdir()
        elif not self.fonts_path.is_dir():
            print("Font path is not a directory!")

        self.image_path = self.base_path / "images/"
        if not self.image_path.exists():
            self.image_path.mkdir()
        elif not self.image_path.is_dir():
            print("Image path is not a directory!")

    async def download_file(self, ctx: commands.Context, file_context: str, link: str, name: str,
                            installer: discord.User) -> FileWrapper:
        guid = uuid.uuid4().__str__()
        file_name = f"{guid}"
        if file_context == "font":
            file_name += ".ttf"
            file_path = self.fonts_path / file_name
        elif file_context == "image":
            file_name += ".png"
            file_path = self.image_path / file_name
        else:
            file_path = self.base_path / file_name
            print(f"Warning: Unknown file context ({file_context}), "
                  f"saving to base cog path. File will be unusable. GUID: {guid}.")

        urllib.request.urlretrieve(link, filename=file_path.resolve())

        time = int(datetime.utcnow().timestamp())
        wrapper = FileWrapper.new(ctx, guid, name, installer.id, time)
        async with getattr(self.config.guild(ctx.guild), f"{file_context}s")() as filedata:
            filedata[name] = wrapper.to_dict()

        return wrapper
