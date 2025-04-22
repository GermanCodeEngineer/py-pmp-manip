from typing import Any

from utility import PypenguinClass

class FRMeta(PypenguinClass):
    _grepr = True
    _grepr_fields = ["semver", "vm", "agent", "platform"]
    
    semver: str
    vm: str
    agent: str
    platform: "FRPlatform"
    
    def __init__(self, 
        semver: str,
        vm: str,
        agent: str,
        platform: "FRPlatform",
    ):
        self.semver   = semver
        self.vm       = vm
        self.agent    = agent
        self.platform = platform

    @classmethod
    def from_data(cls, data: dict[str, Any]) -> "FRMeta":
        return cls(
            semver = data["semver"],
            vm     = data["vm"    ],
            agent  = data["agent" ],
            platform = FRPlatform.from_data(data["platform"]),
        )


class FRPlatform(PypenguinClass):
    _grepr = True
    _grepr_fields = ["name", "url", "version"]
    
    name: str
    url: str
    version: str
    
    def __init__(self, 
        name: str,
        url: str,
        version: str,
    ):
        self.name    = name
        self.url     = url
        self.version = version

    @classmethod
    def from_data(cls, data: dict[str, str]) -> "FRPlatform":
        return cls(
            name    = data["name"   ],
            url     = data["url"    ],
            version = data["version"],
        )
