from __future__ import annotations
from typing     import TYPE_CHECKING

if TYPE_CHECKING: from gceutils.base import AbstractTreePath


class GU_Error(Exception):
    """Base exception for all errors in GceUtils."""


class GU_ValidationError(GU_Error):
    """Base exception for all validation errors in GceUtils."""
class GU_PathValidationError(GU_ValidationError):
    """Validation error with location tracking for nested structures.
    
    Combines path, message, and optional condition to create descriptive validation errors.
    Message automatically includes path location and condition if provided.
    """
    def __init__(self, path: AbstractTreePath, msg: str, condition: str|None = None) -> None:
        self.path      = path
        self.msg       = msg
        self.condition = condition
        
        full_message = ""
        if len(path) > 0:
            full_message += f"At {path.repr_as_python_code()}: "
        if condition is not None:
            full_message += f"{condition}: "
        full_message += msg
        super().__init__(full_message)
    
class GU_TypeValidationError(GU_PathValidationError, TypeError): pass
class GU_InvalidValueError(GU_PathValidationError, ValueError): pass
class GU_RangeValidationError(GU_PathValidationError, ValueError): pass


class GU_FailedFileWriteError(GU_Error, OSError): pass
class GU_FailedFileReadError(GU_Error, OSError): pass
class GU_FailedFileDeleteError(GU_Error, OSError): pass
class GU_FileNotFoundError(GU_Error, FileNotFoundError): pass


__all__ = [
    "GU_Error", "GU_ValidationError", "GU_PathValidationError",
    "GU_TypeValidationError", "GU_InvalidValueError", "GU_RangeValidationError",
    "GU_FailedFileWriteError", "GU_FailedFileReadError", "GU_FailedFileDeleteError",
    "GU_FileNotFoundError",
]

