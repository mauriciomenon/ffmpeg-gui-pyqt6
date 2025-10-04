# Security Policy

## Supported Versions

We actively support and provide security updates for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.2.x   | Yes                |
| 1.1.x   | Yes                |
| 1.0.x   | Limited support    |
| < 1.0   | No                 |

## Security Features

This project implements several security measures:

### Safe File Handling
- **Archive Extraction**: Uses safe extraction utilities to prevent directory traversal attacks
- **Path Validation**: All file paths are validated before processing
- **Temporary Files**: Secure temporary file creation and cleanup

### Network Security
- **HTTPS Only**: All downloads use HTTPS with certificate verification
- **No Credentials**: Application doesn't store or transmit user credentials
- **Safe Downloads**: FFmpeg binaries are downloaded from official sources only

### Input Validation
- **Command Injection Prevention**: All user inputs are properly escaped and validated
- **File Type Validation**: Only supported video file types are processed
- **Parameter Sanitization**: FFmpeg parameters are sanitized before execution

### Process Security
- **Isolated Execution**: External processes run with minimal privileges
- **Resource Limits**: Conversion processes have reasonable resource constraints
- **Clean Shutdown**: Proper cleanup of processes and temporary files

## Reporting a Vulnerability

### How to Report
If you discover a security vulnerability, please report it responsibly:

1. **DO NOT** create a public GitHub issue for security vulnerabilities
2. **Email** the maintainers privately at: [security@project.com] (replace with actual email)
3. **Include** the following information:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact assessment
   - Suggested fix (if you have one)

### Response Timeline
- **Acknowledgment**: We will acknowledge receipt within 24-48 hours
- **Initial Assessment**: We will provide an initial assessment within 7 days
- **Fix Development**: We aim to develop fixes within 30 days for critical issues
- **Public Disclosure**: We will coordinate public disclosure after a fix is available

### Severity Classification

**Critical (CVSS 9.0-10.0)**
- Remote code execution
- Arbitrary file access outside intended directories
- Privilege escalation

**High (CVSS 7.0-8.9)**
- Local file inclusion/disclosure
- Command injection with limited scope
- Authentication bypass

**Medium (CVSS 4.0-6.9)**
- Information disclosure
- Denial of service
- Cross-site scripting (if web interface added)

**Low (CVSS 0.1-3.9)**
- Minor information leakage
- Non-exploitable crashes
- Configuration issues

## Security Best Practices for Users

### Installation
- Always download from official sources
- Verify checksums when available
- Use virtual environments for Python dependencies
- Keep FFmpeg updated to latest stable version

### Usage
- Don't process untrusted video files from unknown sources
- Review FFmpeg commands before execution
- Keep output directories within user-accessible areas
- Regularly update the application and dependencies

### System Security
- Run with standard user privileges (not root/administrator)
- Use updated operating systems with current security patches
- Enable firewall protection
- Scan downloaded files with antivirus software

## Dependency Security

### Python Dependencies
- We regularly update dependencies to address security vulnerabilities
- Use `pip-audit` or similar tools to check for known vulnerabilities:
  ```bash
  pip install pip-audit
  pip-audit
  ```

### FFmpeg Security
- The application helps users download official FFmpeg binaries
- Users should verify FFmpeg signatures when possible
- We don't modify or redistribute FFmpeg binaries

## Security Changelog

### Version 1.2.0
- Updated safe extraction utilities
- Hardened HTTPS downloads with certificate verification
- Updated input validation and sanitization

### Version 1.1.0
- Added safe ZIP/TAR extraction utilities
- Implemented secure temporary file handling
- Added file size limits to prevent resource exhaustion

### Version 1.0.0
- Initial security implementation
- Basic input validation
- Safe external process execution

## Third-Party Security Research

We welcome security research and responsible disclosure. Security researchers who follow our reporting guidelines will be credited in:
- Security advisories
- Release notes
- Public acknowledgments (with their permission)

## Contact Information

For security-related questions or concerns:
- **Security Team**: [security@project.com]
- **General Contact**: [maintainer@project.com]
- **Emergency**: For critical vulnerabilities requiring immediate attention

---

**Remember**: Security is a shared responsibility. Users should also follow security best practices when using this software.