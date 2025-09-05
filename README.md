# MetaKit

A powerful Python library for processing metadata of images, videos, and audio files. Supports adding, reading, and managing metadata information for various media files.

## Features

- 🖼️ **Image Metadata Processing** - Support for EXIF, XMP metadata in JPEG, PNG formats
- 🎬 **Video Metadata Processing** - Support for metadata tags in MP4, AVI and other formats
- 🎵 **Audio Metadata Processing** - Support for ID3 tags in MP3, WAV and other formats
- 📝 **Custom Metadata** - Support for adding custom metadata fields
- 🔧 **Command Line Tool** - Convenient command-line interface
- 🐍 **Python API** - Simple and easy-to-use Python interface

## Installation

### Install from PyPI

```bash
pip install metakit
```

### Install from Source

```bash
git clone https://github.com/ihmily/metakit.git
cd metakit
pip install -e .
```

### Requirements

- Python >= 3.6
- Pillow >= 9.5.0
- pyexiv2 >= 2.15.4

## Quick Start

### Image Metadata Processing

```python
import metakit
from datetime import datetime

# Add custom metadata to image
custom_metadata = {
    "model": "stable-diffusion-v1.5",
    "prompt": "A beautiful landscape",
    "timestamp": datetime.now().isoformat(),
    "creator": "MetaKit"
}

# Add metadata
output_path = metakit.add_image_metadata("input.jpg", custom_metadata=custom_metadata)

# Read metadata
metadata = metakit.read_image_metadata(output_path)
print(metadata)
```

### Video Metadata Processing

```python
import metakit

# Add video metadata
video_metadata = {
    "title": "My Video",
    "description": "This is a test video",
    "author": "MetaKit User",
    "creation_date": "2024-01-01"
}

# Add metadata
metakit.add_video_metadata("input.mp4", custom_metadata=video_metadata)

# Read metadata
metadata = metakit.read_video_metadata("input.mp4")
print(metadata)
```

### Audio Metadata Processing

```python
import metakit

# Add audio metadata
audio_metadata = {
    "title": "My Music",
    "artist": "Artist Name",
    "album": "Album Name",
    "year": "2024"
}

# Add metadata
metakit.add_audio_metadata("input.mp3", custom_metadata=audio_metadata)

# Read metadata
metadata = metakit.read_audio_metadata("input.mp3")
print(metadata)
```

## Command Line Tool

MetaKit provides a convenient command-line tool that can be used directly in the terminal:

```bash
# Show help
metakit --help

# Add image metadata
metakit add-image --input image.jpg --output image_with_metadata.jpg --metadata '{"title":"My Image","author":"User"}'

# Read image metadata
metakit read-image --input image.jpg

# Add video metadata
metakit add-video --input video.mp4 --metadata '{"title":"My Video","description":"Video description"}'

# Read video metadata
metakit read-video --input video.mp4

# Add audio metadata
metakit add-audio --input audio.mp3 --metadata '{"title":"My Music","artist":"Artist"}'

# Read audio metadata
metakit read-audio --input audio.mp3
```

## API Reference

### Image Processing

- `add_image_metadata(image_path, custom_metadata=None, output_path=None)` - Add image metadata
- `read_image_metadata(image_path)` - Read image metadata
- `get_all_image_metadata(image_path)` - Get all image metadata

### Video Processing

- `add_video_metadata(video_path, custom_metadata=metadata_dict)` - Add video metadata
- `read_video_metadata(video_path)` - Read video metadata
- `get_all_video_metadata(video_path)` - Get all video metadata

### Audio Processing

- `add_audio_metadata(audio_path, custom_metadata=metadata_dict)` - Add audio metadata
- `read_audio_metadata(audio_path)` - Read audio metadata
- `get_all_audio_metadata(audio_path)` - Get all audio metadata

## Supported Formats

### Image Formats

- JPEG (.jpg, .jpeg)
- PNG (.png)

### Video Formats

- MP4 (.mp4)
- AVI (.avi)
- MOV (.mov)
- MKV (.mkv)

### Audio Formats

- MP3 (.mp3)
- WAV (.wav)
- FLAC (.flac)
- M4A (.m4a)
- OGG (.ogg)
- AAC (.aac)

## Examples

Check the `examples/basic_usage.py` file for more usage examples.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version update history.

## Contact

- Project Homepage: https://github.com/ihmily/metakit
- Issue Tracker: https://github.com/ihmily/metakit/issues

## Acknowledgments

Thanks to all the developers who contributed to this project!