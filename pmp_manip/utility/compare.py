from logging import getLogger
from lxml    import etree
from PIL     import Image

from pmp_manip.utility.repr import grepr

def xml_equal(xml1: etree._Element, xml2: etree._Element, /) -> bool:
    """
    Compare two xml elements for equality
    
    Args:
        xml1: the first xml element
        xml2: the second xml element
    
    Returns:
        wether the two xml elements are equal
    """
    return etree.tostring(xml1, method="c14n") == etree.tostring(xml2, method="c14n")

def image_equal(img1: Image.Image, img2: Image.Image, /) -> bool:
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

def lists_equal_ignore_order(a: list, b: list, /, log: bool = True) -> bool:
    if len(a) != len(b):
        return False

    if log: logger = getLogger(__name__)
    b_copy = b[:]
    for item in a:
        try:
            b_copy.remove(item)  # uses __eq__, safe for mutable objects
        except ValueError:
            if log: logger.critical(f"second list is missing:\n{item!r}")
            return False
    return not b_copy

def assert_lists_equal_ignore_order(a: list, b: list, /) -> None:
    if not lists_equal_ignore_order(a, b, log=False):
        print(f"a={grepr(a)}\n\n\n\nb={grepr(b)}")
        assert False, "Lists differ."


__all__ = ["xml_equal", "image_equal", "lists_equal_ignore_order", "assert_lists_equal_ignore_order"]

