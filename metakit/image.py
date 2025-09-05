#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
metakit image metadata processing module
"""

import os
import json
import time
import logging
from datetime import datetime
from typing import Dict, Optional, Any

from PIL import Image, ExifTags
from PIL.PngImagePlugin import PngInfo
import pyexiv2

from .core import BaseMetadataManager
from .exceptions import (
    UnsupportedFormatError,
    MetadataReadError,
    MetadataWriteError,
)

logger = logging.getLogger(__name__)


class ImageMetadataManager(BaseMetadataManager):
    # Supported image formats
    SUPPORTED_FORMATS = ('JPEG', 'PNG')

    # Extended default metadata fields
    DEFAULT_METADATA_FIELDS = {
        **BaseMetadataManager.DEFAULT_METADATA_FIELDS,
        "timestamp": None,
        "identifier": None
    }

    # JPEG Exif UserComment tag ID
    EXIF_USER_COMMENT = 0x9286

    XMP_NAMESPACE = 'Xmp.metakit.'
    XMP_NAMESPACE_URI = 'http://github.com/ihmily/metakit/'

    def __init__(self, custom_metadata: Optional[Dict[str, Any]] = None):
        super().__init__(custom_metadata)

        self.metadata.update({
            "timestamp": datetime.now().isoformat(),
            "identifier": f"metakit-{int(time.time())}"
        })

        try:
            pyexiv2.registerNs(self.XMP_NAMESPACE_URI, 'metakit')
        except Exception as e:
            logger.warning(f"Error registering XMP namespace: {e}")

    def add_metadata(self, image_path: str, output_path: Optional[str] = None) -> str:
        """
        Automatically select the method to add metadata based on image format

        Args:
            image_path (str): Input image path
            output_path (str, optional): Output image path, auto-generated if None

        Returns:
            str: Output image path

        Raises:
            UnsupportedFormatError: If image format is not supported
            MetadataWriteError: If metadata writing fails
        """
        try:
            if not self.validate_file_exists(image_path):
                raise FileNotFoundError(f"Image file does not exist: {image_path}")

            with Image.open(image_path) as img:
                if img.format not in self.SUPPORTED_FORMATS:
                    raise UnsupportedFormatError(img.format)

                if output_path is None:
                    output_path = self.generate_output_path(image_path)

                if img.format == 'JPEG':
                    return self._add_metadata_to_jpeg(image_path, output_path)
                elif img.format == 'PNG':
                    return self._add_metadata_to_png(image_path, output_path)

        except (IOError, OSError) as e:
            logger.error(f"Error processing image: {e}")
            raise MetadataWriteError(f"Error processing image: {e}")

    def _add_metadata_to_jpeg(self, image_path: str, output_path: str) -> str:
        """
        Add metadata identifier to JPEG image

        Args:
            image_path (str): Input image path
            output_path (str): Output image path

        Returns:
            str: Output image path

        Raises:
            MetadataWriteError: If metadata writing fails
        """
        try:

            with Image.open(image_path) as img:
                if img.format != 'JPEG':
                    img = img.convert('RGB')

                img.save(output_path, format='JPEG')

            with pyexiv2.Image(output_path) as img_meta:
                xmp_data = {}
                for key, value in self.metadata.items():
                    if isinstance(value, (dict, list)):
                        value = json.dumps(value, ensure_ascii=False)
                    elif value is not None:
                        value = str(value)
                    else:
                        value = ""

                    xmp_key = f"{self.XMP_NAMESPACE}{key}"
                    xmp_data[xmp_key] = value

                if xmp_data:
                    img_meta.modify_xmp(xmp_data)

            logger.info(f"Added metadata identifier to JPEG image, saved to: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"Error adding metadata to JPEG: {e}")
            raise MetadataWriteError(f"Error adding metadata to JPEG: {e}")

    def _add_metadata_to_png(self, image_path: str, output_path: str) -> str:
        """
        Add metadata identifier to PNG image

        Args:
            image_path (str): Input image path
            output_path (str): Output image path

        Returns:
            str: Output image path

        Raises:
            MetadataWriteError: If metadata writing fails
        """
        try:
            with Image.open(image_path) as img:
                if img.format != 'PNG':
                    img = img.convert('RGBA')

                metadata = PngInfo()

                for key, value in self.metadata.items():
                    metadata.add_text(key, str(value))

                img.save(output_path, format='PNG', pnginfo=metadata)
                logger.info(f"Added metadata identifier to PNG image, saved to: {output_path}")
                return output_path

        except Exception as e:
            logger.error(f"Error adding metadata to PNG: {e}")
            raise MetadataWriteError(f"Error adding metadata to PNG: {e}")

    def read_metadata(self, image_path: str, metadata_key: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Read image metadata identifier

        Args:
            image_path (str): Image path
            metadata_key (str, optional): Specific metadata field name to read, returns all metadata if None

        Returns:
            dict: Metadata dictionary, returns None if not found. If metadata_key is specified, returns the value of that field

        Raises:
            UnsupportedFormatError: If image format is not supported
            MetadataReadError: If metadata reading fails
        """
        try:
            if not self.validate_file_exists(image_path):
                raise FileNotFoundError(f"Image file does not exist: {image_path}")

            with Image.open(image_path) as img:
                if img.format not in self.SUPPORTED_FORMATS:
                    raise UnsupportedFormatError(img.format)

                if img.format == 'JPEG':
                    metadata = self._read_jpeg_metadata(img, metadata_key)
                elif img.format == 'PNG':
                    metadata = self._read_png_metadata(img, metadata_key)
                else:
                    metadata = None

                if metadata_key and metadata and metadata_key in metadata:
                    return {metadata_key: metadata[metadata_key]}
                elif metadata_key and metadata:
                    return None  # Specified field does not exist
                else:
                    return metadata

        except (IOError, OSError) as e:
            logger.error(f"Error reading image: {e}")
            raise MetadataReadError(f"Error reading image: {e}")

    def _read_jpeg_metadata(self, img: Image.Image, metadata_key: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Read JPEG image metadata identifier

        Args:
            img (PIL.Image.Image): Opened image object
            metadata_key (str, optional): Specific metadata field name to read

        Returns:
            dict: Metadata dictionary, returns None if not found
        """
        try:
            file_path = getattr(img, 'filename', None)
            if file_path and os.path.exists(file_path):
                try:
                    with pyexiv2.Image(file_path) as img_meta:
                        xmp_data = img_meta.read_xmp()
                        if xmp_data:
                            metadata = {}
                            prefix = self.XMP_NAMESPACE
                            prefix_len = len(prefix)

                            for key, value in xmp_data.items():
                                if key.startswith(prefix):
                                    clean_key = key[prefix_len:]
                                    try:
                                        if value and (value.startswith('{') or value.startswith('[')):
                                            metadata[clean_key] = json.loads(value)
                                        else:
                                            metadata[clean_key] = value
                                    except (json.JSONDecodeError, TypeError):
                                        metadata[clean_key] = value
                                else:
                                    metadata[key] = value

                            if metadata:
                                logger.info("Found JPEG XMP metadata identifier")

                                if metadata_key and metadata_key in metadata:
                                    return {metadata_key: metadata[metadata_key]}
                                elif metadata_key:
                                    return None  # Specified field does not exist
                                else:
                                    return metadata
                except Exception as e:
                    logger.warning(f"Error reading XMP metadata: {e}")

            logger.info("No JPEG metadata identifier found")
            return None

        except Exception as e:
            logger.error(f"Error reading JPEG metadata: {e}")
            return None

    @staticmethod
    def _read_png_metadata(img: Image.Image, metadata_key: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Read PNG image metadata identifier

        Args:
            img (PIL.Image.Image): Opened image object
            metadata_key (str, optional): Specific metadata field name to read

        Returns:
            dict: Metadata dictionary, returns None if not found
        """
        try:
            if 'ai_generated' in img.info:
                metadata = {}

                for key, value in img.info.items():
                    if key.startswith("metakit_"):
                        metadata[key[8:]] = value
                    else:
                        metadata[key] = value

                if metadata:
                    logger.info("Found PNG metadata identifier")

                    if metadata_key and metadata_key in metadata:
                        return {metadata_key: metadata[metadata_key]}
                    elif metadata_key:
                        return None  # Specified field does not exist
                    else:
                        return metadata

            logger.info("No PNG metadata identifier found")
            return None

        except Exception as e:
            logger.error(f"Error reading PNG metadata: {e}")
            return None

    def get_all_metadata(self, image_path: str) -> Dict[str, Any]:
        """
        Get all metadata of the image

        Args:
            image_path (str): Image path

        Returns:
            dict: All metadata dictionary

        Raises:
            UnsupportedFormatError: If image format is not supported
            MetadataReadError: If metadata reading fails
        """
        try:
            if not self.validate_file_exists(image_path):
                raise FileNotFoundError(f"Image file does not exist: {image_path}")

            with Image.open(image_path) as img:
                if img.format not in self.SUPPORTED_FORMATS:
                    raise UnsupportedFormatError(img.format)

                if img.format == 'JPEG':
                    return self._get_all_jpeg_metadata(img)
                elif img.format == 'PNG':
                    return self._get_all_png_metadata(img)

        except (IOError, OSError) as e:
            logger.error(f"Error reading image: {e}")
            raise MetadataReadError(f"Error reading image: {e}")

    @staticmethod
    def _get_all_jpeg_metadata(img: Image.Image) -> Dict[str, Any]:
        """
        Get all metadata of JPEG image

        Args:
            img (PIL.Image.Image): Opened image object

        Returns:
            dict: All metadata dictionary
        """
        result = {}

        try:
            exif_data = img.getexif() if hasattr(img, 'getexif') else None
            if exif_data:
                for tag_id, value in exif_data.items():
                    tag_name = ExifTags.TAGS.get(tag_id, str(tag_id))
                    result[tag_name] = value

            file_path = getattr(img, 'filename', None)
            if file_path and os.path.exists(file_path):
                try:
                    with pyexiv2.Image(file_path) as img_meta:
                        xmp_data = img_meta.read_xmp()
                        if xmp_data:
                            for key, value in xmp_data.items():
                                result[key] = value
                except Exception as e:
                    logger.warning(f"Error reading XMP metadata: {e}")

        except Exception as e:
            logger.error(f"Error reading all JPEG metadata: {e}")

        return result

    @staticmethod
    def _get_all_png_metadata(img: Image.Image) -> Dict[str, Any]:
        """
        Get all metadata of PNG image

        Args:
            img (PIL.Image.Image): Opened image object

        Returns:
            dict: All metadata dictionary
        """
        result = {}

        try:
            if img.info:
                for key, value in img.info.items():
                    if isinstance(value, bytes):
                        try:
                            value = value.decode('utf-8')
                        except UnicodeDecodeError:
                            value = str(value)
                    result[key] = value

        except Exception as e:
            logger.error(f"Error reading all PNG metadata: {e}")

        return result


def add_image_metadata(image_path: str, custom_metadata: Optional[Dict[str, Any]] = None,
                       output_path: Optional[str] = None) -> str:
    manager = ImageMetadataManager(custom_metadata)
    return manager.add_metadata(image_path, output_path)


def read_image_metadata(image_path: str, metadata_key: Optional[str] = None) -> Optional[Dict[str, Any]]:
    manager = ImageMetadataManager()
    return manager.read_metadata(image_path, metadata_key)


def get_all_image_metadata(image_path: str) -> Dict[str, Any]:
    manager = ImageMetadataManager()
    return manager.get_all_metadata(image_path)
