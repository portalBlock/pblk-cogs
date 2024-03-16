import urllib.request
import uuid
from abc import ABC, abstractmethod
from pathlib import Path

import discord
from redbot.core import commands, Config


# Credit to github.com/rHomeLab/Labbot-Cogs Notes cog author(s) for this structure


class FileWrapperABC(ABC):
    guid: str
    name: str
    installer: int
    installed: int

    def __init__(self, **kwargs):
        if kwargs.keys() != self.__annotations__.keys():
            raise Exception("Invalid kwargs provided")

        for key, val in kwargs.items():
            expected_type: type = self.__annotations__[key]
            if not isinstance(val, expected_type):
                raise TypeError(f"Expected type {expected_type} for kwarg {key!r}, got type {type(val)} instead")

            setattr(self, key, val)

    @classmethod
    @abstractmethod
    def new(cls, ctx: commands.Context, guid: str, name: str, installer: int, installed: int):
        """Creates a new instance of this type."""
        pass

    @classmethod
    @abstractmethod
    def from_storage(cls, ctx: commands.Context, data: dict):
        """Constructs a new instance of this type from config data."""
        pass

    @abstractmethod
    def to_dict(self):
        """Returns a dictionary representation of the type, suitable for saving to a config."""
        pass


class ImagezConfigHelperABC(ABC):
    config: Config
    base_path: Path

    async def download_file(self, ctx: commands.Context, file_context: str, link: str, name: str,
                            installer: discord.User) -> FileWrapperABC:
        pass
