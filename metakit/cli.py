#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
metakit command line interface
"""

import sys
import json
import argparse
import logging
from typing import Tuple

from .image import ImageMetadataManager
from .video import VideoMetadataManager
from .audio import AudioMetadataManager
from .exceptions import MetakitError, UnsupportedFormatError

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)


def parse_field(field_str: str) -> Tuple[str, str]:
    """
    Parse field string into key-value pair
    
    Args:
        field_str (str): Field string in format "key=value"
        
    Returns:
        tuple: (key, value)
        
    Raises:
        ValueError: If format is incorrect
    """
    if '=' not in field_str:
        raise ValueError(f"Invalid field format: {field_str}, should be 'key=value' format")
    key, value = field_str.split('=', 1)
    return key.strip(), value.strip()


def add_image_metadata_cmd(args) -> int:
    """
    Add image metadata command handler
    
    Args:
        args: Command line arguments
        
    Returns:
        int: Exit code
    """
    try:
        custom_metadata = {}
        if args.field:
            for field_str in args.field:
                try:
                    key, value = parse_field(field_str)
                    custom_metadata[key] = value
                except ValueError as e:
                    logger.error(str(e))
                    return 1

        manager = ImageMetadataManager(custom_metadata)

        output_path = manager.add_metadata(args.image_path, args.output)

        print(f"Successfully added metadata, saved to: {output_path}")
        return 0

    except UnsupportedFormatError as e:
        logger.error(str(e))
        return 1
    except MetakitError as e:
        logger.error(f"Failed to add metadata: {e}")
        return 1
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        return 1


def read_image_metadata_cmd(args) -> int:
    """
    Read image metadata command handler
    
    Args:
        args: Command line arguments
        
    Returns:
        int: Exit code
    """
    try:
        manager = ImageMetadataManager()

        metadata = manager.read_metadata(args.image_path, args.key)

        if metadata:
            print("Found metadata identifier:")
            print(json.dumps(metadata, indent=2, ensure_ascii=False))
            return 0
        else:
            print("No metadata identifier found")
            return 1

    except UnsupportedFormatError as e:
        logger.error(str(e))
        return 1
    except MetakitError as e:
        logger.error(f"Failed to read metadata: {e}")
        return 1
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        return 1


def get_all_image_metadata_cmd(args) -> int:
    """
    Get all image metadata command handler
    
    Args:
        args: Command line arguments
        
    Returns:
        int: Exit code
    """
    try:
        manager = ImageMetadataManager()

        metadata = manager.get_all_metadata(args.image_path)

        if metadata:
            print(f"All metadata for image {args.image_path}:")
            print(json.dumps(metadata, indent=2, ensure_ascii=False))
            return 0
        else:
            print("No metadata found")
            return 1

    except UnsupportedFormatError as e:
        logger.error(str(e))
        return 1
    except MetakitError as e:
        logger.error(f"Failed to read metadata: {e}")
        return 1
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        return 1


def add_video_metadata_cmd(args) -> int:
    """
    Add video metadata command handler
    
    Args:
        args: Command line arguments
        
    Returns:
        int: Exit code
    """
    try:
        custom_metadata = {}
        if args.field:
            for field_str in args.field:
                try:
                    key, value = parse_field(field_str)
                    custom_metadata[key] = value
                except ValueError as e:
                    logger.error(str(e))
                    return 1

        manager = VideoMetadataManager(custom_metadata)

        output_path = manager.add_metadata(args.video_path, args.output)

        print(f"Successfully added video metadata, saved to: {output_path}")
        return 0

    except UnsupportedFormatError as e:
        logger.error(str(e))
        return 1
    except MetakitError as e:
        logger.error(f"Failed to add video metadata: {e}")
        return 1
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        return 1


def read_video_metadata_cmd(args) -> int:
    """
    Read video metadata command handler
    
    Args:
        args: Command line arguments
        
    Returns:
        int: Exit code
    """
    try:
        manager = VideoMetadataManager()

        metadata = manager.read_metadata(args.video_path, args.key)

        if metadata:
            print(f"Found video metadata ({args.key}):")
            print(json.dumps(metadata, indent=2, ensure_ascii=False))
            return 0
        else:
            print(f"Video metadata not found ({args.key})")
            return 1

    except MetakitError as e:
        logger.error(f"Failed to read video metadata: {e}")
        return 1
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        return 1


def get_all_video_metadata_cmd(args) -> int:
    """
    Get all video metadata command handler
    
    Args:
        args: Command line arguments
        
    Returns:
        int: Exit code
    """
    try:
        manager = VideoMetadataManager()

        metadata = manager.get_all_metadata(args.video_path)

        if metadata:
            print(f"All metadata for video {args.video_path}:")

            if args.format == 'json':
                print(json.dumps(metadata, indent=2, ensure_ascii=False))
            else:
                if 'format' in metadata:
                    format_info = metadata['format']
                    print("\nFormat information:")
                    for key, value in format_info.items():
                        if key != 'tags':
                            print(f"  {key}: {value}")

                    if 'tags' in format_info:
                        print("\nFormat tags:")
                        for key, value in format_info['tags'].items():
                            print(f"  {key}: {value}")

                if 'streams' in metadata:
                    print(f"\nNumber of streams: {len(metadata['streams'])}")
                    for i, stream in enumerate(metadata['streams']):
                        print(f"\nStream #{i}:")
                        for key, value in stream.items():
                            if key != 'tags' and not isinstance(value, dict):
                                print(f"  {key}: {value}")

            return 0
        else:
            print("No metadata found")
            return 1

    except MetakitError as e:
        logger.error(f"Failed to read video metadata: {e}")
        return 1
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        return 1


def add_audio_metadata_cmd(args) -> int:
    """
    Add audio metadata command handler
    
    Args:
        args: Command line arguments
        
    Returns:
        int: Exit code
    """
    try:
        custom_metadata = {}
        if args.field:
            for field_str in args.field:
                try:
                    key, value = parse_field(field_str)
                    custom_metadata[key] = value
                except ValueError as e:
                    logger.error(str(e))
                    return 1

        manager = AudioMetadataManager(custom_metadata)

        output_path = manager.add_metadata(args.audio_path, args.output)

        print(f"Successfully added audio metadata, saved to: {output_path}")
        return 0

    except UnsupportedFormatError as e:
        logger.error(str(e))
        return 1
    except MetakitError as e:
        logger.error(f"Failed to add audio metadata: {e}")
        return 1
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        return 1


def read_audio_metadata_cmd(args) -> int:
    """
    Read audio metadata command handler
    
    Args:
        args: Command line arguments
        
    Returns:
        int: Exit code
    """
    try:
        manager = AudioMetadataManager()

        metadata = manager.read_metadata(args.audio_path, args.key)

        if metadata:
            print(f"Found audio metadata ({args.key}):")
            print(json.dumps(metadata, indent=2, ensure_ascii=False))
            return 0
        else:
            print(f"Audio metadata not found ({args.key})")
            return 1

    except MetakitError as e:
        logger.error(f"Failed to read audio metadata: {e}")
        return 1
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        return 1


def get_all_audio_metadata_cmd(args) -> int:
    """
    Get all audio metadata command handler
    
    Args:
        args: Command line arguments
        
    Returns:
        int: Exit code
    """
    try:
        manager = AudioMetadataManager()

        metadata = manager.get_all_metadata(args.audio_path)

        if metadata:
            print(f"All metadata for audio {args.audio_path}:")

            if args.format == 'json':
                print(json.dumps(metadata, indent=2, ensure_ascii=False))
            else:
                if 'format' in metadata:
                    format_info = metadata['format']
                    print("\nFormat information:")
                    for key, value in format_info.items():
                        if key != 'tags':
                            print(f"  {key}: {value}")

                    if 'tags' in format_info:
                        print("\nFormat tags:")
                        for key, value in format_info['tags'].items():
                            print(f"  {key}: {value}")

                if 'streams' in metadata:
                    print(f"\nNumber of streams: {len(metadata['streams'])}")
                    for i, stream in enumerate(metadata['streams']):
                        print(f"\nStream #{i}:")
                        for key, value in stream.items():
                            if key != 'tags' and not isinstance(value, dict):
                                print(f"  {key}: {value}")

            return 0
        else:
            print("No metadata found")
            return 1

    except MetakitError as e:
        logger.error(f"Failed to read audio metadata: {e}")
        return 1
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        return 1


def main() -> int:
    """
    Main function
    
    Returns:
        int: Exit code
    """
    parser = argparse.ArgumentParser(
        description='metakit - Image, video and audio metadata processing tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Image metadata
  metakit image add image.png
  metakit image add image.png --field model='{\"model\": \"stable-diffusion-v1.5\"}' --field creator=user01
  metakit image read image_metadata.png --key model
  metakit image all image.png
  
  # Video metadata
  metakit video add video.mp4
  metakit video add video.mp4 --field mytag=123456
  metakit video read video_metadata.mp4 --key mytag
  metakit video all video.mp4
  
  # Audio metadata
  metakit audio add audio.mp3
  metakit audio add audio.mp3 --field mytag=123456
  metakit audio read audio_metadata.mp3 --key mytag
  metakit audio all audio.mp3
"""
    )

    # Add global arguments
    parser.add_argument('--version', action='version', version=f'%(prog)s {__import__("metakit").__version__}')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')

    # Add subcommands
    subparsers = parser.add_subparsers(dest='command', help='Subcommands')

    # Image commands
    image_parser = subparsers.add_parser('image', help='Image metadata processing')
    image_subparsers = image_parser.add_subparsers(dest='image_command', help='Image subcommands')

    # image add command
    image_add_parser = image_subparsers.add_parser('add', help='Add image metadata identifier')
    image_add_parser.add_argument('image_path', help='Image file path')
    image_add_parser.add_argument('--output', '-o', help='Output file path')
    image_add_parser.add_argument('--field', '-f', action='append', help='Add custom metadata field, format "key=value"')
    image_add_parser.set_defaults(func=add_image_metadata_cmd)

    # image read command
    image_read_parser = image_subparsers.add_parser('read', help='Read image metadata identifier')
    image_read_parser.add_argument('image_path', help='Image file path')
    image_read_parser.add_argument('--key', '-k', default='', help='Metadata key name')
    image_read_parser.set_defaults(func=read_image_metadata_cmd)

    # image all command
    image_all_parser = image_subparsers.add_parser('all', help='View all image metadata')
    image_all_parser.add_argument('image_path', help='Image file path')
    image_all_parser.set_defaults(func=get_all_image_metadata_cmd)

    # Video commands
    video_parser = subparsers.add_parser('video', help='Video metadata processing')
    video_subparsers = video_parser.add_subparsers(dest='video_command', help='Video subcommands')

    # video add command
    video_add_parser = video_subparsers.add_parser('add', help='Add video metadata')
    video_add_parser.add_argument('video_path', help='Video file path')
    video_add_parser.add_argument('--output', '-o', help='Output file path')
    video_add_parser.add_argument('--field', '-f', action='append', help='Add custom metadata field, format "key=value"')
    video_add_parser.set_defaults(func=add_video_metadata_cmd)

    # video read command
    video_read_parser = video_subparsers.add_parser('read', help='Read video metadata')
    video_read_parser.add_argument('video_path', help='Video file path')
    video_read_parser.add_argument('--key', '-k', default='', help='Metadata key name')
    video_read_parser.set_defaults(func=read_video_metadata_cmd)

    # video all command
    video_all_parser = video_subparsers.add_parser('all', help='View all video metadata')
    video_all_parser.add_argument('video_path', help='Video file path')
    video_all_parser.add_argument('--format', choices=['json', 'simple'], default='simple',
                                  help='Output format, json for complete JSON, simple for simplified output (default)')
    video_all_parser.set_defaults(func=get_all_video_metadata_cmd)

    # Audio commands
    audio_parser = subparsers.add_parser('audio', help='Audio metadata processing')
    audio_subparsers = audio_parser.add_subparsers(dest='audio_command', help='Audio subcommands')

    # audio add command
    audio_add_parser = audio_subparsers.add_parser('add', help='Add audio metadata')
    audio_add_parser.add_argument('audio_path', help='Audio file path')
    audio_add_parser.add_argument('--output', '-o', help='Output file path')
    audio_add_parser.add_argument('--field', '-f', action='append', help='Add custom metadata field, format "key=value"')
    audio_add_parser.set_defaults(func=add_audio_metadata_cmd)

    # audio read command
    audio_read_parser = audio_subparsers.add_parser('read', help='Read audio metadata')
    audio_read_parser.add_argument('audio_path', help='Audio file path')
    audio_read_parser.add_argument('--key', '-k', default='', help='Metadata key name')
    audio_read_parser.set_defaults(func=read_audio_metadata_cmd)

    # audio all command
    audio_all_parser = audio_subparsers.add_parser('all', help='View all audio metadata')
    audio_all_parser.add_argument('audio_path', help='Audio file path')
    audio_all_parser.add_argument('--format', choices=['json', 'simple'], default='simple',
                                  help='Output format, json for complete JSON, simple for simplified output (default)')
    audio_all_parser.set_defaults(func=get_all_audio_metadata_cmd)

    args = parser.parse_args()

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    if hasattr(args, 'func'):
        return args.func(args)
    else:
        parser.print_help()
        return 0


if __name__ == '__main__':
    sys.exit(main())
