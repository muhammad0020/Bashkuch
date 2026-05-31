"""
Updates account details using Fernet encryption.

Updates service name and username in the unique_keys set.

Saves encrypted credentials to JSON file.
"""

from ..common import BaseMenu, menu_options, messages
from ..utils import save_data


def edit_account(accounts_list, item_index, unique_keys, recycle_bin_data):
    """
    Edits account details in vault with validation against unique_keys to prevent duplicates.

    Parameters:
        - accounts_list (list): Saved accounts in vault list.
        - item_index (int): Index of item in accounts_data list.
        - unique_keys (set): Set of unique service names and usernames.
        - recycle_bin_data (list): List of dictionaries containing deleted accounts details.
    """

    def is_duplicate_key(new_key):
        """
        Compare new data and existing data in unique_keys set.

        Parameters:
            - new_key (tuple): tuple of new service name and username.

        Returns:
             - bool:
                * True: if key exists in unique_keys set (duplicate detection).
                * False: if key not in unique_keys set (no duplicate detection).
        """

        return new_key in unique_keys


    def edit_service_name():
        """
        Edit service name of specific account with validation against unique_keys to prevent duplicates.

        Returns:
            - new service name with previous username (set).
        """

        while True:
            new_service_name = input(messages["prompt"]["new_service"]).strip().lower()
            if not new_service_name:
                BaseMenu.show_message(messages["error"]["empty_service_field"])
                continue

            else:
                break

        new_key = (new_service_name, accounts_list[item_index]["username"])

        # check for duplication
        if is_duplicate_key(new_key):
            BaseMenu.show_message(messages["error"]["exist"])
            return None

        accounts_list[item_index]["service_name"] = new_service_name
        BaseMenu.show_message(messages["success"]["service_updated"])
        return new_key


    def edit_username():
        """
        Edit username of specific account with validation against unique_keys to prevent duplicates.

        Returns:
            - new username with previous service name (set).
        """

        while True:
            new_username = input(messages["prompt"]["new_username"]).strip().lower()
            if not new_username:
                BaseMenu.show_message(messages["error"]["empty_username_field"])
                continue

            else:
                break

        new_key = (accounts_list[item_index]["service_name"], new_username)

        if is_duplicate_key(new_key):
            BaseMenu.show_message(messages["error"]["exist"])
            return None

        accounts_list[item_index]["username"] = new_username
        BaseMenu.show_message(messages["success"]["username_updated"])
        return new_key


    def edit_password():
        """Edit username of specific account with validation against unique_keys to prevent duplicates."""

        while True:
            new_password = input(messages["prompt"]["new_password"]).strip()
            if not new_password:
                BaseMenu.show_message(messages["error"]["empty_password_field"])
                continue

            else:
                break

        accounts_list[item_index]["password"] = new_password
        BaseMenu.show_message(messages["success"]["password_updated"])


    def edit_all():
        """
        Edit service name, username and password of specific account.

        Returns:
            - new service name and new username (set).
        """

        while True:
            new_service_name = input(messages["prompt"]["new_service"]).strip().lower()
            if not new_service_name:
                BaseMenu.show_message(messages["error"]["empty_service_field"])
                continue

            else:
                break

        while True:
            new_username = input(messages["prompt"]["new_username"]).strip().lower()
            if not new_username:
                BaseMenu.show_message(messages["error"]["empty_username_field"])
                continue

            else:
                break

        new_key = (new_service_name, new_username)
        if is_duplicate_key(new_key):
            BaseMenu.show_message(messages["error"]["exist"])
            return None

        while True:
            new_password = input(messages["prompt"]["new_password"]).strip()
            if not new_password:
                BaseMenu.show_message(messages["error"]["empty_password_field"])
                continue

            else:
                break

        accounts_list[item_index]["service_name"] = new_service_name
        accounts_list[item_index]["username"] = new_username
        accounts_list[item_index]["password"] = new_password
        BaseMenu.show_message(messages["success"]["information_updated"])
        return new_key

    choice = BaseMenu.get_and_validate(menu_options["manage"]["edit"], messages["prompt"]["choice"])

    # current service name and username in vault
    old_key = (accounts_list[item_index]["service_name"], accounts_list[item_index]["username"])

    if choice == 1: # edit service name
        key = edit_service_name()

    elif choice == 2:
        key = edit_username()

    elif choice == 3:
        # Password changes do not affect unique_keys; no update required
        edit_password()
        save_data(accounts_list, recycle_bin_data)
        return

    else:
        key = edit_all()

    if key is not None:
        unique_keys.discard(old_key)
        unique_keys.add(key)
        save_data(accounts_list, recycle_bin_data)
