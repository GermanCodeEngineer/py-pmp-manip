class FLMeta:
    _grepr = True
    _grepr_fields = ["semver", "vm", "agent", "platform"]
    @staticmethod
    def from_data(data):
        return FLMeta(data)
    
    def __init__(self, data):
        self.semver = data["semver"]
        self.vm     = data["vm"    ]
        self.agent  = data["agent" ]
        self.platform = FLPlatform.from_data(data["platform"])


class FLPlatform:
    _grepr = True
    _grepr_fields = ["name", "url", "version"]
    @staticmethod
    def from_data(data):
        return FLPlatform(data)
    
    def __init__(self, data):
        self.name    = data["name"   ]
        self.url     = data["url"    ]
        self.version = data["version"]
