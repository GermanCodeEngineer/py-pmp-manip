from typing import Any

from pypenguin.utility import grepr_dataclass, ThanksError


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

@grepr_dataclass(grepr_fields=["semver", "vm", "agent", "platform"])
class FRMeta:
    """
    The first representation for the metadata of a project
    """
    
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

    @classmethod
    def new_scratch_meta(cls) -> "FRMeta":
        """
        Generates a new instance of the scratch project meta
        
        Returns:
            the scratch project meta
        """
        return FRMeta(
            semver   = SCRATCH_SEMVER,
            vm       = SCRATCH_VM,
            agent    = "",
            platform = None,
        )
    
    @classmethod
    def new_penguinmod_meta(cls) -> "FRMeta":
        """
        Generates a new instance of the penguinmod project meta
        
        Returns:
            the penguinmod project meta
        """
        return FRMeta(
            semver   = SCRATCH_SEMVER,
            vm       = PENGUINMOD_VM,
            agent    = "",
            platform = FRPenguinModPlatformMeta(
                name    = "PenguinMod",
                url     = "https://penguinmod.com/",
                version = "stable",
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

@grepr_dataclass(grepr_fields=["name", "url", "version"])
class FRPenguinModPlatformMeta:
    """
    The first representation for the metadata of the penguinmod platform
    """
    
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

