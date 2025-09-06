#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
metatoolkit video metadata processing module
"""

import os
import json
import logging
import subprocess
from typing import Dict, Any, Optional

from .core import BaseMetadataManager
from .exceptions import (
    MetadataReadError,
    MetadataWriteError,
    UnsupportedFormatError
)

logger = logging.getLogger(__name__)


class VideoMetadataManager(BaseMetadataManager):
    # Supported video formats
    SUPPORTED_FORMATS = ('.mp4', '.mov', '.mkv', '.avi')

    @staticmethod
    def _check_ffmpeg() -> bool:
        """
        Check if ffmpeg is installed
        
        Returns:
            bool: Whether ffmpeg is installed
        """
        try:
            subprocess.run(['ffmpeg', '-version'], capture_output=True, encoding='utf-8', check=True)
            return True
        except (subprocess.SubprocessError, FileNotFoundError):
            return False

    @staticmethod
    def _check_ffprobe() -> bool:
        """
        Check if ffprobe is installed
        
        Returns:
            bool: Whether ffprobe is installed
        """
        try:
            subprocess.run(['ffprobe', '-version'], capture_output=True, encoding='utf-8', check=True)
            return True
        except (subprocess.SubprocessError, FileNotFoundError):
            return False

    def add_metadata(self, video_path: str, output_path: Optional[str] = None) -> str:
        """
        Add metadata to video
        
        Args:
            video_path (str): Input video path
            output_path (str, optional): Output video path, auto-generated if None
            
        Returns:
            str: Output video path
            
        Raises:
            UnsupportedFormatError: If video format is not supported
            MetadataWriteError: If metadata writing fails
        """
        if not self._check_ffmpeg():
            raise MetadataWriteError("ffmpeg is not installed, please install ffmpeg first")

        if not self.validate_file_exists(video_path):
            raise FileNotFoundError(f"Video file does not exist: {video_path}")

        _, ext = os.path.splitext(video_path)
        if ext.lower() not in self.SUPPORTED_FORMATS:
            raise UnsupportedFormatError(f"Unsupported video format: {ext}")

        if output_path is None:
            output_path = self.generate_output_path(video_path)

        try:
            cmd = [
                'ffmpeg',
                '-i', video_path,
                '-c:v', 'copy',
                '-c:a', 'copy',
                '-movflags', 'use_metadata_tags',
            ]

            for key, value in self.metadata.items():
                if isinstance(value, (dict, list)):
                    str_value = json.dumps(value, ensure_ascii=False)
                elif value is not None:
                    str_value = str(value)
                else:
                    str_value = ""

                cmd.extend(['-metadata', f'{key}={str_value}'])

            cmd.extend([
                '-y',
                output_path
            ])

            _ = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', check=True)

            logger.info(f"Added metadata to video, saved to: {output_path}")
            return output_path

        except subprocess.CalledProcessError as e:
            error_msg = f"Failed to write video metadata: {e.stderr}"
            logger.error(error_msg)
            raise MetadataWriteError(error_msg)

        except Exception as e:
            error_msg = f"Error writing video metadata: {e}"
            logger.error(error_msg)
            raise MetadataWriteError(error_msg)

    def read_metadata(self, video_path: str, metadata_key: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Read video metadata
        
        Args:
            video_path (str): Video path
            metadata_key (str, optional): Metadata key name, returns all metadata if None, defaults to None
            
        Returns:
            dict: Metadata dictionary, returns None if not found
            
        Raises:
            MetadataReadError: If metadata reading fails
        """
        if not self._check_ffprobe():
            raise MetadataReadError("ffprobe is not installed, please install ffmpeg first")

        if not self.validate_file_exists(video_path):
            raise FileNotFoundError(f"Video file does not exist: {video_path}")

        try:
            cmd = [
                'ffprobe',
                '-v', 'quiet',
                '-print_format', 'json',
                '-show_format',
                video_path
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', check=True)

            metadata = json.loads(result.stdout)

            if 'format' in metadata and 'tags' in metadata['format']:
                tags = metadata['format']['tags']

                if metadata_key is not None and metadata_key in tags:
                    try:
                        metadata_obj = json.loads(tags[metadata_key])
                        logger.info(f"Found video metadata: {metadata_key}")
                        return metadata_obj
                    except json.JSONDecodeError:
                        logger.info(f"Found video metadata (non-JSON format): {metadata_key}")
                        return {metadata_key: tags[metadata_key]}
                elif metadata_key is None:
                    result_tags = {}
                    for key, value in tags.items():
                        try:
                            if isinstance(value, str) and (value.startswith('{') or value.startswith('[')):
                                result_tags[key] = json.loads(value)
                            else:
                                result_tags[key] = value
                        except json.JSONDecodeError:
                            result_tags[key] = value

                    if result_tags:
                        logger.info("Found all video metadata tags")
                        return result_tags

            if metadata_key is not None:
                logger.info(f"Video metadata not found: {metadata_key}")
            else:
                logger.info("No video metadata found")
            return None

        except subprocess.CalledProcessError as e:
            error_msg = f"Failed to read video metadata: {e.stderr}"
            logger.error(error_msg)
            raise MetadataReadError(error_msg)

        except Exception as e:
            error_msg = f"Error reading video metadata: {e}"
            logger.error(error_msg)
            raise MetadataReadError(error_msg)

    def get_all_metadata(self, video_path: str) -> Dict[str, Any]:
        """
        Get all metadata of the video
        
        Args:
            video_path (str): Video path
            
        Returns:
            dict: All metadata dictionary
            
        Raises:
            MetadataReadError: If metadata reading fails
        """
        if not self._check_ffprobe():
            raise MetadataReadError("ffprobe is not installed, please install ffmpeg first")

        if not self.validate_file_exists(video_path):
            raise FileNotFoundError(f"Video file does not exist: {video_path}")

        try:
            cmd = [
                'ffprobe',
                '-v', 'quiet',
                '-print_format', 'json',
                '-show_format',
                '-show_streams',
                video_path
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', check=True)

            metadata = json.loads(result.stdout)

            all_metadata = {}

            if 'format' in metadata:
                all_metadata['format'] = metadata['format']

                if 'tags' in metadata['format']:
                    tags = metadata['format']['tags']
                    for key, value in tags.items():
                        try:
                            if isinstance(value, str) and (value.startswith('{') or value.startswith('[')):
                                tags[key] = json.loads(value)
                        except json.JSONDecodeError:
                            pass

            if 'streams' in metadata:
                all_metadata['streams'] = metadata['streams']

                for stream in all_metadata['streams']:
                    if 'tags' in stream:
                        tags = stream['tags']
                        for key, value in tags.items():
                            try:
                                if isinstance(value, str) and (value.startswith('{') or value.startswith('[')):
                                    tags[key] = json.loads(value)
                            except json.JSONDecodeError:
                                pass

            logger.info(f"Retrieved all video metadata")
            return all_metadata

        except subprocess.CalledProcessError as e:
            error_msg = f"Failed to read video metadata: {e.stderr}"
            logger.error(error_msg)
            raise MetadataReadError(error_msg)

        except Exception as e:
            error_msg = f"Error reading video metadata: {e}"
            logger.error(error_msg)
            raise MetadataReadError(error_msg)


def add_video_metadata(video_path: str, output_path: Optional[str] = None,
                       custom_metadata: Optional[Dict[str, Any]] = None) -> str:
    manager = VideoMetadataManager(custom_metadata)
    return manager.add_metadata(video_path, output_path)


def read_video_metadata(video_path: str, metadata_key: Optional[str] = None) -> Optional[Dict[str, Any]]:
    manager = VideoMetadataManager()
    return manager.read_metadata(video_path, metadata_key)


def get_all_video_metadata(video_path: str) -> Dict[str, Any]:
    manager = VideoMetadataManager()
    return manager.get_all_metadata(video_path)
