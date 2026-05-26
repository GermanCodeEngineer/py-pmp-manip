from __future__ import annotations
import pytest

from gceutils import AbstractTreePath
from pmp_manip.utility.errors import (
    MANIP_Error,
    MANIP_BlameDevsError,
    MANIP_ImplementationDetailsExposedError,
    MANIP_ThanksError,
    MANIP_OpcodeInfoError,
    MANIP_UnknownOpcodeError,
    MANIP_SameOpcodeTwiceError,
    MANIP_ExtensionModuleNotFoundError,
    MANIP_UnexpectedExtensionModuleImportError,
    MANIP_UnknownBuiltinExtensionError,
    MANIP_DeserializationError,
    MANIP_ConversionError,
    MANIP_MissingInputError,
    MANIP_UnnecessaryInputError,
    MANIP_MissingDropdownError,
    MANIP_UnnecessaryDropdownError,
    MANIP_InvalidDropdownValueError,
    MANIP_InvalidOpcodeError,
    MANIP_InvalidBlockShapeError,
    MANIP_InvalidDirPathError,
    MANIP_SpriteLayerStackError,
    MANIP_SameValueTwiceError,
    MANIP_InvalidExtensionCodeSourceError,
    MANIP_FetchError,
    MANIP_NetworkFetchError,
    MANIP_UnexpectedFetchError,
    MANIP_FileFetchError,
    MANIP_NoNodeJSInstalledError,
    MANIP_SubprocessTimeoutError,
    MANIP_ExtensionExecutionErrorInJavascript,
    MANIP_UnexpectedSubprocessError,
    MANIP_ExtensionJSONDecodeError,
    MANIP_BadOrInvalidExtensionCodeError,
    MANIP_InvalidExtensionCodeSyntaxError,
    MANIP_BadExtensionCodeFormatError,
    MANIP_InvalidTranslationMessageError,
    MANIP_JsNodeTreeToJsonConversionError,
    MANIP_InvalidExtensionInformationError,
    MANIP_InvalidCustomMenuError,
    MANIP_InvalidCustomBlockError,
    MANIP_UnknownExtensionAttributeError,
    MANIP_ExtensionFetchError,
    MANIP_DirectExtensionInfoExtractionError,
    MANIP_SafeExtensionInfoExtractionError,
    MANIP_ExtensionInfoConvertionError,
    MANIP_ConfigurationError,
)


class TestMANIPErrorHierarchy:
    """Test basic error class hierarchy."""

    def test_manip_error_is_exception(self):
        """Test that MANIP_Error is an Exception."""
        assert issubclass(MANIP_Error, Exception)

    def test_blame_devs_error_is_manip_error(self):
        """Test that MANIP_BlameDevsError is a MANIP_Error."""
        assert issubclass(MANIP_BlameDevsError, MANIP_Error)

    def test_implementation_details_error_is_manip_error(self):
        """Test that MANIP_ImplementationDetailsExposedError is a MANIP_Error."""
        assert issubclass(MANIP_ImplementationDetailsExposedError, MANIP_Error)

    def test_thanks_error_is_manip_error(self):
        """Test that MANIP_ThanksError is a MANIP_Error."""
        assert issubclass(MANIP_ThanksError, MANIP_Error)

    def test_deserialization_error_is_manip_error(self):
        """Test that MANIP_DeserializationError is a MANIP_Error."""
        assert issubclass(MANIP_DeserializationError, MANIP_Error)

    def test_conversion_error_is_manip_error(self):
        """Test that MANIP_ConversionError is a MANIP_Error."""
        assert issubclass(MANIP_ConversionError, MANIP_Error)


class TestThanksError:
    """Test MANIP_ThanksError special message."""

    def test_thanks_error_message(self):
        """Test that MANIP_ThanksError has special message."""
        error = MANIP_ThanksError()
        msg = str(error)
        assert "unique" in msg.lower()
        assert "research" in msg.lower()
        assert "github.com" in msg.lower()

    def test_thanks_error_no_args(self):
        """Test that MANIP_ThanksError takes no arguments."""
        error = MANIP_ThanksError()
        assert error is not None


class TestDeserializationError:
    """Test MANIP_DeserializationError with custom message."""

    def test_deserialization_error_message(self):
        """Test message formatting of deserialization error."""
        error = MANIP_DeserializationError("custom message")
        msg = str(error)
        assert "Issue during deserialization" in msg
        assert "custom message" in msg

    def test_deserialization_error_empty_message(self):
        """Test with empty message."""
        error = MANIP_DeserializationError("")
        msg = str(error)
        assert "Issue during deserialization" in msg


class TestSameValueTwiceError:
    """Test MANIP_SameValueTwiceError with path and condition."""

    def test_same_value_twice_error_basic(self):
        """Test basic initialization."""
        path1 = AbstractTreePath().add_attribute("field1")
        path2 = AbstractTreePath().add_attribute("field2")
        error = MANIP_SameValueTwiceError(path1, path2, "Value conflict")
        
        assert error.path1 == path1
        assert error.path2 == path2
        assert error.msg == "Value conflict"
        assert error.condition is None

    def test_same_value_twice_error_with_condition(self):
        """Test with condition parameter."""
        path1 = AbstractTreePath().add_attribute("field1")
        path2 = AbstractTreePath().add_attribute("field2")
        error = MANIP_SameValueTwiceError(
            path1, path2, "Value conflict", condition="duplicate"
        )
        
        assert error.path1 == path1
        assert error.path2 == path2
        assert error.msg == "Value conflict"
        assert error.condition == "duplicate"

    def test_same_value_twice_error_message_format(self):
        """Test message formatting."""
        path1 = AbstractTreePath().add_attribute("field1")
        path2 = AbstractTreePath().add_attribute("field2")
        error = MANIP_SameValueTwiceError(path1, path2, "Value conflict")
        
        msg = str(error)
        assert "field1" in msg or "At" in msg  # Path should be in message
        assert "Value conflict" in msg

    def test_same_value_twice_error_message_with_condition(self):
        """Test message formatting with condition."""
        path1 = AbstractTreePath().add_attribute("field1")
        path2 = AbstractTreePath().add_attribute("field2")
        error = MANIP_SameValueTwiceError(
            path1, path2, "Value conflict", condition="duplicate"
        )
        
        msg = str(error)
        assert "duplicate" in msg
        assert "Value conflict" in msg


class TestOpcodeInfoErrors:
    """Test opcode info related errors."""

    def test_opcode_info_error_is_manip_error(self):
        """Test MANIP_OpcodeInfoError hierarchy."""
        assert issubclass(MANIP_OpcodeInfoError, MANIP_Error)

    def test_unknown_opcode_error_is_opcode_info_error(self):
        """Test MANIP_UnknownOpcodeError hierarchy."""
        assert issubclass(MANIP_UnknownOpcodeError, MANIP_OpcodeInfoError)

    def test_same_opcode_twice_error_is_opcode_info_error(self):
        """Test MANIP_SameOpcodeTwiceError hierarchy."""
        assert issubclass(MANIP_SameOpcodeTwiceError, MANIP_OpcodeInfoError)

    def test_create_opcode_errors(self):
        """Test creating opcode info errors."""
        error1 = MANIP_UnknownOpcodeError("test")
        error2 = MANIP_SameOpcodeTwiceError("test")
        assert isinstance(error1, MANIP_OpcodeInfoError)
        assert isinstance(error2, MANIP_OpcodeInfoError)


class TestExtensionErrors:
    """Test extension related errors."""

    def test_extension_module_not_found_error(self):
        """Test MANIP_ExtensionModuleNotFoundError."""
        assert issubclass(MANIP_ExtensionModuleNotFoundError, MANIP_Error)
        error = MANIP_ExtensionModuleNotFoundError("test")
        assert isinstance(error, MANIP_Error)

    def test_unexpected_extension_module_import_error(self):
        """Test MANIP_UnexpectedExtensionModuleImportError."""
        assert issubclass(MANIP_UnexpectedExtensionModuleImportError, MANIP_Error)
        error = MANIP_UnexpectedExtensionModuleImportError("test")
        assert isinstance(error, MANIP_Error)

    def test_unknown_builtin_extension_error(self):
        """Test MANIP_UnknownBuiltinExtensionError."""
        assert issubclass(MANIP_UnknownBuiltinExtensionError, MANIP_Error)
        error = MANIP_UnknownBuiltinExtensionError("test")
        assert isinstance(error, MANIP_Error)


class TestValidationErrors:
    """Test validation related errors."""

    def test_missing_input_error_hierarchy(self):
        """Test MANIP_MissingInputError hierarchy."""
        assert issubclass(MANIP_MissingInputError, ValueError)

    def test_unnecessary_input_error_hierarchy(self):
        """Test MANIP_UnnecessaryInputError hierarchy."""
        assert issubclass(MANIP_UnnecessaryInputError, ValueError)

    def test_missing_dropdown_error_hierarchy(self):
        """Test MANIP_MissingDropdownError hierarchy."""
        assert issubclass(MANIP_MissingDropdownError, ValueError)

    def test_unnecessary_dropdown_error_hierarchy(self):
        """Test MANIP_UnnecessaryDropdownError hierarchy."""
        assert issubclass(MANIP_UnnecessaryDropdownError, ValueError)

    def test_invalid_dropdown_value_error_hierarchy(self):
        """Test MANIP_InvalidDropdownValueError hierarchy."""
        assert issubclass(MANIP_InvalidDropdownValueError, ValueError)

    def test_invalid_opcode_error_hierarchy(self):
        """Test MANIP_InvalidOpcodeError hierarchy."""
        assert issubclass(MANIP_InvalidOpcodeError, ValueError)

    def test_invalid_block_shape_error_hierarchy(self):
        """Test MANIP_InvalidBlockShapeError hierarchy."""
        assert issubclass(MANIP_InvalidBlockShapeError, ValueError)

    def test_invalid_dir_path_error_hierarchy(self):
        """Test MANIP_InvalidDirPathError hierarchy."""
        assert issubclass(MANIP_InvalidDirPathError, ValueError)

    def test_sprite_layer_stack_error_hierarchy(self):
        """Test MANIP_SpriteLayerStackError hierarchy."""
        assert issubclass(MANIP_SpriteLayerStackError, ValueError)

    def test_create_validation_errors(self):
        """Test creating various validation errors."""
        path = AbstractTreePath().add_attribute("field")
        errors = [
            MANIP_MissingInputError(path, "msg"),
            MANIP_UnnecessaryInputError(path, "msg"),
            MANIP_MissingDropdownError(path, "msg"),
            MANIP_UnnecessaryDropdownError(path, "msg"),
            MANIP_InvalidDropdownValueError(path, "msg"),
            MANIP_InvalidOpcodeError(path, "msg"),
            MANIP_InvalidBlockShapeError(path, "msg"),
            MANIP_InvalidDirPathError(path, "msg"),
            MANIP_SpriteLayerStackError(path, "msg"),
        ]
        for error in errors:
            # These are path validation errors, so they inherit from ValueError
            assert isinstance(error, ValueError)


class TestFetchErrors:
    """Test fetch related errors."""

    def test_fetch_error_is_manip_error(self):
        """Test MANIP_FetchError hierarchy."""
        assert issubclass(MANIP_FetchError, MANIP_Error)

    def test_network_fetch_error_is_fetch_error(self):
        """Test MANIP_NetworkFetchError hierarchy."""
        assert issubclass(MANIP_NetworkFetchError, MANIP_FetchError)

    def test_unexpected_fetch_error_is_fetch_error(self):
        """Test MANIP_UnexpectedFetchError hierarchy."""
        assert issubclass(MANIP_UnexpectedFetchError, MANIP_FetchError)

    def test_file_fetch_error_is_fetch_error(self):
        """Test MANIP_FileFetchError hierarchy."""
        assert issubclass(MANIP_FileFetchError, MANIP_FetchError)

    def test_create_fetch_errors(self):
        """Test creating fetch errors."""
        errors = [
            MANIP_InvalidExtensionCodeSourceError("msg"),
            MANIP_NetworkFetchError("msg"),
            MANIP_UnexpectedFetchError("msg"),
            MANIP_FileFetchError("msg"),
        ]
        for error in errors:
            assert isinstance(error, MANIP_Error)


class TestSubprocessErrors:
    """Test subprocess related errors."""

    def test_no_nodejs_installed_error(self):
        """Test MANIP_NoNodeJSInstalledError."""
        assert issubclass(MANIP_NoNodeJSInstalledError, MANIP_Error)
        error = MANIP_NoNodeJSInstalledError("msg")
        assert isinstance(error, MANIP_Error)

    def test_subprocess_timeout_error(self):
        """Test MANIP_SubprocessTimeoutError."""
        assert issubclass(MANIP_SubprocessTimeoutError, MANIP_Error)
        error = MANIP_SubprocessTimeoutError("msg")
        assert isinstance(error, MANIP_Error)

    def test_extension_execution_error(self):
        """Test MANIP_ExtensionExecutionErrorInJavascript."""
        assert issubclass(MANIP_ExtensionExecutionErrorInJavascript, MANIP_Error)
        error = MANIP_ExtensionExecutionErrorInJavascript("msg")
        assert isinstance(error, MANIP_Error)

    def test_unexpected_subprocess_error(self):
        """Test MANIP_UnexpectedSubprocessError."""
        assert issubclass(MANIP_UnexpectedSubprocessError, MANIP_Error)
        error = MANIP_UnexpectedSubprocessError("msg")
        assert isinstance(error, MANIP_Error)


class TestExtensionCodeErrors:
    """Test extension code related errors."""

    def test_bad_or_invalid_extension_code_error(self):
        """Test MANIP_BadOrInvalidExtensionCodeError."""
        assert issubclass(MANIP_BadOrInvalidExtensionCodeError, MANIP_Error)
        error = MANIP_BadOrInvalidExtensionCodeError("msg")
        assert isinstance(error, MANIP_Error)

    def test_invalid_extension_code_syntax_error(self):
        """Test MANIP_InvalidExtensionCodeSyntaxError."""
        assert issubclass(MANIP_InvalidExtensionCodeSyntaxError, MANIP_BadOrInvalidExtensionCodeError)
        error = MANIP_InvalidExtensionCodeSyntaxError("msg")
        assert isinstance(error, MANIP_BadOrInvalidExtensionCodeError)

    def test_bad_extension_code_format_error(self):
        """Test MANIP_BadExtensionCodeFormatError."""
        assert issubclass(MANIP_BadExtensionCodeFormatError, MANIP_BadOrInvalidExtensionCodeError)
        error = MANIP_BadExtensionCodeFormatError("msg")
        assert isinstance(error, MANIP_BadOrInvalidExtensionCodeError)

    def test_invalid_translation_message_error(self):
        """Test MANIP_InvalidTranslationMessageError."""
        assert issubclass(MANIP_InvalidTranslationMessageError, MANIP_BadOrInvalidExtensionCodeError)
        error = MANIP_InvalidTranslationMessageError("msg")
        assert isinstance(error, MANIP_BadOrInvalidExtensionCodeError)

    def test_extension_json_decode_error(self):
        """Test MANIP_ExtensionJSONDecodeError."""
        assert issubclass(MANIP_ExtensionJSONDecodeError, MANIP_Error)
        error = MANIP_ExtensionJSONDecodeError("msg")
        assert isinstance(error, MANIP_Error)

    def test_js_node_tree_to_json_conversion_error(self):
        """Test MANIP_JsNodeTreeToJsonConversionError."""
        assert issubclass(MANIP_JsNodeTreeToJsonConversionError, MANIP_Error)
        error = MANIP_JsNodeTreeToJsonConversionError("msg")
        assert isinstance(error, MANIP_Error)


class TestExtensionInformationErrors:
    """Test extension information related errors."""

    def test_invalid_extension_information_error(self):
        """Test MANIP_InvalidExtensionInformationError."""
        assert issubclass(MANIP_InvalidExtensionInformationError, MANIP_Error)
        error = MANIP_InvalidExtensionInformationError("msg")
        assert isinstance(error, MANIP_Error)

    def test_invalid_custom_menu_error(self):
        """Test MANIP_InvalidCustomMenuError."""
        assert issubclass(MANIP_InvalidCustomMenuError, MANIP_InvalidExtensionInformationError)
        error = MANIP_InvalidCustomMenuError("msg")
        assert isinstance(error, MANIP_InvalidExtensionInformationError)

    def test_invalid_custom_block_error(self):
        """Test MANIP_InvalidCustomBlockError."""
        assert issubclass(MANIP_InvalidCustomBlockError, MANIP_InvalidExtensionInformationError)
        error = MANIP_InvalidCustomBlockError("msg")
        assert isinstance(error, MANIP_InvalidExtensionInformationError)

    def test_unknown_extension_attribute_error(self):
        """Test MANIP_UnknownExtensionAttributeError."""
        assert issubclass(MANIP_UnknownExtensionAttributeError, MANIP_InvalidExtensionInformationError)
        error = MANIP_UnknownExtensionAttributeError("msg")
        assert isinstance(error, MANIP_InvalidExtensionInformationError)


class TestExtensionInfoErrors:
    """Test extension info generation and API errors."""

    def test_extension_fetch_error(self):
        """Test MANIP_ExtensionFetchError."""
        assert issubclass(MANIP_ExtensionFetchError, MANIP_Error)
        error = MANIP_ExtensionFetchError("msg")
        assert isinstance(error, MANIP_Error)

    def test_direct_extension_info_extraction_error(self):
        """Test MANIP_DirectExtensionInfoExtractionError."""
        assert issubclass(MANIP_DirectExtensionInfoExtractionError, MANIP_Error)
        error = MANIP_DirectExtensionInfoExtractionError("msg")
        assert isinstance(error, MANIP_Error)

    def test_safe_extension_info_extraction_error(self):
        """Test MANIP_SafeExtensionInfoExtractionError."""
        assert issubclass(MANIP_SafeExtensionInfoExtractionError, MANIP_Error)
        error = MANIP_SafeExtensionInfoExtractionError("msg")
        assert isinstance(error, MANIP_Error)

    def test_extension_info_convertion_error(self):
        """Test MANIP_ExtensionInfoConvertionError."""
        assert issubclass(MANIP_ExtensionInfoConvertionError, MANIP_Error)
        error = MANIP_ExtensionInfoConvertionError("msg")
        assert isinstance(error, MANIP_Error)


class TestConfigurationError:
    """Test configuration error."""

    def test_configuration_error_is_manip_error(self):
        """Test MANIP_ConfigurationError hierarchy."""
        assert issubclass(MANIP_ConfigurationError, MANIP_Error)

    def test_create_configuration_error(self):
        """Test creating configuration error."""
        error = MANIP_ConfigurationError("Invalid config")
        assert isinstance(error, MANIP_Error)
        assert "Invalid config" in str(error)
