"""
Account CLI Interface Library

A utility for building interactive account management interfaces with:
- Clean header displays
- Menu navigation
- User input validation
- Display accounts details
- Contextual messages (success/error)

Features:
- Validates inputs against account rules before processing
- Handles user prompts and menu selection
- Provides standardized error messaging
- Supports account viewing.
"""

from ui import BaseMenu
from inspect import cleandoc

from .data_dictionaries import messages


def select_account(accounts: list) -> str | int:
    """
    Display a list of accounts and prompt user to select one.

    Shows all accounts from the provided list (e.g., vault, deleted accounts,
    or search results). The user can choose an account by entering its number
    or return to the previous menu without selecting.

    Parameters:
        - accounts: List of account dictionaries to display.

    Returns:
        - Back to previous menu: if user chooses to return.
        - index: Index of selected account in the original given list.
    """
    service_names = get_service_names(accounts)  # for show as menu_options
    index = BaseMenu.capture_menu_selection(service_names, messages["prompt"]["choose_service"], convert_to_index=True)
    if service_names[index] == "Back to previous menu":
        return "Back to previous menu"
    return index


def account_details(account: dict, menu_options: dict) -> int:
    """
    Show selected account details and ask user what their wants to do with it.

    Returns:
        - User decisions for selected accounts including edit/delete operations.
    """
    print("=" * 46)
    print(cleandoc(f"""
        Service name: {account["service_name"]}  
        Username: {account["username"]}   
        Password: {account["password"]}
        """))
    print("=" * 46)
    return BaseMenu.capture_menu_selection(menu_options, messages["prompt"]["choice"])


def get_service_names(accounts_list, sort_key=None):
    """
    Returns a list of service names with a 'Back to previous menu' option for user navigation.
    Sort list of service names by sort_key (default: None).

    Parameters:
        - accounts_list (list): List of dictionaries containing service details (name, username, password).
        - sort_key (function): Function to sort service names.

    Returns:
        - List of strings (list): [service_names, 'Back to previous menu'].
    """

    # service_names = sorted([(item["service_name"]) for item in accounts_list], key=sort_key)
    return [item["service_name"] for item in accounts_list] + ["Back to previous menu"]
