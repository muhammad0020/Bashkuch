"""
Application bootstrap and navigation management.

Provides the startup logic and controls the menu
navigation stack throughout the application's lifetime.
"""

import sys
import errno

from core import AccountManager
from core import load_data
from ui import BaseMenu, MainMenu
from navigation import NavigateBack, NavigateTwoStepsBack


errors = {
    "permission": "Access Denied. Cannot read the storage file",
    "disk_full": "Cannot save your changes. Storage is full!",
    "return": "Returning to main menu..."
}

def main():
    """
    Initialize the application and execute the main
    navigation loop.
    """
    show_message = BaseMenu.show_message
    try:
        active_accounts, deleted_accounts = load_data()
    except PermissionError:
        show_message(errors["permission"])
        sys.exit(1)
    unique_account_keys = set()

    for account in active_accounts:
        unique_account_keys.add((account["service_name"], account["username"]))
    manager = AccountManager(active_accounts, deleted_accounts, unique_account_keys)
    menu_navigation_stack: list[BaseMenu] = [MainMenu(manager)]

    while menu_navigation_stack:
        current_menu = menu_navigation_stack[-1]
        try:
            next_menu = current_menu.run()
            if next_menu:
                menu_navigation_stack.append(next_menu)
            else:
                menu_navigation_stack.pop()

        except NavigateBack:
            menu_navigation_stack.pop()

        except NavigateTwoStepsBack:
            del menu_navigation_stack[-2:]

        except PermissionError:
            show_message(errors["permission"])
            show_message(errors["return"])
            continue
        except OSError as error:
            if error.errno == errno.ENOSPC:
                show_message(errors["disk_full"])
                show_message(errors["return"])
            else:
                show_message(f"{error}")


if __name__ == "__main__":
    main()
