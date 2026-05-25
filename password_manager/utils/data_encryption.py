"""
Manage Fernet keys and encrypt/decrypt user data securely.

This module handles:
    - Generation of Fernet keys (if not provided)
    - Loading existing keys from secure storage
    - Encryption/decryption of plaintext data using Fernet.
"""

from pathlib import Path
from cryptography.fernet import Fernet

from .show_and_get_data import show_message
from .data_dictionaries import messages


PROJECT_ROOT = Path(__file__).parent.parent.parent
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
        with open(SECRET_KEY_PATH, "wb") as key_file:  # 'wb': Prevents text artifacts in key files
            key_file.write(key)
            _KEY_CACHE = key
        show_message(messages["success"]["key"])
    # Catch all OS-level errors (permissions, disk full) to re-raise with context
    except OSError:
        raise  # Re-raise the exception to let the caller handle it


def _load_key() -> bytes:
    """
    Loads Fernet key from secret.key file.

    Returns:
        - Binary secret key data (bytes).
    """
    global _KEY_CACHE
    if _KEY_CACHE is not None:
        return _KEY_CACHE

    while True:
        try:
            with open(SECRET_KEY_PATH, "rb") as key_file:  # 'rb': Fernet keys are binary (no text encoding)
                _KEY_CACHE = key_file.read()
                return _KEY_CACHE
        except FileNotFoundError:
            _generate_key()
        # Catch all OS-level errors (permissions, disk full) to re-raise with context
        except OSError:
            raise  # Re-raise the exception to let the caller handle it


def encrypt_data(plain_text: str) -> str:
    """
    Encrypts password using loaded Fernet key.

    Parameters:
        - password (str): User password

    Returns:
        - Encrypted user password (str).
    """

    key = _load_key()
    fernet_key = Fernet(key)
    return fernet_key.encrypt(plain_text.encode()).decode()


def decrypt_data(cipher_text: str) -> str:
    """
    Decrypts password using loaded Fernet key.

    Parameters:
        - Encrypted user password (str)

    Returns:
        - Decrypted password (str).
    """

    key = _load_key()
    fernet_key = Fernet(key)
    return fernet_key.decrypt(cipher_text.encode()).decode()

