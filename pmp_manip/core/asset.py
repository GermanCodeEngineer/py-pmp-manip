from abc    import ABC, abstractmethod
from io     import BytesIO
from lxml   import etree
from PIL    import Image, UnidentifiedImageError
from pydub  import AudioSegment
from typing import Any

from pmp_manip.utility import (
    grepr_dataclass, xml_equal, image_equal, generate_md5,
    AA_TYPE, AA_COORD_PAIR, AA_EQUAL,
    MANIP_ThanksError,
)


EMPTY_SVG_COSTUME_XML = '<svg version="1.1" width="2" height="2" viewBox="-1 -1 2 2" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">\n  <!-- Exported by Scratch - http://scratch.mit.edu/ -->\n</svg>'
EMPTY_SVG_COSTUME_ROTATION_CENTER = (240, 180)


@grepr_dataclass(grepr_fields=["name", "asset_id", "data_format", "md5ext", "rotation_center_x", "rotation_center_y", "bitmap_resolution"])
class FRCostume:
    """
    The first representation for a costume. It is very close to the json data in a project
    """
    
    name: str
    asset_id: str
    data_format: str
    md5ext: str
    rotation_center_x: int | float
    rotation_center_y: int | float
    bitmap_resolution: int | None # will always be None, 1 or 2

    @classmethod
    def from_data(cls, data: dict[str, Any]) -> "FRCostume":
        """
        Deserializes json data into a FRCostume
        
        Args:
            data: the json data
        
        Returns:
            the FRCostume
        """
        md5ext = data["md5ext"] if "md5ext" in data else f'{data["assetId"]}.{data["dataFormat"]}'
        return cls(
            name              = data["name"           ],
            asset_id          = data["assetId"        ],
            data_format       = data["dataFormat"     ],
            md5ext            = md5ext,
            rotation_center_x = data["rotationCenterX"],
            rotation_center_y = data["rotationCenterY"],
            bitmap_resolution = data.get("bitmapResolution", None),
        )
    
    def to_data(self) -> dict[str, Any]:
        """
        Serializes a FRCostume into json data
        
        Returns:
            the json data
        """
        data = {
            "name"            : self.name,
            "assetId"         : self.asset_id,
            "dataFormat"      : self.data_format,
            "md5ext"          : self.md5ext,
            "rotationCenterX" : self.rotation_center_x,
            "rotationCenterY" : self.rotation_center_y,
        }
        if self.bitmap_resolution is not None:
            data["bitmapResolution"] = self.bitmap_resolution
        return data
    
    def to_second(self, asset_files: dict[str, bytes]) -> "SRVectorCostume|SRBitmapCostume": 
        """
        Converts a FRCostume into a SRCostume
        
        Args:
            asset_files: the asset files, which store the contents of costumes and sounds
        
        Returns:
            the SRCostume
        """
        rotation_center = (self.rotation_center_x, self.rotation_center_y)
        content_bytes = asset_files[self.md5ext]
        
        if self.data_format == "svg":
            return SRVectorCostume(
                name              = self.name,
                file_extension    = self.data_format,
                rotation_center   = rotation_center,
                content           = etree.fromstring(content_bytes),
            )
        else: # "png", "jpg", "jpeg", "bmp"
            try:
                image = Image.open(BytesIO(content_bytes))
            except UnidentifiedImageError:
                raise MANIP_ThanksError()
            image.load()  # Ensure it's fully loaded into memory
            if   self.bitmap_resolution == 1:
                has_double_resolution = False
            elif self.bitmap_resolution == 2:
                has_double_resolution = True
            else: raise MANIP_ThanksError()
            return SRBitmapCostume(
                name                  = self.name,
                file_extension        = self.data_format,
                rotation_center       = rotation_center,
                has_double_resolution = has_double_resolution,
                content               = image,
            )

@grepr_dataclass(grepr_fields=["name", "asset_id", "data_format", "md5ext", "rate", "sample_count"])
class FRSound:
    """
    The first representation for a sound. It is very close to the json data in a project
    """
    
    name: str
    asset_id: str
    data_format: str
    md5ext: str
    rate: int
    sample_count: int
    
    @classmethod
    def from_data(cls, data: dict[str, Any]) -> "FRSound":
        """
        Deserializes json data into a FRSound
        
        Args:
            data: the json data
        
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

    def to_data(self) -> dict[str, Any]:
        """
        Serializes a FRSound into json data
        
        Returns:
            the json data
        """
        data = {
            "name"            : self.name,
            "assetId"         : self.asset_id,
            "dataFormat"      : self.data_format,
            "md5ext"          : self.md5ext,
            "rate"            : self.rate,
            "sampleCount"     : self.sample_count,
        }
        return data

    def to_second(self, asset_files: dict[str, bytes]) -> "SRSound":
        """
        Converts a FRSound into a SRSound
        
        Args:
            asset_files: the asset files, which store the contents of costumes and sounds
        
        Returns:
            the SRSound
        """
        content_bytes = asset_files[self.md5ext]
        audio_segment = AudioSegment.from_file(BytesIO(content_bytes), format=self.data_format)
        
        return SRSound(
            name           = self.name,
            file_extension = self.data_format,
            content        = audio_segment,
            # Other attributes can be derived from the sound files
        )

@grepr_dataclass(grepr_fields=["name", "file_extension", "rotation_center"], init=False, forbid_init_only_subcls=True)
class SRCostume(ABC):
    """
    The second representation for a costume. It is more user friendly then the first representation.
    **Please use the subclasses SRVectorCostume and SRBitmapCostume for actual data**
    """

    name: str
    file_extension: str
    rotation_center: tuple[int | float, int | float]

    def validate(self, path: list) -> None:
        """
        Ensure a SRCostume is valid, raise MANIP_ValidationError if not
        
        Args:
            path: the path from the project to itself. Used for better error messages
        
        Returns:
            None
        
        Raises:
            MANIP_ValidationError: if the SRCostume is invalid
        """
        AA_TYPE(self, path, "name", str)
        AA_TYPE(self, path, "file_extension", str)
        AA_COORD_PAIR(self, path, "rotation_center")

    @abstractmethod
    def to_first(self) -> tuple["FRCostume", bytes]: 
        """
        Converts a SRCostume into a FRCostume 
        
        Returns:
            the FRCostume
        """

@grepr_dataclass(grepr_fields=["content"], eq=True) # must be True for order to work, is overwritten
class SRVectorCostume(SRCostume):
    """
    The second representation for a vector(SVG) costume. It is more user friendly then the first representation
    """
    
    content: etree._Element
        
    @classmethod
    def create_empty(cls, name: str = "empty") -> "SRCostume":
        return cls(
            name            = name,
            file_extension  = "svg",
            rotation_center = EMPTY_SVG_COSTUME_ROTATION_CENTER,
            content         = etree.fromstring(EMPTY_SVG_COSTUME_XML),
        )

    def __eq__(self, other) -> bool:
        """
        Checks whether a SRVectorCostume is equal to another.
        Requires same XML data. Ignores wrong identity of content.

        Args:
            other: the object to compare to

        Returns:
            bool: wether self is equal to other
        """
        if not super().__eq__(other):
            return False
        other: SRVectorCostume = other
        return xml_equal(self.content, other.content)
        
    def validate(self, path: list) -> None:
        """
        Ensure a SRVectorCostume is valid, raise MANIP_ValidationError if not
        
        Args:
            path: the path from the project to itself. Used for better error messages
        
        Returns:
            None
        
        Raises:
            MANIP_ValidationError: if the SRVectorCostume is invalid
        """
        super().validate(path)
        
        AA_EQUAL(self, path, "file_extension", "svg")
        AA_TYPE(self, path, "content", etree._Element)
    
    def to_first(self) -> tuple["FRCostume", bytes]:
        """
        Converts a SRVectorCostume into a FRCostume
        
        Returns:
            the FRCostume
        """
        file_bytes: bytes = etree.tostring(self.content, method="c14n")
        md5 = generate_md5(file_bytes) 
        # I am using the md5 hash here(guessed by "md5ext"). 
        # I do not know which hashing method Scratch uses. 
        # Scratch md5ext and mine do NOT match. I have uploaded generated project multiple times
        # and there do not seem to be any consequences.
        return (FRCostume(
            name              = self.name,
            asset_id          = md5, 
            data_format       = self.file_extension, 
            md5ext            = f"{md5}.{self.file_extension}", 
            rotation_center_x = self.rotation_center[0], 
            rotation_center_y = self.rotation_center[1], 
            bitmap_resolution = None, 
        ), file_bytes)

@grepr_dataclass(grepr_fields=["content", "has_double_resolution"], eq=True) # must be True for order to work, is overwritten
class SRBitmapCostume(SRCostume):
    """
    The second representation for a bitmap(usually PNG) costume. It is more user friendly then the first representation
    """
    
    # file_extension: i've only seen "png", "jpg"; others might work
    content: Image.Image
    has_double_resolution: bool
    
    def __eq__(self, other) -> bool:
        """
        Checks whether a SRBitmapCostume is equal to another.
        Requires same image pixel data. Ignores wrong identity of content.

        Args:
            other: the object to compare to

        Returns:
            bool: wether self is equal to other
        """
        if not super().__eq__(other):
            return False
        other: SRBitmapCostume = other
        return (
            (self.has_double_resolution is other.has_double_resolution)
            and image_equal(self.content, other.content)
        )
    
    def validate(self, path: list) -> None:
        """
        Ensure a SRBitmapCostume is valid, raise MANIP_ValidationError if not
        
        Args:
            path: the path from the project to itself. Used for better error messages
        
        Returns:
            None
        
        Raises:
            MANIP_ValidationError: if the SRBitmapCostume is invalid
        """
        super().validate(path)
        
        AA_TYPE(self, path, "content", Image.Image)
        AA_TYPE(self, path, "has_double_resolution", bool)

    def to_first(self) -> tuple["FRCostume", bytes]:
        """
        Converts a SRBitmapCostume into a FRCostume
        
        Returns:
            the FRCostume
        """
        bytes_io = BytesIO()
        self.content.save(bytes_io, format=self.file_extension)
        file_bytes = bytes_io.getvalue()
        md5 = generate_md5(file_bytes)
        # I am using the md5 hash here(guessed by "md5ext"). 
        # I do not know which hashing method Scratch uses. 
        # Scratch md5ext and mine do NOT match. I have uploaded generated project multiple times
        # and there do not seem to be any consequences.
        return (FRCostume(
            name              = self.name,
            asset_id          = md5, 
            data_format       = self.file_extension, 
            md5ext            = f"{md5}.{self.file_extension}", 
            rotation_center_x = self.rotation_center[0], 
            rotation_center_y = self.rotation_center[1], 
            bitmap_resolution = 2 if self.has_double_resolution else 1, 
        ), file_bytes)


@grepr_dataclass(grepr_fields=["name", "file_extension", "content"])
class SRSound:
    """
    The second representation for a sound. It is more user friendly then the first representation
    """

    name: str
    file_extension: str # i've only seen "wav", "mp3", "ogg"; others might work
    content: AudioSegment
    
    def validate(self, path: list) -> None:
        """
        Ensure a SRSound is valid, raise MANIP_ValidationError if not
        
        Args:
            path: the path from the project to itself. Used for better error messages
        
        Returns:
            None
        
        Raises:
            MANIP_ValidationError: if the SRSound is invalid
        """
        AA_TYPE(self, path, "name", str)
        AA_TYPE(self, path, "file_extension", str)
        AA_TYPE(self, path, "content", AudioSegment)
    
    def to_first(self) -> tuple["FRSound", bytes]:
        """
        Converts a SRSound into a FRSound
        
        Returns:
            the FRSound
        """
        bytes_io = BytesIO()
        self.content.export(bytes_io, format=self.file_extension)
        file_bytes = bytes_io.getvalue()
        md5 = generate_md5(file_bytes)
        # I am using the md5 hash here(guessed by "md5ext"). 
        # I do not know which hashing method Scratch uses. 
        # Scratch md5ext and mine do NOT match. I have uploaded generated project multiple times
        # and there do not seem to be any consequences.
        return (FRSound(
            name              = self.name,
            asset_id          = md5, 
            data_format       = self.file_extension, 
            md5ext            = f"{md5}.{self.file_extension}", 
            rate              = self.content.frame_rate,
            sample_count      = len(self.content.get_array_of_samples()),
        ), file_bytes)
 

__all__ = ["FRCostume", "SRVectorCostume", "SRBitmapCostume", "FRSound", "SRCostume", "SRSound"]

