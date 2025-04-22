from typing import Any
from abc import ABC, abstractmethod

from utility import PypenguinClass

class FRCostume(PypenguinClass):
    _grepr = True
    _grepr_fields = ["name", "asset_id", "data_format", "md5ext", "rotation_center_x", "rotation_center_y", "bitmap_resolution"]
    
    name: str
    asset_id: str
    data_format: str
    md5ext: str
    rotation_center_x: int | float
    rotation_center_y: int | float
    bitmap_resolution: int | None
    
    def __init__(self, 
        name: str,
        asset_id: str,
        data_format: str,
        md5ext: str,
        rotation_center_x: int | float,
        rotation_center_y: int | float,
        bitmap_resolution: int | None,
    ):
        self.name              = name
        self.asset_id          = asset_id
        self.data_format       = data_format
        self.md5ext            = md5ext
        self.rotation_center_x = rotation_center_x
        self.rotation_center_y = rotation_center_y
        self.bitmap_resolution = bitmap_resolution

    @classmethod
    def from_data(cls, data: dict[str, Any]) -> "FRCostume":
        self = cls(
            name              = data["name"           ],
            asset_id          = data["assetId"        ],
            data_format       = data["dataFormat"     ],
            md5ext            = data["md5ext"         ],
            rotation_center_x = data["rotationCenterX"],
            rotation_center_y = data["rotationCenterY"],
            bitmap_resolution = data.get("bitmapResolution", None),
        )
        return self

    def step(self) -> "SRCostume":
        return SRCostume(
            name              = self.name,
            file_extension    = self.data_format,
            rotation_center   = (self.rotation_center_x, self.rotation_center_y),
            bitmap_resolution = 1 if self.bitmap_resolution is None else self.bitmap_resolution,
        )

class FRSound(PypenguinClass):
    _grepr = True
    _grepr_fields = ["name", "asset_id", "data_format", "md5ext", "rate", "sample_count"]
    
    name: str
    asset_id: str
    data_format: str
    md5ext: str
    rate: int
    sample_count: int
    
    def __init__(self, 
        name: str,
        asset_id: str,
        data_format: str,
        md5ext: str,
        rate: int,
        sample_count: int,
    ):
        self.name         = name
        self.asset_id     = asset_id
        self.data_format  = data_format
        self.md5ext       = md5ext
        self.rate         = rate
        self.sample_count = sample_count

    @classmethod
    def from_data(cls, data: dict[str, Any]) -> "FRSound":
        self = cls(
            name         = data["name"       ],
            asset_id     = data["assetId"    ],
            data_format  = data["dataFormat" ],
            md5ext       = data["md5ext"     ],
            rate         = data["rate"       ],
            sample_count = data["sampleCount"],
        )
        return self

    def step(self) -> "SRSound":
        return SRSound(
            name           = self.name,
            file_extension = self.data_format,
            # Other attributes can be derived from the sound files.
        )

class SRCostume(PypenguinClass):
    _grepr = True
    _grepr_fields = ["name", "file_extension", "rotation_center", "bitmap_resolution"]

    name: str
    file_extension: str
    rotation_center: tuple[int | float, int | float]
    bitmap_resolution: int

    def __init__(self, 
        name: str, 
        file_extension: str,
        rotation_center: tuple[int | float, int | float],
        bitmap_resolution: int,
    ):
        self.name              = name
        self.file_extension    = file_extension
        self.rotation_center   = rotation_center
        self.bitmap_resolution = bitmap_resolution

class SRSound(PypenguinClass):
    _grepr = True
    _grepr_fields = ["name", "file_extension"]

    name: str
    file_extension: str

    def __init__(self, name: str, file_extension: str):
        self.name           = name
        self.file_extension = file_extension

