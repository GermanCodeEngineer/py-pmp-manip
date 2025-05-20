from typing      import Any
from dataclasses import dataclass

from pypenguin.utility import GreprClass, ThanksError

SCRATCH_SEMVER = "3.0.0"

SCRATCH_VM = "11.1.0"

SCRATCH_META_DATA = {
    "semver": SCRATCH_SEMVER,
    "vm": SCRATCH_VM,
    "agent": "", # doesn't matter
}

PENGUINMOD_VM = "0.2.0"

PENGUINMOD_META_DATA = {
    "semver": SCRATCH_SEMVER,
    "vm": PENGUINMOD_VM,
    "agent": "", # always empty
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
        Deserializes raw data into a FRMeta
        
        Args:
            data: the raw data
        
        Returns:
            the FRMeta
        """
        return cls(
            semver   = data["semver"],
            vm       = data["vm"    ],
            agent    = data["agent" ],
            platform = (
                FRPenguinModPlatformMeta.from_data(data["platform"]) 
                if "platform" in data else None
            ),
        )
    
    def __post_init__(self) -> None:
        """
        Ensure the metadata is valid
        
        Returns:
            None
        """
        if (self.semver != SCRATCH_SEMVER) or (self.vm not in {SCRATCH_VM, PENGUINMOD_VM}):
            # agent can be anything i don't care
            raise ThanksError() # project must be older or newer

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
        Deserializes raw data into a FRPenguinModPlatformMeta
        
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
        Ensure the metadata is valid
        
        Returns:
            None
        """
        if (   (self.name != PENGUINMOD_META_DATA["platform"]["name"])
            or (self.url != PENGUINMOD_META_DATA["platform"]["url"])
            or (self.version != PENGUINMOD_META_DATA["platform"]["version"])
        ):
            raise ThanksError()


__all__ = ["FRMeta", "FRPenguinModPlatformMeta"]

