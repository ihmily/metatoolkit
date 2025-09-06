#!/usr/bin/env python

"""
metatoolkit audio metadata processing module
"""

import json
import logging
import os
import subprocess
from typing import Any, Optional

from .core import BaseMetadataManager
from .exceptions import MetadataReadError, MetadataWriteError, UnsupportedFormatError

logger = logging.getLogger(__name__)


class AudioMetadataManager(BaseMetadataManager):

    # Supported audio formats
    SUPPORTED_FORMATS = ('.mp3', '.flac', '.wav', '.ogg', '.m4a', '.aac')

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

    def add_metadata(self, audio_path: str, output_path: Optional[str] = None) -> str:
        """
        Add metadata to audio
        
        Args:
            audio_path (str): Input audio path
            output_path (str, optional): Output audio path, auto-generated if None
            
        Returns:
            str: Output audio path
            
        Raises:
            UnsupportedFormatError: If audio format is not supported
            MetadataWriteError: If metadata writing fails
        """
        if not self._check_ffmpeg():
            raise MetadataWriteError("ffmpeg is not installed, please install ffmpeg first")

        if not self.validate_file_exists(audio_path):
            raise FileNotFoundError(f"Audio file does not exist: {audio_path}")

        _, ext = os.path.splitext(audio_path)
        if ext.lower() not in self.SUPPORTED_FORMATS:
            raise UnsupportedFormatError(f"Unsupported audio format: {ext}")

        if output_path is None:
            output_path = self.generate_output_path(audio_path)

        try:
            cmd = [
                'ffmpeg',
                '-i', audio_path,
                '-c', 'copy',
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

            logger.info(f"Added metadata to audio, saved to: {output_path}")
            return output_path

        except subprocess.CalledProcessError as e:
            error_msg = f"Failed to write audio metadata: {e.stderr}"
            logger.error(error_msg)
            raise MetadataWriteError(error_msg)

        except Exception as e:
            error_msg = f"Error writing audio metadata: {e}"
            logger.error(error_msg)
            raise MetadataWriteError(error_msg)

    def read_metadata(self, audio_path: str, metadata_key: Optional[str] = None) -> Optional[dict[str, Any]]:
        """
        Read audio metadata
        
        Args:
            audio_path (str): Audio path
            metadata_key (str, optional): Metadata key name, returns all metadata if None, defaults to None
            
        Returns:
            dict: Metadata dictionary, returns None if not found
            
        Raises:
            MetadataReadError: If metadata reading fails
        """
        if not self._check_ffprobe():
            raise MetadataReadError("ffprobe is not installed, please install ffmpeg first")

        if not self.validate_file_exists(audio_path):
            raise FileNotFoundError(f"Audio file does not exist: {audio_path}")

        try:
            cmd = [
                'ffprobe',
                '-v', 'quiet',
                '-print_format', 'json',
                '-show_format',
                audio_path
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', check=True)

            metadata = json.loads(result.stdout)

            if 'format' in metadata and 'tags' in metadata['format']:
                tags = metadata['format']['tags']

                if metadata_key is not None and metadata_key in tags:
                    try:
                        metadata_obj = json.loads(tags[metadata_key])
                        logger.info(f"Found audio metadata: {metadata_key}")
                        return metadata_obj
                    except json.JSONDecodeError:
                        logger.info(f"Found audio metadata (non-JSON format): {metadata_key}")
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
                        logger.info("Found all audio metadata tags")
                        return result_tags

            if metadata_key is not None:
                logger.info(f"Audio metadata not found: {metadata_key}")
            else:
                logger.info("No audio metadata found")
            return None

        except subprocess.CalledProcessError as e:
            error_msg = f"Failed to read audio metadata: {e.stderr}"
            logger.error(error_msg)
            raise MetadataReadError(error_msg)

        except Exception as e:
            error_msg = f"Error reading audio metadata: {e}"
            logger.error(error_msg)
            raise MetadataReadError(error_msg)

    def get_all_metadata(self, audio_path: str) -> dict[str, Any]:
        """
        Get all metadata of the audio
        
        Args:
            audio_path (str): Audio path
            
        Returns:
            dict: All metadata dictionary
            
        Raises:
            MetadataReadError: If metadata reading fails
        """
        if not self._check_ffprobe():
            raise MetadataReadError("ffprobe is not installed, please install ffmpeg first")

        if not self.validate_file_exists(audio_path):
            raise FileNotFoundError(f"Audio file does not exist: {audio_path}")

        try:
            cmd = [
                'ffprobe',
                '-v', 'quiet',
                '-print_format', 'json',
                '-show_format',
                '-show_streams',
                audio_path
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

            logger.info("Retrieved all audio metadata")
            return all_metadata

        except subprocess.CalledProcessError as e:
            error_msg = f"Failed to read audio metadata: {e.stderr}"
            logger.error(error_msg)
            raise MetadataReadError(error_msg)

        except Exception as e:
            error_msg = f"Error reading audio metadata: {e}"
            logger.error(error_msg)
            raise MetadataReadError(error_msg)


def add_audio_metadata(audio_path: str, output_path: Optional[str] = None,
                       custom_metadata: Optional[dict[str, Any]] = None) -> str:
    manager = AudioMetadataManager(custom_metadata)
    return manager.add_metadata(audio_path, output_path)


def read_audio_metadata(audio_path: str, metadata_key: Optional[str] = None) -> Optional[dict[str, Any]]:
    manager = AudioMetadataManager()
    return manager.read_metadata(audio_path, metadata_key)


def get_all_audio_metadata(audio_path: str) -> dict[str, Any]:
    manager = AudioMetadataManager()
    return manager.get_all_metadata(audio_path)
