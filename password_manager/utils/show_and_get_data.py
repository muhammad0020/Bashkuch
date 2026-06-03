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

import os
from time import sleep
from inspect import cleandoc
from collections.abc import Callable

from .data_dictionaries import messages


class BaseMenu:
    """
    Abstract base class establishing the core interface for system menus.

    This class provides the blueprint and shared foundational utilities for
    rendering user interfaces, capturing input, and orchestrating menu-driven
    application workflows.
    """
    @staticmethod
    def clear_terminal(delay: int=0):
        """
        Clears terminal screen after specified delay (default: 0 seconds).

        Parameters:
            - delay: Seconds to wait before clearing terminal.
        """
        sleep(delay)
        # Use 'cls' on Windows, 'clear' on Unix-like systems to clear the screen.
        os.system("cls" if os.name == "nt" else "clear")

    @staticmethod
    def show_header(title: str):
        """
        Displays program header for menus.

        Parameters:
            - title: Title of current menu.
        """
        print("=" * 46)
        print(f"|{title.center(44)}|")
        print("=" * 46)

    @classmethod
    def show_message(cls, message: str):
        """
        Prints message and auto-clears screen after delay (default: 2 seconds).

        Parameters:
            - message (str): Specific message to center in frame.
        """
        print("=" * 46)
        print(f"|{message.center(44)}|")
        print("=" * 46)
        print()
        cls.clear_terminal(2)

    @staticmethod
    def _show_menu(options: dict | list | tuple):
        """Displays menu options for current function."""
        print("=" * 46)
        for row, option in enumerate(options, start=1):
            print(f"|{row}.{option:<42}|")
        print("=" * 46)

    @staticmethod
    def _validation(user_input: str, limit: int) -> tuple[bool, int | None]:
        """
         Validate and convert user input to an integer within a specified range.

        Attempts to parse the input string as an integer and checks if it falls
        within the interval (0, limit]. Serves as a helper for menu selection validation.

        Parameters:
            user_input: Raw string entered by the user (e.g., "3").
            limit: Maximum allowed value (inclusive). Minimum is always 1.

        Returns:
            A tuple (is_valid, value):
                - is_valid (bool): True if input is an integer between 1 and limit, else False.
                - value (int | None): The parsed integer if is_valid is True, otherwise None.
        """
        try:
            choice = int(user_input)
            if 0 < int(user_input) <= limit:
                return True, choice
            else:
                return False, None
        except ValueError:
            return False, None

    @classmethod
    def get_and_validate(cls, options: dict | list | tuple, prompt: str,
                         error: str="Invalid input", *, convert_to_index: bool=False) -> int:
        """
        Display a menu, prompt the user, and return a validated integer choice.

        This class method renders the given options (dictionary, list, or tuple),
        repeatedly asks for input until a valid selection within the available
        range is entered, and optionally converts the 1‑based user choice to
        a 0‑based index.

        Parameters:
            options: A collection of menu items to display.
                     - If a dict, keys are used as option identifiers.
                     - If a list or tuple, the items are shown as numbered options.
            prompt: The message displayed to the user for input.
            error: Optional error message shown when validation fails.
                   Defaults to "Invalid input".
            convert_to_index: If True, returns the choice minus 1 (0‑based index);
                              otherwise returns the raw 1‑based integer choice.
                              Defaults to False.

        Returns:
            int: A valid integer representing the user's choice. If convert_to_index
                 is True, the returned value is in the range [0, len(options)-1];
                 otherwise it is in the range [1, len(options)].

        """
        cls._show_menu(options)
        while True:
            choice = input(cleandoc(prompt))
            success, choice = cls._validation(choice, len(options))
            if success:
                return (choice - 1) if convert_to_index else choice
            cls.show_message(error)
            continue


    def get_validated_string(self, prompt: str, errors: tuple[str, str],
                             *, validator: Callable[[str], str], transform: bool=True) -> str:
        """
        Repeatedly prompt the user for a string input until it passes validation.

        The input is stripped of whitespace and converted to lowercase before being
        passed to the validator function. Based on the validator's return value,
        the method either returns the validated string or displays an appropriate
        error message and retries.

        Parameters:
            prompt: The message displayed to the user when asking for input.

            errors: A tuple of two error messages:
                - errors[0] is shown when the validator returns 'empty' (empty input).
                - errors[1] is shown when the validator returns 'too_long' (input exceeds the limit).

            validator: A callable that takes a single string argument and returns:
                - 'success': if the input is valid
                - 'empty': if the input is empty
                - 'too_long': if the input exceeds the limit.

            transform:
                - True (default): the input is stripped of leading/trailing whitespace
                   (spaces, tabs, newlines) and converted to lowercase. Use this for
                   service names and usernames where case and surrounding spaces are not
                   significant.

                - False: only the trailing newline character is removed (with .rstrip('\n'))
                   and all other whitespace (leading/trailing spaces, tabs) is preserved.
                   This is necessary for passwords where spaces, tabs, or other whitespace
                   characters may be intentionally part of the secret.

       Returns:
            The validated string entered by the user. If transform was True, the string
            has been stripped of leading/trailing whitespace and converted to lowercase.
            If transform was False, only the trailing newline character is removed and
            all other whitespace (including leading/trailing spaces/tabs) is preserved.
        """
        while True:
            user_input = input(prompt)
            status = validator(user_input)
            if status == "success":
                if transform:
                    # Replaces internal tab characters with spaces to clean mid-string input,
                    # then utilizes .strip() to eliminate any leading/trailing whitespace.
                    return user_input.replace("\t", " ").strip().lower()
                else:
                    # Keep the password data 100% raw and untouched to preserve user secrets.
                    return user_input
            elif status == "empty":
                self.show_message(errors[0])
            elif status == "too_long":
                self.show_message(errors[1])


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
    index = BaseMenu.get_and_validate(service_names, messages["prompt"]["choose_service"], convert_to_index=True)
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
    return BaseMenu.get_and_validate(menu_options, messages["prompt"]["choice"])


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
