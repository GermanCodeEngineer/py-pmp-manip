from __future__ import annotations
import pytest

from pmp_manip.utility.errors import (
    MANIP_BlameDevsError,
    MANIP_ImplementationDetailsExposedError,
    MANIP_ThanksError
)


class TestBlameDevsError:
    """Test MANIP_BlameDevsError exception."""
    
    def test_raise_blame_devs_error(self):
        """Test raising BlameDevsError."""
        with pytest.raises(MANIP_BlameDevsError):
            raise MANIP_BlameDevsError("This is a dev error")
    
    def test_blame_devs_error_message(self):
        """Test BlameDevsError message."""
        try:
            raise MANIP_BlameDevsError("Dev mistake")
        except MANIP_BlameDevsError as e:
            assert "Dev mistake" in str(e)
    
    def test_blame_devs_error_inheritance(self):
        """Test that BlameDevsError is an Exception."""
        error = MANIP_BlameDevsError("test")
        assert isinstance(error, Exception)


class TestImplementationDetailsExposedError:
    """Test MANIP_ImplementationDetailsExposedError exception."""
    
    def test_raise_implementation_details_error(self):
        """Test raising ImplementationDetailsExposedError."""
        with pytest.raises(MANIP_ImplementationDetailsExposedError):
            raise MANIP_ImplementationDetailsExposedError("Implementation detail leaked")
    
    def test_implementation_details_error_message(self):
        """Test ImplementationDetailsExposedError message."""
        try:
            raise MANIP_ImplementationDetailsExposedError("Details leaked")
        except MANIP_ImplementationDetailsExposedError as e:
            assert "Details leaked" in str(e)
    
    def test_implementation_details_error_inheritance(self):
        """Test that ImplementationDetailsExposedError is an Exception."""
        error = MANIP_ImplementationDetailsExposedError("test")
        assert isinstance(error, Exception)


class TestThanksError:
    """Test MANIP_ThanksError exception."""
    
    def test_raise_thanks_error(self):
        """Test raising ThanksError."""
        with pytest.raises(MANIP_ThanksError):
            raise MANIP_ThanksError()
    
    def test_thanks_error_message(self):
        """Test ThanksError message."""
        try:
            raise MANIP_ThanksError()
        except MANIP_ThanksError as e:
            # ThanksError has a fixed message
            assert "unique" in str(e).lower() or "research" in str(e).lower()
    
    def test_thanks_error_inheritance(self):
        """Test that ThanksError is an Exception."""
        error = MANIP_ThanksError()
        assert isinstance(error, Exception)


class TestErrorInheritance:
    """Test error inheritance hierarchy."""
    
    def test_blame_devs_is_exception(self):
        """Test BlameDevsError is an Exception."""
        with pytest.raises(Exception):
            raise MANIP_BlameDevsError("test")
    
    def test_implementation_details_is_exception(self):
        """Test ImplementationDetailsExposedError is an Exception."""
        with pytest.raises(Exception):
            raise MANIP_ImplementationDetailsExposedError("test")
    
    def test_thanks_is_exception(self):
        """Test ThanksError is an Exception."""
        with pytest.raises(Exception):
            raise MANIP_ThanksError()
