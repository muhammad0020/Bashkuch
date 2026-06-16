"""
Provides the base class for all application menus.

Includes shared menu utilities and defines the contract
that concrete menu implementations must implement.
"""

from __future__ import annotations
import os
from time import sleep
from inspect import cleandoc
from collections.abc import Callable
from abc import ABC, abstractmethod

from navigation import NavigateBack


class BaseMenu(ABC):
    """
    Abstract base class establishing the core interface for system menus.

    This class provides the blueprint and shared foundational utilities for
    rendering user interfaces, capturing input, and orchestrating menu-driven
    application workflows.
    """
    NAVIGATE_BACK_KEY = "q"

    @abstractmethod
    def run(self) -> BaseMenu | None:
        """
        Execute the menu logic and return the next menu to open.

        Returns:
        BaseMenu | None:
        The next menu instance, or None to close the current menu.
        """
        pass

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
    def _show_menu(options: tuple):
        """
        Displays a formatted menu in the console.

        Prints a numbered list of menu options with fixed-width alignment
        for consistent CLI presentation.

        Parameters:
            - options: A collection of menu items to be displayed as selectable options.
        """
        print("=" * 46)
        for row, option in enumerate(options, start=1):
            print(f"|{row}.{option:<42}|")
        print("=" * 46)

    @staticmethod
    def _show_accounts(accounts: list[dict]):
        """
        Displays a formatted list of accounts in a console table view.

        This function iterates over a list of account dictionaries and prints
        each account with its row number, service name, and username in a structured format.

        Parameters:
            accounts:
                A list of dictionaries where each dictionary represents an account
                containing service name, username, and password.

        Notes:
            - Assumes dictionary values are ordered as: service_name, username, password
            - Output is formatted for CLI display with fixed-width alignment
            """
        print("=" * 46)
        for row, account in enumerate(accounts, start=1):
            name, username, password = account.values()
            content = f"{row}.{name}    {username}"
            print(f"{content:<45}|")
        print("=" * 46)

    @staticmethod
    def _validate_menu_selection(user_input: str, limit: int) -> bool:
        """
        Validate and convert user input to an integer within a specified range.

        Attempts to parse the input string as an integer and checks if it falls
        within the interval (0, limit]. Serves as a helper for menu selection validation.

        Parameters:
            user_input: Raw string entered by the user (e.g., "3").
            limit: Maximum allowed value (inclusive). Minimum is always 1.

        Returns:
            bool:
                - True: If input is an integer between 1 and limit.
                - False: If input is not an integer or is out of range.
        """
        return user_input.isdecimal() and 0 < int(user_input) <= limit

    @classmethod
    def capture_menu_selection(cls, options: tuple | list[dict],
                               prompt: str,
                               error: str="Invalid input",
                               *, convert_to_index: bool=False,
                               allow_navigation_back: bool=True) -> int:
        """
        Display a menu, prompt the user, and return a validated integer choice.

        This class method renders the given options (dictionary, list, or tuple),
        repeatedly asks for input until a valid selection within the available
        range is entered, and optionally converts the 1‑based user choice to
        a 0‑based index.

        If the user enters the value defined by NAVIGATE_BACK_KEY, the method
        raises a NavigateBack exception to signal a request to return to the
        previous menu in the navigation stack.

        Parameters:
            options: A collection of menu items or accounts list to display.
            prompt: The message displayed to the user for input.
            error: Optional error message shown when validation fails.
                   Defaults to "Invalid input".
            convert_to_index: If True, returns the choice minus 1 (0‑based index);
                              otherwise returns the raw 1‑based integer choice.
                              Defaults to False.
            allow_navigation_back:
                Whether the user is allowed to navigate back to the previous menu using the back key.
                 If True, pressing the back key raises a NavigateBack exception.
                  If False, the back key is treated as invalid input. Defaults to True.

        Raises:
            NavigateBack: Triggered when the user requests navigation to the previous menu
            by entering NAVIGATE_BACK_KEY.

        Returns:
            int: A valid integer representing the user's choice. If convert_to_index
                 is True, the returned value is in the range [0, len(options)-1];
                 otherwise it is in the range [1, len(options)].
        """
        # If convert_to_index is True, we use _show_accounts because the options
        # represent account objects that need formatted display.
        # Otherwise, we use _show_menu for standard menu options.
        cls._show_accounts(options) if convert_to_index else cls._show_menu(options)
        while True:
            choice = input(cleandoc(prompt)).strip().lower()
            if allow_navigation_back and choice == cls.NAVIGATE_BACK_KEY:
                cls.clear_terminal()
                raise NavigateBack
            if cls._validate_menu_selection(choice, len(options)):
                choice = int(choice)
                return (choice - 1) if convert_to_index else choice
            cls.show_message(error)

    def get_validated_string(self, prompt: str, errors: tuple[str, str],
                             *, validator: Callable[[str], str], transform: bool=True) -> str:
        """
        Repeatedly prompt the user for a string input until it passes validation.

        The input is stripped of whitespace and converted to lowercase before being
        passed to the validator function. Based on the validator's return value,
        the method either returns the validated string or displays an appropriate
        error message and retries.

        If the user enters the value defined by NAVIGATE_BACK_KEY, the method
        raises a NavigateBack exception to signal a request to return to the
        previous menu in the navigation stack.

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

        Raises:
            NavigateBack: Triggered when the user requests navigation to the previous menu
             by entering NAVIGATE_BACK_KEY.

       Returns:
            The validated string entered by the user. If transform was True, the string
            has been stripped of leading/trailing whitespace and converted to lowercase.
            If transform was False, only the trailing newline character is removed and
            all other whitespace (including leading/trailing spaces/tabs) is preserved.
        """
        while True:
            user_input = input(prompt)
            if user_input.strip().lower() == self.NAVIGATE_BACK_KEY:
                self.clear_terminal()
                raise NavigateBack
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