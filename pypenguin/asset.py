from typing import Any
from abc import ABC, abstractmethod

from utility import PypenguinClass

class FRAsset(PypenguinClass, ABC):
    _grepr = True
    _grepr_fields = ["name", "asset_id", "data_format", "md5ext"]
    
    name: str
    asset_id: str
    data_format: str
    md5ext: str
    
    @classmethod
    def from_data(cls, data: dict[str, str]) -> "FRAsset":
        self = cls()
        self.name              = data["name"           ]
        self.asset_id          = data["assetId"        ]
        self.data_format       = data["dataFormat"     ]
        self.md5ext            = data["md5ext"         ]
        return self

    @abstractmethod
    def step(self) -> "SRAsset": pass


class FRCostume(FRAsset):
    _grepr_fields = FRAsset._grepr_fields + ["rotation_center_x", "rotation_center_y", "bitmap_resolution"]
    
    rotation_center_x: int | float
    rotation_center_y: int | float
    bitmap_resolution: int | None
    
    @classmethod
    def from_data(cls, data: dict[str, Any]) -> "FRCostume":
        self = super().from_data(data)
        self.rotation_center_x = data["rotationCenterX"]
        self.rotation_center_y = data["rotationCenterY"]
        self.bitmap_resolution = data.get("bitmapResolution", None)
        return self

    def step(self) -> "SRCostume":
        return SRCostume(
            name              = self.name,
            file_extension    = self.data_format,
            rotation_center   = (self.rotation_center_x, self.rotation_center_y),
            bitmap_resolution = 1 if self.bitmap_resolution is None else self.bitmap_resolution,
        )


class FRSound(FRAsset):
    _grepr = True
    _grepr_fields = FRAsset._grepr_fields + ["rate", "sample_count"]
    
    rate: int
    sample_count: int
    
    @classmethod
    def from_data(cls, data: dict[str, Any]) -> "FRSound":
        self = super().from_data(data)
        self.rate         = data["rate"       ]
        self.sample_count = data["sampleCount"]
        return self

    def step(self) -> "SRSound":
        return SRSound(
            name           = self.name,
            file_extension = self.data_format,
            # Other attributes can be derived from the sound files.
        )


class SRAsset(PypenguinClass):
    _grepr = True
    _grepr_fields = ["name", "file_extension"]

    name: str
    file_extension: str

    def __init__(self, name: str, file_extension: str):
        self.name = name
        self.file_extension = file_extension

class SRCostume(SRAsset):
    _grepr_fields = SRAsset._grepr_fields + ["rotation_center", "bitmap_resolution"]

    rotation_center: tuple[int | float, int | float]
    bitmap_resolution: int

    def __init__(self, 
        name: str, 
        file_extension: str,
        rotation_center: tuple[int | float, int | float],
        bitmap_resolution: int,
    ):
        super().__init__(name=name, file_extension=file_extension)
        self.rotation_center   = rotation_center
        self.bitmap_resolution = bitmap_resolution

class SRSound(SRAsset):
    _grepr_fields = SRAsset._grepr_fields + []

    def __init__(self, name: str, file_extension: str):
        super().__init__(name=name, file_extension=file_extension)

