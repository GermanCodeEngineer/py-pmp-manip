class FLMeta:
    _grepr = True
    _grepr_fields = ["semver", "vm", "agent", "platform"]
    
    semver: str
    vm: str
    agent: str
    platform: "FLPlatform"
    
    @classmethod
    def from_data(cls, data):
        self = cls()
        self.semver = data["semver"]
        self.vm     = data["vm"    ]
        self.agent  = data["agent" ]
        self.platform = FLPlatform.from_data(data["platform"])
        return self


class FLPlatform:
    _grepr = True
    _grepr_fields = ["name", "url", "version"]
    
    name: str
    url: str
    version: str
    
    @classmethod
    def from_data(cls, data):
        self = cls()
        self.name    = data["name"   ]
        self.url     = data["url"    ]
        self.version = data["version"]
        return self
