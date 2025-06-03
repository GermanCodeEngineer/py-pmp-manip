from io        import BytesIO
from lxml      import etree
from PIL       import Image, UnidentifiedImageError
from pydub     import AudioSegment
from typing    import Any

from pypenguin.utility import (
    grepr_dataclass, xml_equal, image_equal, ValidationConfig,
    AA_TYPE, AA_COORD_PAIR, AA_EQUAL,
    ThanksError,
)


EMPTY_SVG_COSTUME_XML = '<svg version="1.1" width="2" height="2" viewBox="-1 -1 2 2" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">\n  <!-- Exported by Scratch - http://scratch.mit.edu/ -->\n</svg>'
EMPTY_SVG_COSTUME_ROTATION_CENTER = (240, 180)


@grepr_dataclass(grepr_fields=["name", "asset_id", "data_format", "md5ext", "rotation_center_x", "rotation_center_y", "bitmap_resolution"])
class FRCostume:
    """
    The first representation for a costume. It is very close to the raw data in a project
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
        Deserializes raw data into a FRSound
        
        Args:
            data: the raw data
        
        Returns:
            the FRSound
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

    def step(self, asset_files: dict[str, bytes]) -> "SRVectorCostume|SRBitmapCostume": 
        """
        Converts a FRComment into a SRComment
        
        Returns:
            the SRComment
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
                raise ThanksError()
            image.load()  # Ensure it's fully loaded into memory
            if   self.bitmap_resolution == 1:
                has_double_resolution = False
            elif self.bitmap_resolution == 2:
                has_double_resolution = True
            else: raise ThanksError()
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
    The first representation for a sound. It is very close to the raw data in a project
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

    def step(self, asset_files: dict[str, bytes]) -> "SRSound":
        """
        Converts a FRSound into a SRSound
        
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

@grepr_dataclass(grepr_fields=["name", "file_extension", "rotation_center"], init=False)
class SRCostume:
    """
    The second representation for a costume. It is more user friendly then the first representation.
    **Please use the subclasses SRVectorCostume and SRBitmapCostume for actual data**
    """

    name: str
    file_extension: str
    rotation_center: tuple[int | float, int | float]

    def __init__(self, name: str, file_extension: str, rotation_center: tuple[int | float, int | float]) -> None:
        """
        Create a SRInputValue. 
        **Please use the subclasses SRVectorCostume and SRBitmapCostume for concrete data. This method will raise a NotImplementedError.**

        Returns:
            None

        Raises:
            NotImplementedError: always
        """
        raise NotImplementedError("Please use the subclasses SRVectorCostume and SRBitmapCostume for concrete data")
    
    def validate(self, path: list, config: ValidationConfig) -> None:
        """
        Ensure a SRCostume is valid, raise ValidationError if not
        
        Args:
            path: the path from the project to itself. Used for better error messages
            config: Configuration for Validation Behaviour
        
        Returns:
            None
        
        Raises:
            ValidationError: if the SRCostume is invalid
        """
        AA_TYPE(self, path, "name", str)
        AA_TYPE(self, path, "file_extension", str)
        AA_COORD_PAIR(self, path, "rotation_center")

@grepr_dataclass(grepr_fields=["content"], parent_cls=SRCostume, eq=False)
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
        
    def validate(self, path: list, config: ValidationConfig) -> None:
        """
        Ensure a SRVectorCostume is valid, raise ValidationError if not
        
        Args:
            path: the path from the project to itself. Used for better error messages
            config: Configuration for Validation Behaviour
        
        Returns:
            None
        
        Raises:
            ValidationError: if the SRVectorCostume is invalid
        """
        super().validate(path, config)
        
        AA_EQUAL(self, path, "file_extension", "svg")
        AA_TYPE(self, path, "content", etree._Element)

@grepr_dataclass(grepr_fields=["content", "has_double_resolution"], parent_cls=SRCostume, eq=False)
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
            (self.has_double_resolution == other.has_double_resolution)
            and image_equal(self.content, other.content)
        )
    
    def validate(self, path: list, config: ValidationConfig) -> None:
        """
        Ensure a SRBitmapCostume is valid, raise ValidationError if not
        
        Args:
            path: the path from the project to itself. Used for better error messages
            config: Configuration for Validation Behaviour
        
        Returns:
            None
        
        Raises:
            ValidationError: if the SRBitmapCostume is invalid
        """
        super().validate(path, config)
        
        AA_TYPE(self, path, "content", Image.Image)
        AA_TYPE(self, path, "has_double_resolution", bool)


@grepr_dataclass(grepr_fields=["name", "file_extension", "content"])
class SRSound:
    """
    The second representation for a sound. It is more user friendly then the first representation
    """

    name: str
    file_extension: str # i've only seen "wav", "mp3", "ogg"; others might work
    content: AudioSegment
    
    #def __eq__(self, other) -> bool:
    #    """
    #    Checks whether a SRSound is equal to another.
    #    Requires same audio segment bytes. Ignores wrong identity of content.
    #
    #    Args:
    #        other: the object to compare to
    #
    #    Returns:
    #        bool: wether self is equal to other
    #    """
    #    if not isinstance(other, SRSound):
    #        return NotImplemented
    #    return (
    #            (self.name == other.name)
    #        and (self.file_extension == other.file_extension)
    #        and audio_segment_equal(self.content, other.content)
    #    )
    
    def validate(self, path: list, config: ValidationConfig) -> None:
        """
        Ensure a SRSound is valid, raise ValidationError if not
        
        Args:
            path: the path from the project to itself. Used for better error messages
            config: Configuration for Validation Behaviour
        
        Returns:
            None
        
        Raises:
            ValidationError: if the SRSound is invalid
        """
        AA_TYPE(self, path, "name", str)
        AA_TYPE(self, path, "file_extension", str)
        AA_TYPE(self, path, "content", AudioSegment)
 

__all__ = ["FRCostume", "SRVectorCostume", "SRBitmapCostume", "FRSound", "SRCostume", "SRSound"]

