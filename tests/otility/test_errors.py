from __future__ import annotations
import pytest

from gceutils.base import AbstractTreePath
from gceutils.errors import (
    GU_Error,
    GU_ValidationError,
    GU_PathValidationError,
)


class TestGU_PathValidationError:
    """Test GU_PathValidationError logic."""
    
    def test_error_with_empty_path_no_condition(self):
        """Test error with empty path and no condition."""
        path = AbstractTreePath()
        error = GU_PathValidationError(path, "Test message")
        
        # Check attributes
        assert error.path == path
        assert error.msg == "Test message"
        assert error.condition is None
        
        # Check message formatting (no path prefix, no condition)
        error_str = str(error)
        assert error_str == "Test message"
        assert "At" not in error_str
    
    def test_error_with_nonempty_path_no_condition(self):
        """Test error with non-empty path and no condition."""
        path = AbstractTreePath().add_attribute("field")
        error = GU_PathValidationError(path, "Test message")
        
        # Check attributes
        assert error.path == path
        assert error.msg == "Test message"
        assert error.condition is None
        
        # Check message formatting (should include path)
        error_str = str(error)
        assert "Test message" in error_str
        assert "At" in error_str
        assert "field" in error_str
    
    def test_error_with_empty_path_with_condition(self):
        """Test error with empty path and condition."""
        path = AbstractTreePath()
        error = GU_PathValidationError(path, "Test message", condition="my_condition")
        
        # Check attributes
        assert error.path == path
        assert error.msg == "Test message"
        assert error.condition == "my_condition"
        
        # Check message formatting (no path, but has condition)
        error_str = str(error)
        assert "Test message" in error_str
        assert "my_condition:" in error_str
        assert "At" not in error_str
    
    def test_error_with_nonempty_path_with_condition(self):
        """Test error with non-empty path and condition."""
        path = AbstractTreePath().add_attribute("field").add_index_or_key(0)
        error = GU_PathValidationError(path, "Test message", condition="my_condition")
        
        # Check attributes
        assert error.path == path
        assert error.msg == "Test message"
        assert error.condition == "my_condition"
        
        # Check message formatting (should include both path and condition)
        error_str = str(error)
        assert "Test message" in error_str
        assert "my_condition:" in error_str
        assert "At" in error_str
        assert "field" in error_str
    
    def test_error_message_order(self):
        """Test that error message has correct order: path, condition, message."""
        path = AbstractTreePath().add_attribute("my_field")
        error = GU_PathValidationError(path, "value is wrong", condition="when checking")
        
        error_str = str(error)
        
        # Find positions to verify order
        at_pos = error_str.find("At")
        condition_pos = error_str.find("when checking:")
        msg_pos = error_str.find("value is wrong")
        
        # All should be present
        assert at_pos != -1
        assert condition_pos != -1
        assert msg_pos != -1
        
        # Order should be: At ... : when checking: value is wrong
        assert at_pos < condition_pos < msg_pos
    
    def test_error_can_be_raised(self):
        """Test that error can be raised and caught."""
        path = AbstractTreePath()
        
        with pytest.raises(GU_PathValidationError) as exc_info:
            raise GU_PathValidationError(path, "Test error")
        
        assert "Test error" in str(exc_info.value)
    
    def test_error_is_validation_error(self):
        """Test that GU_PathValidationError is a GU_ValidationError."""
        path = AbstractTreePath()
        error = GU_PathValidationError(path, "Test")
        
        assert isinstance(error, GU_ValidationError)
        assert isinstance(error, GU_Error)
        assert isinstance(error, Exception)
    
    def test_path_with_multiple_levels(self):
        """Test error with deeply nested path."""
        path = (AbstractTreePath()
                .add_attribute("root")
                .add_index_or_key(0)
                .add_attribute("child")
                .add_index_or_key("key"))
        
        error = GU_PathValidationError(path, "Deep error")
        error_str = str(error)
        
        assert "At" in error_str
        assert "Deep error" in error_str
