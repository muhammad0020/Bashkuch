"""
Encrypt and decrypt user data using the Fernet class from the cryptography module.

This module provides functions to:
    - Generate and save a Fernet key if missing
    - Load the key from a local file
    - Encrypt and decrypt strings for storage in JSON

Typical usage:
    from utils.data_encryption import encrypt_data, decrypt_data
    encrypted = encrypt_data("my_password")
    decrypted = decrypt_data(encrypted)
"""

from pathlib import Path
from cryptography.fernet import Fernet

PROJECT_ROOT = Path(__file__).parent.parent
SECRET_KEY_PATH = PROJECT_ROOT / "saved_data" / "secret.key"
_KEY_CACHE = None  # Cache Fernet key for performance


def _ensure_key_directory():
    """Create saved_data directory if missing."""
    SECRET_KEY_PATH.parent.mkdir(parents=True, exist_ok=True)


def _generate_key():
    """Generates Fernet encryption key and saves to secret.key."""
    _ensure_key_directory()
    global _KEY_CACHE
    try:
        key = Fernet.generate_key()
        # Write in binary mode to prevent newline conversion and encoding errors; key is raw bytes.
        with open(SECRET_KEY_PATH, "wb") as key_file:
            key_file.write(key)
            _KEY_CACHE = key
    # Catch all OS-level errors (permissions, disk full) to re-raise with context
    except OSError:
        raise  # Re-raise the exception to let the caller handle it


def _load_key() -> bytes:
    """
    Loads Fernet key from secret.key file.

    Returns:
        - secret.key data
    """
    global _KEY_CACHE
    if _KEY_CACHE is not None:
        return _KEY_CACHE

    while True:
        try:
            # Open in binary read mode because Fernet keys are raw bytes, not text
            with open(SECRET_KEY_PATH, "rb") as key_file:
                _KEY_CACHE = key_file.read()
                return _KEY_CACHE
        except FileNotFoundError:
            _generate_key()
        # Catch all OS-level errors (permissions, disk full) to re-raise with context
        except OSError:
            raise  # Re-raise the exception to let the caller handle it


def encrypt_data(plain_text: str) -> str:
    """
    Encrypt plain text using Fernet.

    Parameters:
        - plain_text: String to encrypt (e.g., password)

    Returns:
        - Encrypted string (URL-safe base64)
    """
    key = _load_key()
    fernet_key = Fernet(key)
    # Fernet works with bytes. Input string is encoded to bytes,
    # then the encrypted bytes are decoded back to string for JSON storage.
    # Prevent 'TypeError: Object of type bytes is not JSON serializable'
    return fernet_key.encrypt(plain_text.encode()).decode()


def decrypt_data(cipher_text: str) -> str:
    """
    Decrypt Fernet-encrypted string.

    Parameters:
        - cipher_text: Encrypted string previously returned by encrypt_data

    Returns:
        - Original plain text
    """
    key = _load_key()
    fernet_key = Fernet(key)
    # cipher_text is string from JSON; encode to bytes for Fernet,
    # then decode result to string for output (without decoding output must be like this: b'str')
    # if we don't use encode method, base64 module convert it to bytes in back scene.
    return fernet_key.decrypt(cipher_text.encode()).decode()

