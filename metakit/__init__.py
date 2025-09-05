#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
metakit - Image, video and audio metadata processing tool
"""

__version__ = '0.1.0'
__author__ = 'Hmily'

from .exceptions import MetakitError, UnsupportedFormatError
from .image import ImageMetadataManager, add_image_metadata, read_image_metadata, get_all_image_metadata
from .video import VideoMetadataManager, add_video_metadata, read_video_metadata, get_all_video_metadata
from .audio import AudioMetadataManager, add_audio_metadata, read_audio_metadata, get_all_audio_metadata

__all__ = [
    'ImageMetadataManager',
    'VideoMetadataManager',
    'AudioMetadataManager',
    'add_image_metadata',
    'read_image_metadata',
    'get_all_image_metadata',
    'add_video_metadata',
    'read_video_metadata',
    'get_all_video_metadata',
    'add_audio_metadata',
    'read_audio_metadata',
    'get_all_audio_metadata',
    'MetakitError',
    'UnsupportedFormatError',
]