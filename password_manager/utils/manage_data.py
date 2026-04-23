"""Secure text data handling: save to disk, load from disk, and copy to clipboard."""

from json import load, dump
from subprocess import run, CalledProcessError
from sys import platform
from pathlib import Path

from .show_and_get_data import show_message
from .data_dictionaries import messages
from .data_encryption import encrypt_data, decrypt_data


PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_JSON_PATH = PROJECT_ROOT / "saved_data" / "data.json"


def save_data(vault, deleted_accounts):
    """
    Save created accounts data to vault and deleted services data to deleted_accounts.

    Parameters:
        - vault (list): user saved accounts.
        - deleted_accounts (list): accounts that have been deleted by user.
    """

    encrypted_vault = []
    encrypted_deleted_accounts = []

    for account in vault:
        encrypted_vault.append({
            "service_name": encrypt_data(account["service_name"]),
            "username": encrypt_data(account["username"]),
            "password": encrypt_data(account["password"])
        })

    for account in deleted_accounts:
        encrypted_deleted_accounts.append({
            "service_name": encrypt_data(account["service_name"]),
            "username": encrypt_data(account["username"]),
            "password": encrypt_data(account["password"])
        })

    data = {
        "vault": encrypted_vault,
        "deleted_accounts": encrypted_deleted_accounts
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

    decrypted_vault = []
    decrypted_deleted_accounts = []

    try:
        with open(DATA_JSON_PATH, "r") as f:
            data = load(f)

        for account in data["vault"]:
            decrypted_vault.append({
                "service_name": decrypt_data(account["service_name"]),
                "username": decrypt_data(account["username"]),
                "password": decrypt_data(account["password"])
            })

        for account in data["deleted_accounts"]:
            decrypted_deleted_accounts.append({
                "service_name": decrypt_data(account["service_name"]),
                "username": decrypt_data(account["username"]),
                "password": decrypt_data(account["password"])
            })

        return decrypted_vault, decrypted_deleted_accounts
    except FileNotFoundError:
        return [], []


def copy_to_clipboard(text):
    """
    Copies text to system clipboard using OS-specific methods.

    Parameters:
        - text (str): Text to copy to clipboard.
    """

    try:
        if platform == "win32":
                run(
                    ["powershell", "-command", f"Set-Clipboard -Value '{text}'"],
                    shell=True, capture_output=True)

        elif platform == "darwin":
            run(["pbcopy"], input=text.encode())

        elif platform.startswith("linux"):
            run(["xclip", "-selection", "clipboard"], input=text.encode(), check=True)

        show_message(messages["success"]["copied"])

    except CalledProcessError:
        show_message(messages["error"]["not_copied"])
