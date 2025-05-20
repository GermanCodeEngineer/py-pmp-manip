from typing      import Any
from dataclasses import dataclass

from pypenguin.utility import GreprClass, ValidationConfig
from pypenguin.utility import AA_TYPE, AA_COORD_PAIR, AA_MIN

@dataclass(repr=False)
class FRCostume(GreprClass):
    """
    The first representation for a costume. It is very close to the raw data in a project
    """
    _grepr = True
    _grepr_fields = ["name", "asset_id", "data_format", "md5ext", "rotation_center_x", "rotation_center_y", "bitmap_resolution"]
    
    name: str
    asset_id: str
    data_format: str
    md5ext: str
    rotation_center_x: int | float
    rotation_center_y: int | float
    bitmap_resolution: int | None

    @classmethod
    def from_data(cls, data: dict[str, Any]) -> "FRCostume":
        """
        Deserializes raw data into a FRSound.
        
        Args:
            data: the raw data
        
        Returns:
            the FRSound
        """
        return cls(
            name              = data["name"           ],
            asset_id          = data["assetId"        ],
            data_format       = data["dataFormat"     ],
            md5ext            = data["md5ext"         ],
            rotation_center_x = data["rotationCenterX"],
            rotation_center_y = data["rotationCenterY"],
            bitmap_resolution = data.get("bitmapResolution", None),
        )

    def step(self) -> "SRCostume":
        """
        Converts a FRComment into a SRComment.
        
        Returns:
            the SRComment
        """
        return SRCostume(
            name              = self.name,
            file_extension    = self.data_format,
            rotation_center   = (self.rotation_center_x, self.rotation_center_y),
            bitmap_resolution = 1 if self.bitmap_resolution is None else self.bitmap_resolution,
        )

@dataclass(repr=False)
class FRSound(GreprClass):
    """
    The first representation for a sound. It is very close to the raw data in a project
    """
    _grepr = True
    _grepr_fields = ["name", "asset_id", "data_format", "md5ext", "rate", "sample_count"]
    
    name: str
    asset_id: str
    data_format: str
    md5ext: str
    rate: int
    sample_count: int
    
    @classmethod
    def from_data(cls, data: dict[str, Any]) -> "FRSound":
        """
        Deserializes raw data into a FRSound
        
        Args:
            data: the raw data
        
        Returns:
            the FRSound
        """
        return cls(
            name         = data["name"       ],
            asset_id     = data["assetId"    ],
            data_format  = data["dataFormat" ],
            md5ext       = data["md5ext"     ],
            rate         = data["rate"       ],
            sample_count = data["sampleCount"],
        )

    def step(self) -> "SRSound":
        """
        Converts a FRSound into a SRSound
        
        Returns:
            the SRSound
        """
        return SRSound(
            name           = self.name,
            file_extension = self.data_format,
            # Other attributes can be derived from the sound files.
        )

@dataclass(repr=False)
class SRCostume(GreprClass):
    """
    The second representation for a costume. It is more user friendly then the first representation.
    """
    _grepr = True
    _grepr_fields = ["name", "file_extension", "rotation_center", "bitmap_resolution"]

    name: str
    file_extension: str
    rotation_center: tuple[int | float, int | float]
    bitmap_resolution: int
    
    
    @classmethod
    def create_empty(cls, name: str = "empty") -> "SRCostume":
        return cls(
            name=name,
            file_extension="svg",
            rotation_center=(0,0),
            bitmap_resolution=1,
        )
    
    def validate(self, path: list, config: ValidationConfig) -> None:
        """
        Ensure a SRCostume is valid, raise ValidationError if not.
        
        Args:
            path: the path from the project to itself. Used for better errors
            config: Configuration for Validation Behaviour
        
        Returns:
            None
        """
        AA_TYPE(self, path, "name", str)
        AA_TYPE(self, path, "file_extension", str)
        AA_COORD_PAIR(self, path, "rotation_center")
        AA_TYPE(self, path, "bitmap_resolution", int)
        AA_MIN(self, path, "bitmap_resolution", min=1)

@dataclass(repr=False)
class SRSound(GreprClass):
    """
    The second representation for a sound. It is more user friendly then the first representation.
    """
    _grepr = True
    _grepr_fields = ["name", "file_extension"]

    name: str
    file_extension: str
    
    def validate(self, path: list, config: ValidationConfig) -> None:
        """
        Ensure a SRSound is valid, raise ValidationError if not.
        
        Args:
            path: the path from the project to itself. Used for better errors
            config: Configuration for Validation Behaviour
        
        Returns:
            None
        """
        AA_TYPE(self, path, "name", str)
        AA_TYPE(self, path, "file_extension", str)


__all__ = ["FRCostume", "FRSound", "SRCostume", "SRSound"]

