"""Secure text data handling: save to disk, load from disk, and copy to clipboard."""

from json import load, dump
from pathlib import Path

from pyperclip import copy, PyperclipException

from .show_and_get_data import show_message
from .data_dictionaries import messages
from .data_encryption import encrypt_data, decrypt_data


PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_JSON_PATH = PROJECT_ROOT / "saved_data" / "data.json"


def _encrypt_accounts(accounts: list) -> list:
    """
    Encrypt all sensitive fields in a list of account dicts.

    Parameters:
        - accounts: List of dicts with keys 'service_name', 'username', 'password'.

    Returns:
        - List of dicts with same keys, each value encrypted by encrypt_data().
    """
    return [{
        "service_name": encrypt_data(acc["service_name"]),
        "username": encrypt_data(acc["username"]),
        "password": encrypt_data(acc["password"])
    } for acc in accounts]


def _decrypt_accounts(accounts: list) -> list:
    """
    Decrypt a list of encrypted account dictionaries.

    This helper reverses the encryption applied by _encrypt_accounts(),
    converting stored encrypted strings back to plain text for runtime use.

    Parameters:
        accounts: List of dicts with encrypted values for keys 'service_name', 'username', 'password'.

    Returns:
        List of dicts with the same structure, each value decrypted via decrypt_data().
    """
    return [{
        "service_name": decrypt_data(acc["service_name"]),
        "username": decrypt_data(acc["username"]),
        "password": decrypt_data(acc["password"])
    } for acc in accounts]


def save_data(vault, deleted_accounts):
    """
    Save created accounts data to vault and deleted services data to deleted_accounts.

    Parameters:
        - vault (list): user saved accounts.
        - deleted_accounts (list): accounts that have been deleted by user.
    """
    data = {
        "vault": _encrypt_accounts(vault),
        "deleted_accounts": _encrypt_accounts(deleted_accounts)
    }

    with open(DATA_JSON_PATH, "w") as f:
        dump(data, f, indent=4)  # indent=4 for pretty formatting


def load_data():
    """
    loads saved data from data.json file and decrypt it.

    Returns:
        - decrypted_vault (list): Decrypted saved accounts.
        - decrypted_deleted_accounts (list): Decrypted deleted accounts.
        - Two empty lists if saved file not found (list).
    """
    try:
        with open(DATA_JSON_PATH, "r") as f:
            data = load(f)
        return _decrypt_accounts(data["vault"]), _decrypt_accounts(data["deleted_accounts"])
    except FileNotFoundError:
        return [], []


def copy_to_clipboard(text):
    """
    Copies text to system clipboard using OS-specific methods.

    Parameters:
        - text (str): Text to copy to clipboard.
    """
    try:
        copy(text)
        show_message(messages["success"]["copied"])
    # Display specific error message: missing tool or clipboard access problem.
    except PyperclipException:  
        show_message(messages["error"]["not_copied"])
    except Exception:  # for unexpected errors
        show_message(messages["error"]["not_copied"])
