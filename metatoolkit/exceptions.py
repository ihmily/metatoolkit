#!/usr/bin/env python

"""
metatoolkit exception classes
"""


class MetaToolkitError(Exception):
    """Base exception class for metatoolkit library"""
    pass


class UnsupportedFormatError(MetaToolkitError):
    """Unsupported format exception"""

    def __init__(self, format_name=None):
        if format_name:
            message = f"Unsupported format: {format_name}"
        else:
            message = "Unsupported format"
        super().__init__(message)
        self.format_name = format_name


class MetadataReadError(MetaToolkitError):
    """Metadata read exception"""
    pass


class MetadataWriteError(MetaToolkitError):
    """Metadata write exception"""
    pass


class InvalidMetadataError(MetaToolkitError):
    """Invalid metadata exception"""
    pass
