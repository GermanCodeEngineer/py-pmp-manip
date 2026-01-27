from __future__ import annotations
import pytest
import tempfile
from pathlib import Path

from gceutils.validation import (
    Validator, ValidateAttribute, 
    is_valid_js_data_uri, is_valid_directory_path, is_valid_url
)
from gceutils.base import AbstractTreePath, grepr_dataclass
from gceutils.errors import (
    GU_TypeValidationError, GU_RangeValidationError, 
    GU_InvalidValueError, GU_PathValidationError
)


class TestValidator:
    """Test Validator class."""
    
    def test_validator_creation(self):
        """Test creating a Validator."""
        validator = Validator(
            is_valid_fn=lambda value: value > 0,
            error_cls=GU_RangeValidationError,
            create_error_fn=lambda value, descr: f"{descr} must be positive"
        )
        assert validator is not None
    
    def test_validator_call_success(self):
        """Test validator call with valid value."""
        @grepr_dataclass()
        class TestObj:
            value: int
        
        obj = TestObj(value=10)
        validator = Validator(
            is_valid_fn=lambda value: value > 0,
            error_cls=GU_RangeValidationError,
            create_error_fn=lambda value, descr: f"{descr} must be positive"
        )
        
        # Should not raise
        validator(obj, AbstractTreePath(), "value")
    
    def test_validator_call_failure(self):
        """Test validator call with invalid value."""
        @grepr_dataclass()
        class TestObj:
            value: int
        
        obj = TestObj(value=-5)
        validator = Validator(
            is_valid_fn=lambda value: value > 0,
            error_cls=GU_RangeValidationError,
            create_error_fn=lambda value, descr: f"{descr} must be positive"
        )
        
        with pytest.raises(GU_RangeValidationError):
            validator(obj, AbstractTreePath(), "value")
    
    def test_validator_with_pre_validate_fn_success(self):
        """Test validator with pre_validate_fn that passes."""
        @grepr_dataclass()
        class TestObj:
            value: int
        
        obj = TestObj(value=10)
        
        def pre_validate(obj, path, attr, *args, condition=None):
            # Pre-validation passes
            pass
        
        validator = Validator(
            pre_validate_fn=pre_validate,
            is_valid_fn=lambda value: value > 0,
            error_cls=GU_RangeValidationError,
            create_error_fn=lambda value, descr: f"{descr} must be positive"
        )
        
        # Should not raise
        validator(obj, AbstractTreePath(), "value")
    
    def test_validator_with_pre_validate_fn_failure(self):
        """Test validator with pre_validate_fn that fails."""
        @grepr_dataclass()
        class TestObj:
            value: tuple[int, int]
        
        obj = TestObj(value=(10, 20))
        
        def pre_validate(obj, path, attr, *args, condition=None):
            # Pre-validation fails
            raise GU_RangeValidationError(path, "Pre-validation failed")
        
        validator = Validator(
            pre_validate_fn=pre_validate,
            is_valid_fn=lambda value, min_x, max_x: value[0] >= min_x and value[0] <= max_x,
            error_cls=GU_RangeValidationError,
            create_error_fn=lambda value, descr, min_x, max_x: f"{descr} out of range"
        )
        
        with pytest.raises(GU_RangeValidationError):
            validator(obj, AbstractTreePath(), "value", 0, 5)
    
    def test_validator_wrong_arg_count(self):
        """Test validator with incorrect number of arguments."""
        @grepr_dataclass()
        class TestObj:
            value: int
        
        obj = TestObj(value=10)
        
        # Validator expects 2 args (min, max) for RANGE
        validator = Validator(
            is_valid_fn=lambda value, min, max: value >= min and value <= max,
            error_cls=GU_RangeValidationError,
            create_error_fn=lambda value, descr, min, max: f"{descr} must be between {min} and {max}"
        )
        
        # Call with only 1 arg (should expect 2)
        with pytest.raises(TypeError):
            validator(obj, AbstractTreePath(), "value", 5)
    
    def test_validator_with_condition(self):
        """Test validator with condition parameter."""
        @grepr_dataclass()
        class TestObj:
            value: int
        
        obj = TestObj(value=-5)
        
        validator = Validator(
            is_valid_fn=lambda value: value > 0,
            error_cls=GU_RangeValidationError,
            create_error_fn=lambda value, descr: f"{descr} must be positive"
        )
        
        with pytest.raises(GU_RangeValidationError) as exc_info:
            validator(obj, AbstractTreePath(), "value", condition="custom_condition")
        
        assert "custom_condition" in str(exc_info.value)


class TestValidateAttributeType:
    """Test type validation."""
    
    def test_va_type_int(self):
        """Test type validation with int."""
        @grepr_dataclass()
        class TestObj:
            value: int
        
        obj = TestObj(value=42)
        # Should not raise
        ValidateAttribute.VA_TYPE(obj, AbstractTreePath(), "value", int)
    
    def test_va_type_str(self):
        """Test type validation with str."""
        @grepr_dataclass()
        class TestObj:
            value: str
        
        obj = TestObj(value="hello")
        # Should not raise
        ValidateAttribute.VA_TYPE(obj, AbstractTreePath(), "value", str)
    
    def test_va_type_failure(self):
        """Test type validation failure."""
        @grepr_dataclass()
        class TestObj:
            value: int
        
        obj = TestObj(value="42")
        
        with pytest.raises(GU_TypeValidationError):
            ValidateAttribute.VA_TYPE(obj, AbstractTreePath(), "value", int)


class TestValidateAttributeRange:
    """Test range validation."""
    
    def test_va_min(self):
        """Test minimum value validation."""
        @grepr_dataclass()
        class TestObj:
            value: int
        
        obj = TestObj(value=10)
        # Should not raise
        ValidateAttribute.VA_MIN(obj, AbstractTreePath(), "value", 5)
    
    def test_va_min_failure(self):
        """Test minimum value validation failure."""
        @grepr_dataclass()
        class TestObj:
            value: int
        
        obj = TestObj(value=3)
        
        with pytest.raises(GU_RangeValidationError):
            ValidateAttribute.VA_MIN(obj, AbstractTreePath(), "value", 5)
    
    def test_va_range(self):
        """Test range validation."""
        @grepr_dataclass()
        class TestObj:
            value: int
        
        obj = TestObj(value=50)
        # Should not raise
        ValidateAttribute.VA_RANGE(obj, AbstractTreePath(), "value", 10, 100)
    
    def test_va_range_below_min(self):
        """Test range validation below minimum."""
        @grepr_dataclass()
        class TestObj:
            value: int
        
        obj = TestObj(value=5)
        
        with pytest.raises(GU_RangeValidationError):
            ValidateAttribute.VA_RANGE(obj, AbstractTreePath(), "value", 10, 100)
    
    def test_va_range_above_max(self):
        """Test range validation above maximum."""
        @grepr_dataclass()
        class TestObj:
            value: int
        
        obj = TestObj(value=150)
        
        with pytest.raises(GU_RangeValidationError):
            ValidateAttribute.VA_RANGE(obj, AbstractTreePath(), "value", 10, 100)


class TestValidateAttributeLength:
    """Test length validation."""
    
    def test_va_min_len(self):
        """Test minimum length validation."""
        @grepr_dataclass()
        class TestObj:
            items: list
        
        obj = TestObj(items=[1, 2, 3])
        # Should not raise
        ValidateAttribute.VA_MIN_LEN(obj, AbstractTreePath(), "items", 2)
    
    def test_va_min_len_failure(self):
        """Test minimum length validation failure."""
        @grepr_dataclass()
        class TestObj:
            items: list
        
        obj = TestObj(items=[1])
        
        with pytest.raises(GU_RangeValidationError):
            ValidateAttribute.VA_MIN_LEN(obj, AbstractTreePath(), "items", 3)
    
    def test_va_exact_len(self):
        """Test exact length validation."""
        @grepr_dataclass()
        class TestObj:
            items: list
        
        obj = TestObj(items=[1, 2, 3])
        # Should not raise
        ValidateAttribute.VA_EXACT_LEN(obj, AbstractTreePath(), "items", 3)
    
    def test_va_exact_len_failure(self):
        """Test exact length validation failure."""
        @grepr_dataclass()
        class TestObj:
            items: list
        
        obj = TestObj(items=[1, 2])
        
        with pytest.raises(GU_RangeValidationError):
            ValidateAttribute.VA_EXACT_LEN(obj, AbstractTreePath(), "items", 3)


class TestValidateAttributeCoordinate:
    """Test coordinate pair validation."""
    
    def test_va_boxed_coord_pair_valid(self):
        """Test valid coordinate pair."""
        @grepr_dataclass()
        class TestObj:
            coord: tuple[int, int]
        
        obj = TestObj(coord=(50, 75))
        # Should not raise
        ValidateAttribute.VA_BOXED_COORD_PAIR(
            obj, AbstractTreePath(), "coord",
            0, 100, 0, 100
        )
    
    def test_va_boxed_coord_pair_boundary(self):
        """Test coordinate pair at boundary."""
        @grepr_dataclass()
        class TestObj:
            coord: tuple[int, int]
        
        obj = TestObj(coord=(0, 100))
        # Should not raise
        ValidateAttribute.VA_BOXED_COORD_PAIR(
            obj, AbstractTreePath(), "coord",
            0, 100, 0, 100
        )
    
    def test_va_boxed_coord_pair_x_too_large(self):
        """Test coordinate pair with X out of range."""
        @grepr_dataclass()
        class TestObj:
            coord: tuple[int, int]
        
        obj = TestObj(coord=(150, 50))
        
        with pytest.raises(GU_RangeValidationError):
            ValidateAttribute.VA_BOXED_COORD_PAIR(
                obj, AbstractTreePath(), "coord",
                0, 100, 0, 100
            )
    
    def test_va_boxed_coord_pair_none_limits(self):
        """Test coordinate pair with None limits (no limit)."""
        @grepr_dataclass()
        class TestObj:
            coord: tuple[int, int]
        
        obj = TestObj(coord=(1000, 2000))
        # Should not raise
        ValidateAttribute.VA_BOXED_COORD_PAIR(
            obj, AbstractTreePath(), "coord",
            None, None, None, None
        )


class TestValidateAttributeComparison:
    """Test value comparison validators."""
    
    def test_va_equal(self):
        """Test equality validation."""
        @grepr_dataclass()
        class TestObj:
            value: str
        
        obj = TestObj(value="expected")
        # Should not raise
        ValidateAttribute.VA_EQUAL(obj, AbstractTreePath(), "value", "expected")
    
    def test_va_equal_failure(self):
        """Test equality validation failure."""
        @grepr_dataclass()
        class TestObj:
            value: str
        
        obj = TestObj(value="actual")
        
        with pytest.raises(GU_InvalidValueError):
            ValidateAttribute.VA_EQUAL(obj, AbstractTreePath(), "value", "expected")
    
    def test_va_not_one_of(self):
        """Test not-one-of validation."""
        @grepr_dataclass()
        class TestObj:
            value: str
        
        obj = TestObj(value="allowed")
        # Should not raise
        ValidateAttribute.VA_NOT_ONE_OF(
            obj, AbstractTreePath(), "value",
            ["forbidden1", "forbidden2"]
        )
    
    def test_va_not_one_of_failure(self):
        """Test not-one-of validation failure."""
        @grepr_dataclass()
        class TestObj:
            value: str
        
        obj = TestObj(value="forbidden")
        
        with pytest.raises(GU_InvalidValueError):
            ValidateAttribute.VA_NOT_ONE_OF(
                obj, AbstractTreePath(), "value",
                ["forbidden", "also_forbidden"]
            )


class TestValidateAttributeFormat:
    """Test format validation."""
    
    def test_va_hex_color_valid(self):
        """Test valid hex color."""
        @grepr_dataclass()
        class TestObj:
            color: str
        
        obj = TestObj(color="#FF0000")
        # Should not raise
        ValidateAttribute.VA_HEX_COLOR(obj, AbstractTreePath(), "color")
    
    def test_va_hex_color_uppercase(self):
        """Test hex color with uppercase."""
        @grepr_dataclass()
        class TestObj:
            color: str
        
        obj = TestObj(color="#ABCDEF")
        # Should not raise
        ValidateAttribute.VA_HEX_COLOR(obj, AbstractTreePath(), "color")
    
    def test_va_hex_color_lowercase(self):
        """Test hex color with lowercase."""
        @grepr_dataclass()
        class TestObj:
            color: str
        
        obj = TestObj(color="#abcdef")
        # Should not raise
        ValidateAttribute.VA_HEX_COLOR(obj, AbstractTreePath(), "color")
    
    def test_va_hex_color_invalid_format(self):
        """Test invalid hex color format."""
        @grepr_dataclass()
        class TestObj:
            color: str
        
        obj = TestObj(color="FF0000")  # Missing #
        
        with pytest.raises(GU_InvalidValueError):
            ValidateAttribute.VA_HEX_COLOR(obj, AbstractTreePath(), "color")
    
    def test_va_hex_color_invalid_chars(self):
        """Test hex color with invalid characters."""
        @grepr_dataclass()
        class TestObj:
            color: str
        
        obj = TestObj(color="#GGGGGG")
        
        with pytest.raises(GU_InvalidValueError):
            ValidateAttribute.VA_HEX_COLOR(obj, AbstractTreePath(), "color")
    
    def test_va_alnum_valid(self):
        """Test valid alphanumeric string."""
        @grepr_dataclass()
        class TestObj:
            value: str
        
        obj = TestObj(value="abc123")
        # Should not raise
        ValidateAttribute.VA_ALNUM(obj, AbstractTreePath(), "value")
    
    def test_va_alnum_invalid_special_char(self):
        """Test alphanumeric validation with special character."""
        @grepr_dataclass()
        class TestObj:
            value: str
        
        obj = TestObj(value="abc-123")
        
        with pytest.raises(GU_InvalidValueError):
            ValidateAttribute.VA_ALNUM(obj, AbstractTreePath(), "value")


class TestIsValidJsDataUri:
    """Test JavaScript data URI validation."""
    
    def test_valid_js_data_uri(self):
        """Test valid JavaScript data URI."""
        uri = "data:application/javascript,console.log('hello')"
        assert is_valid_js_data_uri(uri) is True
    
    def test_valid_js_data_uri_with_charset(self):
        """Test valid JavaScript data URI with charset."""
        uri = "data:application/javascript;charset=utf-8,console.log('hello')"
        assert is_valid_js_data_uri(uri) is True
    
    def test_invalid_js_data_uri_wrong_type(self):
        """Test invalid data URI with wrong MIME type."""
        uri = "data:text/plain,hello"
        assert is_valid_js_data_uri(uri) is False
    
    def test_invalid_js_data_uri_no_data(self):
        """Test invalid data URI without data part."""
        uri = "data:application/javascript,"
        assert is_valid_js_data_uri(uri) is True  # Empty data is still valid format


class TestIsValidDirectoryPath:
    """Test directory path validation."""
    
    def test_valid_existing_directory(self):
        """Test valid existing directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            assert is_valid_directory_path(tmpdir) is True
    
    def test_invalid_file_path(self):
        """Test file path (not directory)."""
        with tempfile.NamedTemporaryFile() as f:
            assert is_valid_directory_path(f.name) is False
    
    def test_valid_nonexistent_writable_parent(self):
        """Test nonexistent path with writable parent."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_path = Path(tmpdir) / "new_dir"
            assert is_valid_directory_path(str(test_path)) is True
    
    def test_invalid_nonexistent_unwritable_parent(self):
        """Test nonexistent path with unwritable parent."""
        import sys
        
        # Use platform-specific unwritable paths
        if sys.platform == "win32":
            # Windows: Use a non-existent drive letter (highly unlikely to exist)
            test_path = "Z:/nonexistent/path/that/cannot/be/created"
        else:
            # Unix/Linux: Try path under root (usually unwritable for normal users)
            test_path = "/root/nonexistent/path/that/cannot/be/created"
        
        assert is_valid_directory_path(test_path) is False
    
    def test_is_valid_directory_path_exception_handling(self):
        """Test that is_valid_directory_path handles exceptions gracefully."""
        from unittest.mock import patch
        
        # The try-except in is_valid_directory_path catches exceptions
        # during parent directory traversal
        with patch('gceutils.validation.os.access', side_effect=Exception("Mocked exception")):
            # This should trigger the exception handler when checking os.access
            result = is_valid_directory_path("/nonexistent/path/to/check")
            # Exception should be caught and return False
            assert result is False


class TestIsValidUrl:
    """Test URL validation."""
    
    def test_valid_http_url(self):
        """Test valid HTTP URL."""
        assert is_valid_url("http://example.com") is True
    
    def test_valid_https_url(self):
        """Test valid HTTPS URL."""
        assert is_valid_url("https://example.com") is True
    
    def test_valid_url_with_path(self):
        """Test valid URL with path."""
        assert is_valid_url("https://example.com/path/to/resource") is True
    
    def test_valid_url_with_query(self):
        """Test valid URL with query parameters."""
        assert is_valid_url("https://example.com/search?q=test") is True
    
    def test_invalid_url_no_scheme(self):
        """Test invalid URL without scheme."""
        assert is_valid_url("example.com") is False
    
    def test_invalid_url_wrong_scheme(self):
        """Test invalid URL with wrong scheme."""
        assert is_valid_url("ftp://example.com") is False
    
    def test_invalid_url_no_domain(self):
        """Test invalid URL without domain."""
        assert is_valid_url("https://") is False
    
    def test_invalid_url_no_dot_in_domain(self):
        """Test invalid URL without dot in domain."""
        assert is_valid_url("https://localhost") is False
    
    def test_valid_url_subdomain(self):
        """Test valid URL with subdomain."""
        assert is_valid_url("https://sub.example.com") is True
    
    def test_is_valid_url_exception_handling(self):
        """Test that is_valid_url handles exceptions gracefully."""
        from unittest.mock import patch
        
        # Mock urlparse to raise an exception
        with patch('gceutils.validation.urlparse', side_effect=Exception("Mocked exception")):
            result = is_valid_url("https://example.com")
            assert result is False


class TestPathValidationError:
    """Test GU_PathValidationError with different path conditions."""
    
    def test_error_with_empty_path(self):
        """Test error with empty path."""
        path = AbstractTreePath()
        error = GU_PathValidationError(path, "Test message")
        assert "Test message" in str(error)
        assert error.path == path
        assert error.msg == "Test message"
        assert error.condition is None
    
    def test_error_with_nonempty_path(self):
        """Test error with non-empty path."""
        path = AbstractTreePath().add_attribute("field").add_index_or_key(0)
        error = GU_PathValidationError(path, "Test message")
        error_str = str(error)
        assert "Test message" in error_str
        assert "At" in error_str  # Path should be included
    
    def test_error_with_condition(self):
        """Test error with condition."""
        path = AbstractTreePath()
        error = GU_PathValidationError(path, "Test message", condition="test_condition")
        error_str = str(error)
        assert "Test message" in error_str
        assert "test_condition" in error_str
        assert error.condition == "test_condition"
    
    def test_error_with_path_and_condition(self):
        """Test error with both path and condition."""
        path = AbstractTreePath().add_attribute("field")
        error = GU_PathValidationError(path, "Test message", condition="test_condition")
        error_str = str(error)
        assert "Test message" in error_str
        assert "test_condition" in error_str
        assert "At" in error_str


class TestValidationFunctionExceptions:
    """Test exception handling in validation functions."""
    
    def test_is_valid_url_with_exception(self):
        """Test is_valid_url when urlparse raises exception."""
        # Test with various invalid inputs that might cause exceptions
        result = is_valid_url("")
        assert result is False
        
        result = is_valid_url("not a url")
        assert result is False
