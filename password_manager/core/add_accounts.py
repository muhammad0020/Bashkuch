"""
Adds new accounts with Fernet-encrypted credentials.

"Collects service name, username, and password from the user and encrypts them using Fernet"

Stores encrypted data in JSON file.
"""

from ..common import show_header, clear_terminal
from ..common import menu_titles, messages
from ..utils import show_message
from ..utils import save_data


def add_password(accounts_list, recycle_bin_data, unique_keys):
    """
    Prompts user for service name, username, and password.
    Encrypts and saves to vault. Prevents duplicates by checking username uniqueness.

    Parameters:
        - accounts_list (list): Saved accounts in vault.
        - recycle_bin_data (list): Deleted accounts in deleted_accounts list.
        - unique_keys (set): Set of unique service names and usernames.
    """

    show_header(menu_titles["add"])
    # Re-prompt user to re-enter service details when duplicate service names or usernames
    # are detected during service registration
    while True:
        # Re-prompt user for valid input when empty string is provided during input validation
        while True:
            service_name = input(messages["prompt"]["service_name"]).strip().lower()
            if not service_name:
                show_message(messages["error"]["empty_service_field"])
                continue  # Empty input detected
            break

        # Re-prompt user for valid input when empty string is provided during input validation
        while True:
            username = input(messages["prompt"]["username"]).strip().lower()
            if not username:
                show_message(messages["error"]["empty_username_field"])
                continue  # Empty input detected
            break

        key = (service_name, username)
        if key in unique_keys:  # check for duplicated data
            show_message(messages["error"]["exist"])
            continue  # Duplicated data detected
        break

    # Re-prompt user for valid input when empty string is provided during input validation
    while True:
        password = input(messages["prompt"]["password"]).strip()
        if not password:
            show_message(messages["error"]["empty_password_field"])
            continue  # Empty input detected
        break

    accounts_list.append(
        {"service_name": service_name,
         "username":  username,
         "password": password
         })

    save_data(accounts_list, recycle_bin_data)
    unique_keys.add(key)
    clear_terminal()
    show_message(messages["success"]["saved"])
