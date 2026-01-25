from __future__ import annotations
from typing     import TYPE_CHECKING

if TYPE_CHECKING: from pmp_manip.otility.base import AbstractTreePath


class MANIPO_Error(Exception): pass


class MANIPO_ValidationError(MANIPO_Error): pass
class MANIPO_PathValidationError(MANIPO_ValidationError):
    def __init__(self, path: AbstractTreePath, msg: str, condition: str|None = None) -> None:
        self.path      = path
        self.msg       = msg
        self.condition = condition
        
        full_message = ""
        if len(path) > 0:
            full_message += f"At {path!r}: "
        if condition is not None:
            full_message += f"{condition}: "
        full_message += msg
        super().__init__(full_message)
    
class MANIPO_TypeValidationError(MANIPO_PathValidationError): pass
class MANIPO_InvalidValueError(MANIPO_PathValidationError): pass
class MANIPO_RangeValidationError(MANIPO_PathValidationError): pass


class MANIPO_FailedFileWriteError(MANIPO_Error): pass
class MANIPO_FailedFileReadError(MANIPO_Error): pass
class MANIPO_FailedFileDeleteError(MANIPO_Error): pass
class MANIPO_FileNotFoundError(OSError): pass


__all__ = [
    "MANIPO_Error", "MANIPO_ValidationError", "MANIPO_PathValidationError",
    "MANIPO_TypeValidationError", "MANIPO_InvalidValueError", "MANIPO_RangeValidationError",
    "MANIPO_FailedFileWriteError", "MANIPO_FailedFileReadError", "MANIPO_FailedFileDeleteError",
    "MANIPO_FileNotFoundError",
]

