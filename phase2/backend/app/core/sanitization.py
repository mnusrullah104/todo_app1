"""
Input sanitization utilities for XSS prevention.
"""
import re
import html
from typing import Optional


def sanitize_string(value: Optional[str], max_length: Optional[int] = None) -> Optional[str]:
    """
    Sanitize string input to prevent XSS attacks.

    - Escapes HTML entities
    - Removes control characters
    - Optionally truncates to max_length
    - Strips leading/trailing whitespace

    Args:
        value: Input string to sanitize
        max_length: Maximum allowed length (truncates if exceeded)

    Returns:
        Sanitized string or None if input is None
    """
    if value is None:
        return None

    # Strip whitespace
    value = value.strip()

    # Return empty string if now empty
    if not value:
        return ""

    # Escape HTML entities (prevents <script>, etc.)
    value = html.escape(value)

    # Remove control characters (except newlines, tabs, carriage returns)
    value = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', value)

    # Truncate if max_length specified
    if max_length and len(value) > max_length:
        value = value[:max_length]

    return value


def sanitize_email(email: Optional[str]) -> Optional[str]:
    """
    Sanitize email address.

    - Converts to lowercase
    - Strips whitespace
    - Basic validation (contains @)

    Args:
        email: Email address to sanitize

    Returns:
        Sanitized email or None if invalid
    """
    if email is None:
        return None

    email = email.strip().lower()

    # Basic validation
    if not email or '@' not in email:
        return None

    # Ensure only one @
    if email.count('@') != 1:
        return None

    return email


def is_safe_url(url: str) -> bool:
    """
    Check if URL is safe (prevents javascript:, data:, etc. schemes).

    Args:
        url: URL to validate

    Returns:
        True if URL uses safe scheme (http, https, mailto)
    """
    if not url:
        return False

    url = url.strip().lower()

    # Allow only safe schemes
    safe_schemes = ('http://', 'https://', 'mailto:', '/')
    return any(url.startswith(scheme) for scheme in safe_schemes)


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename to prevent path traversal attacks.

    - Removes path separators (/, \\)
    - Removes special characters
    - Limits to alphanumeric, dots, dashes, underscores

    Args:
        filename: Filename to sanitize

    Returns:
        Safe filename
    """
    # Remove path components
    filename = filename.replace('/', '').replace('\\', '')

    # Keep only safe characters
    filename = re.sub(r'[^a-zA-Z0-9._-]', '_', filename)

    # Prevent hidden files and parent directory references
    filename = filename.lstrip('.')

    # Ensure not empty
    if not filename:
        filename = "file"

    return filename


# Validation patterns
EMAIL_PATTERN = re.compile(
    r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
)

UUID_PATTERN = re.compile(
    r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',
    re.IGNORECASE
)


def is_valid_email(email: str) -> bool:
    """Validate email format using regex."""
    return bool(EMAIL_PATTERN.match(email))


def is_valid_uuid(uuid_str: str) -> bool:
    """Validate UUID format."""
    return bool(UUID_PATTERN.match(uuid_str))
