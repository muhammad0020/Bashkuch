"""Secure text data handling: save to disk, load from disk, and copy to clipboard."""

from pathlib import Path
from inspect import currentframe, getframeinfo

import pyperclip

from core.storage import save_data
from ui import BaseMenu
from .data_dictionaries import messages, menu_options


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
