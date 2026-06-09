"""
Secure password manager application entry point.

Coordinates user commands (search, edit, delete) through secure modules.

Maintains data integrity via unique_keys and Fernet encryption.

"""

import sys
import errno

from core import AccountManager
from core import manage_passwords
from core import password_generator
from core import recycle_bin

from ui import AccountCreatorMenu

from utils import load_data
from ui import BaseMenu
from utils import menu_titles, menu_options, messages


errors = {
    "permission": "Access Denied. Cannot read the storage file",
    "disk_full": "Cannot save your changes. Storage is full!",
    "return": "Returning to main menu..."
}

def main():
    """Main entry point. Executes all password manager functions."""
    main_menu = BaseMenu()
    try:
        vault, deleted_accounts = load_data()
    except PermissionError:
        main_menu.show_message(errors["permission"])
        sys.exit(1)
    unique_service_users = set()

    for item in vault:
        unique_service_users.add((item["service_name"], item["username"]))
    while True:
        main_menu.show_header(menu_titles["main"])
        choice = main_menu.capture_menu_selection(menu_options["main"]["main"], messages["prompt"]["choice"])
        manager = AccountManager(vault, deleted_accounts, unique_service_users)
        try:
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
                decision = main_menu.capture_menu_selection(menu_options["main"]["exit"], messages["prompt"]["exit"])
                if decision == 2:
                    sys.exit(0)
        except PermissionError:
            main_menu.show_message(errors["permission"])
            main_menu.show_message(errors["return"])
            continue
        except OSError as error:
            if error.errno == errno.ENOSPC:
                main_menu.show_message(errors["disk_full"])
                main_menu.show_message(errors["return"])
            else:
                main_menu.show_message(str(error))

        main_menu.clear_terminal()


if __name__ == "__main__":
    main()
