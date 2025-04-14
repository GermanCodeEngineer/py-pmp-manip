class FRAsset:
    _grepr = True
    _grepr_fields = ["name", "asset_id", "data_format", "md5ext"]
    
    name: str
    asset_id: str
    data_format: str
    md5ext: str
    
    @classmethod
    def from_data(cls, data):
        self = cls()
        self.name              = data["name"           ]
        self.asset_id          = data["assetId"        ]
        self.data_format       = data["dataFormat"     ]
        self.md5ext            = data["md5ext"         ]
        return self

class FRCostume(FRAsset):
    _grepr_fields = FRAsset._grepr_fields + ["rotation_center_x", "rotation_center_y", "bitmap_resolution"]
    
    rotation_center_x: int | float
    rotation_center_y: int | float
    bitmap_resolution: int | None
    
    @classmethod
    def from_data(cls, data):
        self = super().from_data(data)
        self.rotation_center_x = data["rotationCenterX"]
        self.rotation_center_y = data["rotationCenterY"]
        self.bitmap_resolution = data.get("bitmapResolution", None)
        return self


class FRSound(FRAsset):
    _grepr = True
    _grepr_fields = FRAsset._grepr_fields + ["rate", "sample_count"]
    
    rate: int
    sample_count: int
    
    @classmethod
    def from_data(cls, data):
        self = super().from_data(data)
        self.rate         = data["rate"       ]
        self.sample_count = data["sampleCount"]
        return self


