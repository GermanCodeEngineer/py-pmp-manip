from __future__ import annotations
import pytest
import warnings

from pmp_manip.utility.warnings import (
    MANIP_Warning,
    MANIP_UnexpectedPropertyAccessWarning,
    MANIP_UnexpectedNotPossibleFeatureWarning,
)


class TestMANIPWarningHierarchy:
    """Test warning class hierarchy."""

    def test_manip_warning_is_user_warning(self):
        """Test that MANIP_Warning is a UserWarning."""
        assert issubclass(MANIP_Warning, UserWarning)

    def test_unexpected_property_access_warning_is_manip_warning(self):
        """Test that MANIP_UnexpectedPropertyAccessWarning is a MANIP_Warning."""
        assert issubclass(MANIP_UnexpectedPropertyAccessWarning, MANIP_Warning)

    def test_unexpected_not_possible_feature_warning_is_manip_warning(self):
        """Test that MANIP_UnexpectedNotPossibleFeatureWarning is a MANIP_Warning."""
        assert issubclass(MANIP_UnexpectedNotPossibleFeatureWarning, MANIP_Warning)


class TestMANIPWarning:
    """Test MANIP_Warning basic functionality."""

    def test_create_warning(self):
        """Test creating a MANIP_Warning."""
        warning = MANIP_Warning("Test warning")
        assert isinstance(warning, UserWarning)
        assert str(warning) == "Test warning"

    def test_issue_warning(self):
        """Test issuing a MANIP_Warning."""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            warnings.warn("Test", MANIP_Warning)
            assert len(w) == 1
            assert issubclass(w[0].category, MANIP_Warning)
            assert "Test" in str(w[0].message)


class TestUnexpectedPropertyAccessWarning:
    """Test MANIP_UnexpectedPropertyAccessWarning."""

    def test_create_warning(self):
        """Test creating warning."""
        warning = MANIP_UnexpectedPropertyAccessWarning("Unexpected property")
        assert isinstance(warning, MANIP_Warning)

    def test_issue_warning(self):
        """Test issuing the warning."""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            warnings.warn("Property access", MANIP_UnexpectedPropertyAccessWarning)
            assert len(w) == 1
            assert issubclass(w[0].category, MANIP_UnexpectedPropertyAccessWarning)

    def test_inherits_from_manip_warning(self):
        """Test inheritance chain."""
        warning = MANIP_UnexpectedPropertyAccessWarning("test")
        assert isinstance(warning, MANIP_Warning)
        assert isinstance(warning, UserWarning)
        assert isinstance(warning, Warning)


class TestUnexpectedNotPossibleFeatureWarning:
    """Test MANIP_UnexpectedNotPossibleFeatureWarning."""

    def test_create_warning(self):
        """Test creating warning."""
        warning = MANIP_UnexpectedNotPossibleFeatureWarning("Feature not possible")
        assert isinstance(warning, MANIP_Warning)

    def test_issue_warning(self):
        """Test issuing the warning."""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            warnings.warn("Not possible", MANIP_UnexpectedNotPossibleFeatureWarning)
            assert len(w) == 1
            assert issubclass(w[0].category, MANIP_UnexpectedNotPossibleFeatureWarning)

    def test_inherits_from_manip_warning(self):
        """Test inheritance chain."""
        warning = MANIP_UnexpectedNotPossibleFeatureWarning("test")
        assert isinstance(warning, MANIP_Warning)
        assert isinstance(warning, UserWarning)
        assert isinstance(warning, Warning)


class TestWarningMessages:
    """Test warning messages."""

    def test_manip_warning_with_detailed_message(self):
        """Test MANIP_Warning with detailed message."""
        message = "Detailed warning message"
        warning = MANIP_Warning(message)
        assert str(warning) == message

    def test_property_warning_with_property_info(self):
        """Test property access warning with property information."""
        message = "Unexpected property: x"
        warning = MANIP_UnexpectedPropertyAccessWarning(message)
        assert "property" in str(warning).lower()

    def test_feature_warning_with_feature_info(self):
        """Test feature warning with feature information."""
        message = "Feature XYZ is not possible"
        warning = MANIP_UnexpectedNotPossibleFeatureWarning(message)
        assert "feature" in str(warning).lower() or "possible" in str(warning).lower()
