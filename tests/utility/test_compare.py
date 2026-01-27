from __future__ import annotations
import pytest
from lxml import etree
from PIL import Image
import tempfile
import os

from pmp_manip.utility.compare import (
    xml_equal,
    image_equal,
    lists_equal_ignore_order,
    assert_lists_equal_ignore_order,
)


@pytest.fixture
def mock_write_file_text(monkeypatch):
    """Mock write_file_text to avoid creating actual files during tests."""
    calls = []
    def mock_write(filename, content):
        calls.append((filename, content))
    
    import pmp_manip.utility.compare
    monkeypatch.setattr(pmp_manip.utility.compare, "write_file_text", mock_write)
    return calls


class TestXmlEqual:
    """Test xml_equal function."""

    def test_identical_elements(self):
        """Test with identical XML elements."""
        xml1 = etree.Element("root")
        xml1.text = "test"
        xml2 = etree.Element("root")
        xml2.text = "test"
        assert xml_equal(xml1, xml2) is True

    def test_different_tags(self):
        """Test with different tag names."""
        xml1 = etree.Element("root")
        xml2 = etree.Element("different")
        assert xml_equal(xml1, xml2) is False

    def test_different_text(self):
        """Test with different text content."""
        xml1 = etree.Element("root")
        xml1.text = "text1"
        xml2 = etree.Element("root")
        xml2.text = "text2"
        assert xml_equal(xml1, xml2) is False

    def test_different_attributes(self):
        """Test with different attributes."""
        xml1 = etree.Element("root")
        xml1.set("attr", "value1")
        xml2 = etree.Element("root")
        xml2.set("attr", "value2")
        assert xml_equal(xml1, xml2) is False

    def test_nested_elements(self):
        """Test with nested elements."""
        xml1 = etree.Element("root")
        child1 = etree.SubElement(xml1, "child")
        child1.text = "content"
        
        xml2 = etree.Element("root")
        child2 = etree.SubElement(xml2, "child")
        child2.text = "content"
        
        assert xml_equal(xml1, xml2) is True

    def test_nested_elements_different(self):
        """Test with different nested elements."""
        xml1 = etree.Element("root")
        child1 = etree.SubElement(xml1, "child")
        child1.text = "content1"
        
        xml2 = etree.Element("root")
        child2 = etree.SubElement(xml2, "child")
        child2.text = "content2"
        
        assert xml_equal(xml1, xml2) is False

    def test_different_number_of_children(self):
        """Test with different number of children."""
        xml1 = etree.Element("root")
        etree.SubElement(xml1, "child1")
        etree.SubElement(xml1, "child2")
        
        xml2 = etree.Element("root")
        etree.SubElement(xml2, "child1")
        
        assert xml_equal(xml1, xml2) is False

    def test_empty_elements(self):
        """Test with empty elements."""
        xml1 = etree.Element("root")
        xml2 = etree.Element("root")
        assert xml_equal(xml1, xml2) is True

    def test_attribute_order_different(self):
        """Test that attribute order doesn't matter."""
        xml1 = etree.Element("root")
        xml1.set("a", "1")
        xml1.set("b", "2")
        
        xml2 = etree.Element("root")
        xml2.set("b", "2")
        xml2.set("a", "1")
        
        # C14N normalization should make them equal
        assert xml_equal(xml1, xml2) is True


class TestImageEqual:
    """Test image_equal function."""

    def test_identical_images(self):
        """Test with identical images."""
        img1 = Image.new("RGB", (10, 10), color="red")
        img2 = Image.new("RGB", (10, 10), color="red")
        assert image_equal(img1, img2) is True

    def test_different_pixels(self):
        """Test with different pixel data."""
        img1 = Image.new("RGB", (10, 10), color="red")
        img2 = Image.new("RGB", (10, 10), color="blue")
        assert image_equal(img1, img2) is False

    def test_different_size(self):
        """Test with different sizes."""
        img1 = Image.new("RGB", (10, 10), color="red")
        img2 = Image.new("RGB", (20, 20), color="red")
        assert image_equal(img1, img2) is False

    def test_different_mode(self):
        """Test with different color modes."""
        img1 = Image.new("RGB", (10, 10), color="red")
        img2 = Image.new("RGBA", (10, 10), color="red")
        assert image_equal(img1, img2) is False

    def test_grayscale_images(self):
        """Test with grayscale images."""
        img1 = Image.new("L", (10, 10), color=128)
        img2 = Image.new("L", (10, 10), color=128)
        assert image_equal(img1, img2) is True

    def test_grayscale_different(self):
        """Test with different grayscale images."""
        img1 = Image.new("L", (10, 10), color=128)
        img2 = Image.new("L", (10, 10), color=64)
        assert image_equal(img1, img2) is False

    def test_rgba_images(self):
        """Test with RGBA images."""
        img1 = Image.new("RGBA", (10, 10), color=(255, 0, 0, 255))
        img2 = Image.new("RGBA", (10, 10), color=(255, 0, 0, 255))
        assert image_equal(img1, img2) is True

    def test_single_pixel_difference(self):
        """Test with single pixel difference."""
        img1 = Image.new("RGB", (10, 10), color="red")
        img2 = Image.new("RGB", (10, 10), color="red")
        # Modify one pixel
        pixels = img2.load()
        pixels[0, 0] = (0, 0, 255)  # blue
        assert image_equal(img1, img2) is False


class TestListsEqualIgnoreOrder:
    """Test lists_equal_ignore_order function."""

    def test_identical_lists(self):
        """Test with identical lists."""
        assert lists_equal_ignore_order([1, 2, 3], [1, 2, 3]) is True

    def test_different_order(self):
        """Test with different order."""
        assert lists_equal_ignore_order([1, 2, 3], [3, 2, 1]) is True

    def test_different_length(self):
        """Test with different lengths."""
        assert lists_equal_ignore_order([1, 2, 3], [1, 2]) is False

    def test_different_elements(self):
        """Test with different elements."""
        assert lists_equal_ignore_order([1, 2, 3], [1, 2, 4]) is False

    def test_empty_lists(self):
        """Test with empty lists."""
        assert lists_equal_ignore_order([], []) is True

    def test_one_empty_list(self):
        """Test with one empty list."""
        assert lists_equal_ignore_order([], [1]) is False

    def test_with_duplicates(self):
        """Test with duplicate elements."""
        assert lists_equal_ignore_order([1, 1, 2], [2, 1, 1]) is True

    def test_different_duplicate_counts(self, monkeypatch: pytest.MonkeyPatch):
        """Test with different duplicate counts."""
        calls = []
        def mock_write(filename, content):
            calls.append((filename, content))
        import pmp_manip.utility.compare
        monkeypatch.setattr(pmp_manip.utility.compare, "write_file_text", mock_write)

        assert lists_equal_ignore_order([1, 1, 2], [1, 2, 2]) is False

    def test_strings(self):
        """Test with strings."""
        assert lists_equal_ignore_order(["a", "b"], ["b", "a"]) is True

    def test_strings_different(self):
        """Test with different strings."""
        assert lists_equal_ignore_order(["a", "b"], ["a", "c"]) is False

    def test_with_none_values(self):
        """Test with None values."""
        assert lists_equal_ignore_order([None, 1, 2], [2, None, 1]) is True

    def test_mutable_objects(self):
        """Test with mutable objects (lists inside)."""
        assert lists_equal_ignore_order([[1, 2], [3, 4]], [[3, 4], [1, 2]]) is True

    def test_mutable_objects_different(self):
        """Test with different mutable objects."""
        assert lists_equal_ignore_order([[1, 2], [3, 4]], [[1, 2], [3, 5]]) is False

    def test_logging_disabled(self):
        """Test with logging disabled."""
        result = lists_equal_ignore_order([1, 2], [1, 3], log=False)
        assert result is False

    def test_logging_enabled(self):
        """Test with logging enabled (should work without error)."""
        result = lists_equal_ignore_order([1, 2], [1, 3], log=True)
        assert result is False


class TestAssertListsEqualIgnoreOrder:
    """Test assert_lists_equal_ignore_order function."""

    def test_equal_lists(self, mock_write_file_text):
        """Test with equal lists - should not raise."""
        # Should not raise
        assert_lists_equal_ignore_order([1, 2, 3], [3, 2, 1])

    def test_different_lists_raises(self, mock_write_file_text):
        """Test with different lists - should raise assertion."""
        with pytest.raises(AssertionError, match="Lists differ"):
            assert_lists_equal_ignore_order([1, 2, 3], [1, 2, 4])

    def test_different_length_raises(self, mock_write_file_text):
        """Test with different lengths - should raise assertion."""
        with pytest.raises(AssertionError, match="Lists differ"):
            assert_lists_equal_ignore_order([1, 2], [1, 2, 3])

    def test_empty_lists(self, mock_write_file_text):
        """Test with empty lists - should not raise."""
        assert_lists_equal_ignore_order([], [])

    def test_with_duplicates(self, mock_write_file_text):
        """Test with duplicates - should not raise."""
        assert_lists_equal_ignore_order([1, 1, 2], [2, 1, 1])

    def test_different_duplicates_raises(self, mock_write_file_text):
        """Test with different duplicate counts - should raise."""
        with pytest.raises(AssertionError, match="Lists differ"):
            assert_lists_equal_ignore_order([1, 1, 2], [1, 2, 2])

    def test_creates_comparison_files(self, mock_write_file_text):
        """Test that comparison files are created on failure."""
        with pytest.raises(AssertionError, match="Lists differ"):
            assert_lists_equal_ignore_order([1, 2, 3], [1, 2, 4])
        
        # Verify write_file_text was called twice (for a.comp and b.comp)
        assert len(mock_write_file_text) == 2
        # Verify it was called with the right file names
        assert mock_write_file_text[0][0] == "a.comp"
        assert mock_write_file_text[1][0] == "b.comp"
