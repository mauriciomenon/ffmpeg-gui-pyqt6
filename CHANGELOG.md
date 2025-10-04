# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Updated documentation and contribution guidelines
- Updated README with detailed installation and usage instructions

## [1.2.0] - 2024-10-03

### Added
- Non-blocking FFprobe operations in PyQt6 GUI
- Hardened HTTPS downloads with certificate verification
- Robust logging system for Tkinter GUI
- Headless test stubs for CI/CD environments

### Security
- Updated safe extraction utilities for ZIP and TAR files
- Input validation and sanitization updates
- Prevention of directory traversal attacks

### Fixed
- Download button functionality and error handling
- Memory leaks in video conversion process
- GUI responsiveness during long operations

## [1.1.0] - 2024-10-02

### Added
- Pre-commit git hooks with file size limits and pytest integration
- Makefile for streamlined development workflow
- VS Code tasks and workspace configuration
- Comprehensive test suite with pytest

### Changed
- Refactored codebase for better maintainability
- Updated error handling and user feedback
- Updated CI/CD pipeline with cost controls

### Security
- Safe ZIP/TAR extraction utilities
- Efficient log append mechanisms to prevent memory exhaustion

## [1.0.0] - 2024-09-30

### Added
- Initial release with dual GUI implementations
- PyQt6 modern interface with advanced features
- Tkinter lightweight alternative interface
- FFmpeg integration and download assistance
- Video information display using ffprobe
- Support for multiple video and audio codecs
- Configurable bitrates and resolutions
- Cross-platform compatibility (Windows, macOS, Linux)

### Features
- **Video Conversion**: H.264, H.265, VP9, AV1 codec support
- **Audio Options**: AAC, MP3, OGG codec support
- **Quality Settings**: Configurable bitrates and resolutions
- **User Experience**: Command preview and progress tracking
- **FFmpeg Management**: Built-in download and installation tools

### Security
- Input validation and sanitization
- Safe file handling and extraction
- Secure external process execution

---

## Version History Legend

- **Added** for new features
- **Changed** for changes in existing functionality
- **Deprecated** for soon-to-be removed features
- **Removed** for now removed features
- **Fixed** for any bug fixes
- **Security** for vulnerability fixes

## Migration Guide

### From v1.1.x to v1.2.0
- No breaking changes
- New features are backward compatible
- Updated security measures are transparent to users

### From v1.0.x to v1.1.0  
- Development workflow improvements
- New Makefile commands available
- Git hooks can be installed with `make hooks`

## Upgrade Instructions

### Latest Version
```bash
git pull origin master
pip install -r requirements.txt --upgrade
```

### From Source
```bash
git fetch --tags
git checkout v1.2.0
make install
```

## Known Issues

### Current
- Large video files (>4GB) may require additional memory
- Some codec combinations may have platform-specific limitations
- Windows UAC may prompt for FFmpeg installation

### Fixed in Recent Versions
- Memory leaks during conversion (fixed in v1.2.0)
- GUI freezing on large files (fixed in v1.2.0)  
- Download failures on some networks (fixed in v1.2.0)

## Roadmap

### Upcoming Features
- Batch conversion support
- Custom FFmpeg parameter input
- Video preview and thumbnails
- GPU acceleration detection
- Plugin system for custom codecs

### Under Consideration
- Web-based interface option
- Mobile companion app
- Cloud conversion integration
- Advanced audio processing

---

*For detailed commit history, see the [Git log](https://github.com/yourusername/ffmpeg-gui-pyqt6/commits/master)*