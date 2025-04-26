from typing      import Any
from dataclasses import dataclass

from utility import GreprClass

@dataclass
class FRMeta(GreprClass):
    _grepr = True
    _grepr_fields = ["semver", "vm", "agent", "platform"]
    
    semver: str
    vm: str
    agent: str
    platform: "FRPlatform"

    @classmethod
    def from_data(cls, data: dict[str, Any]) -> "FRMeta":
        return cls(
            semver = data["semver"],
            vm     = data["vm"    ],
            agent  = data["agent" ],
            platform = FRPlatform.from_data(data["platform"]),
        )

@dataclass
class FRPlatform(GreprClass):
    _grepr = True
    _grepr_fields = ["name", "url", "version"]
    
    name: str
    url: str
    version: str

    @classmethod
    def from_data(cls, data: dict[str, str]) -> "FRPlatform":
        return cls(
            name    = data["name"   ],
            url     = data["url"    ],
            version = data["version"],
        )
