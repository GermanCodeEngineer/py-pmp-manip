from typing import Any

from pmp_manip.config  import get_config
from pmp_manip.utility import grepr_dataclass, MANIP_ThanksError


PENGUINMOD_PLATFORM_META_DATA = {
    "name": "PenguinMod",
    "url": "https://penguinmod.com/",
    "version": "stable",
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
        Deserializes json_data into a FRMeta
        
        Args:
            data: the json_data
        
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

    def to_data(self) -> dict[str, Any]:
        """
        Serializes a FRMeta into json data
        
        Returns:
            the json data
        """
        data = {
            "semver"  : self.semver,
            "vm"      : self.vm,
            "agent"   : self.agent,
        }
        if self.platform is not None:
            data["platform"] = self.platform.to_data()
        return data

    @classmethod
    def new_scratch_meta(cls) -> "FRMeta":
        """
        Generates a new instance of the scratch project meta
        
        Returns:
            the scratch project meta
        """
        cfg = get_config()
        return FRMeta(
            semver   = cfg.platform_meta.scratch_semver,
            vm       = cfg.platform_meta.scratch_vm,
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
        cfg = get_config()
        return FRMeta(
            semver   = cfg.platform_meta.scratch_semver,
            vm       = cfg.platform_meta.penguinmod_vm,
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
        cfg = get_config()
        if (self.semver != cfg.platform_meta.scratch_semver) or (self.vm not in {cfg.platform_meta.scratch_vm, cfg.platform_meta.penguinmod_vm}):
            # agent can be anything i do not care
            raise MANIP_ThanksError() # project must be older or newer

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
        Deserializes json_data into a FRPenguinModPlatformMeta
        
        Args:
            data: the json_data
        
        Returns:
            the FRPenguinModPlatformMeta
        """
        return cls(
            name    = data["name"   ],
            url     = data["url"    ],
            version = data["version"],
        )
    
    def to_data(self) -> dict[str, Any]:
        """
        Serializes a FRPenguinModPlatformMeta into json data
        
        Returns:
            the json data
        """
        return {
            "name"   : self.name,
            "url"    : self.url,
            "version": self.version,
        }
    
    def __post_init__(self) -> None:
        """
        Ensure the metadata is valid
        
        Returns:
            None
        """

        if (   (self.name != "PenguinMod")
            or (self.url != PENGUINMOD_PLATFORM_META_DATA["url"])
            or (self.version != PENGUINMOD_PLATFORM_META_DATA["version"])
        ):
            raise MANIP_ThanksError()


__all__ = ["FRMeta", "FRPenguinModPlatformMeta"]

