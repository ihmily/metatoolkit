#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
metatoolkit core functionality module
"""

import os
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class BaseMetadataManager:
    """Base metadata manager class"""

    # Default metadata fields
    DEFAULT_METADATA_FIELDS = {
        "ai_generated": "true",
        "generator": "metatoolkit",
        "version": None,
    }

    def __init__(self, custom_metadata: Optional[Dict[str, Any]] = None):
        """
        Initialize metadata manager
        
        Args:
            custom_metadata (dict, optional): Custom metadata fields, if provided, will be merged with default metadata
        """
        from . import __version__

        self.metadata = self.DEFAULT_METADATA_FIELDS.copy()

        self.metadata.update({
            "version": __version__
        })

        # Merge custom metadata
        if custom_metadata and isinstance(custom_metadata, dict):
            self.metadata.update(custom_metadata)

    @staticmethod
    def generate_output_path(input_path: str, suffix: str = "_metadata") -> str:
        """
        Generate output path
        
        Args:
            input_path (str): Input file path
            suffix (str): Suffix to add to filename
            
        Returns:
            str: Output file path
        """
        base_name, ext = os.path.splitext(input_path)
        return f"{base_name}{suffix}{ext}"

    @staticmethod
    def validate_file_exists(file_path: str) -> bool:
        """
        Validate if file exists
        
        Args:
            file_path (str): File path
            
        Returns:
            bool: Whether file exists
        """
        if not os.path.isfile(file_path):
            logger.error(f"File does not exist: {file_path}")
            return False
        return True
