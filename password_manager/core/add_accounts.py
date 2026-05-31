"""
Adds new accounts with Fernet-encrypted credentials.

Collects service name, username, and password from the user and encrypts them using Fernet.

Stores encrypted data in JSON file.
"""

from ..common import BaseMenu
from ..common import menu_titles, messages
from ..utils import save_data


def create_accounts(accounts: list, deleted_accounts: list, unique_keys: set):
    """
    Prompts user for service name, username, and password.
    Encrypts and saves to vault. Prevents duplicates by checking service name and username uniqueness.

    Parameters:
        - accounts: user saved accounts.
        - deleted_accounts: accounts that have been deleted by user.
        - unique_keys: Set of unique service names and usernames.
    """
    account_creator = BaseMenu()
    account_creator.show_header(menu_titles["add"])
    chars_limit = 30
    # Nested loop re-prompts user for username/service name when entries are exists in saved accounts
    while True:
        while True:
            service_name = input(messages["prompt"]["service_name"]).strip().lower()
            if not service_name:
                account_creator.show_message(messages["error"]["empty_service_field"])
                continue
            if len(service_name) > chars_limit:
                account_creator.show_message(messages["error"]["too_long_service_name"])
                continue
            break

        while True:
            username = input(messages["prompt"]["username"]).strip().lower()
            if not username:
                account_creator.show_message(messages["error"]["empty_username_field"])
                continue
            if len(username) > chars_limit:
                account_creator.show_message(messages["error"]["too_long_username"])
                continue
            break

        key = (service_name, username)
        if key in unique_keys:
            account_creator.show_message(messages["error"]["exist"])
            continue
        break

    while True:
        password = input(messages["prompt"]["password"]).strip()
        if not password:
            account_creator.show_message(messages["error"]["empty_password_field"])
            continue
        if len(password) > chars_limit:
            account_creator.show_message(messages["error"]["too_long_password"])
            continue
        break

    accounts.append(
        {"service_name": service_name,
         "username":  username,
         "password": password
         })

    save_data(accounts, deleted_accounts)
    unique_keys.add(key)
    account_creator.clear_terminal()
    account_creator.show_message(messages["success"]["saved"])
