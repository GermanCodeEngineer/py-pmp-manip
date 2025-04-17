from typing import Any

from utility import PypenguinClass

class FRMeta(PypenguinClass):
    _grepr = True
    _grepr_fields = ["semver", "vm", "agent", "platform"]
    
    semver: str
    vm: str
    agent: str
    platform: "FRPlatform"
    
    @classmethod
    def from_data(cls, data: dict[str, Any]) -> "FRMeta":
        self = cls()
        self.semver = data["semver"]
        self.vm     = data["vm"    ]
        self.agent  = data["agent" ]
        self.platform = FRPlatform.from_data(data["platform"])
        return self


class FRPlatform(PypenguinClass):
    _grepr = True
    _grepr_fields = ["name", "url", "version"]
    
    name: str
    url: str
    version: str
    
    @classmethod
    def from_data(cls, data: dict[str, str]) -> "FRPlatform":
        self = cls()
        self.name    = data["name"   ]
        self.url     = data["url"    ]
        self.version = data["version"]
        return self
