from typing      import Any
from dataclasses import dataclass

from pypenguin.utility import GreprClass, ThanksError

SCRATCH_SEMVER = "3.0.0"

SCRATCH_META_DATA = {
    "semver": SCRATCH_SEMVER,
    "vm": "11.1.0",
    "agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
}

PENGUINMOD_META_DATA = {
    "semver": SCRATCH_SEMVER,
    "vm": "0.2.0",
    "agent": "",
    "platform": {
        "name": "PenguinMod",
        "url": "https://penguinmod.com/",
        "version": "stable",
    },
}

@dataclass(repr=False)
class FRMeta(GreprClass):
    """
    The first representation for the metadata of a project
    """
    _grepr = True
    _grepr_fields = ["semver", "vm", "agent", "platform"]
    
    semver: str
    vm: str
    agent: str
    platform: "FRPenguinModPlatformMeta | None"

    @classmethod
    def from_data(cls, data: dict[str, Any]) -> "FRMeta":
        """
        Deserializes raw data into a FRMeta.
        
        Args:
            data: the raw data
        
        Returns:
            the FRMeta
        """
        return cls(
            semver = data["semver"],
            vm     = data["vm"    ],
            agent  = data["agent" ],
            platform = FRPenguinModPlatformMeta.from_data(data["platform"]) if "platform" in data else None,
        )
    
    def __post_init__(self) -> None:
        """
        Ensure the metadata is valid.
        
        Returns:
            None
        """
        if (self.semver != SCRATCH_SEMVER) or ((self.vm != SCRATCH_META_DATA["vm"]) and (self.vm != PENGUINMOD_META_DATA["vm"])):
            # agent can be anything i don't care
            raise ThanksError()

@dataclass(repr=False)
class FRPenguinModPlatformMeta(GreprClass):
    """
    The first representation for the metadata of the penguinmod platform
    """
    _grepr = True
    _grepr_fields = ["name", "url", "version"]
    
    name: str
    url: str
    version: str

    @classmethod
    def from_data(cls, data: dict[str, str]) -> "FRPenguinModPlatformMeta":
        """
        Deserializes raw data into a FRPenguinModPlatformMeta.
        
        Args:
            data: the raw data
        
        Returns:
            the FRPenguinModPlatformMeta
        """
        return cls(
            name    = data["name"   ],
            url     = data["url"    ],
            version = data["version"],
        )
    
    def __post_init__(self) -> None:
        """
        Ensure the metadata is valid.
        
        Returns:
            None
        """
        if (   (self.name != PENGUINMOD_META_DATA["platform"]["name"])
            or (self.url != PENGUINMOD_META_DATA["platform"]["url"])
            or (self.version != PENGUINMOD_META_DATA["platform"]["version"])):
            raise ThanksError()
            
