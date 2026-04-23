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


def generate_key():
    """Generates Fernet encryption key and saves to secret.key."""

    try:
        key = Fernet.generate_key()
        with open(SECRET_KEY_PATH, "wb") as key_file:  # 'wb': Prevents text artifacts in key files
            key_file.write(key)
        show_message(messages["success"]["key"])
    except FileNotFoundError as error:
        print(error)


def load_key():
    """
    Loads Fernet key from secret.key file.

    Returns:
        - Binary secret key data (bytes).
    """

    if not SECRET_KEY_PATH.exists():  # prevent FileNotFoundError
        generate_key()

    try:
        with open(SECRET_KEY_PATH, "rb") as key_file:  # 'rb': Fernet keys are binary (no text encoding)
            return key_file.read()
    except Exception as e:  # for unexpected errors
        print(e)


def encrypt_data(data):
    """
    Encrypts password using loaded Fernet key.

    Parameters:
        - password (str): User password

    Returns:
        - Encrypted user password (str).
    """

    key = load_key()
    f = Fernet(key)
    return f.encrypt(data.encode()).decode()


def decrypt_data(encrypted_data):
    """
    Decrypts password using loaded Fernet key.

    Parameters:
        - Encrypted user password (str)

    Returns:
        - Decrypted password (str).
    """

    key = load_key()
    f = Fernet(key)
    return f.decrypt(encrypted_data.encode()).decode()

