#!/usr/bin/env python

"""
metatoolkit - Image, video and audio metadata processing tool
"""

__version__ = '0.1.0'
__author__ = 'Hmily'

from .audio import AudioMetadataManager, add_audio_metadata, get_all_audio_metadata, read_audio_metadata
from .exceptions import MetaToolkitError, UnsupportedFormatError
from .image import ImageMetadataManager, add_image_metadata, get_all_image_metadata, read_image_metadata
from .video import VideoMetadataManager, add_video_metadata, get_all_video_metadata, read_video_metadata

__all__ = [
    'AudioMetadataManager',
    'ImageMetadataManager',
    'MetaToolkitError',
    'UnsupportedFormatError',
    'VideoMetadataManager',
    'add_audio_metadata',
    'add_image_metadata',
    'add_video_metadata',
    'get_all_audio_metadata',
    'get_all_image_metadata',
    'get_all_video_metadata',
    'read_audio_metadata',
    'read_image_metadata',
    'read_video_metadata',
]