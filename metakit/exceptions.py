#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
metakit exception classes
"""


class MetakitError(Exception):
    """Base exception class for metakit library"""
    pass


class UnsupportedFormatError(MetakitError):
    """Unsupported format exception"""

    def __init__(self, format_name=None):
        if format_name:
            message = f"Unsupported format: {format_name}"
        else:
            message = "Unsupported format"
        super().__init__(message)
        self.format_name = format_name


class MetadataReadError(MetakitError):
    """Metadata read exception"""
    pass


class MetadataWriteError(MetakitError):
    """Metadata write exception"""
    pass


class InvalidMetadataError(MetakitError):
    """Invalid metadata exception"""
    pass
