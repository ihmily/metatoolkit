#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
MetaToolkit basic usage example
"""

import os
import sys
import json
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import metatoolkit


def image_example():
    """Image metadata example"""
    print("\n===== Image Metadata Example =====")

    # Example image path (please replace with actual existing image path)
    image_path = "example.jpg"

    # Check if file exists
    if not os.path.isfile(image_path):
        print(f"Error: File {image_path} does not exist")
        return

    # Custom metadata
    custom_metadata = {
        "model": "stable-diffusion-v1.5",
        "prompt": "A cute cat playing on the grass",
        "timestamp": datetime.now().isoformat(),
        "creator": "MetaToolkit example script"
    }

    # Add metadata
    print(f"Adding metadata to image {image_path}...")
    output_path = metatoolkit.add_image_metadata(image_path, custom_metadata=custom_metadata)
    print(f"Saved image with metadata: {output_path}")

    # Read metadata
    print(f"\nReading metadata from image {output_path}...")
    metadata = metatoolkit.read_image_metadata(output_path)
    if metadata:
        print("Found metadata:")
        print(json.dumps(metadata, indent=2, ensure_ascii=False))
    else:
        print("No metadata found")

    # Get all metadata
    print(f"\nGetting all metadata from image {output_path}...")
    all_metadata = metatoolkit.get_all_image_metadata(output_path)
    print("All metadata:")
    print(json.dumps(all_metadata, indent=2, ensure_ascii=False))


def video_example():
    """Video metadata example"""
    print("\n===== Video Metadata Example =====")

    # Example video path (please replace with actual existing video path)
    video_path = "example.mp4"

    # Check if file exists
    if not os.path.isfile(video_path):
        print(f"Error: File {video_path} does not exist")
        return

    # Custom metadata
    custom_metadata = {
        "model": "midjourney",
        "prompt": "Sci-fi city scene, futuristic style",
        "timestamp": datetime.now().isoformat(),
        "creator": "MetaToolkit example script"
    }

    # Add metadata
    print(f"Adding metadata to video {video_path}...")
    try:
        output_path = metatoolkit.add_video_metadata(video_path, custom_metadata=custom_metadata)
        print(f"Saved video with metadata: {output_path}")

        # Read metadata
        print(f"\nReading metadata from video {output_path}...")
        metadata = metatoolkit.read_video_metadata(output_path)
        if metadata:
            print("Found metadata:")
            print(json.dumps(metadata, indent=2, ensure_ascii=False))
        else:
            print("No metadata found")

        # Get all metadata
        print(f"\nGetting all metadata from video {output_path}...")
        all_metadata = metatoolkit.get_all_video_metadata(output_path)
        print("All metadata:")
        print(json.dumps(all_metadata, indent=2, ensure_ascii=False))

    except Exception as e:
        print(f"Error processing video: {e}")
        print("Tip: Make sure FFmpeg is installed")


def audio_example():
    """Audio metadata example"""
    print("\n===== Audio Metadata Example =====")

    # Example audio path (please replace with actual existing audio path)
    audio_path = "example.mp3"

    # Check if file exists
    if not os.path.isfile(audio_path):
        print(f"Error: File {audio_path} does not exist")
        return

    # Custom metadata
    custom_metadata = {
        "model": "whisper",
        "transcript": "This is an audio transcription text",
        "timestamp": datetime.now().isoformat(),
        "creator": "MetaToolkit example script"
    }

    # Add metadata
    print(f"Adding metadata to audio {audio_path}...")
    try:
        output_path = metatoolkit.add_audio_metadata(audio_path, custom_metadata=custom_metadata)
        print(f"Saved audio with metadata: {output_path}")

        # Read metadata
        print(f"\nReading metadata from audio {output_path}...")
        metadata = metatoolkit.read_audio_metadata(output_path)
        if metadata:
            print("Found metadata:")
            print(json.dumps(metadata, indent=2, ensure_ascii=False))
        else:
            print("No metadata found")

        # Get all metadata
        print(f"\nGetting all metadata from audio {output_path}...")
        all_metadata = metatoolkit.get_all_audio_metadata(output_path)
        print("All metadata:")
        print(json.dumps(all_metadata, indent=2, ensure_ascii=False))

    except Exception as e:
        print(f"Error processing audio: {e}")
        print("Tip: Make sure FFmpeg is installed")


def main():
    """Main function"""
    print("MetaToolkit Basic Usage Example")
    print("=" * 30)

    # Run examples
    image_example()
    video_example()
    audio_example()


if __name__ == "__main__":
    main()
