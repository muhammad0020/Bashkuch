"""
Secure password manager application entry point.

Coordinates user commands (search, edit, delete) through secure modules.

Maintains data integrity via unique_keys and Fernet encryption.

"""

import sys

from password_manager.core import AccountManager
from password_manager import AccountCreatorMenu
from password_manager import manage_passwords
from password_manager import password_generator
from password_manager import recycle_bin

from password_manager import load_data
from password_manager import BaseMenu
from password_manager import menu_titles, menu_options, messages

# TODO: Add service names sort and filter, copy option to manage_passwords function
# TODO: get_service_names function has incomplete service name sorter

def main():
    """Main entry point. Executes all password manager functions."""

    vault, deleted_accounts = load_data()
    unique_service_users = set()

    for item in vault:
        unique_service_users.add((item["service_name"], item["username"]))
    main_menu = BaseMenu()
    while True:
        main_menu.show_header(menu_titles["main"])
        choice = main_menu.get_and_validate(menu_options["main"]["main"], messages["prompt"]["choice"])
        manager = AccountManager(vault, deleted_accounts, unique_service_users)
        if choice == 1:
            creator = AccountCreatorMenu(manager)
            creator.run()

        elif choice == 2:
            manage_passwords(vault, deleted_accounts, unique_service_users)

        elif choice == 3:
            password_generator()

        elif choice == 4:
            recycle_bin(vault, deleted_accounts, unique_service_users)

        else:
            decision = main_menu.get_and_validate(menu_options["main"]["exit"], messages["prompt"]["exit"])
            if decision == 2:
                sys.exit(0)

        main_menu.clear_terminal()


if __name__ == "__main__":
    main()
