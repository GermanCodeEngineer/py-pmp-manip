from typing      import Any
from dataclasses import dataclass

from utility import GreprClass

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
    platform: "FRPlatformMeta"

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
            platform = FRPlatformMeta.from_data(data["platform"]),
        )

@dataclass(repr=False)
class FRPlatformMeta(GreprClass):
    """
    The first representation for the metadata of the platform, which is specified in the meta of the project
    """
    _grepr = True
    _grepr_fields = ["name", "url", "version"]
    
    name: str
    url: str
    version: str

    @classmethod
    def from_data(cls, data: dict[str, str]) -> "FRPlatformMeta":
        """
        Deserializes raw data into a FRPlatformMeta.
        
        Args:
            data: the raw data
        
        Returns:
            the FRPlatformMeta
        """
        return cls(
            name    = data["name"   ],
            url     = data["url"    ],
            version = data["version"],
        )
