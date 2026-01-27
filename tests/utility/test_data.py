from __future__ import annotations
import pytest
from pmp_manip.utility.data import (
    remove_duplicates,
    get_closest_matches,
    tuplify,
    listify,
    gdumps,
    string_to_sha256,
    number_to_token,
    generate_md5,
    ContentFingerprint,
)


class TestRemoveDuplicates:
    """Test remove_duplicates function."""

    def test_empty_list(self):
        """Test with empty list."""
        assert remove_duplicates([]) == []

    def test_no_duplicates(self):
        """Test with list that has no duplicates."""
        assert remove_duplicates([1, 2, 3, 4]) == [1, 2, 3, 4]

    def test_with_duplicates(self):
        """Test with list that has duplicates."""
        assert remove_duplicates([1, 2, 2, 3, 1, 4]) == [1, 2, 3, 4]

    def test_with_string_duplicates(self):
        """Test with string duplicates."""
        assert remove_duplicates(["a", "b", "a", "c"]) == ["a", "b", "c"]

    def test_preserves_order(self):
        """Test that order is preserved."""
        assert remove_duplicates([3, 1, 2, 1, 3]) == [3, 1, 2]

    def test_with_mixed_types(self):
        """Test with mixed types."""
        assert remove_duplicates([1, "1", 1, "1"]) == [1, "1"]


class TestGetClosestMatches:
    """Test get_closest_matches function."""

    def test_exact_match(self):
        """Test with exact match available."""
        matches = get_closest_matches("cat", ["cat", "dog", "car"], 2)
        assert "cat" in matches
        assert len(matches) == 2

    def test_partial_matches(self):
        """Test with partial matches."""
        matches = get_closest_matches("ca", ["cat", "car", "dog"], 2)
        assert len(matches) == 2
        assert "cat" in matches or "car" in matches

    def test_single_match(self):
        """Test requesting single match."""
        matches = get_closest_matches("test", ["test", "testing", "tester"], 1)
        assert len(matches) == 1
        assert matches[0] == "test"

    def test_more_matches_than_available(self):
        """Test requesting more matches than available."""
        matches = get_closest_matches("cat", ["cat", "car"], 5)
        assert len(matches) <= 2

    def test_empty_list(self):
        """Test with empty list."""
        matches = get_closest_matches("test", [], 2)
        assert matches == []

    def test_sorted_by_similarity(self):
        """Test that results are sorted by similarity."""
        matches = get_closest_matches("test", ["test", "testing", "abc", "xyz"], 3)
        # "test" should be first or very close
        assert "test" == matches[0]


class TestTuplify:
    """Test tuplify function."""

    def test_tuplify_list(self):
        """Test converting list to tuple."""
        assert tuplify([1, 2, 3]) == (1, 2, 3)

    def test_tuplify_nested_list(self):
        """Test converting nested list to nested tuple."""
        assert tuplify([1, [2, 3], 4]) == (1, (2, 3), 4)

    def test_tuplify_dict(self):
        """Test converting dict (keys and values)."""
        result = tuplify({"a": [1, 2]})
        assert isinstance(result, dict)
        assert result == {"a": (1, 2)}

    def test_tuplify_tuple(self):
        """Test with tuple (should stay as tuple)."""
        assert tuplify((1, 2, 3)) == (1, 2, 3)

    def test_tuplify_scalar(self):
        """Test with scalar values."""
        assert tuplify(42) == 42
        assert tuplify("string") == "string"

    def test_tuplify_complex_nested(self):
        """Test with complex nested structure."""
        input_data = {"list": [1, {"nested": [2, 3]}], "value": 4}
        result = tuplify(input_data)
        assert result == {"list": (1, {"nested": (2, 3)}), "value": 4}


class TestListify:
    """Test listify function."""

    def test_listify_tuple(self):
        """Test converting tuple to list."""
        assert listify((1, 2, 3)) == [1, 2, 3]

    def test_listify_nested_tuple(self):
        """Test converting nested tuple to nested list."""
        assert listify((1, (2, 3), 4)) == [1, [2, 3], 4]

    def test_listify_dict(self):
        """Test converting dict (keys and values)."""
        result = listify({"a": (1, 2)})
        assert isinstance(result, dict)
        assert result == {"a": [1, 2]}

    def test_listify_list(self):
        """Test with list (should stay as list)."""
        assert listify([1, 2, 3]) == [1, 2, 3]

    def test_listify_scalar(self):
        """Test with scalar values."""
        assert listify(42) == 42
        assert listify("string") == "string"

    def test_listify_complex_nested(self):
        """Test with complex nested structure."""
        input_data = {"tuple": (1, {"nested": (2, 3)}), "value": 4}
        result = listify(input_data)
        assert result == {"tuple": [1, {"nested": [2, 3]}], "value": 4}


class TestGdumps:
    """Test gdumps function."""

    def test_simple_dict(self):
        """Test with simple dictionary."""
        result = gdumps({"a": 1, "b": 2})
        # Should not have spaces after separators
        assert " " not in result
        assert ":" in result
        assert "," in result

    def test_no_spaces(self):
        """Test that no spaces are added."""
        result = gdumps({"key": "value"})
        assert ", " not in result
        assert ": " not in result

    def test_complex_structure(self):
        """Test with complex structure."""
        data = {"list": [1, 2, 3], "nested": {"a": 1}}
        result = gdumps(data)
        assert isinstance(result, str)
        assert "[1,2,3]" in result

    def test_empty_dict(self):
        """Test with empty dictionary."""
        assert gdumps({}) == "{}"

    def test_empty_list(self):
        """Test with empty list."""
        assert gdumps([]) == "[]"


class TestStringToSha256:
    """Test string_to_sha256 function."""

    def test_primary_only(self):
        """Test with only primary parameter."""
        result = string_to_sha256("test")
        assert isinstance(result, str)
        assert len(result) == 20

    def test_primary_and_secondary(self):
        """Test with primary and secondary parameters."""
        result = string_to_sha256("primary", "secondary")
        assert isinstance(result, str)
        assert len(result) == 20  # 4 + 16

    def test_all_three_parameters(self):
        """Test with all three parameters."""
        result = string_to_sha256("primary", "secondary", "tertiary")
        assert isinstance(result, str)
        assert len(result) == 20  # 4 + 4 + 12

    def test_secondary_without_tertiary(self):
        """Test with secondary but without tertiary."""
        result = string_to_sha256("primary", "secondary")
        assert len(result) == 20

    def test_integer_primary(self):
        """Test with integer as primary."""
        result = string_to_sha256(42)
        assert isinstance(result, str)
        assert len(result) == 20

    def test_bool_primary(self):
        """Test with boolean as primary."""
        result = string_to_sha256(True)
        assert isinstance(result, str)

    def test_different_inputs_different_outputs(self):
        """Test that different inputs produce different outputs."""
        result1 = string_to_sha256("test1")
        result2 = string_to_sha256("test2")
        assert result1 != result2

    def test_secondary_without_primary_raises(self):
        """Test that None secondary with non-None tertiary raises error."""
        with pytest.raises(ValueError, match="secondary must NOT be None"):
            string_to_sha256("primary", None, "tertiary")


class TestNumberToToken:
    """Test number_to_token function."""

    def test_zero(self):
        """Test with zero."""
        result = number_to_token(0)
        assert result == ""

    def test_one(self):
        """Test with one."""
        result = number_to_token(1)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_small_number(self):
        """Test with small number."""
        result = number_to_token(5)
        assert isinstance(result, str)

    def test_large_number(self):
        """Test with large number."""
        result = number_to_token(1000)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_increasing_numbers_different_results(self):
        """Test that increasing numbers produce different results."""
        result1 = number_to_token(1)
        result2 = number_to_token(2)
        assert result1 != result2


class TestGenerateMd5:
    """Test generate_md5 function."""

    def test_simple_bytes(self):
        """Test with simple bytes."""
        data = b"test"
        result = generate_md5(data)
        assert isinstance(result, str)
        assert len(result) == 32  # MD5 is 32 hex characters

    def test_empty_bytes(self):
        """Test with empty bytes."""
        result = generate_md5(b"")
        assert isinstance(result, str)
        assert len(result) == 32

    def test_large_data(self):
        """Test with large data (larger than 4096)."""
        data = b"x" * 10000
        result = generate_md5(data)
        assert isinstance(result, str)
        assert len(result) == 32

    def test_known_md5(self):
        """Test with known MD5 value."""
        # MD5 of "test" is 098f6bcd4621d373cade4e832627b4f6
        result = generate_md5(b"test")
        assert result == "098f6bcd4621d373cade4e832627b4f6"

    def test_different_inputs_different_hashes(self):
        """Test that different inputs produce different hashes."""
        result1 = generate_md5(b"test1")
        result2 = generate_md5(b"test2")
        assert result1 != result2


class TestContentFingerprint:
    """Test ContentFingerprint class."""

    def test_hash_value(self):
        """Test hash_value static method."""
        hash1 = ContentFingerprint.hash_value("test")
        hash2 = ContentFingerprint.hash_value("test")
        assert hash1 == hash2
        assert len(hash1) == 64  # SHA256 is 64 hex characters

    def test_from_value(self):
        """Test from_value class method."""
        fp = ContentFingerprint.from_value("test content")
        assert fp.length == 12
        assert fp.hash == ContentFingerprint.hash_value("test content")

    def test_from_json(self):
        """Test from_json class method."""
        data = {"length": 4, "hash": "abc123"}
        fp = ContentFingerprint.from_json(data)
        assert fp.length == 4
        assert fp.hash == "abc123"

    def test_matches_true(self):
        """Test matches method returns True for same content."""
        fp = ContentFingerprint.from_value("test")
        assert fp.matches("test") is True

    def test_matches_false_different_content(self):
        """Test matches method returns False for different content."""
        fp = ContentFingerprint.from_value("test")
        assert fp.matches("different") is False

    def test_matches_false_different_length(self):
        """Test matches method returns False for different length."""
        fp = ContentFingerprint.from_value("test")
        # Create a different fingerprint with different length
        assert fp.matches("testextra") is False

    def test_matches_false_same_length_different_hash(self):
        """Test matches method returns False when length matches but hash differs."""
        fp = ContentFingerprint.from_value("aaaa")
        # "bbbb" has the same length but different hash
        assert fp.matches("bbbb") is False

    def test_to_json(self):
        """Test to_json method."""
        fp = ContentFingerprint.from_value("test")
        json_data = fp.to_json()
        assert json_data["length"] == 4
        assert json_data["hash"] == fp.hash

    def test_roundtrip_json(self):
        """Test round-trip conversion to/from JSON."""
        original = ContentFingerprint.from_value("test content")
        json_data = original.to_json()
        restored = ContentFingerprint.from_json(json_data)
        assert restored.length == original.length
        assert restored.hash == original.hash

    def test_empty_string(self):
        """Test with empty string."""
        fp = ContentFingerprint.from_value("")
        assert fp.length == 0
        assert fp.matches("") is True
        assert fp.matches("a") is False

    def test_unicode_content(self):
        """Test with unicode content."""
        fp = ContentFingerprint.from_value("こんにちは")
        assert fp.length == 5
        assert fp.matches("こんにちは") is True
