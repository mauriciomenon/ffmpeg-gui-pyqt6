# Contributing to FFmpeg GUI

This document provides guidelines and information for contributors.

## Code of Conduct

Be respectful and constructive in all interactions.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/yourusername/ffmpeg-gui-pyqt6.git
   cd ffmpeg-gui-pyqt6
   ```
3. **Set up development environment**:
   ```bash
   make venv install hooks
   ```
4. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Guidelines

### Code Style
- Follow PEP 8 Python style guidelines
- Use meaningful variable and function names
- Add docstrings for functions and classes
- Keep line length under 88 characters (Black formatter default)

### Testing
- Write tests for new functionality in the `tests/` directory
- Run tests before submitting: `make test`
- Ensure tests pass in headless environments
- Add integration tests for GUI components when possible

### Security
- Use the provided safe extraction utilities for file operations
- Validate all user inputs
- Avoid shell injection vulnerabilities
- Follow secure coding practices for external process execution

### Commit Guidelines
- Write clear, concise commit messages
- Use present tense ("Add feature" not "Added feature")
- Reference issues and pull requests when relevant
- Keep commits focused on a single logical change

Example commit message format:
```
feat: add H.265 encoding support

- Implement HEVC codec option in dropdown
- Add bitrate validation for H.265
- Update tests for new codec support

Fixes #123
```

### Pull Request Process

1. **Update documentation** if your changes affect usage
2. **Add or update tests** for your changes
3. **Run the full test suite** and ensure it passes
4. **Update the README** if necessary
5. **Create a clear PR description** explaining:
   - What changes you made
   - Why you made them
   - How to test the changes
   - Any breaking changes

### Branch Naming
Use descriptive branch names with prefixes:
- `feature/` for new features
- `fix/` for bug fixes
- `docs/` for documentation changes
- `refactor/` for code refactoring
- `test/` for test improvements

Examples:
- `feature/add-vp9-support`
- `fix/memory-leak-conversion`
- `docs/improve-installation-guide`

## Development Setup

### Prerequisites
- Python 3.8+
- Git
- Make (for using Makefile commands)

### Environment Setup
```bash
# Using Make (recommended)
make venv install hooks

# Manual setup
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
git config core.hooksPath .githooks
```

### Running Tests
```bash
# All tests
make test

# Specific test file
pytest tests/test_safe_extract.py -v

# With coverage
pytest --cov=. tests/
```

### Running the Application
```bash
# PyQt6 version
make run-pyqt
# or
python GUI_pyqt6_WINFF.py

# Tkinter version  
make run-tk
# or
python GUI_tkinter_WINFF.py
```

## Types of Contributions

### Bug Reports
When reporting bugs, please include:
- Operating system and version
- Python version
- PyQt6 version (if applicable)
- Steps to reproduce
- Expected vs actual behavior
- Error messages or logs

### Feature Requests
For new features:
- Describe the use case
- Explain the expected behavior
- Consider implementation complexity
- Check if similar functionality exists

### Documentation Improvements
- Fix typos or unclear instructions
- Add examples or clarifications
- Improve installation guides
- Translate documentation (if multilingual support is added)

### Code Contributions
- Bug fixes
- New features
- Performance improvements
- Code refactoring
- Test improvements

## Project Structure

```
ffmpeg-gui-pyqt6/
├── GUI_pyqt6_WINFF.py      # Main PyQt6 application
├── GUI_tkinter_WINFF.py    # Tkinter implementation
├── utils_safe_extract.py   # Security utilities
├── requirements.txt        # Python dependencies
├── Makefile               # Development automation
├── tests/                 # Test suite
│   ├── test_command_build.py
│   └── test_safe_extract.py
├── .github/               # GitHub workflows and templates
├── .githooks/             # Git hooks for quality control
├── .vscode/               # VS Code configuration
└── docs/                  # Additional documentation
```

## Release Process

Releases are handled by maintainers:
1. Version bump in relevant files
2. Update CHANGELOG.md
3. Create release tag
4. GitHub Actions builds and publishes artifacts

## Getting Help

- **Questions**: Open a discussion or issue
- **Chat**: Join our community discussions
- **Email**: Contact maintainers for security issues

## Recognition

Contributors are recognized in:
- README.md acknowledgments
- Release notes
- GitHub contributors page

See .github/CONTRIBUTING_RULES.md for mandatory writing and formatting standards.