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

from os import name, system
from time import sleep
from inspect import cleandoc

from .data_dictionaries import messages

def clear_terminal(delay=0):
    """
    Clears terminal screen after specified delay (default: 0 seconds).

    Parameters:
        - delay (int): Seconds to wait before clearing terminal.
    """

    sleep(delay)

    # check what type of OS is
    if name == "nt": # windows OS
        system("cls") # clear terminal

    else:
        system("clear")


def show_header(title):
    """
    Displays program header for menus.

    Parameters:
        - title (str): Title of current menu.
    """

    print("=" * 46)
    print(f"|{title.center(44)}|") # print title in center of frame
    print("=" * 46)


def show_message(message, delay=2):
    """
    Prints message and auto-clears screen after delay (default: 2 seconds).

    Parameters:
        - message (str): Specific message to center in frame.
        - delay (int): Seconds to wait before clearing screen.
    """

    print("=" * 46)
    print(f"|{message.center(44)}|")
    print("=" * 46)
    print()

    clear_terminal(delay)


def show_and_get(menu_options, prompt, convert_to_index=False):
    """
    Renders menu options and returns validated user selection.

    Parameters:
        - menu_options (list, tuple, dict): Menu options that prints by show_menu().
        - prompt (str): Specific prompt message use for show to user in get_and_validate().
        - convert_to_index (bool): If True convert user input to index of list(default: False).

    Returns:
        - get_and_validate:
            - Validated user input (int). If convert_to_index is True returns user input - 1.
    """

    def show_menu():
        """Displays menu options for current function."""

        print("=" * 46)
        for index, option in enumerate(menu_options, start=1):
            print(f"|{index}.{option} ")
        print("=" * 46)


    def get_and_validate():
        """
        Prompts for user input with validation. Returns validated data.

        Returns:
            - Validated user input (int). If convert_to_index is True returns user input - 1.
        """

        while True:
            try:
                choice = int(input(cleandoc(prompt)))

                if not 0 < choice <= len(menu_options):
                    raise ValueError
            except ValueError:
                show_message(messages["error"]["invalid"])
                continue

            if convert_to_index:
                return choice - 1  # convert choice to list index to access list elements

            else:
                return choice  # doesn't need index of list


    show_menu()
    return get_and_validate()


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
    return show_and_get(menu_options, messages["prompt"]["choice"])


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
