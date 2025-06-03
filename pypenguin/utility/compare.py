from lxml import etree
from PIL  import Image

def xml_equal(xml1: etree._Element, xml2: etree._Element) -> bool:
    """
    Compare two xml elements for equality
    
    Args:
        xml1: the first xml element
        xml2: the second xml element
    
    Returns:
        wether the two xml elements are equal
    """
    return etree.tostring(xml1, method="c14n") == etree.tostring(xml2, method="c14n")

def image_equal(img1: Image.Image, img2: Image.Image) -> bool:
    """
    Compare two PIL Image instances for strict equality:
    same size, mode, and pixel data.
    
    Args:
        img1: the first image
        img2: the second image
    
    Returns:
        wether the two images are equal
    """
    if (img1.mode != img2.mode) or (img1.size != img2.size):
        return False
    return img1.tobytes() == img2.tobytes()


__all__ = ["xml_equal", "image_equal"]

