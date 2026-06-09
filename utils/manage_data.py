"""Secure text data handling: save to disk, load from disk, and copy to clipboard."""

import json
from pathlib import Path
from inspect import currentframe, getframeinfo

import pyperclip

from ui import BaseMenu
from .data_dictionaries import messages, menu_options
from .data_encryption import encrypt_data, decrypt_data

PROJECT_ROOT = Path(__file__).parent.parent
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
        - accounts: List of dicts with encrypted values for keys 'service_name', 'username', 'password'.

    Returns:
        - List of dicts with the same structure, each value decrypted via decrypt_data().
    """
    return [{
        "service_name": decrypt_data(acc["service_name"]),
        "username": decrypt_data(acc["username"]),
        "password": decrypt_data(acc["password"])
    } for acc in accounts]


def save_data(vault: list, deleted_accounts: list):
    """
    Save created accounts data to vault and deleted services data to deleted_accounts.

    Parameters:
        - vault: user saved accounts.
        - deleted_accounts: accounts that have been deleted by user.
    """
    data = {
        "vault": _encrypt_accounts(vault),
        "deleted_accounts": _encrypt_accounts(deleted_accounts)
    }
    # Ensure the directory exists when generating or loading the Fernet key,
    # so no further directory checks are needed.
    try:
        with open(DATA_JSON_PATH, "w") as f:
            json.dump(data, f, indent=4)  # indent=4 for pretty formatting
    # Catch all OS-level errors (permissions, disk full) to re-raise with context
    except OSError:
        raise  # Re-raise the exception to let the caller handle it


def load_data() -> tuple[list, list]:
    """
    loads saved data from data.json file and decrypt it.

    Returns:
        - Decrypted saved accounts in data['vault'].
        - Decrypted deleted accounts in data['deleted_accounts'].
        - Empty lists if saved file not found or keys are missing.
    """
    try:
        with open(DATA_JSON_PATH, "r") as f:
            data = json.load(f)
        vault_data = data.get("vault", [])
        deleted_data = data.get("deleted_accounts", [])
        return _decrypt_accounts(vault_data), _decrypt_accounts(deleted_data)
    except (FileNotFoundError, json.JSONDecodeError):
        return [], []
    # Catch all OS-level errors (permissions, disk full) to re-raise with context
    except OSError:
        raise  # Re-raise the exception to let the caller handle it


def copy_to_clipboard(text: str):
    """
    Copies text to system clipboard using pyperclip module.

    Parameters:
        - text: Text to copy to clipboard.
    """
    try:
        pyperclip.copy(text)
        BaseMenu.show_message(messages["success"]["copied"])
    # Display specific error message: missing tool or clipboard access problem.
    except pyperclip.PyperclipException:
        BaseMenu.show_message(messages["error"]["not_copied"])


def delete_accounts(accounts: list[dict],
                    deleted_accounts: list[dict],
                    index: int,
                    unique_keys: set[tuple] = None) -> str:
    """
    Delete a selected account from a specified list (depends on the calling module).

    The function removes an account chosen by the user from the provided list
    (e.g., vault, deleted accounts, or search results). Behavior after deletion
    depends on the remaining list content.

    Returns:
        str: One of the following values:
        - 'Empty': Deletion succeeded and the list became empty.
        - 'Success' : Deletion succeeded and the list still contains items.
        - 'Cancel'  : User chose to cancel/back without deleting.
    """
    caller_frame = currentframe().f_back
    caller_file = getframeinfo(caller_frame).filename
    file_name = Path(caller_file).stem  # We need the file name without the extension.

    if file_name == "manage_accounts":
        display_message = messages["prompt"]["delete_confirmation"]
    else:
        display_message = messages["prompt"]["delete_last_confirmation"]
    confirmation = BaseMenu.capture_menu_selection(menu_options["manage"]["delete"], display_message)

    if confirmation == 1:  # confirm delete account
        if file_name == "manage_accounts":
            unique_keys.discard((accounts[index]["service_name"], accounts[index]["username"]))
            deleted_accounts.append(accounts.pop(index))  # add item to recycle bin
        else:
            deleted_accounts.pop(index)

        save_data(accounts, deleted_accounts)
        BaseMenu.show_message(messages["success"]["deleted"])
        lst = accounts if file_name == "manage_accounts" else deleted_accounts

        if not lst:
            BaseMenu.show_message(messages["error"]["no_password"])
            return "Empty"
        else:
            return "Success"
    else:
        return "Cancel"
